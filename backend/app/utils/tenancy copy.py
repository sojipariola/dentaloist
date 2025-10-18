# backend/app/utils/tenancy.py
'''
from flask import g, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from app.models.models import User, Organization

class TenancyMiddleware:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def set_tenant():
            """Set the tenant context for each request"""
            g.tenant_id = None
            g.tenant = None
            g.user = None

            # Skip tenancy completely for auth routes and OPTIONS requests
            if (request.path.startswith('/api/auth/') or 
                request.method == 'OPTIONS'):
                return

            try:
                # Only verify JWT for non-auth routes
                verify_jwt_in_request(optional=True)
                claims = get_jwt()
                if claims:
                    user_id = claims.get("sub")
                    if user_id:
                        user = User.query.get(user_id)
                        if user and user.organization:
                            g.tenant_id = str(user.organization_id)
                            g.tenant = user.organization
                            g.user = user
            except Exception as e:
                current_app.logger.warning(f"Tenancy middleware error: {e}")
                pass

            # Fallback logic for non-auth routes
            if not g.tenant_id:
                tenant_header = request.headers.get("X-Tenant-ID")
                if tenant_header:
                    g.tenant_id = str(tenant_header)
                    g.tenant = Organization.query.get(g.tenant_id)

                if not g.tenant_id:
                    g.tenant_id = current_app.config.get("DEFAULT_TENANT_ID")
                    if g.tenant_id:
                        g.tenant = Organization.query.get(g.tenant_id)



'''

# backend/app/utils/tenancy.py

from flask import g, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity
from functools import wraps
from app.models import User, Organization

class TenancyMiddleware:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        @app.before_request
        def set_tenant():
            """Set the tenant context for each request"""
            g.tenant_id = None
            g.tenant = None
            g.user = None

            # Skip tenancy for auth routes and OPTIONS requests
            if (request.path.startswith('/api/auth/') or 
                request.method == 'OPTIONS' or
                request.endpoint in ['auth.login', 'auth.register', 'auth.google_login', 'auth.google_authorize']):
                return

            try:
                # Try to get tenant from JWT (only for non-auth routes)
                verify_jwt_in_request(optional=True)
                claims = get_jwt()
                if claims:
                    user_id = claims.get("sub")
                    if user_id:
                        user = User.query.get(user_id)
                        if user and user.organization:
                            g.tenant_id = str(user.organization_id)
                            g.tenant = user.organization
                            g.user = user
            except Exception as e:
                current_app.logger.warning(f"Tenancy middleware error: {e}")
                pass

            # Fallback to header or default tenant (only for non-auth routes)
            if not g.tenant_id:
                tenant_header = request.headers.get("X-Tenant-ID")
                if tenant_header:
                    g.tenant_id = str(tenant_header)
                    g.tenant = Organization.query.get(g.tenant_id)

                # Default tenant for public routes
                if not g.tenant_id:
                    g.tenant_id = current_app.config.get("DEFAULT_TENANT_ID")
                    if g.tenant_id:
                        g.tenant = Organization.query.get(g.tenant_id)


def tenant_required(fn):
    """Decorator to ensure tenant context is set"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Skip tenant check for auth routes
        if (request.path.startswith('/api/auth/') or 
            request.method == 'OPTIONS' or
            request.endpoint in ['auth.login', 'auth.register', 'auth.google_login', 'auth.google_authorize']):
            return fn(*args, **kwargs)
            
        if not g.tenant_id:
            return {"message": "Tenant context required"}, 400
        if not g.tenant:
            return {"message": "Invalid tenant"}, 404
        return fn(*args, **kwargs)
    return wrapper


def multi_tenant_query(model):
    """Apply tenant filter to query"""
    # Skip tenant filtering for auth routes
    if (request.path.startswith('/api/auth/') or 
        request.method == 'OPTIONS' or
        request.endpoint in ['auth.login', 'auth.register', 'auth.google_login', 'auth.google_authorize']):
        return model.query
        
    if hasattr(model, 'organization_id') and g.tenant_id:
        return model.query.filter_by(organization_id=g.tenant_id)
    return model.query


def get_current_tenant():
    """Get current tenant organization"""
    return g.tenant


def get_current_tenant_id():
    """Get current tenant ID"""
    return g.tenant_id


def is_multi_tenant_enabled():
    """Check if multi-tenancy is enabled"""
    return current_app.config.get("MULTI_TENANCY_ENABLED", True)


