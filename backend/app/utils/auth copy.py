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

'''

# auth.py
from functools import wraps
from flask import request, jsonify, current_app
import jwt
from models import User, Tenant, UserRole, Permission

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user or not current_user.is_active:
                return jsonify({'message': 'Invalid token!'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def requires_permission(permission_name):
    def decorator(f):
        @wraps(f)
        @token_required
        def decorated(current_user, *args, **kwargs):
            # Check if user has the required permission in their tenant
            user_permissions = set()
            
            for user_role in current_user.roles:
                if user_role.tenant_id == current_user.tenant_id:
                    for permission in user_role.role.permissions:
                        user_permissions.add(permission.name)
            
            if permission_name not in user_permissions:
                return jsonify({'message': 'Insufficient permissions!'}), 403
            
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

def requires_tenant_access(f):
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        # For routes that need tenant-specific data access
        tenant_id = kwargs.get('tenant_id')
        
        if tenant_id and str(tenant_id) != str(current_user.tenant_id):
            return jsonify({'message': 'Access denied to this tenant!'}), 403
        
        return f(current_user, *args, **kwargs)
    return decorated

'''
'''
from app.utils.auth import token_required, permission_required, role_required, admin_required

# Basic token authentication
@app.route('/protected')
@token_required
def protected_route():
    return jsonify({"message": "This is protected"})

# Permission-based access
@app.route('/manage-patients')
@permission_required(Permission.MANAGE_PATIENTS.value)
def manage_patients():
    return jsonify({"message": "You can manage patients"})

# Role-based access  
@app.route('/admin-dashboard')
@role_required('admin')
def admin_dashboard():
    return jsonify({"message": "Welcome admin"})

# Admin access
@app.route('/system-settings')
@admin_required
def system_settings():
    return jsonify({"message": "System settings"})

    


    # Correct import for the new token_required
from app.utils.auth import token_required

# If you need both JWT and permission decorators
from app.utils.auth import token_required, permission_required, role_required

# For getting current user info
from app.utils.auth import get_current_user, get_current_user_id



'''