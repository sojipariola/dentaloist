# routes/settings.py
from flask import Blueprint, request, jsonify
from flask_login import current_user
from datetime import datetime
from typing import Dict, Any, List, Optional

# Import auth and tenancy utilities
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit

from ..models import User, Organization, AuditTrail, db

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')

# RBAC Permission Constants
PERMISSION_VIEW_SETTINGS = 'view_settings'
PERMISSION_EDIT_USER_SETTINGS = 'edit_user_settings'
PERMISSION_EDIT_ORGANIZATION_SETTINGS = 'edit_organization_settings'
PERMISSION_MANAGE_SYSTEM_SETTINGS = 'manage_system_settings'

# Default Settings Templates
DEFAULT_USER_SETTINGS = {
    'preferences': {
        'language': 'en',
        'timezone': 'UTC',
        'date_format': 'MM/DD/YYYY',
        'time_format': '12h',
        'theme': 'light'
    },
    'notifications': {
        'email': True,
        'push': True,
        'sms': False,
        'categories': {
            'appointments': True,
            'lab_results': True,
            'billing': True,
            'system': True
        }
    },
    'dashboard': {
        'default_view': 'overview',
        'refresh_interval': 300,
        'show_metrics': True,
        'recent_items_count': 10
    }
}

DEFAULT_ORGANIZATION_SETTINGS = {
    'practice': {
        'name': '',
        'phone': '',
        'email': '',
        'address': {},
        'business_hours': {},
        'timezone': 'UTC'
    },
    'appointments': {
        'slot_duration': 30,
        'buffer_time': 5,
        'max_daily_appointments': 50,
        'cancellation_policy_hours': 24,
        'reminder_hours': [24, 2]
    },
    'billing': {
        'currency': 'USD',
        'tax_rate': 0.0,
        'payment_terms': 30,
        'late_fee_percentage': 5.0,
        'invoice_prefix': 'INV'
    },
    'clinical': {
        'medical_history_required': True,
        'consent_forms_required': True,
        'medication_interaction_check': False,
        'default_treatment_notes': ''
    },
    'notifications': {
        'patient_reminders': True,
        'staff_notifications': True,
        'low_inventory_alerts': True,
        'system_maintenance_alerts': True
    }
}

@settings_bp.route('/', methods=['GET'])
@rate_limit(limit=120, period=3600)  # 120 requests per hour
@tenant_required
@permission_required(PERMISSION_VIEW_SETTINGS)
def get_settings():
    """
    Get comprehensive settings for user and organization with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get organization settings with tenant filtering
        org_query = multi_tenant_query(Organization.query, tenant_id)
        organization = org_query.first()
        
        settings = {
            'user': _get_user_settings_with_defaults(current_user_obj),
            'organization': _get_organization_settings_with_defaults(organization) if organization else {},
            'permissions': {
                'can_edit_user_settings': current_user_obj.has_permission(PERMISSION_EDIT_USER_SETTINGS),
                'can_edit_organization_settings': current_user_obj.has_permission(PERMISSION_EDIT_ORGANIZATION_SETTINGS),
                'can_manage_system_settings': current_user_obj.has_permission(PERMISSION_MANAGE_SYSTEM_SETTINGS)
            },
            'last_updated': {
                'user': current_user_obj.updated_at.isoformat() if current_user_obj.updated_at else None,
                'organization': organization.updated_at.isoformat() if organization and organization.updated_at else None
            }
        }
        
        return jsonify(settings), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve settings', 'details': str(e)}), 500

@settings_bp.route('/user', methods=['GET', 'PUT'])
@rate_limit(limit=100, period=3600)
@permission_required(PERMISSION_VIEW_SETTINGS)
def manage_user_settings():
    """
    Get or update user-specific settings
    """
    try:
        current_user_obj = get_current_user()
        
        if request.method == 'GET':
            return jsonify(_get_user_settings_with_defaults(current_user_obj)), 200
        
        elif request.method == 'PUT':
            if not current_user_obj.has_permission(PERMISSION_EDIT_USER_SETTINGS):
                return jsonify({'error': 'Insufficient permissions to edit user settings'}), 403
            
            data = request.get_json()
            
            if not isinstance(data, dict):
                return jsonify({'error': 'Settings must be a JSON object'}), 400
            
            # Validate user settings structure
            validation_errors = _validate_user_settings(data)
            if validation_errors:
                return jsonify({'error': 'Invalid user settings', 'details': validation_errors}), 400
            
            # Merge and update settings
            old_settings = current_user_obj.settings or {}
            new_settings = {**DEFAULT_USER_SETTINGS, **old_settings, **data}
            
            # Ensure we only store valid settings
            validated_settings = _filter_valid_user_settings(new_settings)
            
            current_user_obj.settings = validated_settings
            current_user_obj.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(current_user_obj.tenant_id, current_user_obj.id, 'update', 'user_settings', current_user_obj.id, 
                               'User settings updated')
            
            return jsonify({
                'message': 'User settings updated successfully',
                'settings': validated_settings
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage user settings', 'details': str(e)}), 500

@settings_bp.route('/organization', methods=['GET', 'PUT'])
@rate_limit(limit=80, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_SETTINGS)
def manage_organization_settings():
    """
    Get or update organization-wide settings with tenant isolation
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        # Get organization with tenant filtering
        org_query = multi_tenant_query(Organization.query, tenant_id)
        organization = org_query.first()
        
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        if request.method == 'GET':
            return jsonify(_get_organization_settings_with_defaults(organization)), 200
        
        elif request.method == 'PUT':
            if not current_user_obj.has_permission(PERMISSION_EDIT_ORGANIZATION_SETTINGS):
                return jsonify({'error': 'Insufficient permissions to edit organization settings'}), 403
            
            data = request.get_json()
            
            if not isinstance(data, dict):
                return jsonify({'error': 'Settings must be a JSON object'}), 400
            
            # Validate organization settings structure
            validation_errors = _validate_organization_settings(data)
            if validation_errors:
                return jsonify({'error': 'Invalid organization settings', 'details': validation_errors}), 400
            
            # Merge and update settings
            old_settings = organization.settings or {}
            new_settings = {**DEFAULT_ORGANIZATION_SETTINGS, **old_settings, **data}
            
            # Ensure we only store valid settings
            validated_settings = _filter_valid_organization_settings(new_settings)
            
            organization.settings = validated_settings
            organization.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, current_user_obj.id, 'update', 'organization_settings', organization.id, 
                               'Organization settings updated')
            
            return jsonify({
                'message': 'Organization settings updated successfully',
                'settings': validated_settings
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage organization settings', 'details': str(e)}), 500

@settings_bp.route('/organization/practice', methods=['GET', 'PUT'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_SETTINGS)
def manage_practice_settings():
    """
    Get or update practice-specific settings (subset of organization settings)
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        org_query = multi_tenant_query(Organization.query, tenant_id)
        organization = org_query.first()
        
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        current_settings = _get_organization_settings_with_defaults(organization)
        
        if request.method == 'GET':
            return jsonify(current_settings.get('practice', {})), 200
        
        elif request.method == 'PUT':
            if not current_user_obj.has_permission(PERMISSION_EDIT_ORGANIZATION_SETTINGS):
                return jsonify({'error': 'Insufficient permissions to edit practice settings'}), 403
            
            data = request.get_json()
            
            if not isinstance(data, dict):
                return jsonify({'error': 'Practice settings must be a JSON object'}), 400
            
            # Validate practice settings
            validation_errors = _validate_practice_settings(data)
            if validation_errors:
                return jsonify({'error': 'Invalid practice settings', 'details': validation_errors}), 400
            
            # Update only practice settings
            updated_settings = current_settings.copy()
            updated_settings['practice'] = {**updated_settings.get('practice', {}), **data}
            
            organization.settings = updated_settings
            organization.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(tenant_id, current_user_obj.id, 'update', 'practice_settings', organization.id, 
                               'Practice settings updated')
            
            return jsonify({
                'message': 'Practice settings updated successfully',
                'practice_settings': updated_settings['practice']
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage practice settings', 'details': str(e)}), 500

@settings_bp.route('/notifications', methods=['GET', 'PUT'])
@rate_limit(limit=100, period=3600)
@permission_required(PERMISSION_VIEW_SETTINGS)
def manage_notification_settings():
    """
    Get or update notification settings for the current user
    """
    try:
        current_user_obj = get_current_user()
        
        current_settings = _get_user_settings_with_defaults(current_user_obj)
        notification_settings = current_settings.get('notifications', {})
        
        if request.method == 'GET':
            return jsonify(notification_settings), 200
        
        elif request.method == 'PUT':
            if not current_user_obj.has_permission(PERMISSION_EDIT_USER_SETTINGS):
                return jsonify({'error': 'Insufficient permissions to edit notification settings'}), 403
            
            data = request.get_json()
            
            if not isinstance(data, dict):
                return jsonify({'error': 'Notification settings must be a JSON object'}), 400
            
            # Validate notification settings
            validation_errors = _validate_notification_settings(data)
            if validation_errors:
                return jsonify({'error': 'Invalid notification settings', 'details': validation_errors}), 400
            
            # Update only notification settings
            updated_settings = current_settings.copy()
            updated_settings['notifications'] = {**updated_settings.get('notifications', {}), **data}
            
            current_user_obj.settings = updated_settings
            current_user_obj.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(current_user_obj.tenant_id, current_user_obj.id, 'update', 'notification_settings', current_user_obj.id, 
                               'Notification settings updated')
            
            return jsonify({
                'message': 'Notification settings updated successfully',
                'notification_settings': updated_settings['notifications']
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage notification settings', 'details': str(e)}), 500

@settings_bp.route('/preferences', methods=['GET', 'PUT'])
@rate_limit(limit=100, period=3600)
@permission_required(PERMISSION_VIEW_SETTINGS)
def manage_user_preferences():
    """
    Get or update user preferences (subset of user settings)
    """
    try:
        current_user_obj = get_current_user()
        
        current_settings = _get_user_settings_with_defaults(current_user_obj)
        preferences = current_settings.get('preferences', {})
        
        if request.method == 'GET':
            return jsonify(preferences), 200
        
        elif request.method == 'PUT':
            if not current_user_obj.has_permission(PERMISSION_EDIT_USER_SETTINGS):
                return jsonify({'error': 'Insufficient permissions to edit preferences'}), 403
            
            data = request.get_json()
            
            if not isinstance(data, dict):
                return jsonify({'error': 'Preferences must be a JSON object'}), 400
            
            # Validate preferences
            validation_errors = _validate_preference_settings(data)
            if validation_errors:
                return jsonify({'error': 'Invalid preferences', 'details': validation_errors}), 400
            
            # Update only preferences
            updated_settings = current_settings.copy()
            updated_settings['preferences'] = {**updated_settings.get('preferences', {}), **data}
            
            current_user_obj.settings = updated_settings
            current_user_obj.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Create audit trail entry
            _create_audit_trail(current_user_obj.tenant_id, current_user_obj.id, 'update', 'user_preferences', current_user_obj.id, 
                               'User preferences updated')
            
            return jsonify({
                'message': 'User preferences updated successfully',
                'preferences': updated_settings['preferences']
            }), 200
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to manage preferences', 'details': str(e)}), 500

@settings_bp.route('/reset/user', methods=['POST'])
@rate_limit(limit=10, period=3600)  # Very restrictive for resets
@permission_required(PERMISSION_EDIT_USER_SETTINGS)
def reset_user_settings():
    """
    Reset user settings to defaults
    """
    try:
        current_user_obj = get_current_user()
        
        # Store old settings for audit trail
        old_settings = current_user_obj.settings or {}
        
        current_user_obj.settings = DEFAULT_USER_SETTINGS
        current_user_obj.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(current_user_obj.tenant_id, current_user_obj.id, 'reset', 'user_settings', current_user_obj.id, 
                           'User settings reset to defaults')
        
        return jsonify({
            'message': 'User settings reset to defaults successfully',
            'settings': DEFAULT_USER_SETTINGS
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reset user settings', 'details': str(e)}), 500

@settings_bp.route('/reset/organization', methods=['POST'])
@rate_limit(limit=5, period=3600)  # Very restrictive for organization resets
@tenant_required
@permission_required(PERMISSION_EDIT_ORGANIZATION_SETTINGS)
def reset_organization_settings():
    """
    Reset organization settings to defaults
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        org_query = multi_tenant_query(Organization.query, tenant_id)
        organization = org_query.first()
        
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        # Store old settings for audit trail
        old_settings = organization.settings or {}
        
        organization.settings = DEFAULT_ORGANIZATION_SETTINGS
        organization.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create audit trail entry
        _create_audit_trail(tenant_id, current_user_obj.id, 'reset', 'organization_settings', organization.id, 
                           'Organization settings reset to defaults')
        
        return jsonify({
            'message': 'Organization settings reset to defaults successfully',
            'settings': DEFAULT_ORGANIZATION_SETTINGS
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to reset organization settings', 'details': str(e)}), 500

@settings_bp.route('/audit', methods=['GET'])
@rate_limit(limit=60, period=3600)
@tenant_required
@permission_required(PERMISSION_VIEW_SETTINGS)
def get_settings_audit_log():
    """
    Get audit log for settings changes
    """
    try:
        current_user_obj = get_current_user()
        tenant_id = current_user_obj.tenant_id
        
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Query audit trail for settings-related changes
        query = multi_tenant_query(AuditTrail.query, tenant_id)
        audit_logs = query.filter(
            AuditTrail.resource_type.in_(['user_settings', 'organization_settings', 'practice_settings', 'notification_settings', 'user_preferences'])
        ).order_by(AuditTrail.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'audit_logs': [log.to_dict() for log in audit_logs.items],
            'pagination': {
                'page': audit_logs.page,
                'per_page': audit_logs.per_page,
                'total': audit_logs.total,
                'pages': audit_logs.pages
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to retrieve settings audit log', 'details': str(e)}), 500

# Helper functions
def _get_user_settings_with_defaults(user: User) -> Dict[str, Any]:
    """Get user settings merged with defaults"""
    user_settings = user.settings or {}
    return {**DEFAULT_USER_SETTINGS, **user_settings}

def _get_organization_settings_with_defaults(organization: Organization) -> Dict[str, Any]:
    """Get organization settings merged with defaults"""
    org_settings = organization.settings or {}
    return {**DEFAULT_ORGANIZATION_SETTINGS, **org_settings}

def _validate_user_settings(settings: Dict[str, Any]) -> List[str]:
    """Validate user settings structure"""
    errors = []
    
    # Validate top-level structure
    allowed_sections = ['preferences', 'notifications', 'dashboard']
    for key in settings.keys():
        if key not in allowed_sections:
            errors.append(f'Invalid section: {key}')
    
    # Validate preferences
    if 'preferences' in settings:
        pref_errors = _validate_preference_settings(settings['preferences'])
        errors.extend(pref_errors)
    
    # Validate notifications
    if 'notifications' in settings:
        notif_errors = _validate_notification_settings(settings['notifications'])
        errors.extend(notif_errors)
    
    return errors

def _validate_organization_settings(settings: Dict[str, Any]) -> List[str]:
    """Validate organization settings structure"""
    errors = []
    
    allowed_sections = ['practice', 'appointments', 'billing', 'clinical', 'notifications']
    for key in settings.keys():
        if key not in allowed_sections:
            errors.append(f'Invalid section: {key}')
    
    # Validate practice settings
    if 'practice' in settings:
        practice_errors = _validate_practice_settings(settings['practice'])
        errors.extend(practice_errors)
    
    return errors

def _validate_preference_settings(preferences: Dict[str, Any]) -> List[str]:
    """Validate user preference settings"""
    errors = []
    
    allowed_keys = ['language', 'timezone', 'date_format', 'time_format', 'theme']
    for key in preferences.keys():
        if key not in allowed_keys:
            errors.append(f'Invalid preference: {key}')
    
    # Validate specific values
    if 'language' in preferences and not isinstance(preferences['language'], str):
        errors.append('Language must be a string')
    
    if 'theme' in preferences and preferences['theme'] not in ['light', 'dark', 'auto']:
        errors.append('Theme must be light, dark, or auto')
    
    return errors

def _validate_notification_settings(notifications: Dict[str, Any]) -> List[str]:
    """Validate notification settings"""
    errors = []
    
    allowed_keys = ['email', 'push', 'sms', 'categories']
    for key in notifications.keys():
        if key not in allowed_keys:
            errors.append(f'Invalid notification setting: {key}')
    
    # Validate boolean values
    for key in ['email', 'push', 'sms']:
        if key in notifications and not isinstance(notifications[key], bool):
            errors.append(f'{key} must be a boolean value')
    
    return errors

def _validate_practice_settings(practice: Dict[str, Any]) -> List[str]:
    """Validate practice settings"""
    errors = []
    
    allowed_keys = ['name', 'phone', 'email', 'address', 'business_hours', 'timezone']
    for key in practice.keys():
        if key not in allowed_keys:
            errors.append(f'Invalid practice setting: {key}')
    
    # Validate email format if provided
    if 'email' in practice and practice['email']:
        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, practice['email']):
            errors.append('Invalid email format')
    
    return errors

def _filter_valid_user_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Filter settings to only include valid keys"""
    valid_settings = {}
    
    for section, values in settings.items():
        if section in DEFAULT_USER_SETTINGS:
            if isinstance(values, dict):
                # Only include keys that exist in defaults
                valid_settings[section] = {
                    k: v for k, v in values.items() 
                    if k in DEFAULT_USER_SETTINGS.get(section, {})
                }
            else:
                valid_settings[section] = values
    
    return valid_settings

def _filter_valid_organization_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """Filter organization settings to only include valid keys"""
    valid_settings = {}
    
    for section, values in settings.items():
        if section in DEFAULT_ORGANIZATION_SETTINGS:
            if isinstance(values, dict):
                valid_settings[section] = {
                    k: v for k, v in values.items() 
                    if k in DEFAULT_ORGANIZATION_SETTINGS.get(section, {})
                }
            else:
                valid_settings[section] = values
    
    return valid_settings

def _create_audit_trail(tenant_id: str, user_id: int, action: str, resource_type: str, resource_id: int, details: str):
    """Create an audit trail entry"""
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

@settings_bp.errorhandler(403)
def handle_permission_error(e):
    return jsonify({'error': 'Access forbidden', 'message': 'Insufficient permissions'}), 403

@settings_bp.errorhandler(401)
def handle_authentication_error(e):
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401

@settings_bp.errorhandler(429)
def handle_rate_limit_error(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': 'Too many requests'}), 429