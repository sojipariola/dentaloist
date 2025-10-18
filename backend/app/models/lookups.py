# backend/app/models/lookups.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Numeric
from .base import LookupBaseModel
from . import db
from sqlalchemy import Numeric

# =============================================================================
# CLINICAL LOOKUPS
# =============================================================================

class AppointmentStatus(LookupBaseModel):
    __tablename__ = 'appointment_statuses'
    __table_args__ = {'extend_existing': True}  

    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    allows_editing = db.Column(db.Boolean, default=True)
    is_final_status = db.Column(db.Boolean, default=False)
    code = db.Column(db.String(20))  # Optional short code
    sort_order = db.Column(db.Integer, default=0)
    color = db.Column(db.String(7))  # Hex color code
    
    # Relationships
    appointments = db.relationship('Appointment', back_populates='status')
    
    def __repr__(self):
        return f'<AppointmentStatus {self.name}>'

    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'allows_editing': self.allows_editing,
            'is_final_status': self.is_final_status
        })
        return base_dict

class AppointmentType(LookupBaseModel):
    __tablename__ = 'appointment_types'
    
    default_duration = db.Column(db.Integer)  # in minutes
    requires_specialist = db.Column(db.Boolean, default=False)
    category = db.Column(db.String(50))  # consultation, procedure, emergency, etc.
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'default_duration': self.default_duration,
            'requires_specialist': self.requires_specialist,
            'category': self.category
        })
        return base_dict

class PriorityLevel(LookupBaseModel):
    __tablename__ = 'priority_levels'
    
    escalation_hours = db.Column(db.Integer)  # Hours before escalation
    requires_immediate_attention = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'escalation_hours': self.escalation_hours,
            'requires_immediate_attention': self.requires_immediate_attention
        })
        return base_dict

class TreatmentStatus(LookupBaseModel):
    __tablename__ = 'treatment_statuses'
    
    allows_modification = db.Column(db.Boolean, default=True)
    is_completed_status = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'allows_modification': self.allows_modification,
            'is_completed_status': self.is_completed_status
        })
        return base_dict

class TreatmentType(LookupBaseModel):
    __tablename__ = 'treatment_types'
    
    category = db.Column(db.String(50))  # preventive, restorative, etc.
    complexity_level = db.Column(db.String(20))  # simple, moderate, complex
    typical_duration = db.Column(db.Integer)  # in minutes
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'complexity_level': self.complexity_level,
            'typical_duration': self.typical_duration
        })
        return base_dict

class TreatmentPriority(LookupBaseModel):
    __tablename__ = 'treatment_priorities'
    # Inherits all fields from PriorityLevel base
    escalation_hours = db.Column(db.Integer)  # Hours before escalation
    requires_immediate_attention = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'escalation_hours': self.escalation_hours,
            'requires_immediate_attention': self.requires_immediate_attention
        })
        return base_dict
        
class NoteType(LookupBaseModel):
    __tablename__ = 'note_types'
    
    requires_soap_format = db.Column(db.Boolean, default=False)
    template = db.Column(db.Text)  # Template for this note type
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'requires_soap_format': self.requires_soap_format,
            'template': self.template
        })
        return base_dict

class AllergySeverity(LookupBaseModel):
    __tablename__ = 'allergy_severities'
    
    requires_emergency_care = db.Column(db.Boolean, default=False)
    risk_level = db.Column(db.String(20))  # low, medium, high, critical
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'requires_emergency_care': self.requires_emergency_care,
            'risk_level': self.risk_level
        })
        return base_dict

class MedicationRoute(LookupBaseModel):
    __tablename__ = 'medication_routes'
    
    administration_instructions = db.Column(db.Text)
    requires_training = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'administration_instructions': self.administration_instructions,
            'requires_training': self.requires_training
        })
        return base_dict

class VitalSignsUnit(LookupBaseModel):
    __tablename__ = 'vital_signs_units'
    
    unit_type = db.Column(db.String(50))  # pressure, rate, temperature, etc.
    conversion_factor = db.Column(db.Float)  # For unit conversions
    si_unit = db.Column(db.String(20))  # Corresponding SI unit
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'unit_type': self.unit_type,
            'conversion_factor': self.conversion_factor,
            'si_unit': self.si_unit
        })
        return base_dict


# =============================================================================
# ANALYTICS & DASHBOARD LOOKUPS
# =============================================================================

class WidgetType(LookupBaseModel):
    """Widget type catalog"""
    __tablename__ = 'widget_types'
    
    # Basic information
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    component_name = db.Column(db.String(100), nullable=False)  # Frontend component name
    code = db.Column(db.String(50), unique=True, nullable=False)  # ← ADD FROM FIRST
    
    # Configuration
    default_config = db.Column(db.JSON, default=dict)
    config_schema = db.Column(db.JSON, default=dict)  # JSON schema for configuration
    data_schema = db.Column(db.JSON, default=dict)  # JSON schema for expected data
    
    # Categorization
    category = db.Column(db.String(50), default='general')
    subcategory = db.Column(db.String(50))
    tags = db.Column(db.JSON, default=list)
    
    # Capabilities
    supports_filters = db.Column(db.Boolean, default=True)
    supports_refresh = db.Column(db.Boolean, default=True)
    supports_export = db.Column(db.Boolean, default=False)
    supports_drilldown = db.Column(db.Boolean, default=False)
    max_data_points = db.Column(db.Integer)  # ← ADD FROM FIRST
    
    # Display properties
    icon = db.Column(db.String(100))  # Icon name or URL
    color = db.Column(db.String(7), default='#3498db')  # Default color
    default_size = db.Column(db.String(20), default='medium')  # ← ADD FROM FIRST
    
    # System properties
    is_system = db.Column(db.Boolean, default=False)  # System widget vs custom
    is_active = db.Column(db.Boolean, default=True)
    
    # Versioning
    version = db.Column(db.String(20), default='1.0.0')
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'component_name': self.component_name,
            'default_config': self.default_config,
            'config_schema': self.config_schema,
            'data_schema': self.data_schema,
            'category': self.category,
            'subcategory': self.subcategory,
            'tags': self.tags,
            'supports_filters': self.supports_filters,
            'supports_refresh': self.supports_refresh,
            'supports_export': self.supports_export,
            'supports_drilldown': self.supports_drilldown,
            'icon': self.icon,
            'color': self.color,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'version': self.version,
            'default_size': self.default_size,  # ← ADD
            'max_data_points': self.max_data_points,  # ← ADD
            'code': self.code  # ← ADD
        })
        return base_dict

    def __repr__(self):
        return f'<WidgetType {self.name}>'

    

class WidgetTemplate(LookupBaseModel):  # ← CHANGE FROM BaseModel to LookupBaseModel
    """Widget template model - predefined widget configurations"""
    __tablename__ = 'widget_templates'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    widget_type = db.Column(db.String(50), nullable=False)
    default_config = db.Column(db.JSON, default=dict)
    category = db.Column(db.String(50), default='general')
    is_system = db.Column(db.Boolean, default=False)
    
    # Optional: Add organization context for templates
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    organization = db.relationship('Organization', backref='widget_templates')

    def __repr__(self):
        return f'<WidgetTemplate {self.name}>'


class WidgetCategory(LookupBaseModel):
    """Categories for organizing widgets in the UI"""
    __tablename__ = 'widget_categories'
    
    icon = db.Column(db.String(100))  # Icon name or URL
    color = db.Column(db.String(7), default='#3498db')  # Default color
    sort_order = db.Column(db.Integer, default=0)
    is_system = db.Column(db.Boolean, default=False)  # System category vs custom
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'icon': self.icon,
            'color': self.color,
            'sort_order': self.sort_order,
            'is_system': self.is_system
        })
        return base_dict

class DashboardTheme(LookupBaseModel):
    """Available dashboard themes"""
    __tablename__ = 'dashboard_themes'
    
    css_class = db.Column(db.String(50))  # CSS class for theme
    primary_color = db.Column(db.String(7))  # Hex color
    secondary_color = db.Column(db.String(7))  # Hex color
    is_dark = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'css_class': self.css_class,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'is_dark': self.is_dark
        })
        return base_dict

class AnalyticsEventType(LookupBaseModel):
    """Types of analytics events that can be tracked"""
    __tablename__ = 'analytics_event_types'
    
    category = db.Column(db.String(50))  # user, system, business, security
    severity = db.Column(db.String(20), default='info')  # info, warning, error
    requires_user_context = db.Column(db.Boolean, default=True)
    is_system_event = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'severity': self.severity,
            'requires_user_context': self.requires_user_context,
            'is_system_event': self.is_system_event
        })
        return base_dict

class AuditActionType(LookupBaseModel):
    """Standard audit action types"""
    __tablename__ = 'audit_action_types'
    
    category = db.Column(db.String(50))  # CREATE, READ, UPDATE, DELETE, SYSTEM
    requires_approval = db.Column(db.Boolean, default=False)
    log_level = db.Column(db.String(20), default='info')  # debug, info, warning, error
    is_sensitive = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'requires_approval': self.requires_approval,
            'log_level': self.log_level,
            'is_sensitive': self.is_sensitive
        })
        return base_dict

class AuditResourceType(LookupBaseModel):
    """Types of resources that can be audited"""
    __tablename__ = 'audit_resource_types'
    
    module = db.Column(db.String(50))  # user, patient, appointment, financial, etc.
    requires_audit = db.Column(db.Boolean, default=True)
    retention_days = db.Column(db.Integer, default=365)  # How long to keep audit logs
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'module': self.module,
            'requires_audit': self.requires_audit,
            'retention_days': self.retention_days
        })
        return base_dict

class ReportCategory(LookupBaseModel):
    """Categories for organizing reports"""
    __tablename__ = 'report_categories'
    
    icon = db.Column(db.String(100))
    sort_order = db.Column(db.Integer, default=0)
    requires_permission = db.Column(db.Boolean, default=True)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'icon': self.icon,
            'sort_order': self.sort_order,
            'requires_permission': self.requires_permission
        })
        return base_dict

class NotificationType(LookupBaseModel):
    __tablename__ = 'notification_types'
    
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    auto_expire_days = db.Column(db.Integer, default=30)  # Auto expire after days
    requires_action = db.Column(db.Boolean, default=False)
    template = db.Column(db.Text)  # Notification template
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'priority': self.priority,
            'auto_expire_days': self.auto_expire_days,
            'requires_action': self.requires_action,
            'template': self.template
        })
        return base_dict

class IntegrationStatus(LookupBaseModel):
    __tablename__ = 'integration_statuses'
    
    allows_sync = db.Column(db.Boolean, default=True)
    requires_attention = db.Column(db.Boolean, default=False)
    retry_allowed = db.Column(db.Boolean, default=True)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'allows_sync': self.allows_sync,
            'requires_attention': self.requires_attention,
            'retry_allowed': self.retry_allowed
        })
        return base_dict

class WebhookEventStatus(LookupBaseModel):
    __tablename__ = 'webhook_event_statuses'
    
    is_final_status = db.Column(db.Boolean, default=False)
    allows_retry = db.Column(db.Boolean, default=True)
    max_retries = db.Column(db.Integer, default=3)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_final_status': self.is_final_status,
            'allows_retry': self.allows_retry,
            'max_retries': self.max_retries
        })
        return base_dict

class ReportType(LookupBaseModel):
    __tablename__ = 'report_types'
    
    category = db.Column(db.String(50))  # financial, clinical, operational, etc.
    requires_parameters = db.Column(db.Boolean, default=False)
    data_retention_days = db.Column(db.Integer, default=365)
    template_available = db.Column(db.Boolean, default=True)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'requires_parameters': self.requires_parameters,
            'data_retention_days': self.data_retention_days,
            'template_available': self.template_available
        })
        return base_dict


# =============================================================================
# CORE SYSTEM LOOKUPS
# =============================================================================

class UserRole(LookupBaseModel):
    __tablename__ = 'user_roles'
    
    is_system_role = db.Column(db.Boolean, default=False)
    access_level = db.Column(db.String(20))  # admin, staff, user, guest
    can_manage_users = db.Column(db.Boolean, default=False)
    can_access_reports = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_system_role': self.is_system_role,
            'access_level': self.access_level,
            'can_manage_users': self.can_manage_users,
            'can_access_reports': self.can_access_reports
        })
        return base_dict

class OrganizationType(LookupBaseModel):
    __tablename__ = 'organization_types'
    
    max_users = db.Column(db.Integer, default=10)
    max_patients = db.Column(db.Integer, default=1000)
    features_available = db.Column(db.JSON, default=dict)
    requires_verification = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'max_users': self.max_users,
            'max_patients': self.max_patients,
            'features_available': self.features_available or {},
            'requires_verification': self.requires_verification
        })
        return base_dict

class Gender(LookupBaseModel):
    __tablename__ = 'genders'
    
    pronoun = db.Column(db.String(50))  # he/him, she/her, they/them
    is_active = db.Column(db.Boolean, default=True)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'pronoun': self.pronoun,
            'is_active': self.is_active
        })
        return base_dict

class SubscriptionPlan(LookupBaseModel):
    __tablename__ = 'subscription_plans'
    
    price_monthly = db.Column(db.Numeric(10, 2), nullable=False)
    price_yearly = db.Column(db.Numeric(10, 2), nullable=False)
    max_users = db.Column(db.Integer, default=5)
    max_patients = db.Column(db.Integer, default=100)
    max_entries = db.Column(db.Integer, default=1000)
    features = db.Column(db.JSON, default=dict)
    is_active = db.Column(db.Boolean, default=True)

    def next_plan(self):
        """Return the next higher active plan based on price."""
        return (
            SubscriptionPlan.query
            .filter(SubscriptionPlan.price_monthly > self.price_monthly, SubscriptionPlan.is_active == True)
            .order_by(SubscriptionPlan.price_monthly.asc())
            .first()
        )
        
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'price_monthly': float(self.price_monthly) if self.price_monthly else None,
            'price_yearly': float(self.price_yearly) if self.price_yearly else None,
            'max_users': self.max_users,
            'max_patients': self.max_patients,
            'features': self.features or {},
            'is_active': self.is_active
        })
        return base_dict

class TenantStatus(LookupBaseModel):
    __tablename__ = 'tenant_statuses'
    
    allows_login = db.Column(db.Boolean, default=True)
    requires_action = db.Column(db.Boolean, default=False)
    is_trial_status = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'allows_login': self.allows_login,
            'requires_action': self.requires_action,
            'is_trial_status': self.is_trial_status
        })
        return base_dict

class IndustryType(LookupBaseModel):
    __tablename__ = 'industry_types'
    
    category = db.Column(db.String(50))  # healthcare, dental, medical, etc.
    requires_license = db.Column(db.Boolean, default=False)
    special_requirements = db.Column(db.JSON, default=dict)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'requires_license': self.requires_license,
            'special_requirements': self.special_requirements or {}
        })
        return base_dict

class SecurityEventType(LookupBaseModel):
    __tablename__ = 'security_event_types'
    
    severity = db.Column(db.String(20), default='info')  # info, warning, error, critical
    requires_notification = db.Column(db.Boolean, default=False)
    log_level = db.Column(db.String(20), default='info')  # debug, info, warning, error
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'severity': self.severity,
            'requires_notification': self.requires_notification,
            'log_level': self.log_level
        })
        return base_dict

class PermissionCategory(LookupBaseModel):
    __tablename__ = 'permission_categories'
    
    module = db.Column(db.String(50))  # patient, appointment, financial, etc.
    sort_order = db.Column(db.Integer, default=0)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'module': self.module,
            'sort_order': self.sort_order
        })
        return base_dict


# =============================================================================
# FINANCIAL LOOKUPS
# =============================================================================

class PaymentStatus(LookupBaseModel):
    __tablename__ = 'payment_statuses'
    
    is_completed = db.Column(db.Boolean, default=False)
    allows_refund = db.Column(db.Boolean, default=False)
    requires_action = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_completed': self.is_completed,
            'allows_refund': self.allows_refund,
            'requires_action': self.requires_action
        })
        return base_dict

class TransactionType(LookupBaseModel):
    __tablename__ = 'transaction_types'
    
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)  # revenue, expense, asset, liability, adjustment
    is_system = db.Column(db.Boolean, default=False)
    requires_verification = db.Column(db.Boolean, default=False)
    
    # Relationships
    transactions = db.relationship('FinancialTransaction', back_populates='transaction_type')
    
    def _to_dict_impl(self):
        return {
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'is_system': self.is_system,
            'requires_verification': self.requires_verification
        }

class InvoiceStatus(LookupBaseModel):
    __tablename__ = 'invoice_statuses'
    
    is_final = db.Column(db.Boolean, default=False)
    allows_editing = db.Column(db.Boolean, default=True)
    send_notifications = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_final': self.is_final,
            'allows_editing': self.allows_editing,
            'send_notifications': self.send_notifications
        })
        return base_dict

class PaymentMethod(LookupBaseModel):
    __tablename__ = 'payment_methods'
    
    category = db.Column(db.String(50))  # cash, card, transfer, digital
    requires_processing = db.Column(db.Boolean, default=False)
    processing_fee_percentage = db.Column(Numeric(5, 2), default=0.0)
    is_online = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'requires_processing': self.requires_processing,
            'processing_fee_percentage': float(self.processing_fee_percentage) if self.processing_fee_percentage else None,
            'is_online': self.is_online
        })
        return base_dict

class ClaimStatus(LookupBaseModel):
    __tablename__ = 'claim_statuses'
    
    is_active = db.Column(db.Boolean, default=True)
    requires_action = db.Column(db.Boolean, default=False)
    allows_resubmission = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_active': self.is_active,
            'requires_action': self.requires_action,
            'allows_resubmission': self.allows_resubmission
        })
        return base_dict

class ExpenseCategory(LookupBaseModel):
    __tablename__ = 'expense_categories'
    
    is_tax_deductible = db.Column(db.Boolean, default=True)
    requires_approval = db.Column(db.Boolean, default=False)
    budget_category = db.Column(db.String(50))  # operational, capital, personnel
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'is_tax_deductible': self.is_tax_deductible,
            'requires_approval': self.requires_approval,
            'budget_category': self.budget_category
        })
        return base_dict

class Currency(LookupBaseModel):
    __tablename__ = 'currencies'
    
    symbol = db.Column(db.String(10))
    code = db.Column(db.String(3), unique=True, nullable=False)
    decimal_places = db.Column(db.Integer, default=2)
    is_active = db.Column(db.Boolean, default=True)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'symbol': self.symbol,
            'code': self.code,
            'decimal_places': self.decimal_places,
            'is_active': self.is_active
        })
        return base_dict


# =============================================================================
# INVENTORY LOOKUPS
# =============================================================================

class ProductType(LookupBaseModel):
    __tablename__ = 'product_types'
    
    category = db.Column(db.String(50))  # consumable, equipment, medication
    requires_lot_tracking = db.Column(db.Boolean, default=False)
    requires_expiration = db.Column(db.Boolean, default=False)
    is_medical = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'category': self.category,
            'requires_lot_tracking': self.requires_lot_tracking,
            'requires_expiration': self.requires_expiration,
            'is_medical': self.is_medical
        })
        return base_dict

class InventoryTransactionType(LookupBaseModel):
    __tablename__ = 'inventory_transaction_types'
    
    affects_stock = db.Column(db.Boolean, default=True)
    stock_direction = db.Column(db.String(10))  # in, out, neutral
    requires_approval = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'affects_stock': self.affects_stock,
            'stock_direction': self.stock_direction,
            'requires_approval': self.requires_approval
        })
        return base_dict

class PurchaseOrderStatus(LookupBaseModel):
    __tablename__ = 'purchase_order_statuses'
    
    allows_editing = db.Column(db.Boolean, default=True)
    is_final = db.Column(db.Boolean, default=False)
    send_notifications = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'allows_editing': self.allows_editing,
            'is_final': self.is_final,
            'send_notifications': self.send_notifications
        })
        return base_dict

class InventoryAdjustmentType(LookupBaseModel):
    __tablename__ = 'inventory_adjustment_types'
    
    stock_impact = db.Column(db.String(10))  # increase, decrease, correction
    requires_reason = db.Column(db.Boolean, default=True)
    requires_approval = db.Column(db.Boolean, default=False)
    
    def _to_dict_impl(self):
        base_dict = super()._to_dict_impl()
        base_dict.update({
            'stock_impact': self.stock_impact,
            'requires_reason': self.requires_reason,
            'requires_approval': self.requires_approval
        })
        return base_dict


