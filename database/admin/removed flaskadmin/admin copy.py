from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_admin.form import rules
from flask_admin.model.template import macro
from flask import redirect, url_for, flash, request, current_app
from flask_login import current_user
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload
import datetime
from markupsafe import Markup
from wtforms import validators, fields, widgets
from wtforms.validators import DataRequired, Email, Length, Optional
from wtforms.fields import SelectField, TextAreaField, DateField, DateTimeField
import json

from app.models import (
    # Core models
    db, User, Organization, Tenant, Role, Permission, Staff, 
    Subscription, UserRole, OrganizationType, TenantStatus, SubscriptionPlan,
    
    # Clinical models
    Patient, Appointment, Treatment, ClinicalNote, Allergy, Prescription,
    VitalSign, LabOrder, MedicalRecord, Procedure, Note, AvailabilitySlot,
    TreatmentRoom, TelehealthSession, TreatmentPlan,
    
    # Financial models
    Invoice, Payment, PaymentRecord, InsurancePlan, InsuranceClaim, Expense,
    FinancialReport,
    
    # Inventory models
    Product, ProductCategory, ProductImage, ProductPriceHistory, Supplier,
    PurchaseOrder, PurchaseOrderItem, InventoryItem, InventoryTransaction,
    InventoryAdjustment,
    
    # Analytics models
    Widget, WidgetTemplate, WidgetConfig, Notification, AuditTrail,
    RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
    Webhook, WebhookEvent, FileRecord, AnalyticsReport,
    
    # Security models
    PasswordHistory, SecurityEvent, LoginAttempt, UserSession,
    TenantInvitation, TenantAuditLog,
    
    # Family models
    FamilyMember, FamilyRelationship,
    
    # Staff models
    StaffAvailability, StaffLeave, UserOAuth
)

# Custom Admin Index View
class DentaloistAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('auth.login'))
        
        # Get basic statistics
        stats = {
            'total_users': User.query.filter_by(is_active=True).count(),
            'total_patients': Patient.query.filter_by(is_active=True).count(),
            'total_appointments': Appointment.query.filter_by(is_active=True).count(),
            'total_organizations': Organization.query.filter_by(is_active=True).count(),
            'total_tenants': Tenant.query.filter_by(is_active=True).count(),
            'recent_appointments': Appointment.query.filter(
                Appointment.start_time >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
            ).count(),
            'pending_payments': Payment.query.filter_by(status='pending').count(),
            'low_stock_items': Product.query.filter(
                Product.current_stock <= Product.reorder_point
            ).count() if hasattr(Product, 'current_stock') else 0
        }
        
        # Recent activity
        recent_activities = AuditTrail.query.order_by(
            AuditTrail.created_at.desc()
        ).limit(10).all()
        
        return self.render('admin/index.html', stats=stats, recent_activities=recent_activities)

# Base Model View with common configurations
class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
    
    page_size = 50
    can_view_details = True
    can_export = True
    create_modal = True
    edit_modal = True
    details_modal = True
    
    column_display_pk = True
    column_hide_backrefs = False
    
    def _format_date(self, context, model, name):
        value = getattr(model, name)
        if value:
            return value.strftime('%Y-%m-%d %H:%M')
        return ''
    
    def _format_json(self, context, model, name):
        value = getattr(model, name)
        if value:
            return Markup(f'<pre>{json.dumps(value, indent=2)}</pre>')
        return ''

# Core System Admin Views
class UserAdminView(BaseModelView):
    column_list = [
        'id', 'email', 'first_name', 'last_name', 'role', 'organization', 
        'tenant', 'is_active', 'last_login', 'created_at'
    ]
    column_searchable_list = ['email', 'first_name', 'last_name']
    column_filters = ['role', 'is_active', 'organization_id', 'tenant_id', 'created_at']
    column_editable_list = ['is_active']
    
    form_columns = [
        'email', 'first_name', 'last_name', 'phone', 'role', 'organization',
        'tenant', 'is_active', 'is_admin', 'settings'
    ]
    
    form_ajax_refs = {
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        },
        'tenant': {
            'fields': ['name', 'subdomain'],
            'page_size': 10
        }
    }
    
    form_args = {
        'email': {
            'validators': [DataRequired(), Email()]
        },
        'first_name': {
            'validators': [DataRequired(), Length(max=50)]
        },
        'last_name': {
            'validators': [DataRequired(), Length(max=50)]
        }
    }
    
    form_widget_args = {
        'settings': {
            'rows': 10
        }
    }
    
    column_formatters = {
        'last_login': BaseModelView._format_date,
        'settings': BaseModelView._format_json
    }
    
    @action('activate', 'Activate', 'Are you sure you want to activate selected users?')
    def action_activate(self, ids):
        try:
            query = User.query.filter(User.id.in_(ids))
            count = 0
            for user in query.all():
                user.is_active = True
                count += 1
            db.session.commit()
            flash(f'{count} users activated successfully.', 'success')
        except Exception as ex:
            flash(f'Error activating users: {str(ex)}', 'error')
    
    @action('deactivate', 'Deactivate', 'Are you sure you want to deactivate selected users?')
    def action_deactivate(self, ids):
        try:
            query = User.query.filter(User.id.in_(ids))
            count = 0
            for user in query.all():
                user.is_active = False
                count += 1
            db.session.commit()
            flash(f'{count} users deactivated successfully.', 'success')
        except Exception as ex:
            flash(f'Error deactivating users: {str(ex)}', 'error')

class OrganizationAdminView(BaseModelView):
    column_list = [
        'public_id', 'name', 'type', 'email', 'phone', 'tenant', 
        'status', 'is_verified', 'created_at'
    ]
    column_searchable_list = ['name', 'email', 'phone']
    column_filters = ['type', 'status', 'is_verified', 'tenant_id']
    column_editable_list = ['status', 'is_verified']
    
    form_columns = [
        'name', 'description', 'type', 'email', 'phone', 'website',
        'address', 'city', 'state', 'postal_code', 'country',
        'max_staff', 'max_patients', 'status', 'is_verified', 'tenant'
    ]
    
    form_ajax_refs = {
        'tenant': {
            'fields': ['name', 'subdomain'],
            'page_size': 10
        }
    }
    
    form_args = {
        'name': {
            'validators': [DataRequired(), Length(max=100)]
        },
        'email': {
            'validators': [Optional(), Email(), Length(max=120)]
        }
    }

class TenantAdminView(BaseModelView):
    column_list = [
        'id', 'name', 'subdomain', 'display_name', 'contact_email', 
        'subscription_plan', 'status', 'max_users', 'user_count',
        'created_at', 'activated_at'
    ]
    column_searchable_list = ['name', 'subdomain', 'display_name', 'contact_email']
    column_filters = ['subscription_plan', 'status', 'industry', 'created_at']
    column_editable_list = ['status', 'subscription_plan']
    
    form_columns = [
        'name', 'subdomain', 'display_name', 'description', 'industry',
        'contact_email', 'contact_phone', 'website', 'address_line1',
        'address_line2', 'city', 'state', 'postal_code', 'country',
        'timezone', 'subscription_plan', 'status', 'max_users',
        'max_patients', 'max_storage_mb', 'features_enabled', 'settings'
    ]
    
    form_args = {
        'name': {
            'validators': [DataRequired(), Length(max=200)]
        },
        'contact_email': {
            'validators': [DataRequired(), Email(), Length(max=120)]
        }
    }
    
    form_widget_args = {
        'features_enabled': {'rows': 5},
        'settings': {'rows': 10}
    }
    
    column_formatters = {
        'features_enabled': BaseModelView._format_json,
        'settings': BaseModelView._format_json
    }
    
    @action('activate', 'Activate', 'Are you sure you want to activate selected tenants?')
    def action_activate(self, ids):
        try:
            query = Tenant.query.filter(Tenant.id.in_(ids))
            count = 0
            for tenant in query.all():
                tenant.status = 'active'
                tenant.activated_at = datetime.datetime.utcnow()
                count += 1
            db.session.commit()
            flash(f'{count} tenants activated successfully.', 'success')
        except Exception as ex:
            flash(f'Error activating tenants: {str(ex)}', 'error')

class RoleAdminView(BaseModelView):
    column_list = [
        'id', 'name', 'description', 'is_system_role', 'is_default',
        'organization', 'users_count', 'created_at'
    ]
    column_searchable_list = ['name', 'description']
    column_filters = ['is_system_role', 'is_default', 'organization_id']
    
    form_columns = [
        'name', 'description', 'is_system_role', 'is_default',
        'organization', 'permissions'
    ]
    
    form_ajax_refs = {
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        },
        'permissions': {
            'fields': ['name', 'description'],
            'page_size': 10
        }
    }
    
    @property
    def users_count(self):
        return len(self.users)

class PermissionAdminView(BaseModelView):
    column_list = ['id', 'name', 'description', 'category', 'roles_count']
    column_searchable_list = ['name', 'description', 'category']
    column_filters = ['category']
    
    form_columns = ['name', 'description', 'category', 'roles']
    
    form_ajax_refs = {
        'roles': {
            'fields': ['name', 'description'],
            'page_size': 10
        }
    }
    
    @property
    def roles_count(self):
        return len(self.roles)

# Clinical Models Admin Views
class PatientAdminView(BaseModelView):
    column_list = [
        'id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
        'gender', 'organization', 'status', 'last_dental_visit', 'created_at'
    ]
    column_searchable_list = ['first_name', 'last_name', 'email', 'phone']
    column_filters = ['gender', 'status', 'organization_id', 'created_at']
    
    form_columns = [
        'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender',
        'address', 'emergency_contact', 'medical_history', 'allergies',
        'medications', 'insurance_info', 'dental_history', 'oral_hygiene',
        'last_dental_visit', 'next_recall_date', 'status', 'organization'
    ]
    
    form_ajax_refs = {
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'medical_history': {'rows': 5},
        'allergies': {'rows': 3},
        'medications': {'rows': 3},
        'insurance_info': {'rows': 3},
        'dental_history': {'rows': 5}
    }
    
    column_formatters = {
        'medical_history': BaseModelView._format_json,
        'allergies': BaseModelView._format_json,
        'medications': BaseModelView._format_json,
        'insurance_info': BaseModelView._format_json,
        'dental_history': BaseModelView._format_json
    }

class AppointmentAdminView(BaseModelView):
    column_list = [
        'id', 'title', 'patient', 'dentist', 'start_time', 'end_time',
        'type', 'status', 'organization', 'treatment_room', 'created_at'
    ]
    column_searchable_list = ['title', 'patient.first_name', 'patient.last_name']
    column_filters = ['type', 'status', 'organization_id', 'start_time']
    
    form_columns = [
        'title', 'description', 'patient', 'dentist', 'staff', 'treatment',
        'start_time', 'end_time', 'type', 'status', 'priority',
        'treatment_room', 'location', 'chief_complaint', 'treatment_notes',
        'estimated_cost', 'organization'
    ]
    
    form_ajax_refs = {
        'patient': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'dentist': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'description': {'rows': 3},
        'chief_complaint': {'rows': 3},
        'treatment_notes': {'rows': 5}
    }
    
    column_formatters = {
        'start_time': BaseModelView._format_date,
        'end_time': BaseModelView._format_date
    }

class TreatmentAdminView(BaseModelView):
    column_list = [
        'id', 'name', 'patient', 'dentist', 'type', 'status', 'priority',
        'scheduled_date', 'cost_estimate', 'created_at'
    ]
    column_searchable_list = ['name', 'patient.first_name', 'patient.last_name']
    column_filters = ['type', 'status', 'priority', 'tenant_id']
    
    form_columns = [
        'name', 'description', 'patient', 'dentist', 'assistant', 'tenant',
        'type', 'procedure_code', 'diagnosis_codes', 'status', 'priority',
        'scheduled_date', 'estimated_duration', 'tooth_numbers', 'surfaces',
        'anesthesia_used', 'complications', 'post_treatment_instructions',
        'cost_estimate', 'actual_cost'
    ]
    
    form_ajax_refs = {
        'patient': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'dentist': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'tenant': {
            'fields': ['name', 'subdomain'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'description': {'rows': 3},
        'post_treatment_instructions': {'rows': 3},
        'complications': {'rows': 3}
    }
    
    column_formatters = {
        'scheduled_date': BaseModelView._format_date,
        'diagnosis_codes': BaseModelView._format_json,
        'tooth_numbers': BaseModelView._format_json,
        'surfaces': BaseModelView._format_json,
        'anesthesia_used': BaseModelView._format_json
    }

# Financial Models Admin Views
class InvoiceAdminView(BaseModelView):
    column_list = [
        'id', 'invoice_number', 'patient', 'organization', 'invoice_date',
        'due_date', 'status', 'total_amount', 'balance_due', 'created_at'
    ]
    column_searchable_list = ['invoice_number', 'patient.first_name', 'patient.last_name']
    column_filters = ['status', 'organization_id', 'invoice_date']
    
    form_columns = [
        'invoice_number', 'patient', 'organization', 'treatment', 'appointment',
        'invoice_date', 'due_date', 'status', 'items', 'subtotal', 'tax_amount',
        'discount_amount', 'total_amount', 'amount_paid', 'balance_due',
        'currency', 'payment_instructions', 'notes'
    ]
    
    form_ajax_refs = {
        'patient': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'items': {'rows': 10},
        'payment_instructions': {'rows': 3},
        'notes': {'rows': 3}
    }
    
    column_formatters = {
        'invoice_date': BaseModelView._format_date,
        'due_date': BaseModelView._format_date,
        'items': BaseModelView._format_json
    }

class PaymentAdminView(BaseModelView):
    column_list = [
        'id', 'patient', 'invoice', 'amount', 'payment_method', 'status',
        'payment_date', 'reference_number', 'created_at'
    ]
    column_searchable_list = ['reference_number', 'patient.first_name', 'patient.last_name']
    column_filters = ['payment_method', 'status', 'payment_date']
    
    form_columns = [
        'patient', 'invoice', 'amount', 'payment_method', 'currency',
        'status', 'payment_date', 'reference_number', 'transaction_id',
        'fee_amount', 'net_amount', 'notes'
    ]
    
    form_ajax_refs = {
        'patient': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'invoice': {
            'fields': ['invoice_number'],
            'page_size': 10
        }
    }

class InsurancePlanAdminView(BaseModelView):
    column_list = [
        'id', 'insurance_provider', 'plan_name', 'policy_number', 'patient',
        'coverage_type', 'effective_date', 'is_primary', 'is_active',
        'verification_status', 'created_at'
    ]
    column_searchable_list = ['insurance_provider', 'plan_name', 'policy_number']
    column_filters = ['coverage_type', 'is_primary', 'is_active', 'verification_status']
    
    form_columns = [
        'insurance_provider', 'plan_name', 'policy_number', 'group_number',
        'subscriber_name', 'subscriber_dob', 'subscriber_relationship',
        'coverage_type', 'effective_date', 'expiration_date', 'is_primary',
        'is_active', 'verification_status', 'benefits', 'copay_info',
        'deductible_info', 'annual_maximum', 'patient', 'organization'
    ]
    
    form_ajax_refs = {
        'patient': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'benefits': {'rows': 8},
        'copay_info': {'rows': 5},
        'deductible_info': {'rows': 5}
    }
    
    column_formatters = {
        'effective_date': lambda v, c, m, p: m.effective_date.strftime('%Y-%m-%d') if m.effective_date else '',
        'benefits': BaseModelView._format_json,
        'copay_info': BaseModelView._format_json,
        'deductible_info': BaseModelView._format_json
    }

# Inventory Models Admin Views
class ProductAdminView(BaseModelView):
    column_list = [
        'id', 'sku', 'name', 'product_type', 'brand', 'current_stock',
        'cost_price', 'selling_price', 'status', 'organization', 'created_at'
    ]
    column_searchable_list = ['sku', 'name', 'brand', 'description']
    column_filters = ['product_type', 'status', 'organization_id', 'is_medical']
    
    form_columns = [
        'sku', 'name', 'description', 'brand', 'model', 'product_type',
        'unit_of_measure', 'unit_size', 'cost_price', 'selling_price',
        'current_price', 'min_stock_level', 'max_stock_level', 'reorder_point',
        'current_stock', 'is_medical', 'requires_prescription', 'barcode',
        'status', 'organization', 'supplier', 'category'
    ]
    
    form_ajax_refs = {
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        },
        'supplier': {
            'fields': ['name', 'contact_email'],
            'page_size': 10
        },
        'category': {
            'fields': ['name'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'description': {'rows': 3}
    }

class InventoryTransactionAdminView(BaseModelView):
    column_list = [
        'id', 'product', 'transaction_type', 'quantity', 'old_stock_level',
        'new_stock_level', 'unit_cost', 'total_cost', 'performed_by',
        'created_at'
    ]
    column_filters = ['transaction_type', 'created_at']
    
    form_columns = [
        'product', 'transaction_type', 'quantity', 'old_stock_level',
        'new_stock_level', 'unit_cost', 'total_cost', 'reference_type',
        'reference_id', 'notes', 'performed_by'
    ]
    
    form_ajax_refs = {
        'product': {
            'fields': ['sku', 'name'],
            'page_size': 10
        },
        'performed_by': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        }
    }

# Analytics Models Admin Views
class NotificationAdminView(BaseModelView):
    column_list = [
        'id', 'user', 'type', 'title', 'is_read', 'is_archived', 'priority',
        'created_at'
    ]
    column_searchable_list = ['title', 'message']
    column_filters = ['type', 'is_read', 'is_archived', 'priority']
    
    form_columns = [
        'user', 'type', 'title', 'message', 'is_read', 'is_archived',
        'priority', 'action_url', 'action_text', 'source_entity',
        'source_id', 'expires_at'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'message': {'rows': 3}
    }
    
    @action('mark_read', 'Mark as Read', 'Are you sure you want to mark selected notifications as read?')
    def action_mark_read(self, ids):
        try:
            query = Notification.query.filter(Notification.id.in_(ids))
            count = 0
            for notification in query.all():
                notification.is_read = True
                count += 1
            db.session.commit()
            flash(f'{count} notifications marked as read.', 'success')
        except Exception as ex:
            flash(f'Error marking notifications as read: {str(ex)}', 'error')

class AuditTrailAdminView(BaseModelView):
    column_list = [
        'id', 'user', 'action', 'entity', 'entity_id', 'ip_address',
        'created_at'
    ]
    column_searchable_list = ['action', 'entity', 'description']
    column_filters = ['action', 'entity', 'created_at']
    
    form_columns = [
        'user', 'action', 'entity', 'entity_id', 'old_values', 'new_values',
        'changes', 'description', 'ip_address', 'user_agent',
        'organization', 'tenant'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'old_values': {'rows': 5},
        'new_values': {'rows': 5},
        'changes': {'rows': 5},
        'description': {'rows': 3},
        'user_agent': {'rows': 2}
    }
    
    can_create = False
    can_edit = False
    can_delete = False
    
    column_formatters = {
        'old_values': BaseModelView._format_json,
        'new_values': BaseModelView._format_json,
        'changes': BaseModelView._format_json
    }

# Security Models Admin Views
class SecurityEventAdminView(BaseModelView):
    column_list = [
        'id', 'user', 'event_type', 'description', 'ip_address', 'created_at'
    ]
    column_filters = ['event_type', 'created_at']
    
    form_columns = [
        'user', 'event_type', 'description', 'ip_address', 'user_agent'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        }
    }
    
    form_widget_args = {
        'description': {'rows': 3},
        'user_agent': {'rows': 2}
    }
    
    can_create = False
    can_edit = False

class LoginAttemptAdminView(BaseModelView):
    column_list = [
        'id', 'user', 'username', 'ip_address', 'success', 'attempt_type',
        'failure_reason', 'created_at'
    ]
    column_searchable_list = ['username', 'ip_address']
    column_filters = ['success', 'attempt_type', 'created_at']
    
    form_columns = [
        'user', 'username', 'ip_address', 'user_agent', 'success',
        'attempt_type', 'failure_reason'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        }
    }
    
    can_create = False
    can_edit = False

# Staff Models Admin Views
class StaffAdminView(BaseModelView):
    column_list = [
        'id', 'staff_number', 'user', 'job_title', 'department', 
        'employment_type', 'status', 'hire_date', 'organization'
    ]
    column_searchable_list = ['staff_number', 'job_title', 'user.first_name', 'user.last_name']
    column_filters = ['department', 'employment_type', 'status', 'organization_id']
    
    form_columns = [
        'staff_number', 'user', 'job_title', 'department', 'specialization',
        'license_number', 'license_expiry', 'hire_date', 'termination_date',
        'employment_type', 'status', 'work_email', 'work_phone',
        'emergency_contact_name', 'emergency_contact_phone', 'organization'
    ]
    
    form_ajax_refs = {
        'user': {
            'fields': ['first_name', 'last_name', 'email'],
            'page_size': 10
        },
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }

# Subscription Admin View
class SubscriptionAdminView(BaseModelView):
    column_list = [
        'id', 'organization', 'plan', 'price', 'start_date', 'end_date',
        'is_active', 'created_at'
    ]
    column_filters = ['plan', 'is_active', 'start_date']
    
    form_columns = [
        'organization', 'plan', 'price', 'start_date', 'end_date', 'is_active',
        'stripe_subscription_id'
    ]
    
    form_ajax_refs = {
        'organization': {
            'fields': ['name', 'public_id'],
            'page_size': 10
        }
    }

# Initialize Flask-Admin
def init_admin(app):
    admin = Admin(
        app,
        name='Dentaloist Admin',
        template_mode='bootstrap4',
        index_view=DentaloistAdminIndexView()
    )
    
    # Core System Views
    admin.add_view(UserAdminView(User, db.session, name='Users', category='System'))
    admin.add_view(OrganizationAdminView(Organization, db.session, name='Organizations', category='System'))
    admin.add_view(TenantAdminView(Tenant, db.session, name='Tenants', category='System'))
    admin.add_view(RoleAdminView(Role, db.session, name='Roles', category='System'))
    admin.add_view(PermissionAdminView(Permission, db.session, name='Permissions', category='System'))
    admin.add_view(StaffAdminView(Staff, db.session, name='Staff', category='System'))
    admin.add_view(SubscriptionAdminView(Subscription, db.session, name='Subscriptions', category='System'))
    
    # Clinical Views
    admin.add_view(PatientAdminView(Patient, db.session, name='Patients', category='Clinical'))
    admin.add_view(AppointmentAdminView(Appointment, db.session, name='Appointments', category='Clinical'))
    admin.add_view(TreatmentAdminView(Treatment, db.session, name='Treatments', category='Clinical'))
    admin.add_view(ClinicalNoteAdminView(ClinicalNote, db.session, name='Clinical Notes', category='Clinical'))
    admin.add_view(AllergyAdminView(Allergy, db.session, name='Allergies', category='Clinical'))
    admin.add_view(PrescriptionAdminView(Prescription, db.session, name='Prescriptions', category='Clinical'))
    admin.add_view(VitalSignAdminView(VitalSign, db.session, name='Vital Signs', category='Clinical'))
    admin.add_view(TreatmentPlanAdminView(TreatmentPlan, db.session, name='Treatment Plans', category='Clinical'))
    admin.add_view(AvailabilitySlotAdminView(AvailabilitySlot, db.session, name='Availability Slots', category='Clinical'))
    
    # Financial Views
    admin.add_view(InvoiceAdminView(Invoice, db.session, name='Invoices', category='Financial'))
    admin.add_view(PaymentAdminView(Payment, db.session, name='Payments', category='Financial'))
    admin.add_view(InsurancePlanAdminView(InsurancePlan, db.session, name='Insurance Plans', category='Financial'))
    admin.add_view(InsuranceClaimAdminView(InsuranceClaim, db.session, name='Insurance Claims', category='Financial'))
    admin.add_view(ExpenseAdminView(Expense, db.session, name='Expenses', category='Financial'))
    admin.add_view(FinancialReportAdminView(FinancialReport, db.session, name='Financial Reports', category='Financial'))
    
    # Inventory Views
    admin.add_view(ProductAdminView(Product, db.session, name='Products', category='Inventory'))
    admin.add_view(ProductCategoryAdminView(ProductCategory, db.session, name='Product Categories', category='Inventory'))
    admin.add_view(SupplierAdminView(Supplier, db.session, name='Suppliers', category='Inventory'))
    admin.add_view(PurchaseOrderAdminView(PurchaseOrder, db.session, name='Purchase Orders', category='Inventory'))
    admin.add_view(InventoryTransactionAdminView(InventoryTransaction, db.session, name='Inventory Transactions', category='Inventory'))
    
    # Analytics Views
    admin.add_view(NotificationAdminView(Notification, db.session, name='Notifications', category='Analytics'))
    admin.add_view(AuditTrailAdminView(AuditTrail, db.session, name='Audit Trail', category='Analytics'))
    admin.add_view(WidgetAdminView(Widget, db.session, name='Widgets', category='Analytics'))
    admin.add_view(AnalyticsReportAdminView(AnalyticsReport, db.session, name='Analytics Reports', category='Analytics'))
    
    # Security Views
    admin.add_view(SecurityEventAdminView(SecurityEvent, db.session, name='Security Events', category='Security'))
    admin.add_view(LoginAttemptAdminView(LoginAttempt, db.session, name='Login Attempts', category='Security'))
    admin.add_view(PasswordHistoryAdminView(PasswordHistory, db.session, name='Password History', category='Security'))
    
    # Family Views
    admin.add_view(FamilyMemberAdminView(FamilyMember, db.session, name='Family Members', category='Family'))
    
    return admin

# Additional specialized views for remaining models
class ClinicalNoteAdminView(BaseModelView):
    column_list = ['id', 'treatment', 'author', 'note_type', 'created_at']
    column_filters = ['note_type', 'created_at']
    
    form_columns = ['treatment', 'author', 'note_type', 'content', 'subjective', 'objective', 'assessment', 'plan']
    
    form_widget_args = {
        'content': {'rows': 6},
        'subjective': {'rows': 3},
        'objective': {'rows': 3},
        'assessment': {'rows': 3},
        'plan': {'rows': 3}
    }

class AllergyAdminView(BaseModelView):
    column_list = ['id', 'patient', 'allergen', 'reaction', 'severity', 'is_active']
    column_filters = ['severity', 'is_active']
    
    form_columns = ['patient', 'allergen', 'reaction', 'severity', 'onset_date', 'is_active', 'notes']

class PrescriptionAdminView(BaseModelView):
    column_list = ['id', 'patient', 'medication_name', 'dosage', 'frequency', 'is_active']
    column_filters = ['is_active', 'route']
    
    form_columns = [
        'patient', 'treatment', 'medication_name', 'dosage', 'frequency', 'route',
        'quantity', 'refills', 'start_date', 'end_date', 'is_active', 'instructions'
    ]

class VitalSignAdminView(BaseModelView):
    column_list = ['id', 'patient', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'heart_rate', 'record_date']
    
    form_columns = [
        'patient', 'blood_pressure_systolic', 'blood_pressure_diastolic',
        'heart_rate', 'respiratory_rate', 'temperature', 'oxygen_saturation',
        'height', 'weight', 'bmi', 'position', 'notes'
    ]

class TreatmentPlanAdminView(BaseModelView):
    column_list = ['id', 'patient', 'diagnosis', 'status', 'created_at']
    
    form_columns = ['patient', 'diagnosis', 'procedures', 'medications', 'status', 'notes']
    
    form_widget_args = {
        'diagnosis': {'rows': 3},
        'procedures': {'rows': 5},
        'medications': {'rows': 3},
        'notes': {'rows': 3}
    }
    
    column_formatters = {
        'procedures': BaseModelView._format_json,
        'medications': BaseModelView._format_json
    }

class AvailabilitySlotAdminView(BaseModelView):
    column_list = ['id', 'staff', 'date', 'start_time', 'end_time', 'status', 'max_patients']
    column_filters = ['status', 'date']
    
    form_columns = [
        'staff', 'organization', 'date', 'start_time', 'end_time', 'slot_type',
        'status', 'max_patients', 'is_bookable', 'is_online'
    ]

class InsuranceClaimAdminView(BaseModelView):
    column_list = ['id', 'patient', 'insurance_plan', 'claim_number', 'status', 'claim_amount', 'submission_date']
    
    form_columns = [
        'patient', 'insurance_plan', 'invoice', 'treatment', 'claim_number',
        'claim_amount', 'status', 'procedures', 'diagnosis_codes', 'denial_reason'
    ]
    
    form_widget_args = {
        'procedures': {'rows': 5},
        'diagnosis_codes': {'rows': 3},
        'denial_reason': {'rows': 3}
    }
    
    column_formatters = {
        'procedures': BaseModelView._format_json,
        'diagnosis_codes': BaseModelView._format_json
    }

class ExpenseAdminView(BaseModelView):
    column_list = ['id', 'organization', 'amount', 'category', 'expense_date', 'status']
    column_filters = ['category', 'status', 'expense_date']
    
    form_columns = [
        'organization', 'amount', 'category', 'description', 'expense_date',
        'vendor_name', 'payment_method', 'status', 'is_tax_deductible'
    ]

class FinancialReportAdminView(BaseModelView):
    column_list = ['id', 'organization', 'title', 'report_type', 'generated_at']
    column_filters = ['report_type']
    
    form_columns = [
        'organization', 'title', 'description', 'report_type', 'parameters',
        'data', 'summary', 'period_start', 'period_end', 'is_template'
    ]
    
    form_widget_args = {
        'parameters': {'rows': 5},
        'data': {'rows': 8},
        'summary': {'rows': 5}
    }
    
    column_formatters = {
        'parameters': BaseModelView._format_json,
        'data': BaseModelView._format_json,
        'summary': BaseModelView._format_json
    }

class ProductCategoryAdminView(BaseModelView):
    column_list = ['id', 'name', 'organization', 'parent_category', 'products_count']
    
    form_columns = ['name', 'description', 'organization', 'parent_category']
    
    @property
    def products_count(self):
        return len(self.products)

class SupplierAdminView(BaseModelView):
    column_list = ['id', 'name', 'contact_email', 'contact_phone', 'is_preferred', 'is_active']
    column_filters = ['is_preferred', 'is_active']
    
    form_columns = [
        'name', 'contact_name', 'contact_email', 'contact_phone', 'address',
        'city', 'state', 'postal_code', 'payment_terms', 'is_preferred',
        'is_active', 'organization'
    ]

class PurchaseOrderAdminView(BaseModelView):
    column_list = ['id', 'po_number', 'supplier', 'status', 'total_amount', 'order_date']
    column_filters = ['status', 'order_date']
    
    form_columns = [
        'supplier', 'organization', 'po_number', 'order_date', 'status',
        'expected_delivery_date', 'tracking_number', 'notes'
    ]

class WidgetAdminView(BaseModelView):
    column_list = ['id', 'title', 'type', 'user', 'organization', 'is_visible']
    
    form_columns = [
        'user', 'organization', 'type', 'title', 'description', 'config',
        'data_source', 'is_visible', 'requires_permission'
    ]
    
    form_widget_args = {
        'config': {'rows': 6},
        'data_source': {'rows': 4}
    }
    
    column_formatters = {
        'config': BaseModelView._format_json,
        'data_source': BaseModelView._format_json
    }

class PasswordHistoryAdminView(BaseModelView):
    column_list = ['id', 'user', 'created_at']
    
    form_columns = ['user', 'password_hash']
    
    can_create = False
    can_edit = False

class FamilyMemberAdminView(BaseModelView):
    column_list = ['id', 'user', 'first_name', 'last_name', 'relationship_type', 'emergency_contact']
    column_filters = ['relationship_type', 'emergency_contact']
    
    form_columns = [
        'user', 'organization', 'first_name', 'last_name', 'relationship_type',
        'emergency_contact', 'primary_contact'
    ]

# Export the admin initialization function
__all__ = ['init_admin']

# getitem