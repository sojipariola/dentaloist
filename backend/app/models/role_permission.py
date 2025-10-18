# backend/app/models/role_permission.py

from datetime import datetime
from sqlalchemy import Numeric
from sqlalchemy.orm import relationship

from app.models import db, BaseModel


# ====================================================
# ASSOCIATION TABLES
# ====================================================

# Many-to-many: Role ↔ Permission
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True),
    db.Column('granted_at', db.DateTime, default=datetime.utcnow),
    extend_existing=True
)

# Many-to-many: User ↔ Role
user_roles = db.Table(
    'user_roles_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
    extend_existing=True
)

# Many-to-many: Staff ↔ Role
staff_roles = db.Table(
    'staff_roles_association',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow),
    extend_existing=True
)


# ====================================================
# ROLE MODEL
# ====================================================

class Role(BaseModel):
    """Role-based access control model."""
    __tablename__ = 'roles'

    name = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text)
    is_system_role = db.Column(db.Boolean, default=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    is_default = db.Column(db.Boolean, default=False)

    # Relationships
    organization = relationship('Organization', back_populates='roles')
    permissions = db.relationship(
        'Permission',
        secondary='role_permissions',
        back_populates='roles',
        lazy='dynamic'
    )
    users = relationship('User', secondary=user_roles, back_populates='roles')
    staff_members = relationship('Staff', secondary=staff_roles, backref='assigned_roles')

    __table_args__ = (
        db.Index('idx_role_org_name', 'organization_id', 'name'),
        db.Index('idx_role_system', 'is_system_role'),
        db.Index('idx_role_default', 'is_default'),
    )

    # ------------------------------------------------
    # Utility Methods
    # ------------------------------------------------
    def _to_dict_impl(self):
        return {
            'name': self.name,
            'description': self.description,
            'is_system_role': self.is_system_role,
            'is_default': self.is_default,
            'permissions': [perm.name for perm in self.permissions],
            'user_count': self.users.count() if hasattr(self.users, 'count') else len(self.users),
            'staff_count': len(self.staff_members),
        }

    def add_permission(self, permission):
        """Attach a permission to this role."""
        if permission not in self.permissions:
            self.permissions.append(permission)
            return True
        return False

    def remove_permission(self, permission):
        """Detach a permission from this role."""
        if permission in self.permissions:
            self.permissions.remove(permission)
            return True
        return False

    def has_permission(self, permission_name):
        """Check whether this role has a specific permission."""
        return self.permissions.filter_by(name=permission_name).count() > 0

    @classmethod
    def get_system_roles(cls):
        """Retrieve all system roles."""
        return cls.query.filter_by(is_system_role=True).all()

    @classmethod
    def get_default_roles(cls, organization_id):
        """Retrieve default roles within an organization."""
        return cls.query.filter_by(organization_id=organization_id, is_default=True).all()


# ====================================================
# PERMISSION MODEL
# ====================================================

class Permission(BaseModel):
    """Permission model for fine-grained access control."""
    __tablename__ = 'permissions'

    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    category = db.Column(db.String(50))  # e.g. 'patient', 'appointment', 'billing'

    roles = db.relationship(
        'Role',
        secondary='role_permissions',
        back_populates='permissions',
        lazy='dynamic'
    )

    __table_args__ = (
        db.Index('idx_permission_category', 'category'),
        db.Index('idx_permission_name', 'name'),
    )

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'role_count': self.roles.count() if hasattr(self.roles, 'count') else len(self.roles)
        }

    @classmethod
    def get_by_category(cls, category):
        """Retrieve permissions by category."""
        return cls.query.filter_by(category=category).all()

    @classmethod
    def initialize_default_permissions(cls):
        """Initialize default permissions in the system."""
        default_permissions = [
            # PATIENT
            {'name': 'create_patient', 'description': 'Create new patients', 'category': 'patient'},
            {'name': 'view_patient', 'description': 'View patient records', 'category': 'patient'},
            {'name': 'edit_patient', 'description': 'Edit patient information', 'category': 'patient'},
            {'name': 'delete_patient', 'description': 'Delete patients', 'category': 'patient'},

            # APPOINTMENT
            {'name': 'create_appointment', 'description': 'Create appointments', 'category': 'appointment'},
            {'name': 'view_appointment', 'description': 'View appointments', 'category': 'appointment'},
            {'name': 'edit_appointment', 'description': 'Edit appointments', 'category': 'appointment'},
            {'name': 'delete_appointment', 'description': 'Delete appointments', 'category': 'appointment'},

            # CLINICAL
            {'name': 'diagnose', 'description': 'Make diagnoses', 'category': 'clinical'},
            {'name': 'design_restoration', 'description': 'Design dental restorations', 'category': 'clinical'},
            {'name': 'upload_images', 'description': 'Upload medical images', 'category': 'clinical'},
            {'name': 'view_treatment', 'description': 'View treatment plans', 'category': 'clinical'},

            # USER MANAGEMENT
            {'name': 'manage_users', 'description': 'Manage users', 'category': 'user_management'},
            {'name': 'manage_roles', 'description': 'Manage roles', 'category': 'user_management'},

            # ORGANIZATION
            {'name': 'view_organization', 'description': 'View organization details', 'category': 'organization'},
            {'name': 'edit_organization', 'description': 'Edit organization settings', 'category': 'organization'},

            # FINANCIAL
            {'name': 'manage_billing', 'description': 'Manage billing', 'category': 'financial'},
            {'name': 'view_billing', 'description': 'View billing information', 'category': 'financial'},

            # ANALYTICS
            {'name': 'view_analytics', 'description': 'View analytics', 'category': 'analytics'},
            {'name': 'export_data', 'description': 'Export data', 'category': 'analytics'},

            # AI
            {'name': 'access_ai_advice', 'description': 'Access AI advice', 'category': 'ai'},

            # SYSTEM
            {'name': 'manage_system', 'description': 'Manage system settings', 'category': 'system'},
            {'name': 'view_audit_logs', 'description': 'View audit logs', 'category': 'system'},
        ]

        for perm_data in default_permissions:
            existing = cls.query.filter_by(name=perm_data['name']).first()
            if not existing:
                db.session.add(cls(**perm_data))
        db.session.commit()
