# routes/audit.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import AuditTrail, db

audit_bp = Blueprint('audit', __name__, url_prefix='/api/audit')

# RBAC Permission Constants
PERMISSION_VIEW_AUDIT_LOGS = 'view_audit_logs'
PERMISSION_EXPORT_AUDIT_LOGS = 'export_audit_logs'
PERMISSION_MANAGE_AUDIT_CONFIG = 'manage_audit_config'

@audit_bp.route('/logs', methods=['GET'])
@rate_limit(limit=60, period=3600)  # 60 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_AUDIT_LOGS)
def get_audit_logs():
    """
    Get audit logs with advanced filtering, sorting, and tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 200)  # Cap at 200 per page
        
        # Filter parameters
        user_id = request.args.get('user_id', type=int)
        action = request.args.get('action')
        resource_type = request.args.get('resource_type')
        resource_id = request.args.get('resource_id')
        status = request.args.get('status')
        
        # Date range filtering
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        # Build base query with tenant filtering
        query = multi_tenant_query(AuditTrail.query, tenant_id)
        
        # Apply filters
        if user_id:
            query = query.filter(AuditTrail.user_id == user_id)
        if action:
            query = query.filter(AuditTrail.action == action)
        if resource_type:
            query = query.filter(AuditTrail.resource_type == resource_type)
        if resource_id:
            query = query.filter(AuditTrail.resource_id == resource_id)
        if status:
            query = query.filter(AuditTrail.status == status)
        
        # Date range filtering
        if start_date_str:
            try:
                start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
                query = query.filter(AuditTrail.timestamp >= start_date)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use ISO format.'}), 400
        
        if end_date_str:
            try:
                end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                query = query.filter(AuditTrail.timestamp <= end_date)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use ISO format.'}), 400
        
        # Default to last 30 days if no date range provided
        if not start_date_str and not end_date_str:
            default_start_date = datetime.utcnow() - timedelta(days=30)
            query = query.filter(AuditTrail.timestamp >= default_start_date)
        
        # Sorting
        sort_by = request.args.get('sort_by', 'timestamp')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(AuditTrail, sort_by).asc())
        else:
            query = query.order_by(getattr(AuditTrail, sort_by).desc())
        
        # Pagination
        logs = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Get summary statistics
        summary = _get_audit_summary(tenant_id, query)
        
        return jsonify({
            'logs': [log.to_dict() for log in logs.items],
            'pagination': {
                'page': logs.page,
                'per_page': logs.per_page,
                'total': logs.total,
                'pages': logs.pages,
                'has_next': logs.has_next,
                'has_prev': logs.has_prev
            },
            'filters': {
                'user_id': user_id,
                'action': action,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'status': status,
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve audit logs', 'details': str(e)}), 500

@audit_bp.route('/logs/export', methods=['GET'])
@rate_limit(limit=10, period=3600)  # 10 exports per hour
@tenant_required
@permission_required(PERMISSION_EXPORT_AUDIT_LOGS)
def export_audit_logs():
    """
    Export audit logs in various formats (CSV, JSON)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        format_type = request.args.get('format', 'json').lower()
        
        # Get filtered logs (similar to get_audit_logs but without pagination)
        query = _build_audit_query(tenant_id, request.args)
        logs = query.limit(10000).all()  # Limit exports to 10,000 records
        
        if format_type == 'csv':
            return _export_logs_csv(logs), 200
        elif format_type == 'json':
            return _export_logs_json(logs), 200
        else:
            return jsonify({'error': 'Unsupported export format. Use "csv" or "json".'}), 400
            
    except Exception as e:
        return jsonify({'error': 'Failed to export audit logs', 'details': str(e)}), 500

@audit_bp.route('/stats', methods=['GET'])
@rate_limit(limit=30, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_AUDIT_LOGS)
def get_audit_statistics():
    """
    Get audit trail statistics and insights
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'activity_overview': _get_activity_overview(tenant_id, start_date, end_date),
            'top_users': _get_top_users_by_activity(tenant_id, start_date, end_date),
            'action_breakdown': _get_action_breakdown(tenant_id, start_date, end_date),
            'resource_breakdown': _get_resource_breakdown(tenant_id, start_date, end_date),
            'success_rate': _get_success_rate(tenant_id, start_date, end_date),
            'hourly_activity': _get_hourly_activity(tenant_id, start_date, end_date)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve audit statistics', 'details': str(e)}), 500

@audit_bp.route('/config', methods=['GET', 'PUT'])
@rate_limit(limit=20, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_AUDIT_CONFIG)
def manage_audit_config():
    """
    Get or update audit configuration for the tenant
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        if request.method == 'GET':
            config = _get_audit_config(tenant_id)
            return jsonify(config), 200
        
        elif request.method == 'PUT':
            config_data = request.get_json()
            updated_config = _update_audit_config(tenant_id, config_data)
            return jsonify(updated_config), 200
            
    except Exception as e:
        return jsonify({'error': 'Failed to manage audit configuration', 'details': str(e)}), 500

@audit_bp.route('/users/<int:user_id>/activity', methods=['GET'])
@rate_limit(limit=40, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_AUDIT_LOGS)
def get_user_activity(user_id: int):
    """
    Get detailed activity for a specific user
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Verify the user belongs to the same tenant
        from ..models import User
        user_query = multi_tenant_query(User.query, tenant_id)
        user = user_query.filter_by(id=user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        query = multi_tenant_query(AuditTrail.query, tenant_id)
        logs = query.filter_by(user_id=user_id)\
                  .order_by(AuditTrail.timestamp.desc())\
                  .paginate(page=page, per_page=per_page, error_out=False)
        
        user_stats = _get_user_activity_stats(tenant_id, user_id)
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': f"{user.first_name} {user.last_name}" if user.first_name and user.last_name else None
            },
            'activity': [log.to_dict() for log in logs.items],
            'stats': user_stats,
            'pagination': {
                'page': logs.page,
                'per_page': logs.per_page,
                'total': logs.total,
                'pages': logs.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve user activity', 'details': str(e)}), 500

# Helper functions with tenant filtering
def _build_audit_query(tenant_id: str, args: Dict[str, Any]) -> Any:
    """Build filtered audit query"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    
    # Apply filters from request args
    filters = {
        'user_id': args.get('user_id', type=int),
        'action': args.get('action'),
        'resource_type': args.get('resource_type'),
        'resource_id': args.get('resource_id'),
        'status': args.get('status')
    }
    
    for field, value in filters.items():
        if value:
            query = query.filter(getattr(AuditTrail, field) == value)
    
    # Date range filtering
    start_date_str = args.get('start_date')
    end_date_str = args.get('end_date')
    
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
            query = query.filter(AuditTrail.timestamp >= start_date)
        except ValueError:
            pass
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
            query = query.filter(AuditTrail.timestamp <= end_date)
        except ValueError:
            pass
    
    return query

def _get_audit_summary(tenant_id: str, query: Any) -> Dict[str, Any]:
    """Get summary statistics for audit logs"""
    total_logs = query.count()
    
    # Count by status
    status_counts = query.with_entities(
        AuditTrail.status, db.func.count(AuditTrail.id)
    ).group_by(AuditTrail.status).all()
    
    # Count by action
    action_counts = query.with_entities(
        AuditTrail.action, db.func.count(AuditTrail.id)
    ).group_by(AuditTrail.action).order_by(db.func.count(AuditTrail.id).desc()).limit(5).all()
    
    return {
        'total_records': total_logs,
        'status_breakdown': {status: count for status, count in status_counts},
        'top_actions': {action: count for action, count in action_counts}
    }

def _export_logs_csv(logs: List[AuditTrail]) -> Any:
    """Export logs as CSV"""
    import csv
    from io import StringIO
    from flask import Response
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Timestamp', 'User ID', 'Action', 'Resource Type', 'Resource ID',
        'Status', 'IP Address', 'User Agent', 'Details'
    ])
    
    # Write data
    for log in logs:
        writer.writerow([
            log.timestamp.isoformat(),
            log.user_id,
            log.action,
            log.resource_type,
            log.resource_id,
            log.status,
            log.ip_address or '',
            log.user_agent or '',
            log.details or ''
        ])
    
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=audit_logs_export.csv'}
    )

def _export_logs_json(logs: List[AuditTrail]) -> Any:
    """Export logs as JSON"""
    from flask import Response
    import json
    
    logs_data = [log.to_dict() for log in logs]
    
    return Response(
        json.dumps(logs_data, indent=2, default=str),
        mimetype='application/json',
        headers={'Content-Disposition': 'attachment; filename=audit_logs_export.json'}
    )

def _get_activity_overview(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get activity overview statistics"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    query = query.filter(AuditTrail.timestamp.between(start_date, end_date))
    
    total_activities = query.count()
    successful_activities = query.filter_by(status='success').count()
    failed_activities = query.filter_by(status='failed').count()
    
    return {
        'total_activities': total_activities,
        'successful_activities': successful_activities,
        'failed_activities': failed_activities,
        'success_rate': (successful_activities / total_activities * 100) if total_activities > 0 else 0
    }

def _get_top_users_by_activity(tenant_id: str, start_date: datetime, end_date: datetime) -> List[Dict]:
    """Get top users by activity count"""
    from ..models import User
    query = multi_tenant_query(AuditTrail.query.join(User), tenant_id)
    
    top_users = query.filter(AuditTrail.timestamp.between(start_date, end_date))\
                   .group_by(User.id, User.username, User.first_name, User.last_name)\
                   .with_entities(
                       User.id,
                       User.username,
                       User.first_name,
                       User.last_name,
                       db.func.count(AuditTrail.id).label('activity_count')
                   ).order_by(db.func.count(AuditTrail.id).desc())\
                   .limit(10)\
                   .all()
    
    return [{
        'user_id': user_id,
        'username': username,
        'full_name': f"{first_name} {last_name}" if first_name and last_name else None,
        'activity_count': activity_count
    } for user_id, username, first_name, last_name, activity_count in top_users]

def _get_action_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get breakdown of actions"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    
    action_breakdown = query.filter(AuditTrail.timestamp.between(start_date, end_date))\
                          .group_by(AuditTrail.action)\
                          .with_entities(AuditTrail.action, db.func.count(AuditTrail.id))\
                          .order_by(db.func.count(AuditTrail.id).desc())\
                          .all()
    
    return {action: count for action, count in action_breakdown}

def _get_resource_breakdown(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, int]:
    """Get breakdown of resource types"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    
    resource_breakdown = query.filter(AuditTrail.timestamp.between(start_date, end_date))\
                            .group_by(AuditTrail.resource_type)\
                            .with_entities(AuditTrail.resource_type, db.func.count(AuditTrail.id))\
                            .order_by(db.func.count(AuditTrail.id).desc())\
                            .all()
    
    return {resource_type: count for resource_type, count in resource_breakdown}

def _get_success_rate(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
    """Get success rate by action"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    
    success_rates = query.filter(AuditTrail.timestamp.between(start_date, end_date))\
                       .group_by(AuditTrail.action)\
                       .with_entities(
                           AuditTrail.action,
                           db.func.count(AuditTrail.id),
                           db.func.avg(db.case((AuditTrail.status == 'success', 1), else_=0))
                       ).all()
    
    return {action: float(rate * 100) for action, total, rate in success_rates}

def _get_hourly_activity(tenant_id: str, start_date: datetime, end_date: datetime) -> Dict[int, int]:
    """Get activity by hour of day"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    
    hourly_activity = query.filter(AuditTrail.timestamp.between(start_date, end_date))\
                         .group_by(db.func.extract('hour', AuditTrail.timestamp))\
                         .with_entities(
                             db.func.extract('hour', AuditTrail.timestamp).label('hour'),
                             db.func.count(AuditTrail.id)
                         ).order_by('hour')\
                         .all()
    
    return {int(hour): count for hour, count in hourly_activity}

def _get_audit_config(tenant_id: str) -> Dict[str, Any]:
    """Get audit configuration for tenant"""
    # This would typically come from a configuration table
    # For now, return default configuration
    return {
        'retention_period_days': 365,
        'log_level': 'INFO',
        'enabled': True,
        'log_user_actions': True,
        'log_system_events': True,
        'log_failed_logins': True,
        'log_sensitive_operations': True
    }

def _update_audit_config(tenant_id: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Update audit configuration for tenant"""
    # This would typically update a configuration table
    # For now, just return the received data with defaults
    default_config = _get_audit_config(tenant_id)
    updated_config = {**default_config, **config_data}
    return updated_config

def _get_user_activity_stats(tenant_id: str, user_id: int) -> Dict[str, Any]:
    """Get statistics for a specific user's activity"""
    query = multi_tenant_query(AuditTrail.query, tenant_id)
    user_activity = query.filter_by(user_id=user_id)
    
    total_actions = user_activity.count()
    last_activity = user_activity.order_by(AuditTrail.timestamp.desc()).first()
    
    action_breakdown = user_activity.group_by(AuditTrail.action)\
                                  .with_entities(AuditTrail.action, db.func.count(AuditTrail.id))\
                                  .all()
    
    return {
        'total_actions': total_actions,
        'last_activity': last_activity.timestamp.isoformat() if last_activity else None,
        'action_breakdown': {action: count for action, count in action_breakdown},
        'success_rate': (user_activity.filter_by(status='success').count() / total_actions * 100) if total_actions > 0 else 0
    }

@audit_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@audit_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@audit_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429