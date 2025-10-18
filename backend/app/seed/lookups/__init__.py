# backend/app/seed/lookups/__init__.py
from .subscription_plans_seed import seed_subscription_plans
from .appointment_statuses_seed import seed_appointment_statuses
from .appointment_types_seed import seed_appointment_types
from .priority_levels_seed import seed_priority_levels
from .treatment_statuses_seed import seed_treatment_statuses
from .treatment_types_seed import seed_treatment_types
from .treatment_priorities_seed import seed_treatment_priorities

from .note_types_seed import seed_note_types
from .allergy_severities_seed import seed_allergy_severities
from .medication_routes_seed import seed_medication_routes
from .vital_signs_units_seed import seed_vital_signs_units
from .genders_seed import seed_genders
from .user_roles_seed import seed_user_roles
from .payment_methods_seed import seed_payment_methods
from .widget_types_seed import seed_widget_types
from .widget_templates_seed import seed_widget_templates
from .notification_types_seed import seed_notification_types
from .integration_statuses_seed import seed_integration_statuses
from .webhook_event_statuses_seed import seed_webhook_event_statuses
from .report_types_seed import seed_report_types
from .organization_types_seed import seed_organization_types
from .tenant_statuses_seed import seed_tenant_statuses
from .industry_types_seed import seed_industry_types
from .security_event_types_seed import seed_security_event_types
from .permission_categories_seed import seed_permission_categories
from .payment_statuses_seed import seed_payment_statuses
from .transaction_types_seed import seed_transaction_types
from .invoice_statuses_seed import seed_invoice_statuses
from .claim_statuses_seed import seed_claim_statuses
from .expense_categories_seed import seed_expense_categories
from .currencies_seed import seed_currencies
from .product_types_seed import seed_product_types
from .inventory_transaction_types_seed import seed_inventory_transaction_types
from .purchase_order_statuses_seed import seed_purchase_order_statuses
from .inventory_adjustment_types_seed import seed_inventory_adjustment_types

from .analytics_event_types_seed import seed_analytics_event_types
from .audit_action_types_seed import seed_audit_action_types
from .audit_resource_types_seed import seed_audit_resource_types
from .dashboard_themes_seed import seed_dashboard_themes
from .report_categories_seed import seed_report_categories
from .widget_categories_seed import seed_widget_categories



def seed_all():
    """Run all seed functions"""
    print("🌱 Starting database seeding...")
    
    # Core system lookups
    seed_subscription_plans()
    seed_user_roles()
    seed_genders()
    seed_organization_types()
    seed_tenant_statuses()
    seed_industry_types()
    seed_permission_categories()
    
    # Clinical lookups
    seed_appointment_statuses()
    seed_appointment_types()
    seed_priority_levels()
    seed_treatment_statuses()
    seed_treatment_types()
    seed_treatment_priorities()
    seed_note_types()
    seed_allergy_severities()
    seed_medication_routes()
    seed_vital_signs_units()
    
    # Financial lookups
    seed_payment_methods()
    seed_payment_statuses()
    seed_transaction_types()
    seed_invoice_statuses()
    seed_claim_statuses()
    seed_expense_categories()
    seed_currencies()
    
    # Inventory lookups
    seed_product_types()
    seed_inventory_transaction_types()
    seed_purchase_order_statuses()
    seed_inventory_adjustment_types()
    
    # Analytics and system lookups
    seed_widget_types()
    seed_widget_templates()
    seed_notification_types()
    seed_integration_statuses()
    seed_webhook_event_statuses()
    seed_report_types()
    seed_security_event_types()
    
    seed_analytics_event_types()
    seed_audit_action_types()
    seed_audit_resource_types() 
    seed_dashboard_themes()
    seed_report_categories()
    seed_widget_categories()

    print("✅ All database seeds completed successfully!")


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_all_analytics_lookups()