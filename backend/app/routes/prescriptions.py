# routes/prescriptions.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import Prescription, Patient, User, db

prescriptions_bp = Blueprint('prescriptions', __name__, url_prefix='/api/prescriptions')

# RBAC Permission Constants
PERMISSION_VIEW_PRESCRIPTIONS = 'view_prescriptions'
PERMISSION_CREATE_PRESCRIPTIONS = 'create_prescriptions'
PERMISSION_EDIT_PRESCRIPTIONS = 'edit_prescriptions'
PERMISSION_DELETE_PRESCRIPTIONS = 'delete_prescriptions'
PERMISSION_APPROVE_PRESCRIPTIONS = 'approve_prescriptions'
PERMISSION_DISPENSE_PRESCRIPTIONS = 'dispense_prescriptions'

@prescriptions_bp.route('/', methods=['GET'])
@rate_limit(limit=100, period=3600)  # 100 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_PRESCRIPTIONS)
def get_prescriptions():
    """
    Get prescriptions with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        patient_id = request.args.get('patient_id', type=int)
        prescriber_id = request.args.get('prescriber_id', type=int)
        status = request.args.get('status')
        medication = request.args.get('medication')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(Prescription.query, tenant_id)
        
        # Apply filters
        if patient_id:
            query = query.filter(Prescription.patient_id == patient_id)
        if prescriber_id:
            query = query.filter(Prescription.prescriber_id == prescriber_id)
        if status:
            query = query.filter(Prescription.status == status)
        if medication:
            query = query.filter(Prescription.medication.ilike(f'%{medication}%'))
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(Prescription.created_at >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(Prescription.created_at <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(Prescription, sort_by).asc())
        else:
            query = query.order_by(getattr(Prescription, sort_by).desc())
        
        # Pagination
        prescriptions = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'prescriptions': [rx.to_dict(include_details=True) for rx in prescriptions.items],
            'pagination': {
                'page': prescriptions.page,
                'per_page': prescriptions.per_page,
                'total': prescriptions.total,
                'pages': prescriptions.pages,
                'has_next': prescriptions.has_next,
                'has_prev': prescriptions.has_prev
            },
            'filters': {
                'patient_id': patient_id,
                'prescriber_id': prescriber_id,
                'status': status,
                'medication': medication,
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'summary': _get_prescriptions_summary(tenant_id, query)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve prescriptions', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PRESCRIPTIONS)
def get_prescription(prescription_id):
    """
    Get a specific prescription with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        return jsonify(prescription.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_CREATE_PRESCRIPTIONS)
def create_prescription():
    """
    Create a new prescription with tenant isolation and validation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['patient_id', 'medication', 'dosage', 'instructions']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if patient belongs to the same tenant
        patient_query = multi_tenant_query(Patient.query, tenant_id)
        patient = patient_query.filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Validate medication dosage
        if not _validate_dosage(data['dosage']):
            return jsonify({'error': 'Invalid dosage format'}), 400
        
        # Check for drug interactions if medication list is provided
        if 'additional_medications' in data:
            interactions = _check_drug_interactions(data['medication'], data['additional_medications'])
            if interactions:
                return jsonify({
                    'error': 'Potential drug interactions detected',
                    'interactions': interactions,
                    'warning': 'Please review before proceeding'
                }), 409
        
        # Create prescription
        prescription = Prescription(
            tenant_id=tenant_id,
            patient_id=data['patient_id'],
            prescriber_id=user_id,
            medication=data['medication'],
            dosage=data['dosage'],
            instructions=data['instructions'],
            status='draft',  # Start as draft, require approval
            created_by=user_id
        )
        
        # Optional fields
        optional_fields = [
            'quantity', 'refills', 'duration_days', 'route', 'frequency',
            'start_date', 'end_date', 'pharmacy_notes', 'special_instructions',
            'is_controlled', 'dea_schedule', 'prior_authorization_required'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(prescription, field, data[field])
        
        # Handle dates
        if 'start_date' in data:
            prescription.start_date = _parse_date(data['start_date'])
        if 'end_date' in data:
            prescription.end_date = _parse_date(data['end_date'])
        
        db.session.add(prescription)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'create', 'prescription', prescription.id, 
                           f'Prescription created for {patient.first_name} {patient.last_name}')
        
        return jsonify({
            'message': 'Prescription created successfully',
            'prescription': prescription.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>', methods=['PUT'])
@rate_limit(limit=50, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_PRESCRIPTIONS)
def update_prescription(prescription_id):
    """
    Update an existing prescription with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        # Check if prescription can be modified
        if prescription.status in ['approved', 'dispensed', 'completed']:
            return jsonify({'error': f'Cannot modify prescription with status: {prescription.status}'}), 400
        
        data = request.get_json()
        
        # Update fields
        updateable_fields = [
            'medication', 'dosage', 'instructions', 'quantity', 'refills',
            'duration_days', 'route', 'frequency', 'pharmacy_notes',
            'special_instructions', 'prior_authorization_required'
        ]
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                old_value = getattr(prescription, field)
                new_value = data[field]
                
                # Validate dosage if being updated
                if field == 'dosage' and not _validate_dosage(new_value):
                    return jsonify({'error': 'Invalid dosage format'}), 400
                
                if old_value != new_value:
                    setattr(prescription, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        # Handle date updates
        if 'start_date' in data:
            new_start_date = _parse_date(data['start_date'])
            if prescription.start_date != new_start_date:
                changes['start_date'] = {'old': prescription.start_date, 'new': new_start_date}
                prescription.start_date = new_start_date
        
        if 'end_date' in data:
            new_end_date = _parse_date(data['end_date'])
            if prescription.end_date != new_end_date:
                changes['end_date'] = {'old': prescription.end_date, 'new': new_end_date}
                prescription.end_date = new_end_date
        
        if changes:
            prescription.updated_by = user_id
            prescription.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, user_id, 'update', 'prescription', prescription.id, 
                               f'Prescription updated: {changes}')
        
        return jsonify({
            'message': 'Prescription updated successfully',
            'prescription': prescription.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>/approve', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_APPROVE_PRESCRIPTIONS)
def approve_prescription(prescription_id):
    """
    Approve a prescription (typically by a supervising physician or pharmacist)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        if prescription.status != 'draft':
            return jsonify({'error': f'Prescription must be in draft status to approve. Current status: {prescription.status}'}), 400
        
        data = request.get_json()
        approval_notes = data.get('approval_notes', '')
        
        # Store old status for audit trail
        old_status = prescription.status
        
        prescription.status = 'approved'
        prescription.approved_by = user_id
        prescription.approval_date = datetime.utcnow()
        prescription.approval_notes = approval_notes
        prescription.updated_by = user_id
        prescription.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'prescription', prescription.id, 
                           f'Prescription approved. Notes: {approval_notes}')
        
        return jsonify({
            'message': 'Prescription approved successfully',
            'prescription': prescription.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to approve prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>/dispense', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_DISPENSE_PRESCRIPTIONS)
def dispense_prescription(prescription_id):
    """
    Mark a prescription as dispensed
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        if prescription.status != 'approved':
            return jsonify({'error': f'Prescription must be approved to dispense. Current status: {prescription.status}'}), 400
        
        data = request.get_json()
        dispense_notes = data.get('dispense_notes', '')
        quantity_dispensed = data.get('quantity_dispensed', prescription.quantity)
        
        # Store old status for audit trail
        old_status = prescription.status
        
        prescription.status = 'dispensed'
        prescription.dispensed_by = user_id
        prescription.dispense_date = datetime.utcnow()
        prescription.quantity_dispensed = quantity_dispensed
        prescription.dispense_notes = dispense_notes
        prescription.updated_by = user_id
        prescription.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'prescription', prescription.id, 
                           f'Prescription dispensed. Quantity: {quantity_dispensed}')
        
        return jsonify({
            'message': 'Prescription dispensed successfully',
            'prescription': prescription.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to dispense prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>/cancel', methods=['POST'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_EDIT_PRESCRIPTIONS)
def cancel_prescription(prescription_id):
    """
    Cancel a prescription
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        if prescription.status in ['completed', 'cancelled']:
            return jsonify({'error': f'Cannot cancel prescription with status: {prescription.status}'}), 400
        
        data = request.get_json()
        cancellation_reason = data.get('cancellation_reason', '')
        
        if not cancellation_reason:
            return jsonify({'error': 'Cancellation reason is required'}), 400
        
        # Store old status for audit trail
        old_status = prescription.status
        
        prescription.status = 'cancelled'
        prescription.cancelled_by = user_id
        prescription.cancellation_date = datetime.utcnow()
        prescription.cancellation_reason = cancellation_reason
        prescription.updated_by = user_id
        prescription.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'update', 'prescription', prescription.id, 
                           f'Prescription cancelled. Reason: {cancellation_reason}')
        
        return jsonify({
            'message': 'Prescription cancelled successfully',
            'prescription': prescription.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to cancel prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/<int:prescription_id>', methods=['DELETE'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_DELETE_PRESCRIPTIONS)
def delete_prescription(prescription_id):
    """
    Delete a prescription (soft delete)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        user_id = current_user_obj.id
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescription = query.filter_by(id=prescription_id).first()
        
        if not prescription:
            return jsonify({'error': 'Prescription not found'}), 404
        
        # Only allow deletion of draft prescriptions
        if prescription.status != 'draft':
            return jsonify({'error': f'Cannot delete prescription with status: {prescription.status}'}), 400
        
        # Soft delete
        prescription.is_active = False
        prescription.deleted_by = user_id
        prescription.deleted_at = datetime.utcnow()
        prescription.updated_by = user_id
        prescription.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, user_id, 'delete', 'prescription', prescription.id, 
                           'Prescription deleted')
        
        return jsonify({
            'message': 'Prescription deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete prescription', 'details': str(e)}), 500

@prescriptions_bp.route('/patient/<int:patient_id>', methods=['GET'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PRESCRIPTIONS)
def get_patient_prescriptions(patient_id):
    """
    Get all prescriptions for a specific patient
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Verify patient belongs to tenant
        patient_query = multi_tenant_query(Patient.query, tenant_id)
        patient = patient_query.filter_by(id=patient_id).first()
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        query = multi_tenant_query(Prescription.query, tenant_id)
        prescriptions = query.filter_by(patient_id=patient_id)\
                           .order_by(Prescription.created_at.desc())\
                           .all()
        
        return jsonify({
            'patient': patient.to_dict(include_basic_info=True),
            'prescriptions': [rx.to_dict(include_details=True) for rx in prescriptions],
            'total_count': len(prescriptions),
            'active_count': len([rx for rx in prescriptions if rx.status in ['approved', 'dispensed']])
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve patient prescriptions', 'details': str(e)}), 500

@prescriptions_bp.route('/stats', methods=['GET'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_PRESCRIPTIONS)
def get_prescription_statistics():
    """
    Get prescription statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'overview': _get_prescriptions_overview(tenant_id, start_date, end_date),
            'medication_breakdown': _get_medication_breakdown(tenant_id, start_date, end_date),
            'status_breakdown': _get_status_breakdown(tenant_id, start_date, end_date),
            'prescriber_metrics': _get_prescriber_metrics(tenant_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve prescription statistics', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _get_prescriptions_summary(tenant_id: str, query: Any) -> Dict[str, Any]:
    """Get summary statistics for prescriptions"""
    total_prescriptions = query.count()
    
    # Count by status
    status_counts = query.with_entities(
        Prescription.status, db.func.count(Prescription.id)
    ).group_by(Prescription.status).all()
    
    # Count controlled substances
    controlled_count = query.filter_by(is_controlled=True).count()
    
    return {
        'total_prescriptions': total_prescriptions,
        'status_breakdown': {status: count for status, count in status_counts},
        'controlled_substances': controlled_count
    }

def _validate_dosage(dosage: str) -> bool:
    """Validate dosage format"""
    # Basic validation - can be enhanced with more complex rules
    if not dosage or len(dosage) > 100:
        return False
    return True

def _check_drug_interactions(primary_med: str, additional_meds: List[str]) -> List[str]:
    """Check for potential drug interactions"""
    # This would typically integrate with a drug interaction API
    # For now, return empty list (no interactions detected)
    interactions = []
    
    # Placeholder for interaction logic
    # In production, this would call an external API or use a local database
    
    return interactions

def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """Parse date string to datetime object"""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        return None

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

def _get_prescriptions_overview(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get prescriptions overview statistics"""
    query = multi_tenant_query(Prescription.query, tenant_id)
    query = query.filter(Prescription.created_at.between(start_date, end_date))
    
    total_prescriptions = query.count()
    approved_prescriptions = query.filter_by(status='approved').count()
    dispensed_prescriptions = query.filter_by(status='dispensed').count()
    
    return {
        'total_prescriptions': total_prescriptions,
        'approved_prescriptions': approved_prescriptions,
        'dispensed_prescriptions': dispensed_prescriptions,
        'approval_rate': (approved_prescriptions / total_prescriptions * 100) if total_prescriptions > 0 else 0
    }

def _get_medication_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get medication breakdown"""
    query = multi_tenant_query(Prescription.query, tenant_id)
    medication_breakdown = query.filter(Prescription.created_at.between(start_date, end_date))\
                              .group_by(Prescription.medication)\
                              .with_entities(Prescription.medication, db.func.count(Prescription.id))\
                              .order_by(db.func.count(Prescription.id).desc())\
                              .limit(10)\
                              .all()
    
    return {medication: count for medication, count in medication_breakdown}

def _get_status_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get status breakdown"""
    query = multi_tenant_query(Prescription.query, tenant_id)
    status_breakdown = query.filter(Prescription.created_at.between(start_date, end_date))\
                           .group_by(Prescription.status)\
                           .with_entities(Prescription.status, db.func.count(Prescription.id))\
                           .all()
    
    return {status: count for status, count in status_breakdown}

def _get_prescriber_metrics(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get prescriber performance metrics"""
    query = multi_tenant_query(Prescription.query.join(User), tenant_id)
    prescriber_metrics = query.filter(Prescription.created_at.between(start_date, end_date))\
                             .group_by(User.id, User.first_name, User.last_name)\
                             .with_entities(
                                 User.id,
                                 User.first_name,
                                 User.last_name,
                                 db.func.count(Prescription.id),
                                 db.func.avg(db.case((Prescription.status == 'approved', 1), else_=0))
                             ).all()
    
    return [{
        'prescriber_id': prescriber_id,
        'prescriber_name': f"{first_name} {last_name}",
        'total_prescriptions': count,
        'approval_rate': float(approval_rate * 100) if approval_rate else 0
    } for prescriber_id, first_name, last_name, count, approval_rate in prescriber_metrics]

@prescriptions_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@prescriptions_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@prescriptions_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429