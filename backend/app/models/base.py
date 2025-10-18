# backend/app/models/base.py

from sqlalchemy import DateTime
from datetime import datetime
import uuid
from flask import g, has_request_context
from . import db

import threading

# Thread-local storage for tenant context
_tenant_context = threading.local()

class TenantAwareMixin:
    """Mixin for tenant-aware models"""
    
    @classmethod
    def filter_by_tenant(cls, query=None, tenant_id=None):
        """Apply tenant filter to query with explicit tenant_id"""
        if query is None:
            query = cls.query
        
        # Use provided tenant_id or get from context
        effective_tenant_id = tenant_id or get_current_tenant_id()
        
        if effective_tenant_id and hasattr(cls, 'organization_id'):
            return query.filter_by(organization_id=effective_tenant_id)
        
        return query
    
    @classmethod
    def get_tenant_objects(cls, tenant_id=None):
        """Get all objects for a specific tenant"""
        return cls.filter_by_tenant(tenant_id=tenant_id).all()
    
    @classmethod
    def get_tenant_object(cls, public_id, tenant_id=None):
        """Get specific object for a tenant"""
        return cls.filter_by_tenant(tenant_id=tenant_id).filter_by(
            public_id=public_id, 
            is_active=True
        ).first()


class BaseModel(db.Model, TenantAwareMixin):
    """Base model with common fields and methods"""
    __abstract__ = True
    
    # Primary keys
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    
    # Timestamps
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    def to_dict(self):
        """Convert model to dictionary with error handling"""
        try:
            base_data = {
                'id': self.id,
                'public_id': self.public_id,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                'is_active': self.is_active
            }
            
            # Add model-specific fields
            specific_data = self._to_dict_impl() if hasattr(self, '_to_dict_impl') else {}
            return {**base_data, **specific_data}
            
        except Exception as e:
            # Use proper logging in production
            print(f"Error serializing {self.__class__.__name__}: {e}")
            return {
                'id': self.id,
                'public_id': self.public_id,
                'error': 'Serialization failed',
                'error_details': str(e)
            }
    
    def save(self):
        """Save the model with error handling"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error saving {self.__class__.__name__}: {e}")
            return False
    
    def delete(self, soft=True):
        """Delete the model (soft or hard delete)"""
        try:
            if soft:
                self.is_active = False
                self.updated_at = datetime.utcnow()
                db.session.commit()
            else:
                db.session.delete(self)
                db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting {self.__class__.__name__}: {e}")
            return False
    
    @classmethod
    def get_by_public_id(cls, public_id, tenant_id=None):
        """Get model by public_id with tenant awareness"""
        try:
            return cls.filter_by_tenant(tenant_id=tenant_id).filter_by(
                public_id=public_id, 
                is_active=True
            ).first()
        except Exception as e:
            print(f"Error fetching {cls.__name__} by public_id: {e}")
            return None
    
    @classmethod
    def get_active(cls, tenant_id=None):
        """Get all active models for tenant"""
        try:
            return cls.filter_by_tenant(tenant_id=tenant_id).filter_by(is_active=True).all()
        except Exception as e:
            print(f"Error fetching active {cls.__name__}: {e}")
            return []


class LookupBaseModel(BaseModel):
    """Base model for all lookup tables"""
    __abstract__ = True
    
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    color = db.Column(db.String(7))  # For UI purposes
    
    def _to_dict_impl(self):
        return {
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'sort_order': self.sort_order,
            'color': self.color
        }


class TenantSpecificModel(BaseModel):
    """Base model for tenant-specific data (with organization_id)"""
    __abstract__ = True
    
    organization_id = db.Column(
        db.String(50), 
        db.ForeignKey('organizations.public_id'), 
        nullable=False,
        index=True
    )


def get_current_tenant_id():
    """Get current tenant ID from request context with fallbacks"""
    
    # 1. Check request context first (most common)
    if has_request_context() and hasattr(g, 'current_tenant_id'):
        return g.current_tenant_id
    
    # 2. Check if we're in a test environment
    if hasattr(g, 'test_tenant_id'):
        return g.test_tenant_id
    
    # 3. For background tasks or non-request contexts, return None
    # This allows explicit tenant_id passing in those cases
    return None



def get_current_tenant_id():
    """Get the current tenant ID from thread-local storage"""
    return getattr(_tenant_context, 'tenant_id', None)

def set_current_tenant(tenant_id):
    """Set the current tenant ID in thread-local storage"""
    _tenant_context.tenant_id = tenant_id

def clear_current_tenant():
    """Clear the current tenant ID from thread-local storage"""
    if hasattr(_tenant_context, 'tenant_id'):
        del _tenant_context.tenant_id

# Query class for more explicit tenant control
class TenantAwareQuery:
    """Explicit tenant-aware query builder"""
    
    def __init__(self, model_class, tenant_id=None):
        self.model_class = model_class
        self.tenant_id = tenant_id or get_current_tenant_id()
        self._query = model_class.query
    
    def all(self):
        """Get all records for tenant"""
        return self.model_class.filter_by_tenant(self._query, self.tenant_id).all()
    
    def filter(self, *args, **kwargs):
        """Add additional filters"""
        self._query = self._query.filter(*args, **kwargs)
        return self
    
    def first(self):
        """Get first record for tenant"""
        return self.model_class.filter_by_tenant(self._query, self.tenant_id).first()
    
    def count(self):
        """Count records for tenant"""
        return self.model_class.filter_by_tenant(self._query, self.tenant_id).count()


# For super admin or specific use cases
# from app.models.base import TenantAwareQuery

# Super admin viewing specific tenant
# patients = TenantAwareQuery(Patient, tenant_id='org_001').all()

# Regular user (automatic)
# patients = TenantAwareQuery(Patient).all()  # Uses current tenant