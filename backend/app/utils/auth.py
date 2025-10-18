# backend/app/utils/auth.py

from functools import wraps
from flask import jsonify, current_app, request, g, session, redirect, url_for, flash
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt, jwt_required, create_access_token, 
    create_refresh_token, get_jwt_identity, decode_token
)
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import logging
from enum import Enum
import secrets
import time
import hmac
import hashlib
import base64
import struct

# Import models and services
from ..models import User, Permission, Role, Tenant, AuditTrail, db
from ..services.security import SecurityService

logger = logging.getLogger(__name__)

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    API = "api"

# === 2FA Functions (Add these at the top) ===
def generate_2fa_secret():
    """Generate a 2FA secret key"""
    return base64.b32encode(secrets.token_bytes(10)).decode('utf-8')

def generate_2fa_code(secret):
    """Generate current 2FA code"""
    key = base64.b32decode(secret)
    counter = int(time.time()) // 30
    
    msg = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    
    offset = hmac_hash[-1] & 0x0F
    dynamic_binary_code = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7FFFFFFF
    
    code = dynamic_binary_code % 1000000
    return f"{code:06d}"

def verify_2fa_code(secret, code, window=1):
    """Verify 2FA code with time window tolerance"""
    current_time = int(time.time()) // 30
    
    for i in range(-window, window + 1):
        test_counter = current_time + i
        test_code = generate_2fa_code_with_counter(secret, test_counter)
        
        if hmac.compare_digest(test_code, code):
            return True
    
    return False

def generate_2fa_code_with_counter(secret, counter):
    """Generate code for specific counter"""
    key = base64.b32decode(secret)
    msg = struct.pack(">Q", counter)
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    
    offset = hmac_hash[-1] & 0x0F
    dynamic_binary_code = struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7FFFFFFF
    
    code = dynamic_binary_code % 1000000
    return f"{code:06d}"

# === Your Existing Comprehensive Functions (Keep these) ===
def generate_tokens(user: User, tenant_id: str = None) -> Dict[str, str]:
    """Generate JWT tokens with comprehensive claims and tenant context"""
    try:
        # Get user permissions
        permissions = user.get_all_permissions()
        
        # Base claims
        additional_claims = {
            "tenant_id": tenant_id or user.tenant_id,
            "role": user.role,
            "permissions": permissions,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "email_verified": user.email_verified,
            "token_type": TokenType.ACCESS.value,
            "iss": current_app.config.get('JWT_ISS', 'dental-practice-pro'),
            "aud": current_app.config.get('JWT_AUD', 'dental-practice-pro')
        }
        
        # Generate tokens
        access_token = create_access_token(
            identity=user.id, 
            additional_claims=additional_claims,
            expires_delta=timedelta(minutes=current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 60))
        )
        
        refresh_claims = additional_claims.copy()
        refresh_claims['token_type'] = TokenType.REFRESH.value
        
        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims=refresh_claims,
            expires_delta=timedelta(days=current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 30))
        )
        
        # Log token generation
        _log_security_event(
            user.id, 
            'token_generated', 
            'Access and refresh tokens generated',
            severity='info'
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
            'expires_in': current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 60) * 60,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'permissions': permissions,
                'tenant_id': tenant_id or user.tenant_id
            }
        }
        
    except Exception as e:
        logger.error(f"Token generation failed: {str(e)}")
        raise AuthException("Token generation failed")

def permission_required(permission_name: Union[str, List[str]]):
    """
    Decorator that requires specific permission(s)
    
    Args:
        permission_name: Single permission or list of permissions
    """
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                current_user = get_current_user()
                if not current_user:
                    return jsonify({
                        'message': 'Authentication required',
                        'error': 'authentication_required'
                    }), 401
                
                # Convert single permission to list
                required_permissions = [permission_name] if isinstance(permission_name, str) else permission_name
                
                # Check if user has any of the required permissions
                has_permission = any(
                    current_user.has_permission(perm) for perm in required_permissions
                )
                
                if not has_permission:
                    _log_security_event(
                        current_user.id,
                        'permission_denied',
                        f'Attempted access requiring permissions: {required_permissions}',
                        severity='warning'
                    )
                    
                    return jsonify({
                        'message': f'Insufficient permissions. Required: {required_permissions}',
                        'error': 'permission_denied',
                        'required_permissions': required_permissions,
                        'user_permissions': current_user.get_all_permissions()
                    }), 403
                
                # Add user to context for easier access in routes
                g.current_user = current_user
                
                return fn(*args, **kwargs)
                
            except Exception as e:
                logger.error(f"Permission check failed: {str(e)}")
                return jsonify({
                    'message': 'Authorization check failed',
                    'error': 'authorization_failed'
                }), 500
                
        return wrapper
    return decorator

def get_current_user() -> Optional[User]:
    """
    Get current authenticated user with comprehensive validation
    """
    try:
        # Try JWT authentication first
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        
        if user_id:
            user = User.query.get(user_id)
            if user and user.is_active:
                # Verify token claims match user state
                claims = get_jwt()
                if (claims.get('email') == user.email and 
                    claims.get('is_active') == user.is_active and
                    claims.get('tenant_id') == user.tenant_id):
                    return user
        
        # Fall back to API key authentication
        if hasattr(g, 'current_user') and g.current_user:
            return g.current_user
            
        return None
        
    except Exception as e:
        logger.debug(f"Error getting current user: {e}")
        return None

# === Web-specific functions (Add these if needed for web routes) ===
def get_current_web_user():
    """Get current user from session (for web routes)"""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def web_permission_required(permission):
    """Permission decorator for web routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_web_user()
            if not user or not user.has_permission(permission):
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# === Keep the rest of your existing functions ===
# (refresh_access_token, role_required, tenant_required, super_admin_required, 
# api_key_required, get_current_tenant, get_user_permissions, validate_token, 
# revoke_token, is_token_revoked, _log_security_event, _verify_api_key, 
# AuthException, token_required, permission_required_legacy)

class AuthException(Exception):
    """Authentication and authorization related exceptions"""
    pass

# Helper functions (keep these)
def _log_security_event(user_id: int, event_type: str, description: str, severity: str = 'info'):
    """Log security event to database"""
    try:
        audit_event = AuditTrail(
            user_id=user_id,
            action=event_type,
            resource_type='auth',
            details=description,
            ip_address=request.remote_addr if request else None,
            user_agent=request.user_agent.string if request else None,
            severity=severity,
            timestamp=datetime.utcnow()
        )
        
        db.session.add(audit_event)
        db.session.commit()
        
    except Exception as e:
        logger.error(f"Failed to log security event: {str(e)}")

def _verify_api_key(api_key: str) -> Optional[int]:
    """Verify API key and return user ID"""
    try:
        from ..models import ApiKey
        from ..services.security import security_service
        
        # Split API key (format: key_id:key_secret)
        parts = api_key.split(':', 1)
        if len(parts) != 2:
            return None
        
        key_id, key_secret = parts
        
        # Verify API key
        api_key_record = ApiKey.query.filter_by(id=key_id, is_active=True).first()
        if not api_key_record:
            return None
        
        if security_service.verify_api_key(key_id, key_secret):
            return api_key_record.user_id
        
        return None
        
    except Exception as e:
        logger.error(f"API key verification failed: {str(e)}")
        return None

# Backward compatibility aliases
token_required = jwt_required

def permission_required_legacy(roles):
    """Legacy role-based permission decorator for backward compatibility"""
    def wrapper(f):
        @wraps(f)
        @jwt_required()
        def decorated(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role")
            if role not in roles:
                return jsonify({"message": "Forbidden", "error": "insufficient_permissions"}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper


