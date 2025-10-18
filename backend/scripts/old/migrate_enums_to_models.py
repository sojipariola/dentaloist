# backend/scripts/migrate_enums_to_models.py
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    # Lookup models
    AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
    TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
    MedicationRoute, VitalSignsUnit,
    WidgetType, NotificationType, IntegrationStatus, WebhookEventStatus, ReportType,
    UserRole, OrganizationType, Gender, SubscriptionPlan, TenantStatus,
    IndustryType, SecurityEventType, PermissionCategory,
    PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, ExpenseCategory, Currency,
    TransactionType,
    ProductType, InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType
)

# backend/scripts/migrate_enums_to_models.py

def safe_merge(model_class, data):
    """Safely merge data into a model, handling duplicates gracefully"""
    try:
        # Check if record already exists
        existing = model_class.query.filter_by(code=data['code']).first()
        if existing:
            # Update existing record
            for key, value in data.items():
                setattr(existing, key, value)
            return existing
        else:
            # Create new record
            instance = model_class(**data)
            db.session.add(instance)
            return instance
    except Exception as e:
        print(f"⚠️  Error merging {model_class.__name__} with code {data.get('code')}: {e}")
        return None

def seed_security_event_types():
    """Seed security event types with duplicate handling"""
    security_events = [
        {'code': 'login_success', 'name': 'Login Success', 'sort_order': 1, 'severity': 'info', 'requires_notification': False, 'log_level': 'info'},
        {'code': 'login_failed', 'name': 'Login Failed', 'sort_order': 2, 'severity': 'warning', 'requires_notification': True, 'log_level': 'warning'},
        {'code': 'password_change', 'name': 'Password Change', 'sort_order': 3, 'severity': 'info', 'requires_notification': True, 'log_level': 'info'},
        {'code': 'profile_update', 'name': 'Profile Update', 'sort_order': 4, 'severity': 'info', 'requires_notification': False, 'log_level': 'info'},
        {'code': 'logout', 'name': 'Logout', 'sort_order': 5, 'severity': 'info', 'requires_notification': False, 'log_level': 'info'},
        {'code': 'two_factor_enabled', 'name': 'Two-Factor Enabled', 'sort_order': 6, 'severity': 'info', 'requires_notification': True, 'log_level': 'info'},
        {'code': 'two_factor_disabled', 'name': 'Two-Factor Disabled', 'sort_order': 7, 'severity': 'warning', 'requires_notification': True, 'log_level': 'warning'},
        {'code': 'password_reset_request', 'name': 'Password Reset Request', 'sort_order': 8, 'severity': 'info', 'requires_notification': True, 'log_level': 'info'},
        {'code': 'password_reset_complete', 'name': 'Password Reset Complete', 'sort_order': 9, 'severity': 'info', 'requires_notification': True, 'log_level': 'info'},
    ]
    
    for event_data in security_events:
        safe_merge(SecurityEventType, event_data)
    
    print("   ✅ Security Event Types seeded")

def seed_core_lookups():
    """Seed core system lookup tables"""
    
    # User Roles
    user_roles = [
        {'code': 'super_admin', 'name': 'Super Administrator', 'sort_order': 1, 'is_system_role': True, 'access_level': 'admin', 'can_manage_users': True, 'can_access_reports': True},
        {'code': 'org_admin', 'name': 'Organization Admin', 'sort_order': 2, 'is_system_role': True, 'access_level': 'admin', 'can_manage_users': True, 'can_access_reports': True},
        {'code': 'dentist', 'name': 'Dentist', 'sort_order': 3, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': True},
        {'code': 'lab_technician', 'name': 'Lab Technician', 'sort_order': 4, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'assistant', 'name': 'Dental Assistant', 'sort_order': 5, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'nurse', 'name': 'Nurse', 'sort_order': 6, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'billing_staff', 'name': 'Billing Staff', 'sort_order': 7, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': True},
        {'code': 'researcher', 'name': 'Researcher', 'sort_order': 8, 'is_system_role': True, 'access_level': 'user', 'can_manage_users': False, 'can_access_reports': True},
        {'code': 'family_member', 'name': 'Family Member', 'sort_order': 9, 'is_system_role': True, 'access_level': 'user', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'visitor', 'name': 'Visitor', 'sort_order': 10, 'is_system_role': True, 'access_level': 'guest', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'staff', 'name': 'Staff', 'sort_order': 11, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'user', 'name': 'User', 'sort_order': 12, 'is_system_role': True, 'access_level': 'user', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'admin', 'name': 'Administrator', 'sort_order': 13, 'is_system_role': True, 'access_level': 'admin', 'can_manage_users': True, 'can_access_reports': True},
        {'code': 'receptionist', 'name': 'Receptionist', 'sort_order': 14, 'is_system_role': True, 'access_level': 'staff', 'can_manage_users': False, 'can_access_reports': False},
        {'code': 'patient', 'name': 'Patient', 'sort_order': 15, 'is_system_role': True, 'access_level': 'user', 'can_manage_users': False, 'can_access_reports': False},
    ]
    
    for role_data in user_roles:
        safe_merge(UserRole, role_data)
    
    # Organization Types
    org_types = [
        {'code': 'clinic', 'name': 'Dental Clinic', 'sort_order': 1, 'max_users': 50, 'max_patients': 10000, 'requires_verification': True},
        {'code': 'laboratory', 'name': 'Dental Laboratory', 'sort_order': 2, 'max_users': 20, 'max_patients': 0, 'requires_verification': True},
        {'code': 'family', 'name': 'Family Practice', 'sort_order': 3, 'max_users': 10, 'max_patients': 1000, 'requires_verification': False},
    ]
    
    for type_data in org_types:
        safe_merge(OrganizationType, type_data)
    
    # Genders
    genders = [
        {'code': 'male', 'name': 'Male', 'sort_order': 1, 'pronoun': 'he/him', 'is_active': True},
        {'code': 'female', 'name': 'Female', 'sort_order': 2, 'pronoun': 'she/her', 'is_active': True},
        {'code': 'other', 'name': 'Other', 'sort_order': 3, 'pronoun': 'they/them', 'is_active': True},
        {'code': 'prefer_not_to_say', 'name': 'Prefer not to say', 'sort_order': 4, 'pronoun': 'they/them', 'is_active': True},
    ]
    
    for gender_data in genders:
        safe_merge(Gender, gender_data)
    
    # Subscription Plans
    subscription_plans = [
        {'code': 'free', 'name': 'Free Plan', 'sort_order': 1, 'price_monthly': 0, 'price_yearly': 0, 'max_users': 3, 'max_patients': 100, 'is_active': True},
        {'code': 'starter', 'name': 'Starter Plan', 'sort_order': 2, 'price_monthly': 49, 'price_yearly': 490, 'max_users': 10, 'max_patients': 1000, 'is_active': True},
        {'code': 'professional', 'name': 'Professional Plan', 'sort_order': 3, 'price_monthly': 99, 'price_yearly': 990, 'max_users': 25, 'max_patients': 5000, 'is_active': True},
        {'code': 'enterprise', 'name': 'Enterprise Plan', 'sort_order': 4, 'price_monthly': 199, 'price_yearly': 1990, 'max_users': 100, 'max_patients': 50000, 'is_active': True},
        {'code': 'custom', 'name': 'Custom Plan', 'sort_order': 5, 'price_monthly': None, 'price_yearly': None, 'max_users': 0, 'max_patients': 0, 'is_active': True},
    ]
    
    for plan_data in subscription_plans:
        safe_merge(SubscriptionPlan, plan_data)
    
    # Tenant Statuses
    tenant_statuses = [
        {'code': 'active', 'name': 'Active', 'sort_order': 1, 'allows_login': True, 'requires_action': False, 'is_trial_status': False},
        {'code': 'suspended', 'name': 'Suspended', 'sort_order': 2, 'allows_login': False, 'requires_action': True, 'is_trial_status': False},
        {'code': 'trial', 'name': 'Trial', 'sort_order': 3, 'allows_login': True, 'requires_action': False, 'is_trial_status': True},
        {'code': 'expired', 'name': 'Expired', 'sort_order': 4, 'allows_login': False, 'requires_action': True, 'is_trial_status': False},
        {'code': 'setup', 'name': 'Setup', 'sort_order': 5, 'allows_login': True, 'requires_action': True, 'is_trial_status': False},
    ]
    
    for status_data in tenant_statuses:
        safe_merge(TenantStatus, status_data)
    
    # Industry Types
    industry_types = [
        {'code': 'dental', 'name': 'Dental', 'sort_order': 1, 'category': 'healthcare', 'requires_license': True},
        {'code': 'medical', 'name': 'Medical', 'sort_order': 2, 'category': 'healthcare', 'requires_license': True},
        {'code': 'veterinary', 'name': 'Veterinary', 'sort_order': 3, 'category': 'healthcare', 'requires_license': True},
        {'code': 'other_healthcare', 'name': 'Other Healthcare', 'sort_order': 4, 'category': 'healthcare', 'requires_license': True},
    ]
    
    for industry_data in industry_types:
        safe_merge(IndustryType, industry_data)
    
    # Security Event Types
    seed_security_event_types()
    
    # Permission Categories
    permission_categories = [
        {'code': 'user_management', 'name': 'User Management', 'sort_order': 1, 'description': 'Permissions related to user management'},
        {'code': 'patient_management', 'name': 'Patient Management', 'sort_order': 2, 'description': 'Permissions related to patient management'},
        {'code': 'clinical_operations', 'name': 'Clinical Operations', 'sort_order': 3, 'description': 'Permissions related to clinical operations'},
        {'code': 'financial_management', 'name': 'Financial Management', 'sort_order': 4, 'description': 'Permissions related to financial management'},
        {'code': 'inventory_management', 'name': 'Inventory Management', 'sort_order': 5, 'description': 'Permissions related to inventory management'},
        {'code': 'system_administration', 'name': 'System Administration', 'sort_order': 6, 'description': 'Permissions related to system administration'},
        {'code': 'reporting_analytics', 'name': 'Reporting & Analytics', 'sort_order': 7, 'description': 'Permissions related to reporting and analytics'},
    ]
    
    for category_data in permission_categories:
        safe_merge(PermissionCategory, category_data)

        
def seed_clinical_lookups():
    """Seed all lookup tables with enum data"""
    
    # Appointment Statuses
    appointment_statuses = [
        {'code': 'scheduled', 'name': 'Scheduled', 'sort_order': 1, 'allows_editing': True, 'is_final_status': False},
        {'code': 'confirmed', 'name': 'Confirmed', 'sort_order': 2, 'allows_editing': True, 'is_final_status': False},
        {'code': 'in_progress', 'name': 'In Progress', 'sort_order': 3, 'allows_editing': False, 'is_final_status': False},
        {'code': 'completed', 'name': 'Completed', 'sort_order': 4, 'allows_editing': False, 'is_final_status': True},
        {'code': 'cancelled', 'name': 'Cancelled', 'sort_order': 5, 'allows_editing': False, 'is_final_status': True},
        {'code': 'no_show', 'name': 'No Show', 'sort_order': 6, 'allows_editing': False, 'is_final_status': True},
        {'code': 'rescheduled', 'name': 'Rescheduled', 'sort_order': 7, 'allows_editing': True, 'is_final_status': False},
    ]
    
    for status_data in appointment_statuses:
        status = AppointmentStatus(**status_data)
        db.session.merge(status)
    
    # Appointment Types
    appointment_types = [
        {'code': 'consultation', 'name': 'Consultation', 'sort_order': 1, 'default_duration': 30, 'category': 'consultation'},
        {'code': 'checkup', 'name': 'Checkup', 'sort_order': 2, 'default_duration': 45, 'category': 'preventive'},
        {'code': 'cleaning', 'name': 'Cleaning', 'sort_order': 3, 'default_duration': 60, 'category': 'preventive'},
        {'code': 'filling', 'name': 'Filling', 'sort_order': 4, 'default_duration': 45, 'category': 'restorative'},
        {'code': 'extraction', 'name': 'Extraction', 'sort_order': 5, 'default_duration': 30, 'category': 'surgery', 'requires_specialist': True},
        {'code': 'root_canal', 'name': 'Root Canal', 'sort_order': 6, 'default_duration': 90, 'category': 'endodontic', 'requires_specialist': True},
        {'code': 'crown', 'name': 'Crown', 'sort_order': 7, 'default_duration': 60, 'category': 'prosthodontic'},
        {'code': 'braces', 'name': 'Braces', 'sort_order': 8, 'default_duration': 45, 'category': 'orthodontic', 'requires_specialist': True},
        {'code': 'implant', 'name': 'Implant', 'sort_order': 9, 'default_duration': 120, 'category': 'surgery', 'requires_specialist': True},
        {'code': 'emergency', 'name': 'Emergency', 'sort_order': 10, 'default_duration': 30, 'category': 'emergency'},
        {'code': 'follow_up', 'name': 'Follow Up', 'sort_order': 11, 'default_duration': 20, 'category': 'consultation'},
        {'code': 'other', 'name': 'Other', 'sort_order': 12, 'default_duration': 30, 'category': 'other'},
    ]
    
    for type_data in appointment_types:
        appt_type = AppointmentType(**type_data)
        db.session.merge(appt_type)
    
    # Priority Levels
    priority_levels = [
        {'code': 'low', 'name': 'Low', 'sort_order': 1, 'color': '#28a745', 'escalation_hours': 72},
        {'code': 'medium', 'name': 'Medium', 'sort_order': 2, 'color': '#ffc107', 'escalation_hours': 48},
        {'code': 'high', 'name': 'High', 'sort_order': 3, 'color': '#fd7e14', 'escalation_hours': 24},
        {'code': 'urgent', 'name': 'Urgent', 'sort_order': 4, 'color': '#dc3545', 'escalation_hours': 4, 'requires_immediate_attention': True},
    ]
    
    for priority_data in priority_levels:
        priority = PriorityLevel(**priority_data)
        db.session.merge(priority)
    
    # Treatment Statuses
    treatment_statuses = [
        {'code': 'scheduled', 'name': 'Scheduled', 'sort_order': 1, 'allows_modification': True, 'is_completed_status': False},
        {'code': 'in_progress', 'name': 'In Progress', 'sort_order': 2, 'allows_modification': True, 'is_completed_status': False},
        {'code': 'completed', 'name': 'Completed', 'sort_order': 3, 'allows_modification': False, 'is_completed_status': True},
        {'code': 'cancelled', 'name': 'Cancelled', 'sort_order': 4, 'allows_modification': False, 'is_completed_status': True},
        {'code': 'postponed', 'name': 'Postponed', 'sort_order': 5, 'allows_modification': True, 'is_completed_status': False},
    ]
    
    for status_data in treatment_statuses:
        status = TreatmentStatus(**status_data)
        db.session.merge(status)
    
    # Treatment Types
    treatment_types = [
        {'code': 'preventive', 'name': 'Preventive', 'sort_order': 1, 'category': 'preventive', 'complexity_level': 'simple', 'typical_duration': 45},
        {'code': 'restorative', 'name': 'Restorative', 'sort_order': 2, 'category': 'restorative', 'complexity_level': 'moderate', 'typical_duration': 60},
        {'code': 'endodontic', 'name': 'Endodontic', 'sort_order': 3, 'category': 'specialty', 'complexity_level': 'complex', 'typical_duration': 90},
        {'code': 'periodontal', 'name': 'Periodontal', 'sort_order': 4, 'category': 'specialty', 'complexity_level': 'moderate', 'typical_duration': 60},
        {'code': 'prosthodontic', 'name': 'Prosthodontic', 'sort_order': 5, 'category': 'prosthetic', 'complexity_level': 'complex', 'typical_duration': 120},
        {'code': 'orthodontic', 'name': 'Orthodontic', 'sort_order': 6, 'category': 'specialty', 'complexity_level': 'complex', 'typical_duration': 45},
        {'code': 'oral_surgery', 'name': 'Oral Surgery', 'sort_order': 7, 'category': 'surgical', 'complexity_level': 'complex', 'typical_duration': 60},
        {'code': 'cosmetic', 'name': 'Cosmetic', 'sort_order': 8, 'category': 'cosmetic', 'complexity_level': 'moderate', 'typical_duration': 90},
        {'code': 'diagnostic', 'name': 'Diagnostic', 'sort_order': 9, 'category': 'diagnostic', 'complexity_level': 'simple', 'typical_duration': 30},
        {'code': 'other', 'name': 'Other', 'sort_order': 10, 'category': 'other', 'complexity_level': 'simple', 'typical_duration': 30},
    ]
    
    for type_data in treatment_types:
        treatment_type = TreatmentType(**type_data)
        db.session.merge(treatment_type)
    
    # Treatment Priorities (same as priority levels)
    treatment_priorities = [
        {'code': 'low', 'name': 'Low', 'sort_order': 1, 'color': '#28a745'},
        {'code': 'medium', 'name': 'Medium', 'sort_order': 2, 'color': '#ffc107'},
        {'code': 'high', 'name': 'High', 'sort_order': 3, 'color': '#fd7e14'},
        {'code': 'urgent', 'name': 'Urgent', 'sort_order': 4, 'color': '#dc3545'},
    ]
    
    for priority_data in treatment_priorities:
        priority = TreatmentPriority(**priority_data)
        db.session.merge(priority)
    
    # Note Types
    note_types = [
        {'code': 'progress', 'name': 'Progress Note', 'sort_order': 1, 'requires_soap_format': False},
        {'code': 'assessment', 'name': 'Assessment Note', 'sort_order': 2, 'requires_soap_format': False},
        {'code': 'plan', 'name': 'Treatment Plan', 'sort_order': 3, 'requires_soap_format': False},
        {'code': 'soap', 'name': 'SOAP Note', 'sort_order': 4, 'requires_soap_format': True},
        {'code': 'clinical', 'name': 'Clinical Note', 'sort_order': 5, 'requires_soap_format': False},
        {'code': 'patient', 'name': 'Patient Note', 'sort_order': 6, 'requires_soap_format': False},
    ]
    
    for note_data in note_types:
        note_type = NoteType(**note_data)
        db.session.merge(note_type)
    
    # Allergy Severities
    allergy_severities = [
        {'code': 'mild', 'name': 'Mild', 'sort_order': 1, 'risk_level': 'low', 'requires_emergency_care': False},
        {'code': 'moderate', 'name': 'Moderate', 'sort_order': 2, 'risk_level': 'medium', 'requires_emergency_care': False},
        {'code': 'severe', 'name': 'Severe', 'sort_order': 3, 'risk_level': 'high', 'requires_emergency_care': True},
        {'code': 'anaphylactic', 'name': 'Anaphylactic', 'sort_order': 4, 'risk_level': 'critical', 'requires_emergency_care': True},
    ]
    
    for severity_data in allergy_severities:
        severity = AllergySeverity(**severity_data)
        db.session.merge(severity)
    
    # Medication Routes
    medication_routes = [
        {'code': 'oral', 'name': 'Oral', 'sort_order': 1, 'administration_instructions': 'Take by mouth with water'},
        {'code': 'topical', 'name': 'Topical', 'sort_order': 2, 'administration_instructions': 'Apply to affected area'},
        {'code': 'injection', 'name': 'Injection', 'sort_order': 3, 'administration_instructions': 'Administer by injection', 'requires_training': True},
        {'code': 'inhalation', 'name': 'Inhalation', 'sort_order': 4, 'administration_instructions': 'Inhale as directed'},
        {'code': 'sublingual', 'name': 'Sublingual', 'sort_order': 5, 'administration_instructions': 'Place under tongue'},
    ]
    
    for route_data in medication_routes:
        route = MedicationRoute(**route_data)
        db.session.merge(route)
    
    # Vital Signs Units
    vital_units = [
        {'code': 'mmHg', 'name': 'Millimeters of Mercury', 'sort_order': 1, 'unit_type': 'pressure', 'si_unit': 'Pa'},
        {'code': 'bpm', 'name': 'Beats per Minute', 'sort_order': 2, 'unit_type': 'rate', 'si_unit': 'Hz'},
        {'code': 'breaths/min', 'name': 'Breaths per Minute', 'sort_order': 3, 'unit_type': 'rate', 'si_unit': 'Hz'},
        {'code': '°C', 'name': 'Degrees Celsius', 'sort_order': 4, 'unit_type': 'temperature', 'si_unit': 'K'},
        {'code': '%', 'name': 'Percentage', 'sort_order': 5, 'unit_type': 'percentage', 'si_unit': '1'},
    ]
    
    for unit_data in vital_units:
        unit = VitalSignsUnit(**unit_data)
        db.session.merge(unit)
    
    try:
        db.session.commit()
        print("Successfully seeded all lookup tables!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding lookup tables: {e}")
        raise

def seed_analytics_lookups():
    """Seed analytics lookup tables"""
    
    # Widget Types
    widget_types = [
        {'code': 'stats_card', 'name': 'Stats Card', 'sort_order': 1, 'default_size': 'small', 'category': 'overview'},
        {'code': 'line_chart', 'name': 'Line Chart', 'sort_order': 2, 'default_size': 'medium', 'category': 'analytics', 'supports_refresh': True, 'max_data_points': 100},
        {'code': 'bar_chart', 'name': 'Bar Chart', 'sort_order': 3, 'default_size': 'medium', 'category': 'analytics', 'supports_refresh': True, 'max_data_points': 50},
        {'code': 'pie_chart', 'name': 'Pie Chart', 'sort_order': 4, 'default_size': 'small', 'category': 'analytics', 'supports_refresh': True, 'max_data_points': 10},
        {'code': 'table', 'name': 'Data Table', 'sort_order': 5, 'default_size': 'large', 'category': 'data', 'supports_refresh': True},
        {'code': 'list', 'name': 'List View', 'sort_order': 6, 'default_size': 'medium', 'category': 'data'},
        {'code': 'metric', 'name': 'Metric Display', 'sort_order': 7, 'default_size': 'xsmall', 'category': 'overview'},
        {'code': 'actions', 'name': 'Action Buttons', 'sort_order': 8, 'default_size': 'small', 'category': 'actions'},
        {'code': 'calendar', 'name': 'Calendar', 'sort_order': 9, 'default_size': 'large', 'category': 'scheduling'},
    ]
    
    for type_data in widget_types:
        widget_type = WidgetType(**type_data)
        db.session.merge(widget_type)
    
    # Notification Types
    notification_types = [
        {'code': 'info', 'name': 'Information', 'sort_order': 1, 'priority': 'low', 'auto_expire_days': 7},
        {'code': 'warning', 'name': 'Warning', 'sort_order': 2, 'priority': 'normal', 'auto_expire_days': 14, 'requires_action': False},
        {'code': 'error', 'name': 'Error', 'sort_order': 3, 'priority': 'high', 'auto_expire_days': 30, 'requires_action': True},
        {'code': 'success', 'name': 'Success', 'sort_order': 4, 'priority': 'low', 'auto_expire_days': 3},
        {'code': 'appointment_reminder', 'name': 'Appointment Reminder', 'sort_order': 5, 'priority': 'normal', 'auto_expire_days': 1, 'requires_action': True},
        {'code': 'payment_due', 'name': 'Payment Due', 'sort_order': 6, 'priority': 'high', 'auto_expire_days': 7, 'requires_action': True},
        {'code': 'system_alert', 'name': 'System Alert', 'sort_order': 7, 'priority': 'urgent', 'auto_expire_days': 30, 'requires_action': True},
    ]
    
    for type_data in notification_types:
        notification_type = NotificationType(**type_data)
        db.session.merge(notification_type)
    
    # Integration Statuses
    integration_statuses = [
        {'code': 'disconnected', 'name': 'Disconnected', 'sort_order': 1, 'allows_sync': False, 'requires_attention': True},
        {'code': 'connected', 'name': 'Connected', 'sort_order': 2, 'allows_sync': True, 'requires_attention': False},
        {'code': 'error', 'name': 'Error', 'sort_order': 3, 'allows_sync': False, 'requires_attention': True, 'retry_allowed': True},
        {'code': 'syncing', 'name': 'Syncing', 'sort_order': 4, 'allows_sync': False, 'requires_attention': False},
    ]
    
    for status_data in integration_statuses:
        status = IntegrationStatus(**status_data)
        db.session.merge(status)
    
    # Webhook Event Statuses
    webhook_statuses = [
        {'code': 'pending', 'name': 'Pending', 'sort_order': 1, 'is_final_status': False, 'allows_retry': True, 'max_retries': 3},
        {'code': 'delivered', 'name': 'Delivered', 'sort_order': 2, 'is_final_status': True, 'allows_retry': False},
        {'code': 'failed', 'name': 'Failed', 'sort_order': 3, 'is_final_status': True, 'allows_retry': True, 'max_retries': 3},
        {'code': 'retrying', 'name': 'Retrying', 'sort_order': 4, 'is_final_status': False, 'allows_retry': True, 'max_retries': 3},
    ]
    
    for status_data in webhook_statuses:
        status = WebhookEventStatus(**status_data)
        db.session.merge(status)
    
    # Report Types
    report_types = [
        {'code': 'patient_summary', 'name': 'Patient Summary', 'sort_order': 1, 'category': 'clinical', 'requires_parameters': True, 'data_retention_days': 365},
        {'code': 'financial_report', 'name': 'Financial Report', 'sort_order': 2, 'category': 'financial', 'requires_parameters': True, 'data_retention_days': 730},
        {'code': 'appointment_history', 'name': 'Appointment History', 'sort_order': 3, 'category': 'operational', 'requires_parameters': True, 'data_retention_days': 365},
        {'code': 'clinical_outcomes', 'name': 'Clinical Outcomes', 'sort_order': 4, 'category': 'clinical', 'requires_parameters': True, 'data_retention_days': 1825},
        {'code': 'inventory_report', 'name': 'Inventory Report', 'sort_order': 5, 'category': 'inventory', 'requires_parameters': False, 'data_retention_days': 90},
        {'code': 'staff_performance', 'name': 'Staff Performance', 'sort_order': 6, 'category': 'hr', 'requires_parameters': True, 'data_retention_days': 365},
        {'code': 'revenue_analysis', 'name': 'Revenue Analysis', 'sort_order': 7, 'category': 'financial', 'requires_parameters': True, 'data_retention_days': 365},
        {'code': 'treatment_stats', 'name': 'Treatment Statistics', 'sort_order': 8, 'category': 'clinical', 'requires_parameters': False, 'data_retention_days': 1825},
    ]
    
    for type_data in report_types:
        report_type = ReportType(**type_data)
        db.session.merge(report_type)





def seed_transaction_types():
    """Seed transaction types for FinancialTransaction model"""
    transaction_types = [
        # Invoice related
        {'code': 'invoice_creation', 'name': 'Invoice Creation', 'description': 'Creation of a new invoice', 'category': 'revenue', 'sort_order': 1},
        {'code': 'invoice_discount', 'name': 'Invoice Discount', 'description': 'Discount applied to invoice', 'category': 'adjustment', 'sort_order': 2},
        {'code': 'write_off', 'name': 'Write Off', 'description': 'Amount written off from accounts receivable', 'category': 'adjustment', 'sort_order': 3},
        
        # Payment related
        {'code': 'payment_receipt', 'name': 'Payment Receipt', 'description': 'Receipt of payment from patient', 'category': 'revenue', 'sort_order': 4},
        {'code': 'cash_receipt', 'name': 'Cash Receipt', 'description': 'Cash payment received', 'category': 'asset', 'sort_order': 5},
        {'code': 'refund', 'name': 'Refund', 'description': 'Refund issued to patient', 'category': 'adjustment', 'sort_order': 6},
        
        # Insurance related
        {'code': 'insurance_claim', 'name': 'Insurance Claim', 'description': 'Insurance claim submitted', 'category': 'asset', 'sort_order': 7},
        {'code': 'insurance_payment', 'name': 'Insurance Payment', 'description': 'Payment received from insurance', 'category': 'revenue', 'sort_order': 8},
        {'code': 'insurance_cash_receipt', 'name': 'Insurance Cash Receipt', 'description': 'Cash receipt from insurance payment', 'category': 'asset', 'sort_order': 9},
        
        # Expense related
        {'code': 'expense', 'name': 'Expense', 'description': 'Business expense incurred', 'category': 'expense', 'sort_order': 10},
        {'code': 'expense_payment', 'name': 'Expense Payment', 'description': 'Payment made for expense', 'category': 'asset', 'sort_order': 11},
        
        # Adjustments and corrections
        {'code': 'correction', 'name': 'Correction', 'description': 'Transaction correction', 'category': 'adjustment', 'sort_order': 12},
        {'code': 'reversal', 'name': 'Reversal', 'description': 'Transaction reversal', 'category': 'adjustment', 'sort_order': 13, 'requires_verification': True},
        
        # System transactions
        {'code': 'system_adjustment', 'name': 'System Adjustment', 'description': 'System-generated adjustment', 'category': 'adjustment', 'sort_order': 14, 'is_system': True},
    ]
    
    for type_data in transaction_types:
        transaction_type = TransactionType(**type_data)
        db.session.merge(transaction_type)
    
    print("   ✅ Transaction Types seeded")


def seed_financial_lookups():
    """Seed financial lookup tables"""
    
    # Payment Statuses
    payment_statuses = [
        {'code': 'pending', 'name': 'Pending', 'sort_order': 1, 'is_completed': False, 'allows_refund': False, 'requires_action': False},
        {'code': 'completed', 'name': 'Completed', 'sort_order': 2, 'is_completed': True, 'allows_refund': True, 'requires_action': False},
        {'code': 'failed', 'name': 'Failed', 'sort_order': 3, 'is_completed': False, 'allows_refund': False, 'requires_action': True},
        {'code': 'refunded', 'name': 'Refunded', 'sort_order': 4, 'is_completed': True, 'allows_refund': False, 'requires_action': False},
        {'code': 'partially_refunded', 'name': 'Partially Refunded', 'sort_order': 5, 'is_completed': True, 'allows_refund': True, 'requires_action': False},
        {'code': 'cancelled', 'name': 'Cancelled', 'sort_order': 6, 'is_completed': False, 'allows_refund': False, 'requires_action': False},
    ]
    
    for status_data in payment_statuses:
        status = PaymentStatus(**status_data)
        db.session.merge(status)
    
    # Invoice Statuses
    invoice_statuses = [
        {'code': 'draft', 'name': 'Draft', 'sort_order': 1, 'is_final': False, 'allows_editing': True, 'send_notifications': False},
        {'code': 'sent', 'name': 'Sent', 'sort_order': 2, 'is_final': False, 'allows_editing': True, 'send_notifications': True},
        {'code': 'viewed', 'name': 'Viewed', 'sort_order': 3, 'is_final': False, 'allows_editing': True, 'send_notifications': True},
        {'code': 'partial', 'name': 'Partially Paid', 'sort_order': 4, 'is_final': False, 'allows_editing': True, 'send_notifications': True},
        {'code': 'paid', 'name': 'Paid', 'sort_order': 5, 'is_final': True, 'allows_editing': False, 'send_notifications': True},
        {'code': 'overdue', 'name': 'Overdue', 'sort_order': 6, 'is_final': False, 'allows_editing': True, 'send_notifications': True},
        {'code': 'cancelled', 'name': 'Cancelled', 'sort_order': 7, 'is_final': True, 'allows_editing': False, 'send_notifications': True},
        {'code': 'written_off', 'name': 'Written Off', 'sort_order': 8, 'is_final': True, 'allows_editing': False, 'send_notifications': True},
    ]
    
    for status_data in invoice_statuses:
        status = InvoiceStatus(**status_data)
        db.session.merge(status)
    
    # Payment Methods
    payment_methods = [
        {'code': 'cash', 'name': 'Cash', 'sort_order': 1, 'category': 'cash', 'requires_processing': False, 'processing_fee_percentage': 0.0, 'is_online': False},
        {'code': 'credit_card', 'name': 'Credit Card', 'sort_order': 2, 'category': 'card', 'requires_processing': True, 'processing_fee_percentage': 2.9, 'is_online': True},
        {'code': 'debit_card', 'name': 'Debit Card', 'sort_order': 3, 'category': 'card', 'requires_processing': True, 'processing_fee_percentage': 1.9, 'is_online': True},
        {'code': 'bank_transfer', 'name': 'Bank Transfer', 'sort_order': 4, 'category': 'transfer', 'requires_processing': True, 'processing_fee_percentage': 0.5, 'is_online': True},
        {'code': 'check', 'name': 'Check', 'sort_order': 5, 'category': 'check', 'requires_processing': True, 'processing_fee_percentage': 0.0, 'is_online': False},
        {'code': 'stripe', 'name': 'Stripe', 'sort_order': 6, 'category': 'digital', 'requires_processing': True, 'processing_fee_percentage': 2.9, 'is_online': True},
        {'code': 'paypal', 'name': 'PayPal', 'sort_order': 7, 'category': 'digital', 'requires_processing': True, 'processing_fee_percentage': 2.9, 'is_online': True},
        {'code': 'insurance', 'name': 'Insurance', 'sort_order': 8, 'category': 'insurance', 'requires_processing': True, 'processing_fee_percentage': 0.0, 'is_online': False},
        {'code': 'hsa', 'name': 'Health Savings Account', 'sort_order': 9, 'category': 'insurance', 'requires_processing': True, 'processing_fee_percentage': 0.0, 'is_online': True},
        {'code': 'fsa', 'name': 'Flexible Spending Account', 'sort_order': 10, 'category': 'insurance', 'requires_processing': True, 'processing_fee_percentage': 0.0, 'is_online': True},
    ]
    
    for method_data in payment_methods:
        method = PaymentMethod(**method_data)
        db.session.merge(method)
    
    # Claim Statuses
    claim_statuses = [
        {'code': 'draft', 'name': 'Draft', 'sort_order': 1, 'is_active': True, 'requires_action': False, 'allows_resubmission': True},
        {'code': 'submitted', 'name': 'Submitted', 'sort_order': 2, 'is_active': True, 'requires_action': False, 'allows_resubmission': True},
        {'code': 'processing', 'name': 'Processing', 'sort_order': 3, 'is_active': True, 'requires_action': False, 'allows_resubmission': True},
        {'code': 'approved', 'name': 'Approved', 'sort_order': 4, 'is_active': False, 'requires_action': False, 'allows_resubmission': False},
        {'code': 'partially_approved', 'name': 'Partially Approved', 'sort_order': 5, 'is_active': False, 'requires_action': True, 'allows_resubmission': True},
        {'code': 'denied', 'name': 'Denied', 'sort_order': 6, 'is_active': False, 'requires_action': True, 'allows_resubmission': True},
        {'code': 'paid', 'name': 'Paid', 'sort_order': 7, 'is_active': False, 'requires_action': False, 'allows_resubmission': False},
        {'code': 'appealed', 'name': 'Appealed', 'sort_order': 8, 'is_active': True, 'requires_action': True, 'allows_resubmission': True},
        {'code': 'closed', 'name': 'Closed', 'sort_order': 9, 'is_active': False, 'requires_action': False, 'allows_resubmission': False},
    ]
    
    for status_data in claim_statuses:
        status = ClaimStatus(**status_data)
        db.session.merge(status)
    
    # Expense Categories
    expense_categories = [
        {'code': 'supplies', 'name': 'Medical Supplies', 'sort_order': 1, 'is_tax_deductible': True, 'requires_approval': False, 'budget_category': 'operational'},
        {'code': 'equipment', 'name': 'Equipment', 'sort_order': 2, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'capital'},
        {'code': 'salaries', 'name': 'Salaries', 'sort_order': 3, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'personnel'},
        {'code': 'rent', 'name': 'Rent', 'sort_order': 4, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'utilities', 'name': 'Utilities', 'sort_order': 5, 'is_tax_deductible': True, 'requires_approval': False, 'budget_category': 'operational'},
        {'code': 'insurance', 'name': 'Insurance', 'sort_order': 6, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'marketing', 'name': 'Marketing', 'sort_order': 7, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'professional_fees', 'name': 'Professional Fees', 'sort_order': 8, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'travel', 'name': 'Travel', 'sort_order': 9, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'maintenance', 'name': 'Maintenance', 'sort_order': 10, 'is_tax_deductible': True, 'requires_approval': False, 'budget_category': 'operational'},
        {'code': 'software', 'name': 'Software', 'sort_order': 11, 'is_tax_deductible': True, 'requires_approval': True, 'budget_category': 'operational'},
        {'code': 'other', 'name': 'Other', 'sort_order': 12, 'is_tax_deductible': False, 'requires_approval': True, 'budget_category': 'operational'},
    ]
    
    for category_data in expense_categories:
        category = ExpenseCategory(**category_data)
        db.session.merge(category)
    
    # Currencies
    currencies = [
        {'code': 'USD', 'name': 'US Dollar', 'sort_order': 1, 'symbol': '$', 'decimal_places': 2, 'is_active': True},
        {'code': 'EUR', 'name': 'Euro', 'sort_order': 2, 'symbol': '€', 'decimal_places': 2, 'is_active': True},
        {'code': 'GBP', 'name': 'British Pound', 'sort_order': 3, 'symbol': '£', 'decimal_places': 2, 'is_active': True},
        {'code': 'CAD', 'name': 'Canadian Dollar', 'sort_order': 4, 'symbol': 'C$', 'decimal_places': 2, 'is_active': True},
        {'code': 'AUD', 'name': 'Australian Dollar', 'sort_order': 5, 'symbol': 'A$', 'decimal_places': 2, 'is_active': True},
        {'code': 'JPY', 'name': 'Japanese Yen', 'sort_order': 6, 'symbol': '¥', 'decimal_places': 0, 'is_active': True},
    ]
    
    for currency_data in currencies:
        currency = Currency(**currency_data)
        db.session.merge(currency)
    
    # Transaction Types
    seed_transaction_types()



def seed_inventory_lookups():
    """Seed inventory lookup tables"""
    
    # Product Types
    product_types = [
        {'code': 'consumable', 'name': 'Consumable', 'sort_order': 1, 'category': 'supplies', 'requires_lot_tracking': False, 'requires_expiration': False, 'is_medical': False},
        {'code': 'equipment', 'name': 'Equipment', 'sort_order': 2, 'category': 'equipment', 'requires_lot_tracking': False, 'requires_expiration': False, 'is_medical': True},
        {'code': 'medication', 'name': 'Medication', 'sort_order': 3, 'category': 'medical', 'requires_lot_tracking': True, 'requires_expiration': True, 'is_medical': True},
        {'code': 'supply', 'name': 'Supply', 'sort_order': 4, 'category': 'supplies', 'requires_lot_tracking': False, 'requires_expiration': False, 'is_medical': False},
        {'code': 'dental_material', 'name': 'Dental Material', 'sort_order': 5, 'category': 'medical', 'requires_lot_tracking': True, 'requires_expiration': True, 'is_medical': True},
        {'code': 'lab_supply', 'name': 'Lab Supply', 'sort_order': 6, 'category': 'supplies', 'requires_lot_tracking': False, 'requires_expiration': False, 'is_medical': True},
        {'code': 'office_supply', 'name': 'Office Supply', 'sort_order': 7, 'category': 'supplies', 'requires_lot_tracking': False, 'requires_expiration': False, 'is_medical': False},
    ]
    
    for type_data in product_types:
        product_type = ProductType(**type_data)
        db.session.merge(product_type)
    
    # Inventory Transaction Types
    transaction_types = [
        {'code': 'purchase', 'name': 'Purchase', 'sort_order': 1, 'affects_stock': True, 'stock_direction': 'in', 'requires_approval': False},
        {'code': 'sale', 'name': 'Sale', 'sort_order': 2, 'affects_stock': True, 'stock_direction': 'out', 'requires_approval': False},
        {'code': 'adjustment', 'name': 'Adjustment', 'sort_order': 3, 'affects_stock': True, 'stock_direction': 'neutral', 'requires_approval': True},
        {'code': 'transfer', 'name': 'Transfer', 'sort_order': 4, 'affects_stock': True, 'stock_direction': 'neutral', 'requires_approval': True},
        {'code': 'return', 'name': 'Return', 'sort_order': 5, 'affects_stock': True, 'stock_direction': 'in', 'requires_approval': False},
        {'code': 'damage', 'name': 'Damage', 'sort_order': 6, 'affects_stock': True, 'stock_direction': 'out', 'requires_approval': True},
        {'code': 'expiration', 'name': 'Expiration', 'sort_order': 7, 'affects_stock': True, 'stock_direction': 'out', 'requires_approval': True},
    ]
    
    for type_data in transaction_types:
        transaction_type = InventoryTransactionType(**type_data)
        db.session.merge(transaction_type)
    
    # Purchase Order Statuses
    po_statuses = [
        {'code': 'draft', 'name': 'Draft', 'sort_order': 1, 'allows_editing': True, 'is_final': False, 'send_notifications': False},
        {'code': 'pending', 'name': 'Pending Approval', 'sort_order': 2, 'allows_editing': False, 'is_final': False, 'send_notifications': True},
        {'code': 'approved', 'name': 'Approved', 'sort_order': 3, 'allows_editing': False, 'is_final': False, 'send_notifications': True},
        {'code': 'ordered', 'name': 'Ordered', 'sort_order': 4, 'allows_editing': False, 'is_final': False, 'send_notifications': True},
        {'code': 'received', 'name': 'Received', 'sort_order': 5, 'allows_editing': False, 'is_final': True, 'send_notifications': True},
        {'code': 'partially_received', 'name': 'Partially Received', 'sort_order': 6, 'allows_editing': False, 'is_final': False, 'send_notifications': True},
        {'code': 'cancelled', 'name': 'Cancelled', 'sort_order': 7, 'allows_editing': False, 'is_final': True, 'send_notifications': True},
    ]
    
    for status_data in po_statuses:
        status = PurchaseOrderStatus(**status_data)
        db.session.merge(status)
    
    # Inventory Adjustment Types
    adjustment_types = [
        {'code': 'increase', 'name': 'Stock Increase', 'sort_order': 1, 'stock_impact': 'increase', 'requires_reason': True, 'requires_approval': False},
        {'code': 'decrease', 'name': 'Stock Decrease', 'sort_order': 2, 'stock_impact': 'decrease', 'requires_reason': True, 'requires_approval': True},
        {'code': 'correction', 'name': 'Stock Correction', 'sort_order': 3, 'stock_impact': 'correction', 'requires_reason': True, 'requires_approval': True},
    ]
    
    for type_data in adjustment_types:
        adjustment_type = InventoryAdjustmentType(**type_data)
        db.session.merge(adjustment_type)

# Update the main seed function to call all new seed functions
def seed_lookup_data():
    """Seed all lookup tables with enum data"""
    # Existing clinical lookups
    seed_clinical_lookups() 
    seed_analytics_lookups()
    seed_core_lookups()
    seed_financial_lookups()
    seed_inventory_lookups()
    
    try:
        db.session.commit()
        print("Successfully seeded all lookup tables!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding lookup tables: {e}")
        raise









if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_lookup_data()
