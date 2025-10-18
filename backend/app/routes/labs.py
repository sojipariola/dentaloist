# routes/labs.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import LabOrder, Patient, User, db

labs_bp = Blueprint('labs', __name__, url_prefix='/api/labs')

# RBAC Permission Constants
PERMISSION_VIEW_LAB_ORDERS = 'view_lab_orders'
PERMISSION_CREATE_LAB_ORDERS = 'create_lab_orders'
PERMISSION_EDIT_LAB_ORDERS = 'edit_lab_orders'
PERMISSION_MANAGE_LAB_RESULTS = 'manage_lab_results'
PERMISSION_APPROVE_LAB_RESULTS = 'approve_lab_results'

@labs_bp.route('/orders', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_LAB_ORDERS)
def get_lab_orders():
    """
    Get lab orders with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        status = request.args.get('status')
        patient_id = request.args.get('patient_id', type=int)
        dentist_id = request.args.get('dentist_id', type=int)
        lab_id = request.args.get('lab_id', type=int)
        order_type = request.args.get('type')
        priority = request.args.get('priority')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        due_date_str = request.args.get('due_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(LabOrder.query, tenant_id)
        
        # Apply filters
        if status:
            query = query.filter(LabOrder.status == status)
        if patient_id:
            query = query.filter(LabOrder.patient_id == patient_id)
        if dentist_id:
            query = query.filter(LabOrder.dentist_id == dentist_id)
        if lab_id:
            query = query.filter(LabOrder.lab_id == lab_id)
        if order_type:
            query = query.filter(LabOrder.type == order_type)
        if priority:
            query = query.filter(LabOrder.priority == priority)
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(LabOrder.created_at >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(LabOrder.created_at <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        if due_date_str:
            try:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                query = query.filter(LabOrder.due_date == due_date)
            except ValueError:
                return jsonify({'error': 'Invalid due_date format. Use ISO format.'}), 400
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(LabOrder, sort_by).asc())
        else:
            query = query.order_by(getattr(LabOrder, sort_by).desc())
        
        # Pagination
        orders = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict(include_details=True) for order in orders.items],
            'pagination': {
                'page': orders.page,
                'per_page': orders.per_page,
                'total': orders.total,
                'pages': orders.pages,
                'has_next': orders.has_next,
                'has_prev': orders.has_prev
            },
            'filters': {
                'status': status,
                'patient_id': patient_id,
                'dentist_id': dentist_id,
                'lab_id': lab_id,
                'type': order_type,
                'priority': priority,
                'start_date': start_date_str,
                'end_date': end_date_str,
                'due_date': due_date_str
            },
            'summary': _get_lab_orders_summary(tenant_id, query)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve lab orders', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_LAB_ORDERS)
def get_lab_order(order_id):
    """
    Get a specific lab order with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        return jsonify(order.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve lab order', 'details': str(e)}), 500

@labs_bp.route('/orders', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CREATE_LAB_ORDERS)
def create_lab_order():
    """
    Create a new lab order with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'lab_id', 'type', 'specimens', 'tests', 'due_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if patient and lab belong to the same tenant
        patient_query = multi_tenant_query(Patient.query, tenant_id)
        patient = patient_query.filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Check if lab exists and belongs to tenant (assuming Lab is a model)
        # For now, we'll just validate the lab_id exists in the system
        lab_query = multi_tenant_query(User.query, tenant_id)  # Assuming labs are users with lab role
        lab = lab_query.filter_by(id=data['lab_id'], role='lab').first()
        if not lab:
            return jsonify({'error': 'Lab not found or access denied'}), 404
        
        # Parse due date
        try:
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid due_date format. Use ISO format.'}), 400
        
        # Validate due date is not in the past
        if due_date < datetime.utcnow():
            return jsonify({'error': 'Due date cannot be in the past'}), 400
        
        # Create lab order
        order = LabOrder(
            tenant_id=tenant_id,
            patient_id=data['patient_id'],
            dentist_id=user_id,  # Current user is the dentist
            lab_id=data['lab_id'],
            type=data['type'],
            specimens=data['specimens'],
            tests=data['tests'],
            due_date=due_date,
            created_by=user_id
        )
        
        # Optional fields
        optional_fields = ['instructions', 'priority', 'urgency', 'shipping_method', 'special_requirements']
        for field in optional_fields:
            if field in data:
                setattr(order, field, data[field])
        
        db.session.add(order)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'create', 'lab_order', order.id, 'Lab order created')
        
        return jsonify({
            'message': 'Lab order created successfully',
            'order': order.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create lab order', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>', methods=['PUT'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_LAB_ORDERS)
def update_lab_order(order_id):
    """
    Update an existing lab order with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        # Check if order can be modified (not completed or cancelled)
        if order.status in ['completed', 'cancelled']:
            return jsonify({'error': f'Cannot modify order with status: {order.status}'}), 400
        
        data = request.get_json()
        
        # Update fields
        updateable_fields = [
            'type', 'specimens', 'tests', 'instructions', 'priority', 'urgency',
            'due_date', 'shipping_method', 'special_requirements'
        ]
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                old_value = getattr(order, field)
                new_value = data[field]
                
                if field == 'due_date' and isinstance(new_value, str):
                    try:
                        new_value = datetime.fromisoformat(new_value.replace('Z', '+00:00'))
                        if new_value < datetime.utcnow():
                            return jsonify({'error': 'Due date cannot be in the past'}), 400
                    except ValueError:
                        return jsonify({'error': 'Invalid due_date format. Use ISO format.'}), 400
                
                if old_value != new_value:
                    setattr(order, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        if changes:
            order.updated_by = user_id
            order.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'update', 'lab_order', order.id, f'Lab order updated: {changes}')
        
        return jsonify({
            'message': 'Lab order updated successfully',
            'order': order.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update lab order', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_LAB_ORDERS)
def update_lab_order_status(order_id):
    """
    Update lab order status with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        data = request.get_json()
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        # Validate status transition
        valid_transitions = {
            'pending': ['sent_to_lab', 'cancelled'],
            'sent_to_lab': ['received_by_lab', 'in_progress', 'cancelled'],
            'received_by_lab': ['in_progress', 'cancelled'],
            'in_progress': ['ready_for_review', 'cancelled'],
            'ready_for_review': ['completed', 'needs_revision'],
            'needs_revision': ['in_progress', 'cancelled'],
            'completed': [],  # Cannot change completed orders
            'cancelled': []   # Cannot change cancelled orders
        }
        
        if new_status not in valid_transitions.get(order.status, []):
            return jsonify({'error': f'Invalid status transition from {order.status} to {new_status}'}), 400
        
        # Store old status for audit trail
        old_status = order.status
        
        order.status = new_status
        order.updated_by = user_id
        order.updated_at = datetime.utcnow()
        
        # Set timestamps based on status
        if new_status == 'sent_to_lab':
            order.sent_to_lab_date = datetime.utcnow()
        elif new_status == 'received_by_lab':
            order.received_by_lab_date = datetime.utcnow()
        elif new_status == 'in_progress':
            order.in_progress_date = datetime.utcnow()
        elif new_status == 'ready_for_review':
            order.ready_for_review_date = datetime.utcnow()
        elif new_status == 'completed':
            order.completed_date = datetime.utcnow()
        elif new_status == 'cancelled':
            order.cancelled_date = datetime.utcnow()
            order.cancelled_by = user_id
        
        # Add status note if provided
        if notes:
            if not order.status_notes:
                order.status_notes = []
            order.status_notes.append({
                'status': new_status,
                'note': notes,
                'created_by': user_id,
                'created_at': datetime.utcnow().isoformat()
            })
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'lab_order', order.id, 
                           f'Lab order status changed from {old_status} to {new_status}. Notes: {notes}')
        
        return jsonify({
            'message': f'Lab order status updated to {new_status}',
            'order': order.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update lab order status', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>/results', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_LAB_RESULTS)
def add_lab_results(order_id):
    """
    Add lab results with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        # Check if user has permission to add results (should be lab staff)
        if current_user_obj.role not in ['lab', 'admin']:
            return jsonify({'error': 'Permission denied. Only lab staff can add results.'}), 403
        
        data = request.get_json()
        
        if 'results' not in data:
            return jsonify({'error': 'Results data is required'}), 400
        
        # Validate results structure
        if not _validate_lab_results(data['results']):
            return jsonify({'error': 'Invalid results format'}), 400
        
        order.results = data['results']
        order.results_entered_by = user_id
        order.results_entered_date = datetime.utcnow()
        order.status = 'ready_for_review'
        order.updated_by = user_id
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'lab_order', order.id, 'Lab results added')
        
        return jsonify({
            'message': 'Lab results added successfully',
            'order': order.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add lab results', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>/approve', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_APPROVE_LAB_RESULTS)
def approve_lab_results(order_id):
    """
    Approve lab results with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        if order.status != 'ready_for_review':
            return jsonify({'error': 'Lab order must be in ready_for_review status to approve'}), 400
        
        if not order.results:
            return jsonify({'error': 'No results to approve'}), 400
        
        data = request.get_json()
        approval_notes = data.get('approval_notes', '')
        
        order.status = 'completed'
        order.approved_by = user_id
        order.approval_date = datetime.utcnow()
        order.approval_notes = approval_notes
        order.updated_by = user_id
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'lab_order', order.id, 
                           f'Lab results approved. Notes: {approval_notes}')
        
        return jsonify({
            'message': 'Lab results approved successfully',
            'order': order.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to approve lab results', 'details': str(e)}), 500

@labs_bp.route('/orders/<int:order_id>/reject', methods=['POST'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_APPROVE_LAB_RESULTS)
def reject_lab_results(order_id):
    """
    Reject lab results and request revision
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(LabOrder.query, tenant_id)
        order = query.filter_by(id=order_id).first()
        
        if not order:
            return jsonify({'error': 'Lab order not found'}), 404
        
        if order.status != 'ready_for_review':
            return jsonify({'error': 'Lab order must be in ready_for_review status to reject'}), 400
        
        data = request.get_json()
        rejection_reason = data.get('rejection_reason')
        
        if not rejection_reason:
            return jsonify({'error': 'Rejection reason is required'}), 400
        
        order.status = 'needs_revision'
        order.rejection_reason = rejection_reason
        order.rejected_by = user_id
        order.rejection_date = datetime.utcnow()
        order.updated_by = user_id
        order.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'lab_order', order.id, 
                           f'Lab results rejected. Reason: {rejection_reason}')
        
        return jsonify({
            'message': 'Lab results rejected and sent for revision',
            'order': order.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reject lab results', 'details': str(e)}), 500

@labs_bp.route('/stats', methods=['GET'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_LAB_ORDERS)
def get_lab_stats():
    """
    Get lab statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'overview': _get_lab_orders_overview(tenant_id, start_date, end_date),
            'status_breakdown': _get_lab_orders_status_breakdown(tenant_id, start_date, end_date),
            'type_breakdown': _get_lab_orders_type_breakdown(tenant_id, start_date, end_date),
            'turnaround_times': _get_turnaround_times(tenant_id, start_date, end_date),
            'lab_performance': _get_lab_performance(tenant_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve lab statistics', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _get_lab_orders_summary(tenant_id: str, query: Any) -> Dict[str, Any]:
    """Get summary statistics for lab orders"""
    total_orders = query.count()
    
    # Count by status
    status_counts = query.with_entities(
        LabOrder.status, db.func.count(LabOrder.id)
    ).group_by(LabOrder.status).all()
    
    # Count overdue orders
    overdue_orders = query.filter(
        LabOrder.due_date < datetime.utcnow(),
        LabOrder.status.notin_(['completed', 'cancelled'])
    ).count()
    
    return {
        'total_orders': total_orders,
        'status_breakdown': {status: count for status, count in status_counts},
        'overdue_orders': overdue_orders
    }

def _validate_lab_results(results: List[Dict]) -> bool:
    """Validate lab results structure"""
    if not isinstance(results, list):
        return False
    
    for result in results:
        if not isinstance(result, dict):
            return False
        if 'test_name' not in result or 'result' not in result:
            return False
        if not isinstance(result['test_name'], str) or not isinstance(result['result'], (str, int, float)):
            return False
    
    return True

def _create_audit_trail(tenant_id: str, user_id: int, action: str, resource_type: str, resource_id: int, details: str):
    """Create an audit trail entry"""
    from ..models import AuditTrail
    
    audit_entry = AuditTrail(
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string
    )
    
    db.session.add(audit_entry)
    # Don't commit here - let the calling function handle the transaction

def _get_lab_orders_overview(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get lab orders overview statistics"""
    query = multi_tenant_query(LabOrder.query, tenant_id)
    query = query.filter(LabOrder.created_at.between(start_date, end_date))
    
    total_orders = query.count()
    completed_orders = query.filter_by(status='completed').count()
    overdue_orders = query.filter(
        LabOrder.due_date < datetime.utcnow(),
        LabOrder.status.notin_(['completed', 'cancelled'])
    ).count()
    
    return {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'overdue_orders': overdue_orders,
        'completion_rate': (completed_orders / total_orders * 100) if total_orders > 0 else 0
    }

def _get_lab_orders_status_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get lab orders status breakdown"""
    query = multi_tenant_query(LabOrder.query, tenant_id)
    status_breakdown = query.filter(LabOrder.created_at.between(start_date, end_date))\
                          .group_by(LabOrder.status)\
                          .with_entities(LabOrder.status, db.func.count(LabOrder.id))\
                          .all()
    
    return {status: count for status, count in status_breakdown}

def _get_lab_orders_type_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get lab orders type breakdown"""
    query = multi_tenant_query(LabOrder.query, tenant_id)
    type_breakdown = query.filter(LabOrder.created_at.between(start_date, end_date))\
                         .group_by(LabOrder.type)\
                         .with_entities(LabOrder.type, db.func.count(LabOrder.id))\
                         .all()
    
    return {order_type: count for order_type, count in type_breakdown}

def _get_turnaround_times(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """Get average turnaround times for completed orders"""
    query = multi_tenant_query(LabOrder.query, tenant_id)
    completed_orders = query.filter(
        LabOrder.status == 'completed',
        LabOrder.created_at.between(start_date, end_date),
        LabOrder.completed_date.isnot(None)
    )
    
    avg_turnaround = completed_orders.with_entities(
        db.func.avg(LabOrder.completed_date - LabOrder.created_at)
    ).scalar()
    
    return {
        'average_turnaround_days': avg_turnaround.days if avg_turnaround else 0
    }

def _get_lab_performance(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get performance metrics by lab"""
    query = multi_tenant_query(LabOrder.query, tenant_id)
    lab_performance = query.filter(LabOrder.created_at.between(start_date, end_date))\
                          .group_by(LabOrder.lab_id)\
                          .with_entities(
                              LabOrder.lab_id,
                              db.func.count(LabOrder.id),
                              db.func.avg(LabOrder.completed_date - LabOrder.created_date),
                              db.func.avg(db.case((LabOrder.status == 'completed', 1), else_=0))
                          ).all()
    
    # This would need to be enhanced with lab details
    return [{
        'lab_id': lab_id,
        'total_orders': count,
        'avg_turnaround_days': avg_turnaround.days if avg_turnaround else 0,
        'completion_rate': float(completion_rate * 100) if completion_rate else 0
    } for lab_id, count, avg_turnaround, completion_rate in lab_performance]

@labs_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@labs_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@labs_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429