# backend/app/admin/lookup_views.py

from app.admin.manager import admin_manager
from app.admin.views import BaseModelView, ModelView

class LookupModelView(BaseModelView):
    """Specialized view for lookup tables"""
    
    page_size = 100
    can_create = True
    can_edit = True
    can_delete = False  # Usually don't delete lookup entries
    can_export = True
    
    # Common columns for lookup tables
    column_list = ['id', 'name', 'code', 'description', 'is_active', 'created_at']
    column_searchable_list = ['name', 'code', 'description']
    column_sortable_list = ['name', 'code', 'created_at']
    
    form_columns = ['name', 'code', 'description', 'is_active']
    
    def get_column_formatters(self):
        formatters = super().get_column_formatters()
        formatters['is_active'] = self._format_boolean
        return formatters

def init_lookup_views():
    """Initialize all lookup table views"""
    try:
        from app.models.lookups import (
            # Clinical Lookups
            AppointmentStatus, AppointmentType, TreatmentStatus, TreatmentType,
            TreatmentPriority, AllergySeverity, MedicationRoute, NoteType,
            VitalSignsUnit,
            
            # Financial Lookups  
            InvoiceStatus, PaymentStatus, PaymentMethod, ClaimStatus,
            ExpenseCategory, Currency,
            
            # System Lookups
            OrganizationType, IndustryType, SubscriptionPlan, TenantStatus,
            UserRole, PermissionCategory, NotificationType, SecurityEventType,
            WebhookEventStatus, IntegrationStatus,
            
            # Inventory Lookups
            ProductType, PurchaseOrderStatus, InventoryAdjustmentType,
            InventoryTransactionType,
            
            # Analytics Lookups
            ReportType, WidgetType, PriorityLevel
        )
        
        lookup_models = [
            # Clinical Lookups
            (AppointmentStatus, 'Appointment Statuses', 'Lookup Tables'),
            (AppointmentType, 'Appointment Types', 'Lookup Tables'),
            (TreatmentStatus, 'Treatment Statuses', 'Lookup Tables'),
            (TreatmentType, 'Treatment Types', 'Lookup Tables'),
            (TreatmentPriority, 'Treatment Priorities', 'Lookup Tables'),
            (AllergySeverity, 'Allergy Severities', 'Lookup Tables'),
            (MedicationRoute, 'Medication Routes', 'Lookup Tables'),
            (NoteType, 'Note Types', 'Lookup Tables'),
            (VitalSignsUnit, 'Vital Signs Units', 'Lookup Tables'),
            
            # Financial Lookups
            (InvoiceStatus, 'Invoice Statuses', 'Lookup Tables'),
            (PaymentStatus, 'Payment Statuses', 'Lookup Tables'),
            (PaymentMethod, 'Payment Methods', 'Lookup Tables'),
            (ClaimStatus, 'Claim Statuses', 'Lookup Tables'),
            (ExpenseCategory, 'Expense Categories', 'Lookup Tables'),
            (Currency, 'Currencies', 'Lookup Tables'),
            
            # System Lookups
            (OrganizationType, 'Organization Types', 'Lookup Tables'),
            (IndustryType, 'Industry Types', 'Lookup Tables'),
            (SubscriptionPlan, 'Subscription Plans', 'Lookup Tables'),
            (TenantStatus, 'Tenant Statuses', 'Lookup Tables'),
            (UserRole, 'User Roles', 'Lookup Tables'),
            (PermissionCategory, 'Permission Categories', 'Lookup Tables'),
            (NotificationType, 'Notification Types', 'Lookup Tables'),
            (SecurityEventType, 'Security Event Types', 'Lookup Tables'),
            (WebhookEventStatus, 'Webhook Event Statuses', 'Lookup Tables'),
            (IntegrationStatus, 'Integration Statuses', 'Lookup Tables'),
            
            # Inventory Lookups
            (ProductType, 'Product Types', 'Lookup Tables'),
            (PurchaseOrderStatus, 'Purchase Order Statuses', 'Lookup Tables'),
            (InventoryAdjustmentType, 'Inventory Adjustment Types', 'Lookup Tables'),
            (InventoryTransactionType, 'Inventory Transaction Types', 'Lookup Tables'),
            
            # Analytics Lookups
            (ReportType, 'Report Types', 'Lookup Tables'),
            (WidgetType, 'Widget Types', 'Lookup Tables'),
            (PriorityLevel, 'Priority Levels', 'Lookup Tables'),
        ]
        
        # Add lookup table category first
        admin_manager.add_category('Lookup Tables', 'fa-list')
        
        successful_views = 0
        for model, name, category in lookup_models:
            try:
                view = LookupModelView(model, name=name, category=category)
                admin_manager.add_view(view)
                successful_views += 1
                print(f"✅ Registered lookup view: {name}")
            except Exception as e:
                print(f"❌ Failed to add lookup view for {name}: {e}")
                continue
        
        print(f"🎯 Lookup tables initialized: {successful_views} views")
        return successful_views
        
    except ImportError as e:
        print(f"⚠️ Could not import lookup models: {e}")
        return 0