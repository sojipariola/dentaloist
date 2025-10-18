# backend/app/models/__init__.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Create SINGLE instances
db = SQLAlchemy()
bcrypt = Bcrypt()

"""
Models package initialization with proper import handling
"""

# Import base first
from .base import BaseModel, LookupBaseModel

# Import lookup models
from .lookups import (
    # Clinical lookups
    AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
    TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
    MedicationRoute, VitalSignsUnit,
    
    # Analytics lookups
    WidgetType, WidgetCategory, DashboardTheme, AnalyticsEventType, 
    AuditActionType, AuditResourceType, ReportCategory, NotificationType, 
    IntegrationStatus, WebhookEventStatus, WidgetTemplate, ReportType,
    
    # Core lookups
    UserRole, OrganizationType, Gender, SubscriptionPlan, TenantStatus, 
    IndustryType, SecurityEventType, PermissionCategory,
    
    # Financial lookups
    PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, ExpenseCategory, Currency,
    TransactionType,
    
    # Inventory lookups
    ProductType, InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType
)

# Import models in dependency order
from .role_permission import (
    Role, Permission, role_permissions, user_roles, staff_roles
)

from .core import (
    User, Organization, Tenant, Staff, StaffAvailability, TenantUsage,
    StaffLeave, UserOAuth, FamilyMember, FamilyRelationship, 
    PasswordHistory, SecurityEvent, LoginAttempt, UserSession, 
    TenantInvitation, TenantAuditLog, Subscription, SocialLogin
)

from .clinical import (
    Patient, Appointment, Treatment, ClinicalNote, Allergy, TreatmentRoom,
    Prescription, VitalSign, LabOrder, MedicalRecord, Procedure, 
    TreatmentPlan, Note, TelehealthSession, AvailabilitySlot
)

from .financial import (
    FinancialTransaction, Invoice, Payment, PaymentRecord, InsurancePlan, InsuranceClaim,
    Expense, FinancialReport 
)

from .inventory import (
    Product, ProductCategory, ProductImage, ProductPriceHistory,
    InventoryItem, InventoryTransaction, InventoryAdjustment,
    Supplier, PurchaseOrder, PurchaseOrderItem
)

# Import analytics models from their respective files
from .analytics import (
    AnalyticsDashboard, AnalyticsWidget, DashboardLayout, WidgetDataCache,
    AnalyticsEvent, Widget, WidgetConfig, Notification, AuditTrail
)

from .system_models import (
    RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog, 
    Webhook, WebhookEvent, FileRecord, AnalyticsReport, KPI, KPIHistory, 
    ReportSchedule, ReportRun, DataExport
)


# Re-export all models with proper organization
__all__ = [
    'BaseModel', 'LookupBaseModel',
    
    # Lookup models
    # Clinical lookups
    'AppointmentStatus', 'AppointmentType', 'PriorityLevel', 'TreatmentStatus',
    'TreatmentType', 'TreatmentPriority', 'NoteType', 'AllergySeverity',
    'MedicationRoute', 'VitalSignsUnit',
    
    # Analytics lookups
    'WidgetType', 'WidgetCategory', 'DashboardTheme', 'AnalyticsEventType',
    'AuditActionType', 'AuditResourceType', 'ReportCategory', 'NotificationType', 
    'IntegrationStatus', 'WebhookEventStatus', 'ReportType',
    
    # Core lookups
    'UserRole', 'OrganizationType', 'Gender', 'SubscriptionPlan', 'TenantStatus',
    'IndustryType', 'SecurityEventType', 'PermissionCategory',
    
    # Financial lookups
    'PaymentStatus', 'InvoiceStatus', 'PaymentMethod', 'ClaimStatus', 'ExpenseCategory', 
    'Currency', 'TransactionType',
    
    # Inventory lookups
    'ProductType', 'InventoryTransactionType', 'PurchaseOrderStatus', 'InventoryAdjustmentType',
    
    # Core models
    'Tenant', 'Organization', 'User', 'Role', 'Permission', 'Staff', 'TenantUsage',
    'StaffAvailability', 'StaffLeave', 'UserOAuth', 'FamilyMember', 'FamilyRelationship',
    'PasswordHistory', 'SecurityEvent', 'LoginAttempt', 'UserSession', 
    'TenantInvitation', 'TenantAuditLog', 'Subscription', 'SocialLogin',
    
    # Clinical models
    'Patient', 'Appointment', 'Treatment', 'ClinicalNote', 'Allergy', 'TreatmentRoom',
    'Prescription', 'VitalSign', 'LabOrder', 'MedicalRecord', 'Procedure', 
    'TreatmentPlan', 'Note', 'TelehealthSession', 'AvailabilitySlot',
    
    # Financial models
    'FinancialTransaction', 'Invoice', 'Payment', 'PaymentRecord', 'InsurancePlan', 
    'InsuranceClaim', 'Expense', 'FinancialReport',
    
    # Inventory models
    'Product', 'ProductCategory', 'ProductImage', 'ProductPriceHistory',
    'InventoryItem', 'InventoryTransaction', 'InventoryAdjustment',
    'Supplier', 'PurchaseOrder', 'PurchaseOrderItem',
    
    # Analytics models (new structure)
    'AnalyticsDashboard', 'AnalyticsWidget', 'DashboardLayout', 'WidgetDataCache',
    'AnalyticsEvent', 'AnalyticsReport', 'KPI', 'KPIHistory', 'ReportSchedule', 
    'ReportRun', 'DataExport',
    
    # System models
    'RateLimiter', 'RateLimit', 'EmailLog', 'Integration', 'IntegrationLog',
    'Webhook', 'WebhookEvent', 'FileRecord',
    
    # Legacy/Widget models (consider consolidating)
    'Widget', 'WidgetTemplate', 'WidgetConfig', 'Notification', 'AuditTrail'
]

# Create a function to get all models (useful for migrations)
def get_models():
    """Return all model classes for database operations"""
    return [
        # Lookup models
        # Clinical lookups
        AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
        TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
        MedicationRoute, VitalSignsUnit,
        
        # Analytics lookups
        WidgetType, WidgetCategory, DashboardTheme, AnalyticsEventType,
        AuditActionType, AuditResourceType, ReportCategory, NotificationType,
        IntegrationStatus, WebhookEventStatus, ReportType,
        
        # Core lookups
        UserRole, OrganizationType, Gender, SubscriptionPlan, TenantStatus,
        IndustryType, SecurityEventType, PermissionCategory,
        
        # Financial lookups
        PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, ExpenseCategory,
        Currency, TransactionType,
        
        # Inventory lookups
        ProductType, InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType,
        
        # Core models
        Tenant, Organization, User, Role, Permission, Staff, TenantUsage,
        StaffAvailability, StaffLeave, UserOAuth, FamilyMember, FamilyRelationship,
        PasswordHistory, SecurityEvent, LoginAttempt, UserSession,
        TenantInvitation, TenantAuditLog, Subscription, SocialLogin,
        
        # Clinical models
        Patient, Appointment, Treatment, ClinicalNote, Allergy, TreatmentRoom,
        Prescription, VitalSign, LabOrder, MedicalRecord, Procedure,
        TreatmentPlan, Note, TelehealthSession, AvailabilitySlot,
        
        # Financial models
        FinancialTransaction, Invoice, Payment, PaymentRecord, InsurancePlan, InsuranceClaim,
        Expense, FinancialReport,
        
        # Inventory models
        Product, ProductCategory, ProductImage, ProductPriceHistory,
        InventoryItem, InventoryTransaction, InventoryAdjustment,
        Supplier, PurchaseOrder, PurchaseOrderItem,
        
        # Analytics models (new structure)
        AnalyticsDashboard, AnalyticsWidget, DashboardLayout, WidgetDataCache,
        AnalyticsEvent, AnalyticsReport, KPI, KPIHistory, ReportSchedule,
        ReportRun, DataExport,
        
        # System models
        RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
        Webhook, WebhookEvent, FileRecord,
        
        # Legacy/Widget models
        Widget, WidgetTemplate, WidgetConfig, Notification, AuditTrail
    ]

# Create a function to get lookup models separately (useful for seeding)
def get_lookup_models():
    """Return all lookup model classes for data seeding"""
    return [
        # Clinical lookups
        AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
        TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
        MedicationRoute, VitalSignsUnit,
        
        # Analytics lookups
        WidgetType, WidgetCategory, DashboardTheme, AnalyticsEventType,
        AuditActionType, AuditResourceType, ReportCategory, NotificationType,
        IntegrationStatus, WebhookEventStatus, ReportType,
        
        # Core lookups
        UserRole, OrganizationType, Gender, SubscriptionPlan, TenantStatus,
        IndustryType, SecurityEventType, PermissionCategory,
        
        # Financial lookups
        PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, ExpenseCategory,
        Currency, TransactionType,
        
        # Inventory lookups
        ProductType, InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType
    ]

# Create a function to get business models (non-lookup)
def get_business_models():
    """Return all business model classes (non-lookup)"""
    return [
        # Core models
        Tenant, Organization, User, Role, Permission, Staff, TenantUsage,
        StaffAvailability, StaffLeave, UserOAuth, FamilyMember, FamilyRelationship,
        PasswordHistory, SecurityEvent, LoginAttempt, UserSession,
        TenantInvitation, TenantAuditLog, Subscription, SocialLogin,
        
        # Clinical models
        Patient, Appointment, Treatment, ClinicalNote, Allergy, TreatmentRoom,
        Prescription, VitalSign, LabOrder, MedicalRecord, Procedure,
        TreatmentPlan, Note, TelehealthSession, AvailabilitySlot,
        
        # Financial models
        FinancialTransaction, Invoice, Payment, PaymentRecord, InsurancePlan, InsuranceClaim,
        Expense, FinancialReport,
        
        # Inventory models
        Product, ProductCategory, ProductImage, ProductPriceHistory,
        InventoryItem, InventoryTransaction, InventoryAdjustment,
        Supplier, PurchaseOrder, PurchaseOrderItem,
        
        # Analytics models (new structure)
        AnalyticsDashboard, AnalyticsWidget, DashboardLayout, WidgetDataCache,
        AnalyticsEvent, AnalyticsReport, KPI, KPIHistory, ReportSchedule,
        ReportRun, DataExport,
        
        # System models
        RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
        Webhook, WebhookEvent, FileRecord,
        
        # Legacy/Widget models
        Widget, WidgetTemplate, WidgetConfig, Notification, AuditTrail
    ]

# Create a function to get analytics models specifically
def get_analytics_models():
    """Return all analytics model classes"""
    return [
        # Analytics models (new structure)
        AnalyticsDashboard, AnalyticsWidget, DashboardLayout, WidgetDataCache,
        AnalyticsEvent, AnalyticsReport, KPI, KPIHistory, ReportSchedule,
        ReportRun, DataExport,
        
        # System models (analytics related)
        RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
        Webhook, WebhookEvent, FileRecord,
        
        # Legacy/Widget models
        Widget, WidgetTemplate, WidgetConfig, Notification, AuditTrail,
        
        # Analytics lookup models
        WidgetType, WidgetCategory, DashboardTheme, AnalyticsEventType,
        AuditActionType, AuditResourceType, ReportCategory, NotificationType,
        IntegrationStatus, WebhookEventStatus, ReportType
    ]

# Create a function to get financial models specifically
def get_financial_models():
    """Return all financial model classes"""
    return [
        # Financial models
        FinancialTransaction, Invoice, Payment, PaymentRecord, InsurancePlan, InsuranceClaim,
        Expense, FinancialReport,
        
        # Financial lookup models
        PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, ExpenseCategory, Currency,
        TransactionType
    ]

# Create a function to get clinical models specifically
def get_clinical_models():
    """Return all clinical model classes"""
    return [
        # Clinical models
        Patient, Appointment, Treatment, ClinicalNote, Allergy, TreatmentRoom,
        Prescription, VitalSign, LabOrder, MedicalRecord, Procedure,
        TreatmentPlan, Note, TelehealthSession, AvailabilitySlot,
        
        # Clinical lookup models
        AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
        TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
        MedicationRoute, VitalSignsUnit
    ]

# Create a function to get inventory models specifically
def get_inventory_models():
    """Return all inventory model classes"""
    return [
        # Inventory models
        Product, ProductCategory, ProductImage, ProductPriceHistory,
        InventoryItem, InventoryTransaction, InventoryAdjustment,
        Supplier, PurchaseOrder, PurchaseOrderItem,
        
        # Inventory lookup models
        ProductType, InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType
    ]

# Create a function to get system models specifically
def get_system_models():
    """Return all system model classes"""
    return [
        # System models
        RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
        Webhook, WebhookEvent, FileRecord,
        
        # System lookup models
        IntegrationStatus, WebhookEventStatus, NotificationType
    ]