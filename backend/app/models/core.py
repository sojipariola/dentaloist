# backend/app/models/core.py


from sqlalchemy import (Text, DateTime, Float, Integer, String, Boolean, ForeignKey, 
                       Numeric, CheckConstraint, LargeBinary, Date, Time)
from sqlalchemy.dialects.postgresql import JSON 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import secrets
import hmac
import hashlib

from .base import BaseModel
from .lookups import (
    UserRole, OrganizationType, Gender, SubscriptionPlan, 
    TenantStatus, IndustryType, SecurityEventType
)
from .clinical import Appointment
from .role_permission import user_roles
from . import db #, bcrypt

class Tenant(BaseModel):
    """
    Multi-tenant isolation model for SaaS application
    """
    __tablename__ = 'tenants'
    __table_args__ = {'extend_existing': True}  
    
    # Basic Information
    name = db.Column(db.String(200), nullable=False, unique=True, index=True)
    domain = db.Column(db.String(50), unique=True, index=True)
    subdomain = db.Column(db.String(50), unique=True, index=True)
    display_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    industry_id = db.Column(db.Integer, db.ForeignKey('industry_types.id'), nullable=False)
    
    # Contact Information
    contact_email = db.Column(db.String(120), nullable=False, index=True)
    contact_phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Location Information
    address_line1 = db.Column(db.String(200))
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='USA')
    timezone = db.Column(db.String(50), default='UTC')
    
    # Subscription and Billing
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('tenant_statuses.id'), nullable=False)
    stripe_customer_id = db.Column(db.String(100), index=True)
    stripe_subscription_id = db.Column(db.String(100))
    
    # Subscription Dates
    trial_ends_at = db.Column(DateTime)
    subscription_ends_at = db.Column(DateTime)
    billing_cycle_start = db.Column(DateTime)
    billing_cycle_end = db.Column(DateTime)
    
    # Usage Limits and Quotas
    max_organizations = db.Column(Integer, default=5)
    max_users = db.Column(Integer, default=5)
    max_patients = db.Column(Integer, default=1000)
    max_storage_mb = db.Column(Integer, default=1024)
    features_enabled = db.Column(db.JSON, default=dict)
    
    # Customization
    logo_url = db.Column(db.String(500))
    favicon_url = db.Column(db.String(500))
    theme_settings = db.Column(db.JSON, default=dict)
    custom_domain = db.Column(db.String(200), unique=True, index=True)
    
    # Configuration
    settings = db.Column(db.JSON, default=dict)
    business_hours = db.Column(db.JSON, default=dict)
    holiday_schedule = db.Column(db.JSON, default=dict)
    
    # Compliance and Legal
    privacy_policy_url = db.Column(db.String(500))
    terms_of_service_url = db.Column(db.String(500))
    data_retention_days = db.Column(Integer, default=1095)
    compliance_settings = db.Column(db.JSON, default=dict)
    
    # Activation
    activated_at = db.Column(db.DateTime, nullable=True)
    activated_by = db.Column(db.Integer, nullable=True)
    
    # Relationships
    industry = relationship('IndustryType')
    subscription_plan = relationship('SubscriptionPlan')
    status = relationship('TenantStatus')
    organizations = relationship('Organization', back_populates='tenant')
    users = db.relationship('User', foreign_keys='User.tenant_id', back_populates='tenant', lazy=True)
    treatments = db.relationship('Treatment', foreign_keys='Treatment.tenant_id', back_populates='tenant', lazy=True)
    invitations = relationship('TenantInvitation', back_populates='tenant')
    audit_logs = relationship('TenantAuditLog', back_populates='tenant')       

    # Indexes
    __table_args__ = (
        db.Index('idx_tenant_status_plan', 'status_id', 'subscription_plan_id'),
        db.Index('idx_tenant_created_at', 'created_at'),
        db.Index('idx_tenant_custom_domain', 'custom_domain'),
        db.Index('idx_tenant_contact_email', 'contact_email'),
    )

    @hybrid_property
    def is_trial(self):
        """Check if tenant is in trial period"""
        return (self.status.code == 'trial' and 
                self.trial_ends_at and 
                self.trial_ends_at > datetime.utcnow())

    @hybrid_property
    def is_paid(self):
        """Check if tenant has active paid subscription"""
        paid_plan_codes = ['starter', 'professional', 'enterprise', 'custom']
        return (self.status.code == 'active' and 
                self.subscription_plan.code in paid_plan_codes and
                (self.subscription_ends_at is None or 
                 self.subscription_ends_at > datetime.utcnow()))

    @hybrid_property
    def user_count(self):
        """Get current number of active users"""
        return len([u for u in self.users if u.is_active])

    @hybrid_property
    def storage_usage_percentage(self):
        """Calculate storage usage percentage"""
        if self.max_storage_mb == 0:
            return 0.0
        # This would query actual storage usage
        current_usage = 0  # Placeholder
        return (current_usage / self.max_storage_mb) * 100

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'subdomain': self.subdomain,
            'display_name': self.display_name,
            'industry': self.industry.to_dict() if self.industry else None,
            'contact_email': self.contact_email,
            'subscription_plan': self.subscription_plan.to_dict() if self.subscription_plan else None,
            'status': self.status.to_dict() if self.status else None,
            'is_trial': self.is_trial,
            'is_paid': self.is_paid,
            'max_users': self.max_users,
            'user_count': self.user_count,
            'storage_usage_percentage': round(self.storage_usage_percentage, 2),
            'timezone': self.timezone
        }

    def activate(self, activated_by_user):
        """Activate the tenant"""
        if not self.is_active:
            self.is_active = True
            # Set status to active
            active_status = TenantStatus.query.filter_by(code='active').first()
            if active_status:
                self.status_id = active_status.id
            self.activated_at = datetime.utcnow()
            self.activated_by = activated_by_user.id
            return True
        return False

    def suspend(self, reason=None):
        """Suspend the tenant"""
        suspended_status = TenantStatus.query.filter_by(code='suspended').first()
        if suspended_status and self.status_id != suspended_status.id:
            self.status_id = suspended_status.id
            if reason:
                suspension_log = {
                    'suspended_at': datetime.utcnow().isoformat(),
                    'reason': reason,
                    'action_by': 'system'
                }
                if 'suspension_history' not in self.settings:
                    self.settings['suspension_history'] = []
                self.settings['suspension_history'].append(suspension_log)
            return True
        return False

    def upgrade_plan(self, new_plan_id, new_limits=None):
        """Upgrade tenant subscription plan"""
        if self.subscription_plan_id == new_plan_id:
            return False
        
        old_plan = self.subscription_plan
        self.subscription_plan_id = new_plan_id
        
        if new_limits:
            if 'max_users' in new_limits:
                self.max_users = new_limits['max_users']
            if 'max_patients' in new_limits:
                self.max_patients = new_limits['max_patients']
            if 'max_storage_mb' in new_limits:
                self.max_storage_mb = new_limits['max_storage_mb']
            if 'features_enabled' in new_limits:
                self.features_enabled = new_limits['features_enabled']
        
        # Log plan change
        plan_change = {
            'old_plan': old_plan.code if old_plan else None,
            'new_plan': self.subscription_plan.code if self.subscription_plan else None,
            'changed_at': datetime.utcnow().isoformat(),
            'limits': new_limits or {}
        }
        if 'plan_history' not in self.settings:
            self.settings['plan_history'] = []
        self.settings['plan_history'].append(plan_change)
        
        return True

    def can_add_user(self):
        """Check if tenant can add more users"""
        return self.user_count < self.max_users

    def is_feature_enabled(self, feature):
        """Check if a feature is enabled for this tenant"""
        return self.features_enabled.get(feature, False)

class Organization(BaseModel):
    """
    Organization model for multi-organization support within tenants
    """
    __tablename__ = 'organizations'

    # Basic Information
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    
    # Contact Information
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='USA')
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    website = db.Column(db.String(200))
    timezone = db.Column(db.String(20))
    currency_id = db.Column(db.String(200))
    
    # Business Information
    organization_type_id = db.Column(db.Integer, db.ForeignKey('organization_types.id'), nullable=False)
    tax_id = db.Column(db.String(100))
    business_type = db.Column(db.String(50))
    industry = db.Column(db.String(100))
    
    # Limits and Configuration
    max_staff = db.Column(db.Integer, default=3)
    max_patients = db.Column(db.Integer, default=10)
    
    # Status
    status = db.Column(db.String(20), default='active')
    is_verified = db.Column(db.Boolean, default=False)
    
    # Tenant Relationship
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=True)
    
    # Relationships
    tenant = relationship('Tenant', back_populates='organizations')
    organization_type = relationship('OrganizationType')
    users = relationship('User', back_populates='organization')
    roles = relationship('Role', back_populates='organization')
    staff_members = relationship('Staff', back_populates='organization')
    patients = relationship('Patient', back_populates='organization')
    appointments = relationship('Appointment', back_populates='organization')
    insurance_plans = relationship('InsurancePlan', back_populates='organization')
    inventory_items = relationship('InventoryItem', back_populates='organization')
    family_members = relationship('FamilyMember', back_populates='organization')
    suppliers = relationship('Supplier', back_populates='organization')
    purchase_orders = relationship('PurchaseOrder', back_populates='organization')
    expenses = relationship('Expense', back_populates='organization')
    products = db.relationship('Product', back_populates='organization', lazy=True)
    financial_reports = db.relationship('FinancialReport', back_populates='organization', lazy=True)
    analytics_reports = db.relationship('AnalyticsReport', back_populates='organization', lazy=True)
    widgets = relationship('Widget', back_populates='organization')
    
    integrations = relationship('Integration', back_populates='organization')
    payment_records = relationship('PaymentRecord', back_populates='organization')
    invoices = relationship('Invoice', back_populates='organization')
    availability_slots = relationship('AvailabilitySlot', back_populates='organization')
    treatment_rooms = relationship('TreatmentRoom', back_populates='organization')
    subscriptions = relationship('Subscription', back_populates='organization', foreign_keys='Subscription.organization_id')
    analytics_dashboards = db.relationship("AnalyticsDashboard", back_populates="organization", cascade="all, delete-orphan")
    kpis = db.relationship("KPI", back_populates="organization", cascade="all, delete-orphan")
    analytics_events = db.relationship("AnalyticsEvent", back_populates="organization", cascade="all, delete-orphan")
    report_schedules = db.relationship("ReportSchedule", back_populates="organization", cascade="all, delete-orphan") 
    data_exports = db.relationship( "DataExport", back_populates="organization", cascade="all, delete-orphan")
    financial_transactions = db.relationship('FinancialTransaction', back_populates='organization')
    
    
    # Add a helper property to get the current active subscription
    @property
    def current_subscription(self):
        """Get the current active subscription"""
        active_subs = [sub for sub in self.subscriptions if sub.is_active]
        return active_subs[0] if active_subs else None
    
    @hybrid_property
    def subscription_plan(self):
        """Get current subscription plan (for backward compatibility)"""
        current_sub = self.current_subscription
        return current_sub.plan if current_sub else None
        
    # Indexes
    __table_args__ = (
        db.Index('idx_organization_tenant', 'tenant_id', 'name'),
        db.Index('idx_organization_type', 'organization_type_id'),
        db.Index('idx_organization_status', 'status'),
        db.Index('idx_organization_email', 'email'),
    )

    @hybrid_property
    def staff_count(self):
        """Get current number of active staff"""
        return len([s for s in self.staff_members if s.status == 'active'])

    @hybrid_property
    def patient_count(self):
        """Get current number of active patients"""
        return len([p for p in self.patients if p.is_active])

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'description': self.description,
            'type': self.organization_type.to_dict() if self.organization_type else None,
            'subscription': self.subscription_plan.to_dict() if self.subscription_plan else None,
            'status': self.status,
            'is_verified': self.is_verified,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'staff_count': self.staff_count,
            'patient_count': self.patient_count,
            'max_staff': self.max_staff,
            'max_patients': self.max_patients,
            'tenant_name': self.tenant.name if self.tenant else None
        }

    def can_add_staff(self):
        """Check if organization can add more staff"""
        return self.staff_count < self.max_staff

    def can_add_patients(self):
        """Check if organization can add more patients"""
        return self.patient_count < self.max_patients

    def verify_organization(self):
        """Mark organization as verified"""
        self.is_verified = True
        return True

class TenantUsage(BaseModel):
    __tablename__ = 'tenant_usage'

    # id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, nullable=False)
    subscription_plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'))
    current_users = db.Column(db.Integer, default=0)
    current_patients = db.Column(db.Integer, default=0)
    current_entries = db.Column(db.Integer, default=0)
    last_notified = db.Column(db.DateTime, default=None)

    subscription_plan = db.relationship('SubscriptionPlan', backref='tenants')
    
    def usage_percentage(self):
        plan = self.subscription_plan
        users_pct = (self.current_users / plan.max_users) * 100 if plan.max_users else 0
        patients_pct = (self.current_patients / plan.max_patients) * 100 if plan.max_patients else 0
        entries_pct = (self.current_entries / plan.max_entries) * 100 if plan.max_entries else 0
        return {
            'users': users_pct,
            'patients': patients_pct,
            'entries': entries_pct
        }
        
    def highest_usage(self):
        usage = self.usage_percentage()
        return max(usage.values(), default=0)


class User(BaseModel, UserMixin):
    """
    Core user model with authentication and profile management
    """
    __tablename__ = 'users'
    
    # Authentication
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    
    address = db.Column(db.String(100))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    country = db.Column(db.String(20))
    state = db.Column(db.String(20))
    postal_code = db.Column(db.String(20))
    timezone = db.Column(db.String(20))

    avatar_url = db.Column(db.String(255))  # For social login profile pictures
    bio = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    
    # Professional Information
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    clinic_name = db.Column(db.String(100))
    
    # Roles and Permissions
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    custom_role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    
    # Status and Preferences
    is_admin = db.Column(db.Boolean, default=False)
    email_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(DateTime)
    last_activity = db.Column(DateTime)
    stripe_customer_id = db.Column(db.String(255))
    
    # Settings and Preferences
    settings = db.Column(db.JSON, default=lambda: {
        "theme": "auto",
        "language": "en",
        "email_notifications": True,
        "sms_notifications": False,
        "push_notifications": True,
        "appointment_reminders": True,
        "billing_notifications": True,
        "timezone": "UTC",
        "date_format": "MM/DD/YYYY",
        "time_format": "12h",
        "week_start": 0,
        "show_online_status": True,
        "allow_profile_view": True,
        "high_contrast_mode": False,
        "reduced_motion": False,
    })
    
    # Relationships
    organization = relationship('Organization', back_populates='users')
    tenant = relationship('Tenant', foreign_keys=[tenant_id], back_populates='users')
    custom_role = relationship('Role', back_populates='users')
    
    user_role = relationship('UserRole', foreign_keys=[user_role_id])
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    gender = relationship('Gender')

    staff_record = relationship('Staff', back_populates='user', uselist=False)
    password_history = relationship('PasswordHistory', back_populates='user')
    security_events = relationship('SecurityEvent', back_populates='user')
    login_attempts = relationship('LoginAttempt', back_populates='user')
    user_sessions = relationship('UserSession', back_populates='user')
    oauth_accounts = relationship('UserOAuth', back_populates='user')
    family_members = db.relationship("FamilyMember", foreign_keys="FamilyMember.user_id", back_populates="user")
    user_family_members = db.relationship("FamilyMember", foreign_keys="FamilyMember.family_user_id", back_populates="family_user", lazy=True)
    notifications = relationship('Notification', back_populates='user')
    audit_trails = relationship('AuditTrail', back_populates='user')
    file_records = relationship('FileRecord', back_populates='user')
    widgets = relationship('Widget', back_populates='user')
    widget_configs = relationship('WidgetConfig', foreign_keys='WidgetConfig.user_id', back_populates='user')
    user_created_insurance_plans = db.relationship('InsurancePlan', back_populates='insurance_creator', foreign_keys='InsurancePlan.created_by')
    user_inventory_transactions = db.relationship('InventoryTransaction', back_populates='transaction_performer')
    rate_limiters = db.relationship('RateLimiter', back_populates='user', lazy=True)
    analytics_events = db.relationship("AnalyticsEvent", back_populates="user", cascade="all, delete-orphan")

    # Add this property for backward compatibility

    @property
    def role_name(self):
        """Get role name as string for compatibility"""
        if self.user_role:
            return self.user_role.name
        return None
    
    @property 
    def is_admin_user(self):
        """Check if user has admin role"""
        return self.user_role and self.user_role.name == 'admin'
    
    def to_dict(self):
        """Enhanced to_dict method with role compatibility"""
        data = self._to_dict_impl()
        # Add string role for compatibility
        data['role'] = self.role_name
        return data
    
    @property
    def role(self):
        """Provide backward compatibility for 'role' attribute."""
        from app.models.lookups import UserRole
        if self.user_role_id:
            return UserRole.query.get(self.user_role_id)
        return None
    
    @role.setter 
    def role(self, value):
        """Set role through user_role_id."""
        if hasattr(value, 'id'):
            self.user_role_id = value.id
        else:
            self.user_role_id = value

    @property
    def role_names(self):
        """Return comma-separated role names for admin display."""
        names = []
        if self.user_role:
            names.append(self.user_role.name)
        if self.custom_role:
            names.append(self.custom_role.name)
        if self.roles:
            names.extend([r.name for r in self.roles])
        return ", ".join(names) if names else "No Role"


    # Indexes
    __table_args__ = (
        db.Index('idx_user_email_org', 'email', 'organization_id'),
        db.Index('idx_user_role_status', 'user_role_id', 'is_active'),
        db.Index('idx_user_tenant', 'tenant_id'),
        db.Index('idx_user_last_login', 'last_login'),
        db.Index('idx_user_activity', 'last_activity'),
    )

    @hybrid_property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def is_online(self):
        """Check if user is currently online"""
        if self.last_activity:
            return (datetime.utcnow() - self.last_activity) < timedelta(minutes=5)
        return False

    def set_password(self, password):
        """Set user password with hashing"""
        self.password_hash = generate_password_hash(password)
        # self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Record password change in history
        password_history = PasswordHistory(
            user_id=self.id,
            password_hash=self.password_hash
        )
        db.session.add(password_history)

    def check_password(self, password):
        """Check if password matches hash"""
        return check_password_hash(self.password_hash, password)
        # return bcrypt.check_password_hash(self.password_hash, password)

    def get_permissions(self):
        """Get user's permissions based on roles"""
        permissions = set()
        
        # Add user role permissions
        if self.user_role:
            # This would need to be implemented based on your permission system
            pass
        
        # Add custom role permissions
        if self.custom_role and self.custom_role.permissions:
            custom_perms = [perm.name for perm in self.custom_role.permissions]
            permissions.update(custom_perms)
        
        # Add individual user permissions from roles
        for role in self.roles:
            if hasattr(role, 'permissions') and role.permissions:
                role_perms = [perm.name for perm in role.permissions]
                permissions.update(role_perms)
        
        return list(permissions)

    def has_permission(self, permission):
        """Check if user has specific permission"""
        return permission in self.get_permissions()

    def record_login(self, ip_address=None, user_agent=None):
        """Record user login"""
        self.last_login = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        
        # Record security event
        login_event_type = SecurityEventType.query.filter_by(code='login_success').first()
        if login_event_type:
            security_event = SecurityEvent(
                user_id=self.id,
                event_type_id=login_event_type.id,
                ip_address=ip_address,
                user_agent=user_agent,
                description="User logged in successfully"
            )
            db.session.add(security_event)

    def record_activity(self):
        """Record user activity"""
        self.last_activity = datetime.utcnow()

    def generate_api_key(self):
        """Generate API key for user"""
        api_key = secrets.token_urlsafe(32)
        # Store hashed API key
        api_key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        if 'api_keys' not in self.settings:
            self.settings['api_keys'] = []
        
        self.settings['api_keys'].append({
            'key_hash': api_key_hash,
            'created_at': datetime.utcnow().isoformat(),
            'last_used': None,
            'is_active': True
        })
        
        return api_key

    def _to_dict_impl(self):
        return {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'phone': self.phone,
            'role': getattr(self.user_role, 'to_dict', lambda: {'name': self.user_role.name if self.user_role else None})(),
            'gender': getattr(self.gender, 'to_dict', lambda: {'name': self.gender.name if self.gender else None})(),
            'specialization': self.specialization,
            'license_number': self.license_number,
            'is_admin': self.is_admin,
            'is_online': self.is_online,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'organization_id': self.organization_id,
            'tenant_id': self.tenant_id,
            'permissions': self.get_permissions(),
            'settings': self.settings
        }

    @classmethod
    def find_by_email(cls, email):
        """Find user by email"""
        return cls.query.filter_by(email=email, is_active=True).first()

    @classmethod
    def search_users(cls, organization_id, query, limit=20):
        """Search users by name or email"""
        return cls.query.filter(
            cls.organization_id == organization_id,
            cls.is_active == True,
            db.or_(
                cls.first_name.ilike(f"%{query}%"),
                cls.last_name.ilike(f"%{query}%"),
                cls.email.ilike(f"%{query}%")
            )
        ).limit(limit).all()




class Staff(BaseModel):
    """
    Staff member model with professional details
    """
    __tablename__ = 'staff'
    
    # Foreign keys
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    
    # Professional Information
    staff_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    job_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    specialization = db.Column(db.String(100))
    license_number = db.Column(db.String(100))
    license_expiry = db.Column(db.Date)
    
    # Employment Details
    hire_date = db.Column(db.Date, nullable=False)
    termination_date = db.Column(db.Date)
    salary = db.Column(Numeric(10, 2))
    employment_type = db.Column(db.String(20), nullable=False)  # full-time, part-time, contract
    status = db.Column(db.String(20), default='active')  # active, inactive, suspended
    employee_id = db.Column(db.String(20))

    # Contact Information
    work_email = db.Column(db.String(120), unique=True)
    work_phone = db.Column(db.String(20))
    emergency_contact = db.Column(db.JSON)
    # emergency_contact_name = db.Column(db.String(100))
    # emergency_contact_phone = db.Column(db.String(20))
    # emergency_contact_relationship = db.Column(db.String(50))
    
    # Work Details
    office_location = db.Column(db.String(200))
    office_hours = db.Column(db.String(100))
    
    # Qualifications
    qualifications = db.Column(db.Text)
    certifications = db.Column(db.Text)
    languages_spoken = db.Column(db.Text)
    
    # Relationships
    organization = relationship('Organization', back_populates='staff_members')
    user = relationship('User', back_populates='staff_record')
    appointments = relationship('Appointment', back_populates='staff')
    treatment_plans = relationship('TreatmentPlan', back_populates='treating_staff', lazy=True)
    availability_slots = relationship('AvailabilitySlot', back_populates='staff')
    leave_requests = relationship('StaffLeave', back_populates='staff')
    availability = relationship('StaffAvailability', back_populates='staff')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_staff_org_number', 'organization_id', 'staff_number'),
        db.Index('idx_staff_status', 'status'),
        db.Index('idx_staff_job_title', 'job_title'),
        db.Index('idx_staff_hire_date', 'hire_date'),
    )

    @hybrid_property
    def is_active(self):
        """Check if staff member is active"""
        return self.status == 'active' and not self.termination_date

    @hybrid_property
    def years_of_service(self):
        """Calculate years of service"""
        if self.hire_date:
            today = date.today()
            return today.year - self.hire_date.year - (
                (today.month, today.day) < (self.hire_date.month, self.hire_date.day)
            )
        return 0

    def _to_dict_impl(self):
        return {
            'staff_number': self.staff_number,
            'job_title': self.job_title,
            'department': self.department,
            'specialization': self.specialization,
            'employment_type': self.employment_type,
            'status': self.status,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'years_of_service': self.years_of_service,
            'work_email': self.work_email,
            'work_phone': self.work_phone,
            'is_active': self.is_active,
            'user_info': {
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
                'email': self.user.email,
                'phone': self.user.phone
            } if self.user else None
        }

    def get_availability(self, date):
        """Get staff availability for specific date"""
        return StaffAvailability.query.filter_by(
            staff_id=self.id,
            date=date,
            is_available=True
        ).all()

    def request_leave(self, leave_type, start_date, end_date, reason=None):
        """Create leave request"""
        leave = StaffLeave(
            staff_id=self.id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        return leave

    def get_upcoming_appointments(self, days=7):
        """Get upcoming appointments for staff member"""
        cutoff_date = datetime.utcnow() + timedelta(days=days)
        return Appointment.query.filter(
            Appointment.staff_id == self.id,
            Appointment.start_time >= datetime.utcnow(),
            Appointment.start_time <= cutoff_date,
            Appointment.status.has(code__in=['scheduled', 'confirmed'])
        ).order_by(Appointment.start_time.asc()).all()

class StaffAvailability(BaseModel):
    """Staff availability scheduling"""
    __tablename__ = 'staff_availability'
    
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6 (Monday-Sunday)
    start_time = db.Column(Time, nullable=False)
    end_time = db.Column(Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    
    staff = relationship('Staff', back_populates='availability')

    def _to_dict_impl(self):
        return {
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'is_available': self.is_available,
            'staff_name': f"{self.staff.user.first_name} {self.staff.user.last_name}" if self.staff and self.staff.user else None
        }

class StaffLeave(BaseModel):
    """Staff leave management"""
    __tablename__ = 'staff_leave'
    
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    
    staff = relationship('Staff', back_populates='leave_requests')

    def _to_dict_impl(self):
        return {
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'reason': self.reason,
            'status': self.status,
            'staff_name': f"{self.staff.user.first_name} {self.staff.user.last_name}" if self.staff and self.staff.user else None
        }

class UserOAuth(BaseModel):
    """OAuth authentication providers"""
    __tablename__ = 'user_oauths'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    provider_user_id = db.Column(db.String(100), nullable=False)
    access_token = db.Column(db.String(255), nullable=False)
    refresh_token = db.Column(db.String(255))
    token_expiry = db.Column(DateTime)
    
    user = relationship('User', back_populates='oauth_accounts')

    def _to_dict_impl(self):
        return {
            'provider': self.provider,
            'provider_user_id': self.provider_user_id,
            'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None
        }

class FamilyMember(BaseModel):
    """Family member relationships"""
    __tablename__ = 'family_members'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    family_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    relationship_type = db.Column(db.String(50), default='family')
    emergency_contact = db.Column(db.Boolean, default=False)
    primary_contact = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship("User", foreign_keys=[user_id], back_populates="family_members")
    family_user = db.relationship("User", foreign_keys=[family_user_id], back_populates="user_family_members")
    creator = db.relationship("User", foreign_keys=[created_by], backref="created_family_members") 
    organization = db.relationship('Organization', back_populates='family_members')
    insurance_plans = db.relationship('InsurancePlan', back_populates='family_member', lazy=True)
    patient = db.relationship('Patient', back_populates='patient_family_members')
    family_relationships = db.relationship('FamilyRelationship', 
        foreign_keys='FamilyRelationship.family_member_id',
        back_populates='family_member', 
        cascade='all, delete-orphan')

    def _to_dict_impl(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'relationship_type': self.relationship_type,
            'emergency_contact': self.emergency_contact,
            'primary_contact': self.primary_contact,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None,
            'family_user_name': f"{self.family_user.first_name} {self.family_user.last_name}" if self.family_user else None,
            'patient_name': f"{self.patient.first_name} {self.patient.last_name}" if self.patient else None
        }

class FamilyRelationship(BaseModel):
    """Model for family member relationships"""
    __tablename__ = 'family_relationships'
    
    family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False)
    related_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=False)
    relationship_type = db.Column(db.String(50), nullable=False)  # parent, child, spouse, sibling, etc.
    notes = db.Column(db.Text)
    
    # Relationships
    family_member = relationship('FamilyMember', foreign_keys=[family_member_id], back_populates='family_relationships')
    related_member = relationship('FamilyMember', foreign_keys=[related_member_id])
    
    __table_args__ = (
        db.Index('idx_family_relationship_members', 'family_member_id', 'related_member_id'),
        db.Index('idx_family_relationship_type', 'relationship_type'),
    )

    def _to_dict_impl(self):
        return {
            'relationship_type': self.relationship_type,
            'notes': self.notes,
            'family_member_id': self.family_member_id,
            'related_member_id': self.related_member_id,
            'related_member_name': f"{self.related_member.first_name} {self.related_member.last_name}" if self.related_member else None
        }
    
# Security and audit models
class PasswordHistory(BaseModel):
    """Password history for security"""
    __tablename__ = 'password_history'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    user = relationship('User', back_populates='password_history')

    def _to_dict_impl(self):
        return {
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SecurityEvent(BaseModel):
    """Security event logging"""
    __tablename__ = 'security_events'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_type_id = db.Column(db.Integer, db.ForeignKey('security_event_types.id'), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    user = relationship('User', back_populates='security_events')
    event_type = relationship('SecurityEventType')

    def _to_dict_impl(self):
        return {
            'event_type': self.event_type.to_dict() if self.event_type else None,
            'description': self.description,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None
        }

class LoginAttempt(BaseModel):
    """Login attempt tracking"""
    __tablename__ = 'login_attempts'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    username = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text)
    success = db.Column(db.Boolean, default=False)
    attempt_type = db.Column(db.String(20), default='password')
    failure_reason = db.Column(db.String(100), nullable=True)
    
    user = relationship('User', back_populates='login_attempts')

    def mark_successful(self):
        """Mark this attempt as successful"""
        self.success = True
    
    def mark_failed(self, reason=None):
        """Mark this attempt as failed"""
        self.success = False
        self.failure_reason = reason

    def _to_dict_impl(self):
        return {
            'username': self.username,
            'ip_address': self.ip_address,
            'success': self.success,
            'attempt_type': self.attempt_type,
            'failure_reason': self.failure_reason,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None
        }

class UserSession(BaseModel):
    """User session management"""
    __tablename__ = 'user_sessions'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    login_time = db.Column(DateTime, default=datetime.utcnow)
    logout_time = db.Column(DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    user = relationship('User', back_populates='user_sessions')

    def _to_dict_impl(self):
        return {
            'session_token': self.session_token[:10] + '...' if self.session_token else None,
            'ip_address': self.ip_address,
            'login_time': self.login_time.isoformat() if self.login_time else None,
            'logout_time': self.logout_time.isoformat() if self.logout_time else None,
            'is_active': self.is_active,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None
        }

class TenantInvitation(BaseModel):
    """Tenant invitation system"""
    __tablename__ = 'tenant_invitations'
    
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    invited_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    expires_at = db.Column(DateTime, nullable=False)
    accepted_at = db.Column(DateTime)
    
    tenant = relationship('Tenant', back_populates='invitations')
    inviter = relationship('User')

    def _to_dict_impl(self):
        return {
            'email': self.email,
            'role': self.role,
            'token': self.token[:10] + '...',
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None,
            'tenant_name': self.tenant.name if self.tenant else None,
            'inviter_name': f"{self.inviter.first_name} {self.inviter.last_name}" if self.inviter else None
        }

class TenantAuditLog(BaseModel):
    """Tenant-specific audit logging"""
    __tablename__ = 'tenant_audit_logs'
    
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(100))
    resource_id = db.Column(db.String(50))
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    tenant = relationship('Tenant', back_populates='audit_logs')
    user = relationship('User')

    def _to_dict_impl(self):
        return {
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details or {},
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'tenant_name': self.tenant.name if self.tenant else None,
            'user_name': f"{self.user.first_name} {self.user.last_name}" if self.user else None
        }

class Subscription(BaseModel):
    """Subscription management"""
    __tablename__ = 'subscriptions'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('subscription_plans.id'), nullable=False)
    price = db.Column(Numeric(10, 2))
    start_date = db.Column(DateTime, default=datetime.utcnow)
    end_date = db.Column(DateTime)
    is_active = db.Column(db.Boolean, default=True)
    stripe_subscription_id = db.Column(db.String(100))
    
    organization = db.relationship("Organization", back_populates="subscriptions", foreign_keys=[organization_id])
    plan = relationship('SubscriptionPlan')

    def _to_dict_impl(self):
        return {
            'plan': self.plan.to_dict() if self.plan else None,
            'price': float(self.price) if self.price else None,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'organization_name': self.organization.name if self.organization else None
        }

class SocialLogin(db.Model):
    __tablename__ = 'social_logins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider = db.Column(db.String(50), nullable=False)  # google, facebook, github
    provider_id = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('social_logins', lazy=True))
    
    __table_args__ = (
        db.UniqueConstraint('provider', 'provider_id', name='unique_provider_user'),
    )



