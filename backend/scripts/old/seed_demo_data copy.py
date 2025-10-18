# backend/scripts/seed_demo_data.py
import os
import sys
from datetime import datetime, timedelta
import random
from faker import Faker
from werkzeug.security import generate_password_hash

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
 
from app.models import (db, bcrypt, 
    # Lookup models
    AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
    TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
    MedicationRoute, VitalSignsUnit, WidgetType, NotificationType,
    IntegrationStatus, WebhookEventStatus, ReportType, UserRole,
    OrganizationType, Gender, SubscriptionPlan, TenantStatus,
    IndustryType, SecurityEventType, PermissionCategory,
    PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus,
    ExpenseCategory, Currency, TransactionType, ProductType,
    InventoryTransactionType, PurchaseOrderStatus, InventoryAdjustmentType,
    
    # Core models
    Tenant, Organization, User, Staff, Role, Permission,
    StaffAvailability, StaffLeave, UserOAuth, FamilyMember, FamilyRelationship,
    PasswordHistory, SecurityEvent, LoginAttempt, UserSession,
    TenantInvitation, TenantAuditLog, Subscription,
    
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
    
    # Analytics models
    Widget, WidgetTemplate, WidgetConfig, Notification, AuditTrail,
    RateLimiter, RateLimit, EmailLog, Integration, IntegrationLog,
    Webhook, WebhookEvent, FileRecord, AnalyticsReport,
    AnalyticsDashboard, AnalyticsWidget, KPI, KPIHistory, AnalyticsEvent,
    ReportSchedule, ReportRun, DataExport
)

fake = Faker()

class DemoDataSeeder:
    def __init__(self):
        self.app = create_app()
        self.fake = Faker()
        self.admin_email = "sojipariola@gmail.com"
        self.admin_password = "Soji1111"
        self.organizations = []
        self.users = []
        self.patients = []
        self.staff_members = []
        
    def seed_all_data(self):
        """Seed all demo data"""
        with self.app.app_context():
            print("🚀 Starting demo data seeding...")
            
            try:
                # Clear existing data first
                self.clear_existing_data()
                
                # Create core infrastructure
                self.seed_tenants_and_organizations()
                self.seed_roles_and_permissions()
                self.seed_users_and_staff()
                self.seed_patients_and_families()
                self.seed_clinical_data()
                self.seed_financial_data()
                self.seed_inventory_data()
                self.seed_analytics_data()
                
                db.session.commit()
                print("✅ All demo data seeded successfully!")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error seeding demo data: {e}")
                import traceback
                print(f"🔍 Detailed traceback: {traceback.format_exc()}")
                raise
    
    def clear_existing_data(self):
        """Clear existing demo data to avoid conflicts"""
        print("🧹 Clearing existing demo data...")
        
        try:
            # Clear in reverse dependency order
            models_to_clear = [
                # Analytics models
                AnalyticsWidget, AnalyticsDashboard, KPIHistory, KPI, AnalyticsEvent,
                ReportRun, ReportSchedule, DataExport, Notification, AuditTrail,
                EmailLog, IntegrationLog, Integration, WebhookEvent, Webhook,
                FileRecord, AnalyticsReport, WidgetConfig, WidgetTemplate, Widget,
                
                # Inventory models  
                PurchaseOrderItem, PurchaseOrder, InventoryAdjustment, InventoryTransaction,
                InventoryItem, ProductPriceHistory, ProductImage, Product, ProductCategory, Supplier,
                
                # Financial models
                FinancialTransaction, Expense, FinancialReport, InsuranceClaim, InsurancePlan,
                PaymentRecord, Payment, Invoice,
                
                # Clinical models
                TelehealthSession, Note, TreatmentPlan, Procedure, MedicalRecord, LabOrder,
                VitalSign, Prescription, Allergy, ClinicalNote, Treatment, Appointment,
                AvailabilitySlot, TreatmentRoom,
                
                # Core models
                FamilyRelationship, FamilyMember, UserOAuth, StaffLeave, StaffAvailability,
                Staff, UserSession, LoginAttempt, SecurityEvent, PasswordHistory,
                TenantAuditLog, TenantInvitation, Subscription, Patient, User,
                
                # Role and permission models
                Role, Permission,
                
                # Organization and tenant
                Organization, Tenant,
            ]
            
            for model in models_to_clear:
                try:
                    count = db.session.query(model).delete()
                    print(f"   🧹 Cleared {count} records from {model.__name__}")
                except Exception as e:
                    print(f"   ⚠️  Could not clear {model.__name__}: {e}")
                    db.session.rollback()
            
            # Clear many-to-many tables
            try:
                db.session.execute("DELETE FROM user_roles")
                db.session.execute("DELETE FROM staff_roles") 
                db.session.execute("DELETE FROM role_permissions")
                print("   🧹 Cleared relationship tables")
            except Exception as e:
                print(f"   ⚠️  Could not clear relationship tables: {e}")
            
            db.session.commit()
            print("✅ Existing demo data cleared")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing data: {e}")
            raise
    
    def seed_tenants_and_organizations(self):
        """Seed tenants and organizations"""
        print("🏢 Seeding tenants and organizations...")
        
        # Create main tenant first without relationships
        tenant = Tenant(
            name="Dentaloist Demo Tenant",
            domain="demo.dentaloist.com",
            status='active',
            max_organizations=10,
            max_users=100
        )
        db.session.add(tenant)
        db.session.flush()  # Get the tenant ID
        
        # Get lookup values
        org_type = OrganizationType.query.first()
        subscription_plan = SubscriptionPlan.query.first()
        currency = Currency.query.filter_by(code='USD').first()
        
        if not org_type:
            print("   ⚠️  No organization types found, creating default")
            org_type = OrganizationType(
                code='clinic',
                name='Dental Clinic',
                description='Default dental clinic type'
            )
            db.session.add(org_type)
            db.session.flush()
        
        if not subscription_plan:
            print("   ⚠️  No subscription plans found, creating default")
            subscription_plan = SubscriptionPlan(
                code='professional',
                name='Professional Plan',
                description='Default professional plan'
            )
            db.session.add(subscription_plan)
            db.session.flush()
        
        # Create 3 organizations
        org_names = [
            "Bright Smile Dental Clinic",
            "Perfect Teeth Orthodontics", 
            "Family Dental Care Center"
        ]
        
        for i, org_name in enumerate(org_names):
            organization = Organization(
                public_id=f"org_{i+1}",
                name=org_name,
                legal_name=org_name,
                tax_id=f"TAX-{self.fake.random_number(digits=9)}",
                organization_type_id=org_type.id,
                subscription_plan_id=subscription_plan.id,
                address=self.fake.address(),
                city=self.fake.city(),
                state=self.fake.state(),
                country="USA",
                postal_code=self.fake.zipcode(),
                phone=self.fake.phone_number(),
                email=f"info@{org_name.lower().replace(' ', '')}.com",
                website=f"www.{org_name.lower().replace(' ', '')}.com",
                timezone="America/New_York",
                currency_id=currency.id if currency else None,
                is_active=True
            )
            db.session.add(organization)
            self.organizations.append(organization)
        
        db.session.flush()
        print("   ✅ Tenants and organizations seeded")
    
    def seed_roles_and_permissions(self):
        """Seed roles and permissions"""
        print("👥 Seeding roles and permissions...")
        
        # Create global permissions first
        permissions_data = [
            {'name': 'user_create', 'description': 'Create users', 'category': 'user_management'},
            {'name': 'user_read', 'description': 'View users', 'category': 'user_management'},
            {'name': 'user_update', 'description': 'Update users', 'category': 'user_management'},
            {'name': 'user_delete', 'description': 'Delete users', 'category': 'user_management'},
            {'name': 'patient_create', 'description': 'Create patients', 'category': 'patient_management'},
            {'name': 'patient_read', 'description': 'View patients', 'category': 'patient_management'},
            {'name': 'patient_update', 'description': 'Update patients', 'category': 'patient_management'},
            {'name': 'appointment_create', 'description': 'Create appointments', 'category': 'clinical_operations'},
            {'name': 'appointment_read', 'description': 'View appointments', 'category': 'clinical_operations'},
            {'name': 'invoice_create', 'description': 'Create invoices', 'category': 'financial_management'},
            {'name': 'invoice_read', 'description': 'View invoices', 'category': 'financial_management'},
        ]
        
        for perm_data in permissions_data:
            permission = Permission.query.filter_by(name=perm_data['name']).first()
            if not permission:
                permission = Permission(**perm_data)
                db.session.add(permission)
        
        db.session.flush()
        all_permissions = Permission.query.all()
        
        # Create roles for each organization
        for org in self.organizations:
            # Admin role
            admin_role = Role(
                name='Administrator',
                description='Full system access',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            admin_role.permissions = all_permissions
            db.session.add(admin_role)
            
            # Dentist role
            dentist_role = Role(
                name='Dentist',
                description='Dental practitioner',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            # Assign subset of permissions to dentist
            dentist_permissions = [p for p in all_permissions if 'patient' in p.name or 'appointment' in p.name]
            dentist_role.permissions = dentist_permissions
            db.session.add(dentist_role)
            
            # Assistant role
            assistant_role = Role(
                name='Dental Assistant',
                description='Dental assistant',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            # Limited permissions for assistant
            assistant_permissions = [p for p in all_permissions if 'read' in p.name and 'patient' in p.name]
            assistant_role.permissions = assistant_permissions
            db.session.add(assistant_role)
            
            # Receptionist role
            receptionist_role = Role(
                name='Receptionist',
                description='Front desk receptionist',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            # Limited permissions for receptionist
            receptionist_permissions = [p for p in all_permissions if 'read' in p.name and ('patient' in p.name or 'appointment' in p.name)]
            receptionist_role.permissions = receptionist_permissions
            db.session.add(receptionist_role)
        
        db.session.flush()
        print("   ✅ Roles and permissions seeded")
    
    def seed_users_and_staff(self):
        """Seed users and staff members"""
        print("👨‍💼 Seeding users and staff...")
        
        gender_male = Gender.query.filter_by(code='male').first()
        gender_female = Gender.query.filter_by(code='female').first()
        
        if not gender_male or not gender_female:
            print("   ⚠️  Gender lookup data missing")
            return
        
        for i, org in enumerate(self.organizations):
            # Get organization roles
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
            assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
            receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
            
            # Create admin user
            admin_user = User(
                public_id=f"user_admin_{i+1}",
                email=self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com",
                password_hash=bcrypt.generate_password_hash(self.admin_password).decode('utf-8'),
                first_name="Soji" if i == 0 else self.fake.first_name(),
                last_name="Pariola" if i == 0 else self.fake.last_name(),
                phone=self.fake.phone_number(),
                date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=55),
                gender_id=gender_male.id,
                address=self.fake.address(),
                city=self.fake.city(),
                state=self.fake.state(),
                country="USA",
                postal_code=self.fake.zipcode(),
                timezone="America/New_York",
                email_verified=True,
                is_active=True
            )
            db.session.add(admin_user)
            self.users.append(admin_user)
            
            # Create staff record for admin
            admin_staff = Staff(
                user=admin_user,
                organization=org,
                employee_id=f"EMP{org.public_id.upper()}{i+1:03d}",
                hire_date=self.fake.date_between(start_date='-5y', end_date='-1y'),
                job_title="Practice Administrator",
                department="Administration",
                specialization="Practice Management",
                license_number=f"LIC-{self.fake.random_number(digits=6)}" if i == 0 else None,
                license_expiry=self.fake.future_date(end_date='+2y') if i == 0 else None,
                is_active=True
            )
            db.session.add(admin_staff)
            self.staff_members.append(admin_staff)
            
            # Assign admin role
            if admin_role:
                admin_user.roles.append(admin_role)
            
            # Create additional staff members
            staff_configs = [
                {'role': dentist_role, 'title': 'Senior Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry', 'gender': gender_male},
                {'role': dentist_role, 'title': 'General Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry', 'gender': gender_female},
                {'role': assistant_role, 'title': 'Dental Assistant', 'dept': 'Clinical', 'specialization': 'Chairside Assistance', 'gender': gender_female},
                {'role': receptionist_role, 'title': 'Receptionist', 'dept': 'Front Desk', 'specialization': 'Patient Coordination', 'gender': gender_female},
            ]
            
            for j, config in enumerate(staff_configs):
                staff_user = User(
                    public_id=f"user_staff_{i+1}_{j+1}",
                    email=f"staff{i+1}_{j+1}@{org.name.lower().replace(' ', '')}.com",
                    password_hash=bcrypt.generate_password_hash("Password123!").decode('utf-8'),
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=22, maximum_age=65),
                    gender_id=config['gender'].id,
                    address=self.fake.address(),
                    city=self.fake.city(),
                    state=self.fake.state(),
                    country="USA",
                    postal_code=self.fake.zipcode(),
                    timezone="America/New_York",
                    email_verified=True,
                    is_active=True
                )
                db.session.add(staff_user)
                self.users.append(staff_user)
                
                staff_member = Staff(
                    user=staff_user,
                    organization=org,
                    employee_id=f"EMP{org.public_id.upper()}{i+1:03d}{j+1:02d}",
                    hire_date=self.fake.date_between(start_date='-3y', end_date='today'),
                    job_title=config['title'],
                    department=config['dept'],
                    specialization=config['specialization'],
                    license_number=f"LIC-{self.fake.random_number(digits=6)}" if config['role'] == dentist_role else None,
                    license_expiry=self.fake.future_date(end_date='+2y') if config['role'] == dentist_role else None,
                    is_active=True
                )
                db.session.add(staff_member)
                self.staff_members.append(staff_member)
                
                # Assign role
                if config['role']:
                    staff_user.roles.append(config['role'])
        
        db.session.flush()
        print("   ✅ Users and staff seeded")

    # ... [Keep the other seed functions mostly the same, but ensure they use self.fake instead of fake]
    
    def seed_patients_and_families(self):
        """Seed patients and family relationships"""
        print("👥 Seeding patients and families...")
        
        genders = Gender.query.all()
        if not genders:
            print("   ⚠️  No genders found for patient creation")
            return
            
        for org in self.organizations:
            num_patients = random.randint(20, 30)
            
            for i in range(num_patients):
                patient = Patient(
                    public_id=f"pat_{org.public_id}_{i+1:03d}",
                    organization=org,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    email=self.fake.email() if random.random() > 0.2 else None,
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=1, maximum_age=85),
                    gender_id=random.choice(genders).id,
                    address=self.fake.address(),
                    city=self.fake.city(),
                    state=self.fake.state(),
                    country="USA",
                    postal_code=self.fake.zipcode(),
                    emergency_contact_name=self.fake.name(),
                    emergency_contact_phone=self.fake.phone_number(),
                    emergency_contact_relationship=random.choice(['Spouse', 'Parent', 'Child', 'Sibling']),
                    primary_care_physician=self.fake.name(),
                    dental_insurance_provider=random.choice(['Delta Dental', 'Cigna', 'Aetna', 'MetLife', None]),
                    insurance_policy_number=f"POL-{self.fake.random_number(digits=8)}" if random.random() > 0.3 else None,
                    medical_history=random.choice([None, "No significant medical history", "Hypertension", "Diabetes", "Asthma"]),
                    dental_history=random.choice([None, "Regular dental visits", "Occasional cavities", "Gum disease treatment"]),
                    allergies=random.choice([None, "Penicillin", "Latex", "No known allergies"]),
                    medications=random.choice([None, "Blood pressure medication", "None", "Cholesterol medication"]),
                    notes=random.choice([None, "Prefers morning appointments", "Anxious about dental procedures"]),
                    is_active=True
                )
                db.session.add(patient)
                self.patients.append(patient)
        
        db.session.flush()
        print("   ✅ Patients and families seeded")

    # Continue with the other seed functions (clinical, financial, inventory, analytics)
    # Make sure to replace any 'fake' calls with 'self.fake' and handle missing lookup data
    
    def seed_clinical_data(self):
        """Seed basic clinical data"""
        print("🏥 Seeding clinical data...")
        
        # Create minimal clinical data for now
        for org in self.organizations:
            # Create a few treatment rooms
            for i in range(3):
                room = TreatmentRoom(
                    organization=org,
                    room_number=f"Room {i+1}",
                    name=f"Treatment Room {i+1}",
                    description="Standard dental treatment room",
                    is_active=True
                )
                db.session.add(room)
        
        db.session.flush()
        print("   ✅ Basic clinical data seeded")
    
    def seed_financial_data(self):
        """Seed basic financial data"""
        print("💰 Seeding financial data...")
        
        currency = Currency.query.filter_by(code='USD').first()
        if not currency:
            print("   ⚠️  No currency found for financial data")
            return
            
        for org in self.organizations:
            org_patients = [p for p in self.patients if p.organization_id == org.id]
            if not org_patients:
                continue
                
            # Create a few simple invoices
            for i in range(10):
                patient = random.choice(org_patients)
                invoice = Invoice(
                    organization=org,
                    patient=patient,
                    status_id=InvoiceStatus.query.filter_by(code='draft').first().id,
                    currency_id=currency.id,
                    invoice_number=f"INV-{org.public_id.upper()}-{i+1:04d}",
                    invoice_date=self.fake.date_between(start_date='-30d', end_date='today'),
                    due_date=self.fake.date_between(start_date='today', end_date='+30d'),
                    items=[{
                        'description': 'Dental Examination',
                        'quantity': 1,
                        'unit_price': 150.00,
                        'total': 150.00
                    }],
                    subtotal=150.00,
                    tax_amount=12.00,
                    total_amount=162.00,
                    amount_paid=0.00,
                    balance_due=162.00,
                    tax_rate=8.0
                )
                db.session.add(invoice)
        
        db.session.flush()
        print("   ✅ Basic financial data seeded")
    
    def seed_inventory_data(self):
        """Seed basic inventory data"""
        print("📦 Seeding inventory data...")
        
        product_type = ProductType.query.first()
        if not product_type:
            print("   ⚠️  No product types found for inventory data")
            return
            
        for org in self.organizations:
            # Create a product category
            category = ProductCategory(
                organization=org,
                name="Dental Supplies",
                description="General dental supplies",
                is_active=True
            )
            db.session.add(category)
            
            # Create a few products
            product = Product(
                organization=org,
                name="Dental Floss",
                description="Waxed dental floss 50m",
                sku=f"SKU-{self.fake.random_number(digits=6)}",
                product_type_id=product_type.id,
                category_id=category.id,
                unit_price=2.50,
                cost_price=1.50,
                reorder_level=10,
                is_active=True
            )
            db.session.add(product)
        
        db.session.flush()
        print("   ✅ Basic inventory data seeded")
    
    def seed_analytics_data(self):
        """Seed basic analytics data"""
        print("📊 Seeding analytics data...")
        
        for org in self.organizations:
            org_staff = [s for s in self.staff_members if s.organization_id == org.id]
            if not org_staff:
                continue
                
            # Create a simple dashboard
            dashboard = AnalyticsDashboard(
                organization=org,
                name="Clinical Overview",
                description=f"{org.name} analytics dashboard",
                layout_config={'columns': 3, 'theme': 'light'},
                is_default=True,
                is_public=False,
                created_by=org_staff[0].user_id
            )
            db.session.add(dashboard)
            
            # Create a KPI
            kpi = KPI(
                organization=org,
                name="Monthly Revenue",
                description="Track monthly revenue performance",
                target_value=50000,
                unit="USD",
                category="financial",
                is_active=True
            )
            db.session.add(kpi)
        
        db.session.flush()
        print("   ✅ Basic analytics data seeded")

def seed_demo_data():
    """Main function to seed all demo data"""
    seeder = DemoDataSeeder()
    seeder.seed_all_data()

if __name__ == '__main__':
    seed_demo_data()