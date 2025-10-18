# routes/organizations.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query, get_current_tenant
from ..utils.rate_limit import rate_limit

from ..models import Organization, User, db

organizations_bp = Blueprint('organizations', __name__, url_prefix='/api/organizations')

# RBAC Permission Constants
PERMISSION_VIEW_ORGANIZATIONS = 'view_organizations'
PERMISSION_CREATE_ORGANIZATIONS = 'create_organizations'
PERMISSION_EDIT_ORGANIZATIONS = 'edit_organizations'
PERMISSION_DELETE_ORGANIZATIONS = 'delete_organizations'
PERMISSION_MANAGE_ORGANIZATION_SETTINGS = 'manage_organization_settings'
PERMISSION_VIEW_ORGANIZATION_REPORTS = 'view_organization_reports'

@organizations_bp.route('/', methods=['GET'])
@rate_limit(limit=60, period=3600)  # 60 requests per hour
@permission_required(PERMISSION_VIEW_ORGANIZATIONS)
def get_organizations():
    """
    Get organizations with advanced filtering, sorting, and pagination
    Note: This endpoint is typically for super admins only
    """
    try:
        current_user_obj = get_current_user()
        
        # Only super admins can list all organizations
        if not current_user_obj.is_super_admin:
            return jsonify({'error': 'Access denied. Super admin privileges required.'}), 403
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Cap at 100 per page
        
        # Filter parameters
        organization_type = request.args.get('type')
        subscription_plan = request.args.get('subscription_plan')
        is_active = request.args.get('is_active', type=bool)
        search = request.args.get('search')
        
        # Date range filtering
        created_after_str = request.args.get('created_after')
        created_before_str = request.args.get('created_before')
        
        # Build base query
        query = Organization.query
        
        # Apply filters
        if organization_type:
            query = query.filter(Organization.type == organization_type)
        if subscription_plan:
            query = query.filter(Organization.subscription_plan == subscription_plan)
        if is_active is not None:
            query = query.filter(Organization.is_active == is_active)
        if search:
            query = query.filter(
                db.or_(
                    Organization.name.ilike(f'%{search}%'),
                    Organization.id.ilike(f'%{search}%')
                )
            )
        
        # Date range filtering
        if created_after_str:
            try:
                created_after = datetime.fromisoformat(created_after_str.replace('Z', '+00:00'))
                query = query.filter(Organization.created_at >= created_after)
            except ValueError:
                return jsonify({'error': 'Invalid created_after format. Use ISO format.'}), 400
        
        if created_before_str:
            try:
                created_before = datetime.fromisoformat(created_before_str.replace('Z', '+00:00'))
                query = query.filter(Organization.created_at <= created_before)
            except ValueError:
                return jsonify({'error': 'Invalid created_before format. Use ISO format.'}), 400
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(Organization, sort_by).asc())
        else:
            query = query.order_by(getattr(Organization, sort_by).desc())
        
        # Pagination
        organizations = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'organizations': [org.to_dict(include_details=True) for org in organizations.items],
            'pagination': {
                'page': organizations.page,
                'per_page': organizations.per_page,
                'total': organizations.total,
                'pages': organizations.pages,
                'has_next': organizations.has_next,
                'has_prev': organizations.has_prev
            },
            'filters': {
                'type': organization_type,
                'subscription_plan': subscription_plan,
                'is_active': is_active,
                'search': search,
                'created_after': created_after_str,
                'created_before': created_before_str
            },
            'summary': _get_organizations_summary(query)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve organizations', 'details': str(e)}), 500

@organizations_bp.route('/current', methods=['GET'])
@rate_limit(limit=120, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_ORGANIZATIONS)
def get_current_organization():
    """
    Get the current user's organization with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        query = multi_tenant_query(Organization.query, tenant_id)
        organization = query.first()  # Each tenant has one organization
        
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        return jsonify(organization.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve organization', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>', methods=['GET'])
@rate_limit(limit=100, period=3600)
@permission_required(PERMISSION_VIEW_ORGANIZATIONS)
def get_organization(org_id):
    """
    Get a specific organization (super admin only or tenant access)
    """
    try:
        current_user_obj = get_current_user()
        
        # For super admins, allow access to any organization
        if current_user_obj.is_super_admin:
            organization = Organization.query.get_or_404(org_id)
        else:
            # For regular users, only allow access to their own organization
            if current_user_obj.tenant_id != org_id:
                return jsonify({'error': 'Access denied'}), 403
            
            query = multi_tenant_query(Organization.query, org_id)
            organization = query.first()
            
            if not organization:
                return jsonify({'error': 'Organization not found'}), 404
        
        return jsonify(organization.to_dict(include_details=True)), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve organization', 'details': str(e)}), 500

@organizations_bp.route('/', methods=['POST'])
@rate_limit(limit=20, period=3600)  # Limit organization creation
@permission_required(PERMISSION_CREATE_ORGANIZATIONS)
def create_organization():
    """
    Create a new organization (typically for super admins or self-signup)
    """
    try:
        current_user_obj = get_current_user()
        
        # Only super admins can create organizations directly
        # For self-signup, this would be handled differently with proper validation
        if not current_user_obj.is_super_admin:
            return jsonify({'error': 'Access denied. Super admin privileges required.'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id', 'name', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if organization ID already exists
        if Organization.query.filter_by(id=data['id']).first():
            return jsonify({'error': 'Organization ID already exists'}), 409
        
        # Create organization
        organization = Organization(
            id=data['id'],
            name=data['name'],
            type=data['type'],
            subscription_plan=data.get('subscription_plan', 'starter'),
            is_active=data.get('is_active', True),
            settings=data.get('settings', {})
        )
        
        db.session.add(organization)
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(None, current_user_obj.id, 'create', 'organization', organization.id, 
                           f'Organization created: {organization.name}')
        
        return jsonify({
            'message': 'Organization created successfully',
            'organization': organization.to_dict(include_details=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create organization', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>', methods=['PUT'])
@rate_limit(limit=40, period=3600)
@permission_required(PERMISSION_EDIT_ORGANIZATIONS)
def update_organization(org_id):
    """
    Update an organization (super admin or organization admin)
    """
    try:
        current_user_obj = get_current_user()
        
        # Check access rights
        if current_user_obj.is_super_admin:
            organization = Organization.query.get_or_404(org_id)
        else:
            # Organization admins can only update their own organization
            if current_user_obj.tenant_id != org_id:
                return jsonify({'error': 'Access denied'}), 403
            
            if not current_user_obj.has_permission(PERMISSION_EDIT_ORGANIZATIONS):
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            query = multi_tenant_query(Organization.query, org_id)
            organization = query.first()
            
            if not organization:
                return jsonify({'error': 'Organization not found'}), 404
        
        data = request.get_json()
        
        # Validate and update fields
        updateable_fields = [
            'name', 'type', 'subscription_plan', 'is_active', 'settings'
        ]
        
        # Super admins have additional privileges
        super_admin_fields = ['subscription_plan', 'is_active']
        
        changes = {}
        for field in updateable_fields:
            if field in data:
                # Check if regular user is trying to update super-admin-only fields
                if not current_user_obj.is_super_admin and field in super_admin_fields:
                    return jsonify({'error': f'Insufficient permissions to update {field}'}), 403
                
                old_value = getattr(organization, field)
                new_value = data[field]
                
                if old_value != new_value:
                    setattr(organization, field, new_value)
                    changes[field] = {'old': old_value, 'new': new_value}
        
        if changes:
            organization.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(organization.id, current_user_obj.id, 'update', 'organization', organization.id, 
                               f'Organization updated: {changes}')
        
        return jsonify({
            'message': 'Organization updated successfully',
            'organization': organization.to_dict(include_details=True),
            'changes': changes if changes else 'No changes made'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update organization', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>/settings', methods=['GET', 'PUT'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_MANAGE_ORGANIZATION_SETTINGS)
def manage_organization_settings(org_id):
    """
    Get or update organization settings with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Verify the user is accessing their own organization
        if tenant_id != org_id:
            return jsonify({'error': 'Access denied'}), 403
        
        query = multi_tenant_query(Organization.query, tenant_id)
        organization = query.first()
        
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'settings': organization.settings or {},
                'last_updated': organization.updated_at.isoformat() if organization.updated_at else None
            }), 200
        
        elif request.method == 'PUT':
            data = request.get_json()
            new_settings = data.get('settings', {})
            
            if not isinstance(new_settings, dict):
                return jsonify({'error': 'Settings must be a dictionary'}), 400
            
            # Validate settings structure
            validation_error = _validate_organization_settings(new_settings)
            if validation_error:
                return jsonify({'error': f'Invalid settings: {validation_error}'}), 400
            
            old_settings = organization.settings or {}
            organization.settings = {**(old_settings or {}), **new_settings}
            organization.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, current_user_obj.id, 'update', 'organization_settings', org_id, 
                               'Organization settings updated')
            
            return jsonify({
                'message': 'Organization settings updated successfully',
                'settings': organization.settings
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage organization settings', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>/stats', methods=['GET'])
@rate_limit(limit=60, period=3600)
@permission_required(PERMISSION_VIEW_ORGANIZATION_REPORTS)
def get_organization_stats(org_id):
    """
    Get organization statistics and analytics
    """
    try:
        current_user_obj = get_current_user()
        
        # Check access rights
        if not current_user_obj.is_super_admin and current_user_obj.tenant_id != org_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Get date range
        days = int(request.args.get('days', 30))
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        stats = {
            'user_metrics': _get_user_metrics(org_id, start_date, end_date),
            'subscription_metrics': _get_subscription_metrics(org_id),
            'activity_metrics': _get_activity_metrics(org_id, start_date, end_date),
            'storage_metrics': _get_storage_metrics(org_id)
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve organization statistics', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>/users', methods=['GET'])
@rate_limit(limit=80, period=3600)
@permission_required(PERMISSION_VIEW_ORGANIZATIONS)
def get_organization_users(org_id):
    """
    Get users belonging to an organization
    """
    try:
        current_user_obj = get_current_user()
        
        # Check access rights
        if not current_user_obj.is_super_admin and current_user_obj.tenant_id != org_id:
            return jsonify({'error': 'Access denied'}), 403
        
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Filter parameters
        role = request.args.get('role')
        is_active = request.args.get('is_active', type=bool)
        
        query = User.query.filter_by(tenant_id=org_id)
        
        if role:
            query = query.filter_by(role=role)
        if is_active is not None:
            query = query.filter_by(is_active=is_active)
        
        users = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict(include_basic_info=True) for user in users.items],
            'pagination': {
                'page': users.page,
                'per_page': users.per_page,
                'total': users.total,
                'pages': users.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve organization users', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>', methods=['DELETE'])
@rate_limit(limit=10, period=3600)  # Very restrictive for deletion
@permission_required(PERMISSION_DELETE_ORGANIZATIONS)
def delete_organization(org_id):
    """
    Delete an organization (super admin only with confirmation)
    """
    try:
        current_user_obj = get_current_user()
        
        # Only super admins can delete organizations
        if not current_user_obj.is_super_admin:
            return jsonify({'error': 'Access denied. Super admin privileges required.'}), 403
        
        organization = Organization.query.get_or_404(org_id)
        
        # Check if organization has users
        user_count = User.query.filter_by(tenant_id=org_id).count()
        if user_count > 0:
            return jsonify({
                'error': f'Cannot delete organization with {user_count} users. Remove users first.'
            }), 409
        
        # Require confirmation for deletion
        confirmation = request.args.get('confirm', '').lower()
        if confirmation != 'true':
            return jsonify({
                'message': 'Deletion requires confirmation',
                'instruction': 'Add ?confirm=true to confirm deletion'
            }), 400
        
        # Create audit trail before deletion
        _create_audit_trail(None, current_user_obj.id, 'delete', 'organization', organization.id, 
                           f'Organization deleted: {organization.name}')
        
        db.session.delete(organization)
        db.session.commit()
        
        return jsonify({
            'message': 'Organization deleted successfully',
            'deleted_organization': organization.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete organization', 'details': str(e)}), 500

@organizations_bp.route('/<org_id>/subscription', methods=['PUT'])
@rate_limit(limit=20, period=3600)
@permission_required(PERMISSION_EDIT_ORGANIZATIONS)
def update_subscription(org_id):
    """
    Update organization subscription plan (super admin only)
    """
    try:
        current_user_obj = get_current_user()
        
        # Only super admins can update subscriptions
        if not current_user_obj.is_super_admin:
            return jsonify({'error': 'Access denied. Super admin privileges required.'}), 403
        
        organization = Organization.query.get_or_404(org_id)
        
        data = request.get_json()
        new_plan = data.get('subscription_plan')
        
        if not new_plan:
            return jsonify({'error': 'subscription_plan is required'}), 400
        
        valid_plans = ['free', 'starter', 'professional', 'enterprise']
        if new_plan not in valid_plans:
            return jsonify({'error': f'Invalid plan. Must be one of: {", ".join(valid_plans)}'}), 400
        
        old_plan = organization.subscription_plan
        organization.subscription_plan = new_plan
        organization.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(organization.id, current_user_obj.id, 'update', 'subscription', org_id, 
                           f'Subscription changed from {old_plan} to {new_plan}')
        
        return jsonify({
            'message': f'Subscription plan updated to {new_plan}',
            'organization': organization.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update subscription', 'details': str(e)}), 500

# Helper functions
def _get_organizations_summary(query: Any) -> Dict[str, Any]:
    """Get summary statistics for organizations"""
    total_organizations = query.count()
    
    # Count by type
    type_counts = query.group_by(Organization.type)\
                      .with_entities(Organization.type, db.func.count(Organization.id))\
                      .all()
    
    # Count by subscription plan
    plan_counts = query.group_by(Organization.subscription_plan)\
                      .with_entities(Organization.subscription_plan, db.func.count(Organization.id))\
                      .all()
    
    # Count active vs inactive
    active_count = query.filter_by(is_active=True).count()
    
    return {
        'total_organizations': total_organizations,
        'by_type': {org_type: count for org_type, count in type_counts},
        'by_plan': {plan: count for plan, count in plan_counts},
        'active_count': active_count,
        'inactive_count': total_organizations - active_count
    }

def _validate_organization_settings(settings: Dict[str, Any]) -> Optional[str]:
    """Validate organization settings structure"""
    # Define allowed settings and their types
    allowed_settings = {
        'business_hours': dict,
        'appointment_duration': int,
        'reminder_settings': dict,
        'billing_settings': dict,
        'notification_preferences': dict,
        'theme_settings': dict
    }
    
    for key, value in settings.items():
        if key not in allowed_settings:
            return f'Invalid setting: {key}'
        
        expected_type = allowed_settings[key]
        if not isinstance(value, expected_type):
            return f'Setting {key} must be of type {expected_type.__name__}'
    
    return None

def _create_audit_trail(tenant_id: Optional[str], user_id: int, action: str, resource_type: str, resource_id: str, details: str):
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

def _get_user_metrics(org_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get user metrics for an organization"""
    total_users = User.query.filter_by(tenant_id=org_id).count()
    active_users = User.query.filter_by(tenant_id=org_id, is_active=True).count()
    
    new_users = User.query.filter(
        User.tenant_id == org_id,
        User.created_at.between(start_date, end_date)
    ).count()
    
    return {
        'total_users': total_users,
        'active_users': active_users,
        'new_users': new_users,
        'user_growth_rate': (new_users / total_users * 100) if total_users > 0 else 0
    }

def _get_subscription_metrics(org_id: str) -> Dict[str, Any]:
    """Get subscription metrics for an organization"""
    organization = Organization.query.get(org_id)
    if not organization:
        return {}
    
    return {
        'current_plan': organization.subscription_plan,
        'is_active': organization.is_active,
        'created_at': organization.created_at.isoformat() if organization.created_at else None,
        'days_since_creation': (datetime.utcnow() - organization.created_at).days if organization.created_at else 0
    }

def _get_activity_metrics(org_id: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
    """Get activity metrics for an organization"""
    # This would typically query various activity tables
    # For now, return placeholder data
    from ..models import Appointment, AuditTrail
    
    appointment_count = Appointment.query.filter(
        Appointment.tenant_id == org_id,
        Appointment.created_at.between(start_date, end_date)
    ).count()
    
    audit_count = AuditTrail.query.filter(
        AuditTrail.tenant_id == org_id,
        AuditTrail.timestamp.between(start_date, end_date)
    ).count()
    
    return {
        'appointments_created': appointment_count,
        'audit_events': audit_count,
        'average_daily_activity': audit_count / ((end_date - start_date).days or 1)
    }

def _get_storage_metrics(org_id: str) -> Dict[str, Any]:
    """Get storage usage metrics for an organization"""
    # This would typically calculate storage usage from file uploads, etc.
    # For now, return placeholder data
    return {
        'storage_used_mb': 0,
        'storage_limit_mb': 0,
        'storage_usage_percentage': 0
    }

@organizations_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@organizations_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@organizations_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429