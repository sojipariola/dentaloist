# backend/app/utils/tenancy.py
# backend/app/utils/tenancy.py

from flask import g, request, current_app, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from ..models import User, Organization
import time
from datetime import datetime, timedelta
import functools
from sqlalchemy import or_


class TenancyMiddleware:
    def __init__(self, app=None):
        self.tenant_cache = {}
        self.cache_timeout = 300
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def set_tenant():
            """Set the tenant context for each request"""
            g.tenant_id = None
            g.tenant = None
            g.user = None
            g.tenant_loaded_at = None

            # Skip tenancy for auth routes, static files, and OPTIONS requests
            if (request.path.startswith('/api/auth/') or 
                request.path.startswith('/static/') or
                request.method == 'OPTIONS' or
                request.endpoint in ['auth.login', 'auth.register', 'auth.google_login', 
                                   'auth.google_authorize', 'static']):
                return

            try:
                # Improved JWT verification with better error handling
                try:
                    verify_jwt_in_request(optional=True)
                    claims = get_jwt()
                    user_identity = get_jwt_identity()
                except Exception as jwt_error:
                    current_app.logger.debug(f"JWT verification optional failed: {jwt_error}")
                    claims = None
                    user_identity = None

                if claims and user_identity:
                    # user_identity should be the user ID from JWT
                    user_id = user_identity
                    
                    # Cache user lookup
                    cache_key = f"user_{user_id}"
                    if cache_key in self.tenant_cache:
                        cached_data = self.tenant_cache[cache_key]
                        if time.time() - cached_data['timestamp'] < self.cache_timeout:
                            user = cached_data['data']
                        else:
                            user = User.query.get(user_id)
                            self.tenant_cache[cache_key] = {'data': user, 'timestamp': time.time()}
                    else:
                        user = User.query.get(user_id)
                        if user:
                            self.tenant_cache[cache_key] = {'data': user, 'timestamp': time.time()}
                    
                    if user and user.organization_id:
                        g.tenant_id = str(user.organization_id)
                        g.user = user
                        
                        # Cache tenant lookup
                        tenant_cache_key = f"tenant_{g.tenant_id}"
                        if tenant_cache_key in self.tenant_cache:
                            cached_tenant = self.tenant_cache[tenant_cache_key]
                            if time.time() - cached_tenant['timestamp'] < self.cache_timeout:
                                g.tenant = cached_tenant['data']
                            else:
                                g.tenant = Organization.query.get(g.tenant_id)
                                if g.tenant:
                                    self.tenant_cache[tenant_cache_key] = {'data': g.tenant, 'timestamp': time.time()}
                        else:
                            g.tenant = Organization.query.get(g.tenant_id)
                            if g.tenant:
                                self.tenant_cache[tenant_cache_key] = {'data': g.tenant, 'timestamp': time.time()}
                        
                        g.tenant_loaded_at = datetime.utcnow()
                        current_app.logger.debug(f"Tenant context set: {g.tenant_id} for user {user_id}")
                        
            except Exception as e:
                current_app.logger.error(f"Tenancy middleware error: {e}", exc_info=True)
                # Don't fail the request for tenancy errors in optional routes

            # Fallback to header for API requests
            if not g.tenant_id and request.path.startswith('/api/'):
                tenant_header = request.headers.get("X-Tenant-ID")
                api_key = request.headers.get("X-API-Key")
                
                if tenant_header:
                    if api_key and self.validate_api_key(api_key, tenant_header):
                        g.tenant_id = str(tenant_header)
                        g.tenant = Organization.query.get(g.tenant_id)
                        g.is_service_account = True
                    elif not api_key and current_app.config.get("ALLOW_HEADER_TENANT"):
                        # Allow tenant header without API key in development
                        g.tenant_id = str(tenant_header)
                        g.tenant = Organization.query.get(g.tenant_id)
                        g.is_header_tenant = True

            # Development fallback
            if (not g.tenant_id and 
                current_app.config.get("FLASK_ENV") == "development" and
                current_app.config.get("DEFAULT_TENANT_ID")):
                g.tenant_id = current_app.config.get("DEFAULT_TENANT_ID")
                g.tenant = Organization.query.get(g.tenant_id)
                g.is_default_tenant = True
                current_app.logger.info(f"Using default tenant for development: {g.tenant_id}")

    def validate_api_key(self, api_key, tenant_id):
        """Validate API key for service accounts"""
        # Implement your API key validation logic here
        # For now, allow in development
        if current_app.config.get("FLASK_ENV") == "development":
            return True
        # TODO: Implement proper API key validation
        return False

    def clear_cache(self, tenant_id=None, user_id=None):
        """Clear cache entries"""
        if tenant_id:
            tenant_cache_key = f"tenant_{tenant_id}"
            if tenant_cache_key in self.tenant_cache:
                del self.tenant_cache[tenant_cache_key]
        
        if user_id:
            user_cache_key = f"user_{user_id}"
            if user_cache_key in self.tenant_cache:
                del self.tenant_cache[user_cache_key]


def multi_tenant_query(model, enforce_tenant=True):
    """
    Apply tenant filter to query with improved error handling
    """
    # Skip tenant filtering for excluded routes
    excluded_paths = ['/api/auth/', '/static/', '/health']
    if any(request.path.startswith(path) for path in excluded_paths) or request.method == 'OPTIONS':
        return model.query
    
    # Get base query
    query = model.query
    
    # Check if we should apply tenant filtering
    if enforce_tenant and hasattr(model, 'organization_id'):
        if not hasattr(g, 'tenant_id') or not g.tenant_id:
            current_app.logger.warning(f"No tenant_id in context for multi_tenant_query on {model.__name__}")
            # Return empty query rather than failing
            return query.filter_by(id=None)
        
        # Apply tenant filter
        query = query.filter_by(organization_id=g.tenant_id)
    
    return query


# Keep the rest of your functions as they are...
def get_current_tenant_id():
    """Get current tenant ID with fallback for non-request contexts"""
    if hasattr(g, 'tenant_id'):
        return g.tenant_id
    
    # For non-request contexts (like CLI, tests), check if we're in app context
    if current_app and hasattr(g, 'tenant_id'):
        return g.tenant_id
    
    return None

def get_current_tenant():
    """Alias for get_current_tenant_id for backward compatibility"""
    return get_current_tenant_id()

def set_current_tenant(tenant_id):
    """Set current tenant for the context"""
    g.tenant_id = tenant_id

def multi_tenant_query(model):
    """
    Apply tenant filtering to queries.
    This is the core function that ensures data isolation.
    """
    tenant_id = get_current_tenant_id()
    
    # If no tenant context, return unfiltered query (admin/superuser view)
    if not tenant_id:
        return model.query
    
    # Check excluded paths for request context
    from flask import has_request_context
    if has_request_context():
        excluded_paths = ['/health', '/metrics', '/admin', '/static']
        if any(request.path.startswith(path) for path in excluded_paths) or request.method == 'OPTIONS':
            return model.query
    
    # Apply tenant filter based on model structure
    if hasattr(model, 'organization_id'):
        # Most models use organization_id for tenancy
        return model.query.filter(model.organization_id == tenant_id)
    elif hasattr(model, 'tenant_id'):
        # Some models might use tenant_id directly
        return model.query.filter(model.tenant_id == tenant_id)
    else:
        # Model doesn't support tenant isolation
        # Log this in development
        if current_app and current_app.config.get('DEBUG'):
            print(f"⚠️  Model {model.__name__} doesn't support tenant isolation")
        return model.query


def require_tenant(func):
    """Decorator to ensure tenant context is set"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            raise RuntimeError("Tenant context required but not set")
        return func(*args, **kwargs)
    return wrapper

def tenant_required(func):
    """Decorator to ensure tenant context is set"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tenant_id = get_current_tenant_id()
        if not tenant_id:
            raise RuntimeError("Tenant context required but not set")
        return func(*args, **kwargs)
    return wrapper


def with_tenant_context(tenant_id):
    """Decorator to execute function within a specific tenant context"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            original_tenant = get_current_tenant_id()
            set_current_tenant(tenant_id)
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                set_current_tenant(original_tenant)
        return wrapper
    return decorator

def get_current_user():
    """Get current user from tenancy context"""
    return g.user if hasattr(g, 'user') else None

def is_multi_tenant_enabled():
    """Check if multi-tenancy is enabled"""
    return current_app.config.get("MULTI_TENANCY_ENABLED", True)

def tenant_required(fn):
    """Decorator to ensure tenant context is set"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Skip tenant check for excluded routes
        excluded_paths = ['/api/auth/', '/static/', '/health']
        if any(request.path.startswith(path) for path in excluded_paths) or request.method == 'OPTIONS':
            return fn(*args, **kwargs)
            
        if not hasattr(g, 'tenant_id') or not g.tenant_id:
            current_app.logger.warning(f"Tenant context missing for path: {request.path}")
            return jsonify({
                "message": "Tenant context required", 
                "code": "TENANT_REQUIRED",
                "details": "Unable to determine tenant context. Please ensure proper authentication."
            }), 400
        
        if not hasattr(g, 'tenant') or not g.tenant:
            return jsonify({
                "message": "Invalid tenant", 
                "code": "INVALID_TENANT",
                "tenant_id": g.tenant_id
            }), 404
        
        return fn(*args, **kwargs)
    return wrapper

def require_tenant_membership(fn):
    """
    Decorator to ensure user belongs to the current tenant
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not hasattr(g, 'user') or not g.user:
            return jsonify({"message": "Authentication required", "code": "AUTH_REQUIRED"}), 401
        
        if not hasattr(g, 'tenant_id') or not g.tenant_id:
            return jsonify({"message": "Tenant context required", "code": "TENANT_REQUIRED"}), 400
        
        # Super admins can access any tenant
        if hasattr(g.user, 'role') and g.user.role == 'SUPER_ADMIN':
            return fn(*args, **kwargs)
        
        # Check if user belongs to the current tenant
        if str(g.user.organization_id) != str(g.tenant_id):
            return jsonify({
                "message": "Access denied: User does not belong to this tenant",
                "code": "TENANT_ACCESS_DENIED"
            }), 403
        
        return fn(*args, **kwargs)
    return wrapper


def cross_tenant_access(allowed_roles=None):
    """
    Decorator to allow cross-tenant access for specific roles
    
    Args:
        allowed_roles: List of roles that can access cross-tenant data
    """
    if allowed_roles is None:
        allowed_roles = ['SUPER_ADMIN']
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not hasattr(g, 'user') or not g.user:
                return jsonify({"message": "Authentication required", "code": "AUTH_REQUIRED"}), 401
            
            # Check if user has required role for cross-tenant access
            if hasattr(g.user, 'role') and g.user.role in allowed_roles:
                # For cross-tenant access, we might want to get tenant_id from query params
                tenant_param = request.args.get('tenant_id')
                if tenant_param:
                    g.tenant_id = tenant_param
                    g.tenant = Organization.query.get(tenant_param)
                
                return fn(*args, **kwargs)
            else:
                return jsonify({
                    "message": "Insufficient permissions for cross-tenant access",
                    "code": "CROSS_TENANT_DENIED"
                }), 403
        return wrapper
    return decorator



'''

# Standard tenant-scoped endpoint
@bp.route("/data")
@tenant_required
@require_tenant_membership
def get_data():
    # This will only return data for the current tenant
    data = multi_tenant_query(DataModel).all()
    return jsonify([item.to_dict() for item in data])

# Cross-tenant endpoint for super admins
@bp.route("/all-data")
@cross_tenant_access(allowed_roles=['SUPER_ADMIN'])
def get_all_data():
    # Super admins can access data from all tenants
    data = DataModel.query.all()  # No tenant filtering
    return jsonify([item.to_dict() for item in data])

# Service account endpoint
@bp.route("/system-data")
@tenant_required
def get_system_data():
    # Service accounts can access data with proper headers
    data = multi_tenant_query(DataModel, enforce_tenant=False).all()
    return jsonify([item.to_dict() for item in data])

    
'''