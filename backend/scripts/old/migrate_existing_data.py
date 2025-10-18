# backend/scripts/migrate_existing_data.py
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.clinical import Appointment, Treatment, ClinicalNote, Allergy, Prescription
from app.models.lookups import (
    AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
    TreatmentType, TreatmentPriority, NoteType, AllergySeverity, MedicationRoute
)

def migrate_clinical_data():
    """Migrate existing enum data to new lookup tables"""
    
    # Map old enum values to new lookup IDs
    def get_lookup_id(model, code):
        lookup = model.query.filter_by(code=code).first()
        return lookup.id if lookup else None
    
    # Migrate Appointments
    appointments = Appointment.query.all()
    for appointment in appointments:
        if appointment.type:  # Old string field
            appointment.appointment_type_id = get_lookup_id(AppointmentType, appointment.type)
        if appointment.status:  # Old string field
            appointment.status_id = get_lookup_id(AppointmentStatus, appointment.status)
        # Priority remains as enum for now, but you can migrate it similarly
    
    # Migrate Treatments
    treatments = Treatment.query.all()
    for treatment in treatments:
        if treatment.type:  # Old enum field
            treatment.treatment_type_id = get_lookup_id(TreatmentType, treatment.type.value)
        if treatment.status:  # Old enum field
            treatment.status_id = get_lookup_id(TreatmentStatus, treatment.status.value)
        if treatment.priority:  # Old enum field
            treatment.priority_id = get_lookup_id(TreatmentPriority, treatment.priority.value)
    
    # Migrate ClinicalNotes
    clinical_notes = ClinicalNote.query.all()
    for note in clinical_notes:
        if note.note_type:  # Old enum field
            note.note_type_id = get_lookup_id(NoteType, note.note_type.value)
    
    # Migrate Allergies
    allergies = Allergy.query.all()
    for allergy in allergies:
        if allergy.severity:  # Old enum field
            allergy.severity_id = get_lookup_id(AllergySeverity, allergy.severity.value)
    
    # Migrate Prescriptions
    prescriptions = Prescription.query.all()
    for prescription in prescriptions:
        if prescription.route:  # Old enum field
            prescription.route_id = get_lookup_id(MedicationRoute, prescription.route.value)
    
    try:
        db.session.commit()
        print("Successfully migrated existing data!")
    except Exception as e:
        db.session.rollback()
        print(f"Error migrating data: {e}")
        raise

def migrate_analytics_data():
    """Migrate existing analytics enum data to new lookup tables"""
    
    # Migrate Widgets
    widgets = Widget.query.all()
    for widget in widgets:
        if widget.type:  # Old enum field
            widget.widget_type_id = get_lookup_id(WidgetType, widget.type.value)
    
    # Migrate Notifications
    notifications = Notification.query.all()
    for notification in notifications:
        if notification.type:  # Old enum field
            notification.notification_type_id = get_lookup_id(NotificationType, notification.type.value)
    
    # Migrate Integrations
    integrations = Integration.query.all()
    for integration in integrations:
        if integration.status:  # Old enum field
            integration.status_id = get_lookup_id(IntegrationStatus, integration.status.value)
    
    # Migrate WebhookEvents
    webhook_events = WebhookEvent.query.all()
    for event in webhook_events:
        if event.status:  # Old enum field
            event.status_id = get_lookup_id(WebhookEventStatus, event.status.value)
    
    # Migrate AnalyticsReports
    reports = AnalyticsReport.query.all()
    for report in reports:
        if report.report_type:  # Old enum field
            report.report_type_id = get_lookup_id(ReportType, report.report_type.value)

def migrate_core_data():
    """Migrate existing core enum data to new lookup tables"""
    
    # Migrate Tenants
    tenants = Tenant.query.all()
    for tenant in tenants:
        if tenant.industry:  # Old enum field
            tenant.industry_id = get_lookup_id(IndustryType, tenant.industry.value)
        if tenant.subscription_plan:  # Old enum field
            tenant.subscription_plan_id = get_lookup_id(SubscriptionPlan, tenant.subscription_plan.value)
        if tenant.status:  # Old enum field
            tenant.status_id = get_lookup_id(TenantStatus, tenant.status.value)
    
    # Migrate Organizations
    organizations = Organization.query.all()
    for org in organizations:
        if org.type:  # Old enum field
            org.organization_type_id = get_lookup_id(OrganizationType, org.type.value)
    
    # Migrate Users
    users = User.query.all()
    for user in users:
        if user.role:  # Old enum field
            user.user_role_id = get_lookup_id(UserRole, user.role.value)
        if user.gender:  # Old enum field
            user.gender_id = get_lookup_id(Gender, user.gender.value)
    
    # Migrate SecurityEvents
    security_events = SecurityEvent.query.all()
    for event in security_events:
        if event.event_type:  # Old enum field
            event.event_type_id = get_lookup_id(SecurityEventType, event.event_type.value)
    
    # Migrate Subscriptions
    subscriptions = Subscription.query.all()
    for subscription in subscriptions:
        if subscription.plan:  # Old enum field
            subscription.plan_id = get_lookup_id(SubscriptionPlan, subscription.plan.value)

def migrate_financial_data():
    """Migrate existing financial enum data to new lookup tables"""
    
    # Migrate Invoices
    invoices = Invoice.query.all()
    for invoice in invoices:
        if invoice.status:  # Old enum field
            invoice.status_id = get_lookup_id(InvoiceStatus, invoice.status.value)
        if invoice.currency:  # Old enum field
            invoice.currency_id = get_lookup_id(Currency, invoice.currency.value)
    
    # Migrate Payments
    payments = Payment.query.all()
    for payment in payments:
        if payment.status:  # Old enum field
            payment.status_id = get_lookup_id(PaymentStatus, payment.status.value)
        if payment.payment_method:  # Old enum field
            payment.payment_method_id = get_lookup_id(PaymentMethod, payment.payment_method.value)
        if payment.currency:  # Old enum field
            payment.currency_id = get_lookup_id(Currency, payment.currency.value)
    
    # Migrate InsuranceClaims
    claims = InsuranceClaim.query.all()
    for claim in claims:
        if claim.status:  # Old enum field
            claim.status_id = get_lookup_id(ClaimStatus, claim.status.value)
    
    # Migrate Expenses
    expenses = Expense.query.all()
    for expense in expenses:
        if expense.category:  # Old enum field
            expense.category_id = get_lookup_id(ExpenseCategory, expense.category.value)
        if expense.payment_method:  # Old enum field
            expense.payment_method_id = get_lookup_id(PaymentMethod, expense.payment_method.value)

def migrate_inventory_data():
    """Migrate existing inventory enum data to new lookup tables"""
    
    # Migrate Products
    products = Product.query.all()
    for product in products:
        if product.product_type:  # Old enum field
            product.product_type_id = get_lookup_id(ProductType, product.product_type.value)
    
    # Migrate PurchaseOrders
    purchase_orders = PurchaseOrder.query.all()
    for po in purchase_orders:
        if po.status:  # Old enum field
            po.status_id = get_lookup_id(PurchaseOrderStatus, po.status.value)
    
    # Migrate InventoryTransactions
    transactions = InventoryTransaction.query.all()
    for transaction in transactions:
        if transaction.transaction_type:  # Old enum field
            transaction.transaction_type_id = get_lookup_id(InventoryTransactionType, transaction.transaction_type.value)
    
    # Migrate InventoryAdjustments
    adjustments = InventoryAdjustment.query.all()
    for adjustment in adjustments:
        if adjustment.adjustment_type:  # Old enum field
            adjustment.adjustment_type_id = get_lookup_id(InventoryAdjustmentType, adjustment.adjustment_type.value)

# Update the main migration function
def migrate_existing_data():
    """Migrate existing enum data to new lookup tables"""
    
    # Helper function
    def get_lookup_id(model, code):
        lookup = model.query.filter_by(code=code).first()
        return lookup.id if lookup else None
    
    # Migrate all data
    migrate_analytics_data()
    migrate_core_data()
    migrate_financial_data()
    migrate_inventory_data()
    migrate_clinical_data() 
    
    try:
        db.session.commit()
        print("Successfully migrated all existing data!")
    except Exception as e:
        db.session.rollback()
        print(f"Error migrating data: {e}")
        raise

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        migrate_existing_data()