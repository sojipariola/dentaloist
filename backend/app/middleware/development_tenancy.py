# app/middleware/development_tenancy.py

"""
Development middleware for easy tenant switching
"""

from flask import request, g, current_app
import functools

def development_tenant_middleware():
    """
    Middleware for development that allows easy tenant switching via headers
    """
    def should_apply_tenancy():
        # Skip tenancy for certain paths
        excluded_paths = ['/health', '/metrics', '/admin', '/static']
        return not any(request.path.startswith(path) for path in excluded_paths)
    
    if should_apply_tenancy():
        # Development: Allow tenant override via header
        tenant_id = request.headers.get('X-Tenant-ID')
        
        if not tenant_id and current_app.config.get('DEBUG'):
            # Default to first tenant in development
            from app.models import Organization
            org = Organization.query.first()
            if org:
                tenant_id = org.public_id
        
        if tenant_id:
            g.tenant_id = tenant_id

def development_tenant_loader():
    """Development tenant loader for easy testing"""
    def load_tenant():
        from app.models import Organization
        tenant_id = getattr(g, 'tenant_id', None)
        
        if tenant_id and current_app.config.get('DEBUG'):
            org = Organization.query.filter_by(public_id=tenant_id).first()
            if org:
                return {
                    'id': org.public_id,
                    'name': org.name,
                    'is_active': org.is_active
                }
        return None
    
    return load_tenant