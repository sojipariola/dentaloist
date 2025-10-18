# backend/app/utils/rbac.py
# role-based access control utilities

from flask import jsonify
from flask_login import current_user

def require_role(*roles):
    """Require that the current_user has one of the given roles"""
    if not current_user.is_authenticated:
        return jsonify({"error": "Authentication required"}), 401

    if current_user.role not in roles and current_user.role != "super_admin":
        return jsonify({"error": "Insufficient privileges"}), 403

    return None


def require_permission(permission):
    """Require a specific permission from current_user"""
    if not current_user.is_authenticated:
        return jsonify({"error": "Authentication required"}), 401

    if not hasattr(current_user, "has_permission"):
        return jsonify({"error": "Permission system not configured"}), 403

    if not current_user.has_permission(permission) and current_user.role != "super_admin":
        return jsonify({"error": f"Permission '{permission}' required"}), 403

    return None



'''
from ..utils.rbac import require_role, require_permission


@admin_api_bp.route('/system/status', methods=['GET'])
@login_required
def system_status():
    if error := require_role("admin"):
        return error
    ...

if error := require_permission("manage_users"):
    return error


def admin_access_required(fn):
    """Decorator to require admin role"""
    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):
        error_response = require_role("admin", "super_admin")
        if error_response:
            return error_response
        return fn(*args, **kwargs)

    return wrapper

def require_admin_access():
    """Middleware to require admin privileges"""
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required'}), 401
    
    if not current_user.has_permission('manage_users') and current_user.role != 'super_admin':
        return jsonify({'error': 'Administrator access required'}), 403
    
    return None
'''