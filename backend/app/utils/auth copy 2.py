# backend/app/utils/auth.py

from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required, create_access_token, create_refresh_token
from app.models.models import User, Permission
from datetime import datetime, timedelta

def generate_tokens(user):
    additional_claims = {"organization_id": user.organization_id, "role": user.role.value}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.id)
    return access_token, refresh_token

def token_required(fn):
    """
    Decorator that requires a valid JWT token to be present in the request.
    This is a simple wrapper around flask_jwt_extended.jwt_required()
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

def permission_required(permission_name):
    """
    Decorator that requires both a valid JWT token and specific permission.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user = User.query.get(claims['sub'])
            
            if not user or not user.has_permission(permission_name):
                return jsonify({
                    'message': f'Permission denied: {permission_name} required',
                    'error': 'permission_denied'
                }), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def role_required(role_name):
    """
    Decorator that requires both a valid JWT token and specific role.
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user = User.query.get(claims['sub'])
            
            if not user or user.role.value != role_name:
                return jsonify({
                    'message': f'Role required: {role_name}',
                    'error': 'role_required'
                }), 403
                
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def admin_required(fn):
    """
    Decorator that requires admin privileges.
    """
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        user = User.query.get(claims['sub'])
        
        if not user or not user.is_admin:
            return jsonify({
                'message': 'Admin access required',
                'error': 'admin_required'
            }), 403
            
        return fn(*args, **kwargs)
    return wrapper

def get_current_user():
    """
    Get the current authenticated user from JWT token.
    Returns None if no valid token is present.
    """
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt()
        if claims:
            return User.query.get(claims['sub'])
    except Exception as e:
        current_app.logger.debug(f"Error getting current user: {e}")
    return None

def get_current_user_id():
    """
    Get the current authenticated user ID from JWT token.
    Returns None if no valid token is present.
    """
    try:
        verify_jwt_in_request(optional=True)
        claims = get_jwt()
        if claims:
            return claims['sub']
    except Exception as e:
        current_app.logger.debug(f"Error getting current user ID: {e}")
    return None

# Alternative simple token_required (if needed for legacy code)
def token_required_legacy(fn):
    """
    Legacy token_required decorator for backward compatibility.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            if not claims:
                return jsonify({'message': 'Token is missing'}), 401
        except Exception as e:
            return jsonify({'message': 'Token is invalid', 'error': str(e)}), 401
        return fn(*args, **kwargs)
    return wrapper

def permission_required(roles):
    """Restrict endpoint to certain roles."""
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role not in roles:
                return {"message": "Forbidden"}, 403
            return f(*args, **kwargs)
        return decorated
    return wrapper
