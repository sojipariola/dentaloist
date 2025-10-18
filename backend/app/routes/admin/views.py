from flask import render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import current_user
from app.models import db
from sqlalchemy import inspect, desc, or_
import datetime
from functools import wraps
from typing import List, Dict, Any, Optional
import csv
import io
from markupsafe import Markup
import json

class BaseModelView:
    """Complete replacement for Flask-Admin's ModelView"""
    
    # Basic configuration (same as Flask-Admin)
    page_size = 50
    can_view_details = True
    can_export = True
    can_create = True
    can_edit = True
    can_delete = True
    can_set_page_size = True
    
    # Column configuration
    column_list = None
    column_exclude_list = None
    column_details_list = None
    column_filters = None
    column_searchable_list = None
    column_editable_list = None
    column_sortable_list = None
    column_formatters = None
    
    # Form configuration
    form_columns = None
    form_excluded_columns = None
    form_ajax_refs = None
    form_widget_args = None
    
    # Template configuration (same as Flask-Admin)
    list_template = 'admin/model/list.html'
    create_template = 'admin/model/create.html'
    edit_template = 'admin/model/edit.html'
    details_template = 'admin/model/details.html'
    
    # Actions
    action_disallowed_list = None
    inline_models = None
    
    def __init__(self, model, name=None, category=None, endpoint=None, **kwargs):
        self.model = model
        self.name = name or model.__name__
        self.category = category
        self.endpoint = endpoint or model.__name__.lower()
        self.session = db.session
        
        # Apply any kwargs to override defaults
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        self._init_defaults()
    
    def _init_defaults(self):
        """Initialize default configurations"""
        # Ensure all attributes exist
        self._ensure_attributes()
        
        if self.column_list is None:
            self.column_list = self._get_default_columns()
        
        if self.column_searchable_list is None:
            self.column_searchable_list = self._get_searchable_columns()
        
        if self.column_formatters is None:
            self.column_formatters = self.get_column_formatters()
    
    def _ensure_attributes(self):
        """Ensure all Flask-Admin compatible attributes exist"""
        attributes = [
            'page_size', 'can_view_details', 'can_export', 'can_create',
            'can_edit', 'can_delete', 'can_set_page_size',
            'column_list', 'column_exclude_list', 'column_details_list',
            'column_filters', 'column_searchable_list', 'column_editable_list',
            'column_sortable_list', 'column_formatters',
            'form_columns', 'form_excluded_columns', 'form_ajax_refs',
            'form_widget_args', 'action_disallowed_list', 'inline_models'
        ]
        
        for attr in attributes:
            if not hasattr(self, attr):
                if attr in ['page_size']:
                    setattr(self, attr, 50)
                elif attr in ['can_view_details', 'can_export', 'can_create', 
                            'can_edit', 'can_delete', 'can_set_page_size']:
                    setattr(self, attr, True)
                else:
                    setattr(self, attr, None)
    
    def _get_default_columns(self) -> List[str]:
        """Get default columns from model (replicates Flask-Admin behavior)"""
        inspector = inspect(self.model)
        columns = [column.name for column in inspector.columns]
        
        # Exclude common unwanted columns
        exclude = ['password_hash', 'secret_key', 'token']
        columns = [col for col in columns if col not in exclude]
        
        # Limit to first 8 columns for better UX (like Flask-Admin)
        return columns[:8]
    
    def _get_searchable_columns(self) -> List[str]:
        """Get searchable columns based on type"""
        inspector = inspect(self.model)
        searchable_types = ['String', 'Text', 'Unicode', 'UnicodeText', 'VARCHAR']
        searchable_columns = []
        
        for column in inspector.columns:
            if any(t in str(column.type) for t in searchable_types):
                searchable_columns.append(column.name)
        
        return searchable_columns
    
    def get_pk_value(self, model):
        """Get primary key value from model"""
        inspector = inspect(self.model)
        pk_column = inspector.primary_key[0].name
        return getattr(model, pk_column)
    
    def get_query(self):
        """Get base query (replicates Flask-Admin get_query)"""
        return self.model.query
    
    def get_count_query(self):
        """Get count query"""
        return self.model.query
    
    def get_list(self, page: int, sort_field: str, sort_desc: bool, search: str, filters: List, 
                 page_size: int = None):
        """Get paginated list of items (replicates Flask-Admin list view)"""
        query = self.get_query()
        
        # Apply search (like Flask-Admin)
        if search and self.column_searchable_list:
            search_filters = []
            for column in self.column_searchable_list:
                if hasattr(self.model, column):
                    search_filters.append(getattr(self.model, column).ilike(f'%{search}%'))
            if search_filters:
                query = query.filter(or_(*search_filters))
        
        # Apply sorting (like Flask-Admin)
        if sort_field and hasattr(self.model, sort_field):
            if sort_desc:
                query = query.order_by(desc(getattr(self.model, sort_field)))
            else:
                query = query.order_by(getattr(self.model, sort_field))
        else:
            # Default sort by primary key (like Flask-Admin)
            inspector = inspect(self.model)
            pk_column = inspector.primary_key[0].name
            query = query.order_by(desc(getattr(self.model, pk_column)))
        
        # Use provided page_size or default
        page_size = page_size or self.page_size
        
        return query.paginate(page=page, per_page=page_size, error_out=False)
    
    def scaffold_form(self):
        """Create form based on model columns (simplified version)"""
        # In a full implementation, this would integrate with WTForms
        # For now, return None and handle forms in templates
        return None
    
    def scaffold_list_columns(self):
        """Get columns for list view (replicates Flask-Admin)"""
        if self.column_list:
            return self.column_list
        
        columns = self._get_default_columns()
        
        # Apply exclusions
        if self.column_exclude_list:
            columns = [col for col in columns if col not in self.column_exclude_list]
        
        return columns
    
    def get_column_formatters(self):
        """Get column formatters for display (replicates Flask-Admin formatting)"""
        formatters = {}
        
        # Add default formatters for common types
        inspector = inspect(self.model)
        for column in inspector.columns:
            column_name = column.name
            column_type = str(column.type)
            
            if 'DateTime' in column_type:
                formatters[column_name] = self._format_datetime
            elif 'Date' in column_type:
                formatters[column_name] = self._format_date
            elif 'Boolean' in column_type:
                formatters[column_name] = self._format_boolean
            elif 'JSON' in column_type or 'PickleType' in column_type:
                formatters[column_name] = self._format_json
        
        return formatters
    
    def _format_datetime(self, context, model, name):
        """Format datetime columns (like Flask-Admin)"""
        value = getattr(model, name)
        if value:
            return value.strftime('%Y-%m-%d %H:%M')
        return ''
    
    def _format_date(self, context, model, name):
        """Format date columns"""
        value = getattr(model, name)
        if value:
            return value.strftime('%Y-%m-%d')
        return ''
    
    def _format_boolean(self, context, model, name):
        """Format boolean columns (like Flask-Admin)"""
        value = getattr(model, name)
        if value:
            return Markup('<span class="badge badge-success">Yes</span>')
        else:
            return Markup('<span class="badge badge-secondary">No</span>')
    
    def _format_json(self, context, model, name):
        """Format JSON columns (like Flask-Admin)"""
        value = getattr(model, name)
        if value:
            try:
                formatted = json.dumps(value, indent=2)
                return Markup(f'<pre>{formatted}</pre>')
            except:
                return str(value)
        return ''
    
    def create_model(self, form):
        """Create new model instance (replicates Flask-Admin create)"""
        try:
            model = self.model()
            form_data = self._handle_form_data(form)
            self._update_model(model, form_data)
            
            self.session.add(model)
            self.session.commit()
            
            # Flash message like Flask-Admin
            flash(f'{self.name} was successfully created.', 'success')
            return True, model
        except Exception as e:
            self.session.rollback()
            flash(f'Failed to create {self.name}. Error: {str(e)}', 'error')
            return False, str(e)
    
    def update_model(self, model, form):
        """Update existing model instance (replicates Flask-Admin edit)"""
        try:
            form_data = self._handle_form_data(form)
            self._update_model(model, form_data)
            
            self.session.commit()
            
            # Flash message like Flask-Admin
            flash(f'{self.name} was successfully updated.', 'success')
            return True, model
        except Exception as e:
            self.session.rollback()
            flash(f'Failed to update {self.name}. Error: {str(e)}', 'error')
            return False, str(e)
    
    def delete_model(self, model):
        """Delete model instance (replicates Flask-Admin delete)"""
        try:
            self.session.delete(model)
            self.session.commit()
            
            # Flash message like Flask-Admin
            flash(f'{self.name} was successfully deleted.', 'success')
            return True
        except Exception as e:
            self.session.rollback()
            flash(f'Failed to delete {self.name}. Error: {str(e)}', 'error')
            return False
    
    def _handle_form_data(self, form_data):
        """Handle form data preprocessing"""
        processed_data = {}
        
        for key, value in form_data.items():
            if key in ['csrf_token', 'submit']:
                continue
            processed_data[key] = value
        
        return processed_data
    
    def _update_model(self, model, form_data):
        """Update model from form data (handles various types like Flask-Admin)"""
        for field, value in form_data.items():
            if hasattr(model, field) and field != 'id':
                current_value = getattr(model, field)
                
                # Handle different field types like Flask-Admin
                if isinstance(current_value, bool):
                    setattr(model, field, bool(value))
                elif isinstance(current_value, int):
                    setattr(model, field, int(value) if value else 0)
                elif isinstance(current_value, float):
                    setattr(model, field, float(value) if value else 0.0)
                elif isinstance(current_value, datetime.datetime):
                    if value:
                        # Handle various datetime formats
                        if 'T' in value:
                            setattr(model, field, datetime.datetime.fromisoformat(value.replace('Z', '+00:00')))
                        else:
                            setattr(model, field, datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S'))
                elif isinstance(current_value, datetime.date):
                    if value:
                        setattr(model, field, datetime.datetime.strptime(value, '%Y-%m-%d').date())
                else:
                    setattr(model, field, value)
    
    def get_edit_form(self):
        """Get form for editing (simplified)"""
        return self.scaffold_form()
    
    def get_create_form(self):
        """Get form for creating (simplified)"""
        return self.scaffold_form()
    
    def on_model_change(self, form, model, is_created):
        """Hook for model changes (like Flask-Admin)"""
        pass
    
    def after_model_change(self, form, model, is_created):
        """Hook after model changes (like Flask-Admin)"""
        pass
    
    def on_form_prefill(self, form, id):
        """Hook for form prefill (like Flask-Admin)"""
        pass

# Specialized ModelViews (replicating Flask-Admin patterns)
class ModelView(BaseModelView):
    """Default ModelView with common configurations"""
    pass

class UserModelView(BaseModelView):
    """Customized view for User model"""
    
    page_size = 30
    column_list = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at']
    column_searchable_list = ['email', 'first_name', 'last_name']
    column_sortable_list = ['email', 'created_at', 'last_login_at']
    column_filters = ['role', 'is_active', 'is_admin']
    
    form_columns = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_admin']
    
    def get_column_formatters(self):
        formatters = super().get_column_formatters()
        formatters['role'] = self._format_user_role
        formatters['is_active'] = self._format_boolean
        formatters['is_admin'] = self._format_boolean
        return formatters
    
    def _format_user_role(self, context, model, name):
        role = getattr(model, name)
        role_colors = {
            'admin': 'danger',
            'doctor': 'primary',
            'staff': 'info',
            'patient': 'success'
        }
        color = role_colors.get(role, 'secondary')
        return Markup(f'<span class="badge badge-{color}">{role}</span>')

class PatientModelView(BaseModelView):
    """Customized view for Patient model"""
    
    page_size = 25
    column_list = ['id', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'blood_type', 'created_at']
    column_searchable_list = ['first_name', 'last_name', 'email', 'phone']
    column_sortable_list = ['first_name', 'last_name', 'created_at']
    column_filters = ['blood_type', 'gender']
    
    form_columns = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 
                   'blood_type', 'gender', 'address', 'medical_history']

class AppointmentModelView(BaseModelView):
    """Customized view for Appointment model"""
    
    page_size = 20
    column_list = ['id', 'patient', 'dentist', 'appointment_date', 'status', 'type', 'duration', 'created_at']
    column_searchable_list = ['patient.first_name', 'patient.last_name', 'dentist.first_name', 'dentist.last_name']
    column_sortable_list = ['appointment_date', 'created_at']
    column_filters = ['status', 'type']
    
    form_columns = ['patient_id', 'dentist_id', 'appointment_date', 'status', 'type', 
                   'duration', 'notes', 'treatment_plan']
    
    def get_column_formatters(self):
        formatters = super().get_column_formatters()
        formatters['status'] = self._format_appointment_status
        return formatters
    
    def _format_appointment_status(self, context, model, name):
        status = getattr(model, name)
        status_colors = {
            'scheduled': 'primary',
            'confirmed': 'info',
            'in_progress': 'warning',
            'completed': 'success',
            'cancelled': 'danger',
            'no_show': 'secondary'
        }
        color = status_colors.get(status, 'secondary')
        return Markup(f'<span class="badge badge-{color}">{status}</span>')

# Admin Manager (replaces Flask-Admin Admin class)
class AdminManager:
    """Manager for admin views (replaces Flask-Admin Admin)"""
    
    def __init__(self, name='Admin', template_mode='bootstrap4', url='/admin', endpoint='admin'):
        self.name = name
        self.template_mode = template_mode
        self.url = url
        self.endpoint = endpoint
        self._views = {}
        self._menu = {}
    
    def add_view(self, view, name=None, category=None):
        """Add a view to admin (replicates Flask-Admin add_view)"""
        if name:
            view.name = name
        if category:
            view.category = category
            
        endpoint = view.endpoint
        self._views[endpoint] = view
        
        # Build menu structure like Flask-Admin
        if view.category not in self._menu:
            self._menu[view.category] = []
        
        self._menu[view.category].append({
            'name': view.name,
            'endpoint': endpoint,
            'view': view
        })
        
        print(f"✅ Added admin view for {view.name} in category {view.category}")
    
    def get_view(self, endpoint):
        """Get view by endpoint"""
        return self._views.get(endpoint)
    
    def get_menu(self):
        """Get menu structure (like Flask-Admin)"""
        return self._menu
    
    def get_models(self):
        """Get all registered models"""
        return [view for view in self._views.values()]

# Global admin manager instance (replaces Flask-Admin instance)
admin_manager = AdminManager(name='Dentaloist Admin', template_mode='bootstrap4')

# Convenience function to register views (replicates Flask-Admin pattern)
def register_view(view, name=None, category=None):
    """Register a view with the admin manager"""
    admin_manager.add_view(view, name, category)

def create_model_view(model_class, name=None, category=None, view_class=ModelView, **kwargs):
    """Safely create a ModelView for a given model class (replicates Flask-Admin pattern)"""
    try:
        # Create dynamic view class
        class DynamicModelView(view_class):
            pass
        
        if name:
            DynamicModelView.__name__ = f"{name}AdminView"
        
        # Configure column list safely
        try:
            inspector = inspect(model_class)
            columns = [column.name for column in inspector.columns][:8]
            DynamicModelView.column_list = columns
            
            # Add ID column for better navigation (like Flask-Admin)
            if 'id' in columns:
                DynamicModelView.column_list = ['id'] + [col for col in columns if col != 'id']
                
        except Exception as e:
            print(f"⚠️ Could not inspect columns for {model_class.__name__}: {e}")
        
        return DynamicModelView(model_class, name=name, category=category, **kwargs)
    except Exception as e:
        print(f"⚠️ Failed to create admin view for {model_class.__name__}: {e}")
        return None

# Initialize default views (replaces Flask-Admin init)
def init_default_views():
    """Register default model views (replaces Flask-Admin model registration)"""
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
        
        # Define model groups exactly like your Flask-Admin setup
        model_groups = [
            # System
            [(User, 'Users', 'System', UserModelView),
             (Organization, 'Organizations', 'System', ModelView),
             (Tenant, 'Tenants', 'System', ModelView),
             (Role, 'Roles', 'System', ModelView),
             (Staff, 'Staff', 'System', ModelView),
             (Subscription, 'Subscriptions', 'System', ModelView)],
            
            # Clinical
            [(Patient, 'Patients', 'Clinical', PatientModelView),
             (Appointment, 'Appointments', 'Clinical', AppointmentModelView),
             (Treatment, 'Treatments', 'Clinical', ModelView),
             (TreatmentPlan, 'Treatment Plans', 'Clinical', ModelView),
             (ClinicalNote, 'Clinical Notes', 'Clinical', ModelView),
             (Allergy, 'Allergies', 'Clinical', ModelView),
             (Prescription, 'Prescriptions', 'Clinical', ModelView),
             (VitalSign, 'Vital Signs', 'Clinical', ModelView)],
            
            # Financial
            [(Invoice, 'Invoices', 'Financial', ModelView),
             (Payment, 'Payments', 'Financial', ModelView),
             (InsurancePlan, 'Insurance Plans', 'Financial', ModelView),
             (InsuranceClaim, 'Insurance Claims', 'Financial', ModelView),
             (Expense, 'Expenses', 'Financial', ModelView),
             (FinancialReport, 'Financial Reports', 'Financial', ModelView)],
            
            # Inventory
            [(Product, 'Products', 'Inventory', ModelView),
             (ProductCategory, 'Product Categories', 'Inventory', ModelView),
             (Supplier, 'Suppliers', 'Inventory', ModelView),
             (PurchaseOrder, 'Purchase Orders', 'Inventory', ModelView),
             (InventoryTransaction, 'Inventory Transactions', 'Inventory', ModelView)],
            
            # Analytics & Security
            [(Notification, 'Notifications', 'Analytics', ModelView),
             (AuditTrail, 'Audit Trail', 'Analytics', ModelView),
             (SecurityEvent, 'Security Events', 'Security', ModelView),
             (LoginAttempt, 'Login Attempts', 'Security', ModelView),
             (FamilyMember, 'Family Members', 'Family', ModelView)]
        ]
        
        # Add all models exactly like your Flask-Admin setup
        successful_views = 0
        for model_group in model_groups:
            for model, name, category, view_class in model_group:
                try:
                    view = create_model_view(model, name, category, view_class)
                    if view:
                        register_view(view)
                        successful_views += 1
                except Exception as e:
                    print(f"❌ Failed to add admin view for {name}: {e}")
                    continue
        
        print(f"✅ Custom Admin interface initialized with {successful_views} views (replacing Flask-Admin)")
        
    except ImportError as e:
        print(f"⚠️ Could not import models: {e}")
        # Add at least one view to test (like your Flask-Admin fallback)
        try:
            from app.models import User
            view = create_model_view(User, 'Users', 'System', UserModelView)
            if view:
                register_view(view)
                print("✅ Added Users view for testing (replacing Flask-Admin)")
        except Exception as e:
            print(f"❌ Could not add any views: {e}")

# Call this when the admin module is initialized
init_default_views()