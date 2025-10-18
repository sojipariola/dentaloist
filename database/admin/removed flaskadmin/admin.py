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

# Custom Admin Index View
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
        login_options = [
            ('auth.admin_direct_login', '/api/auth/admin-direct-login'),
            ('auth.login_form', '/api/auth/login-form'),
            ('auth.login', '/api/auth/login'),
        ]
        
        for endpoint, path in login_options:
            try:
                url = url_for(endpoint, next=request.url)
                return redirect(url)
            except:
                continue
        
        return redirect(f"/api/auth/admin-direct-login?next={request.url}")
    
    def get_main_index(self):
        try:
            return url_for('main.index')
        except:
            return '/'
    
    @expose('/')
    def index(self):
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
            stats = {
                'total_users': 0,
                'total_patients': 0,
                'total_appointments': 0,
                'total_organizations': 0,
                'now': datetime.datetime.now()
            }
        
        return self.render('admin/index.html', stats=stats)

# Base Model View with proper template configuration
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
    
    # Ensure proper template configuration
    page_size = 50
    can_view_details = True
    can_export = True
    can_create = True
    can_edit = True
    can_delete = True
    
    # Use Flask-Admin's default templates
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    details_template = 'admin/model/details.html'

# Safe model view creator
def create_model_view(model_class, name=None, category=None, **kwargs):
    """Safely create a ModelView for a given model class"""
    try:
        class DynamicModelView(BaseModelView):
            pass
        
        if name:
            DynamicModelView.__name__ = f"{name}AdminView"
        
        # Configure column list safely
        try:
            from sqlalchemy import inspect
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns][:8]
            DynamicModelView.column_list = columns
            
            # Add ID column for better navigation
            if 'id' in columns:
                DynamicModelView.column_list = ['id'] + [col for col in columns if col != 'id']
                
        except Exception as e:
            print(f"⚠️ Could not inspect columns for {model_class.__name__}: {e}")
            # Use default column list
            pass
            
        return DynamicModelView(model_class, db.session, name=name, category=category, **kwargs)
    except Exception as e:
        print(f"⚠️ Failed to create admin view for {model_class.__name__}: {e}")
        return None

# Initialize Flask-Admin
def init_admin(app):
    try:
        # Initialize admin with proper configuration
        admin = Admin(
            app,
            name='Dentaloist Admin',
            template_mode='bootstrap4',  # Use bootstrap4 template mode
            index_view=DentaloistAdminIndexView(),
            url='/admin',
            endpoint='admin'  # Explicit endpoint
        )
        
        # Import models safely
        try:
            from app.models import (
                User, Organization, Tenant, Role, Staff, Subscription,
                Patient, Appointment, Treatment, ClinicalNote, Allergy, 
                Prescription, VitalSign, TreatmentPlan, Invoice, Payment,
                InsurancePlan, InsuranceClaim, Expense, FinancialReport,
                Product, ProductCategory, Supplier, PurchaseOrder, 
                InventoryTransaction, Notification, AuditTrail,
                SecurityEvent, LoginAttempt, FamilyMember
            )
            
            # Define model groups
            model_groups = [
                # System
                [(User, 'Users', 'System'),
                 (Organization, 'Organizations', 'System'),
                 (Tenant, 'Tenants', 'System'),
                 (Role, 'Roles', 'System'),
                 (Staff, 'Staff', 'System'),
                 (Subscription, 'Subscriptions', 'System')],
                
                # Clinical
                [(Patient, 'Patients', 'Clinical'),
                 (Appointment, 'Appointments', 'Clinical'),
                 (Treatment, 'Treatments', 'Clinical'),
                 (TreatmentPlan, 'Treatment Plans', 'Clinical'),
                 (ClinicalNote, 'Clinical Notes', 'Clinical'),
                 (Allergy, 'Allergies', 'Clinical'),
                 (Prescription, 'Prescriptions', 'Clinical'),
                 (VitalSign, 'Vital Signs', 'Clinical')],
                
                # Financial
                [(Invoice, 'Invoices', 'Financial'),
                 (Payment, 'Payments', 'Financial'),
                 (InsurancePlan, 'Insurance Plans', 'Financial'),
                 (InsuranceClaim, 'Insurance Claims', 'Financial'),
                 (Expense, 'Expenses', 'Financial'),
                 (FinancialReport, 'Financial Reports', 'Financial')],
                
                # Inventory
                [(Product, 'Products', 'Inventory'),
                 (ProductCategory, 'Product Categories', 'Inventory'),
                 (Supplier, 'Suppliers', 'Inventory'),
                 (PurchaseOrder, 'Purchase Orders', 'Inventory'),
                 (InventoryTransaction, 'Inventory Transactions', 'Inventory')],
                
                # Analytics & Security
                [(Notification, 'Notifications', 'Analytics'),
                 (AuditTrail, 'Audit Trail', 'Analytics'),
                 (SecurityEvent, 'Security Events', 'Security'),
                 (LoginAttempt, 'Login Attempts', 'Security'),
                 (FamilyMember, 'Family Members', 'Family')]
            ]
            
            # Add all models
            successful_views = 0
            for model_group in model_groups:
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
            
        except ImportError as e:
            print(f"⚠️ Could not import models: {e}")
            # Add at least one view to test
            try:
                from app.models import User
                view = create_model_view(User, 'Users', 'System')
                if view:
                    admin.add_view(view)
                    print("✅ Added Users view for testing")
            except:
                print("❌ Could not add any views")
        
        return admin
        
    except Exception as e:
        print(f"❌ Critical error initializing admin: {e}")
        traceback.print_exc()
        # Return minimal admin instance
        return Admin(
            app, 
            name='Dentaloist Admin', 
            template_mode='bootstrap4',
            url='/admin'
        )