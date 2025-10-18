from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, flash, request, current_app
from flask_login import current_user
import datetime
from markupsafe import Markup
import json
import traceback
import logging
from app.models import db

# Import all models safely
try:
    from app.models import (
        User, Organization, Tenant, Role, Permission, Staff, Subscription,
        Patient, Appointment, Treatment, ClinicalNote, Allergy, Prescription,
        VitalSign, TreatmentPlan, Invoice, Payment, InsurancePlan, InsuranceClaim,
        Expense, FinancialReport, Product, ProductCategory, Supplier,
        PurchaseOrder, InventoryTransaction, Notification, AuditTrail,
        SecurityEvent, LoginAttempt, PasswordHistory, FamilyMember,
        AvailabilitySlot, FamilyRelationship, StaffAvailability, StaffLeave,
        UserOAuth, TenantInvitation, TenantAuditLog, UserSession,
        ProductImage, ProductPriceHistory, PurchaseOrderItem, InventoryItem,
        InventoryAdjustment, Widget, WidgetTemplate, WidgetConfig, RateLimiter,
        RateLimit, EmailLog, Integration, IntegrationLog, Webhook, WebhookEvent,
        FileRecord, AnalyticsReport, LabOrder, MedicalRecord, Procedure, Note,
        TreatmentRoom, TelehealthSession
    )
    MODELS_IMPORTED = True
except ImportError as e:
    print(f"⚠️ Error importing models: {e}")
    MODELS_IMPORTED = False
    # Define fallback empty lists
    all_models = []

# Custom Admin Index View with robust route handling
class DentaloistAdminIndexView(AdminIndexView):
    
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)
    
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return self.redirect_to_login()
        else:
            flash('Admin access required.', 'error')
            return redirect(self.get_main_index())
    
    def redirect_to_login(self):
        """Smart redirect to login page"""
        print("🔍 Admin redirecting to login...")
        
        # Your blueprint creates endpoints under 'auth.' namespace
        login_options = [
            ('auth.admin_direct_login', '/api/auth/admin-direct-login'),
            ('auth.login_form', '/api/auth/login-form'),
            ('auth.login', '/api/auth/login'),
        ]
        
        for endpoint, path in login_options:
            try:
                url = url_for(endpoint, next=request.url)
                print(f"🎯 Redirecting to: {endpoint} -> {url}")
                return redirect(url)
            except Exception as e:
                print(f"❌ {endpoint} failed: {e}")
                continue
        
        # Final fallback
        fallback_url = f"/api/auth/admin-direct-login?next={request.url}"
        print(f"🔄 Using fallback: {fallback_url}")
        return redirect(fallback_url)
    
    def get_main_index(self):
        """Get the main index page URL"""
        try:
            return url_for('main.index')
        except:
            return '/'
    
    @expose('/')
    def index(self):
        """Render the admin index page with stats"""
        if not current_user.is_authenticated:
            return self.redirect_to_login()
        
        if not getattr(current_user, 'is_admin', False):
            flash('Admin access required.', 'error')
            return redirect(self.get_main_index())
        
        stats = {}
        try:
            from app.models import User, Patient, Appointment, Organization
            stats = {
                'total_users': User.query.filter_by(is_active=True).count(),
                'total_patients': Patient.query.filter_by(is_active=True).count(),
                'total_appointments': Appointment.query.filter_by(is_active=True).count(),
                'total_organizations': Organization.query.filter_by(is_active=True).count(),
                'now': datetime.datetime.now()
            }
        except Exception as e:
            print(f"⚠️ Error loading admin stats: {e}")
            # Provide default stats
            stats = {
                'total_users': 0,
                'total_patients': 0,
                'total_appointments': 0,
                'total_organizations': 0,
                'now': datetime.datetime.now()
            }
        
        # Use Flask-Admin's built-in template rendering
        return self.render('admin/index.html', stats=stats)

# Base Model View with same route handling
class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)
    
    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            view = DentaloistAdminIndexView()
            return view.redirect_to_login()
        else:
            flash('Admin access required.', 'error')
            view = DentaloistAdminIndexView()
            return redirect(view.get_main_index())
    
    page_size = 50
    can_view_details = True
    can_export = True
    
    def _format_date(self, context, model, name):
        value = getattr(model, name)
        if value:
            return value.strftime('%Y-%m-%d %H:%M')
        return ''
    
    def _format_json(self, context, model, name):
        value = getattr(model, name)
        if value:
            try:
                return Markup(f'<pre>{json.dumps(value, indent=2)}</pre>')
            except:
                return str(value)
        return ''

# Safe model view creator
def create_model_view(model_class, name=None, category=None, **kwargs):
    """Safely create a ModelView for a given model class"""
    if not MODELS_IMPORTED:
        return None
        
    try:
        class DynamicModelView(BaseModelView):
            pass
        
        if name:
            DynamicModelView.__name__ = f"{name}AdminView"
        
        # Configure basic column list
        try:
            from sqlalchemy import inspect
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns][:8]  # First 8 columns
            DynamicModelView.column_list = columns
        except:
            pass
            
        return DynamicModelView(model_class, db.session, name=name, category=category, **kwargs)
    except Exception as e:
        print(f"⚠️ Failed to create admin view for {model_class.__name__}: {e}")
        return None


# Initialize Flask-Admin with error handling
def init_admin(app):
    try:
        admin = Admin(
            app,
            name='Dentaloist Admin',
            template_mode='bootstrap4',
            index_view=DentaloistAdminIndexView(),
            url='/admin',
            # base_template='my_admin_base.html'  # Use our custom base template
            # base_template='my_master.html'  # This should be in app/templates/, not app/templates/admin/
        )
        
        if not MODELS_IMPORTED:
            print("⚠️ Models not imported, admin will be empty")
            return admin
        
        # Core System Views
        core_models = [
            (User, 'Users', 'System'),
            (Organization, 'Organizations', 'System'),
            (Tenant, 'Tenants', 'System'),
            (Role, 'Roles', 'System'),
            (Staff, 'Staff', 'System'),
            (Subscription, 'Subscriptions', 'System'),
        ]
        
        # Clinical Models
        clinical_models = [
            (Patient, 'Patients', 'Clinical'),
            (Appointment, 'Appointments', 'Clinical'),
            (Treatment, 'Treatments', 'Clinical'),
            (TreatmentPlan, 'Treatment Plans', 'Clinical'),
            (ClinicalNote, 'Clinical Notes', 'Clinical'),
            (Allergy, 'Allergies', 'Clinical'),
            (Prescription, 'Prescriptions', 'Clinical'),
            (VitalSign, 'Vital Signs', 'Clinical'),
        ]
        
        # Financial Models
        financial_models = [
            (Invoice, 'Invoices', 'Financial'),
            (Payment, 'Payments', 'Financial'),
            (InsurancePlan, 'Insurance Plans', 'Financial'),
            (InsuranceClaim, 'Insurance Claims', 'Financial'),
            (Expense, 'Expenses', 'Financial'),
            (FinancialReport, 'Financial Reports', 'Financial'),
        ]
        
        # Inventory Models
        inventory_models = [
            (Product, 'Products', 'Inventory'),
            (ProductCategory, 'Product Categories', 'Inventory'),
            (Supplier, 'Suppliers', 'Inventory'),
            (PurchaseOrder, 'Purchase Orders', 'Inventory'),
            (InventoryTransaction, 'Inventory Transactions', 'Inventory'),
        ]
        
        # Analytics & Security
        other_models = [
            (Notification, 'Notifications', 'Analytics'),
            (AuditTrail, 'Audit Trail', 'Analytics'),
            (SecurityEvent, 'Security Events', 'Security'),
            (LoginAttempt, 'Login Attempts', 'Security'),
            (FamilyMember, 'Family Members', 'Family'),
        ]
        
        # Add all models safely
        all_model_groups = [core_models, clinical_models, financial_models, inventory_models, other_models]
        
        successful_views = 0
        for model_group in all_model_groups:
            for model, name, category in model_group:
                try:
                    view = create_model_view(model, name, category)
                    if view:
                        admin.add_view(view)
                        successful_views += 1
                        print(f"✅ Added admin view for {name}")
                except Exception as e:
                    print(f"❌ Failed to add admin view for {name}: {e}")
                    continue
        
        print(f"✅ Admin interface initialized with {successful_views} views")
        return admin
        
    except Exception as e:
        print(f"❌ Critical error initializing admin: {e}")
        traceback.print_exc()
        # Return a basic admin instance without views
        return Admin(app, name='Dentaloist Admin', template_mode='bootstrap4')


