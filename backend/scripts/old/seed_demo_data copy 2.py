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


'''
def seed_roles_and_permissions(self):
    """Seed roles and permissions"""
    print("👥 Seeding roles and permissions...")
    
    # Create permissions (these are global, not organization-specific)
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
    
    # Create roles for each organization
    for org in self.organizations:
        # Admin role for this organization
        admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
        if not admin_role:
            admin_role = Role(
                name='Administrator',
                description='Full system access for this organization',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            db.session.add(admin_role)
        
        # Dentist role for this organization
        dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
        if not dentist_role:
            dentist_role = Role(
                name='Dentist',
                description='Dental practitioner for this organization',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            db.session.add(dentist_role)
        
        # Assistant role for this organization
        assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
        if not assistant_role:
            assistant_role = Role(
                name='Dental Assistant',
                description='Dental assistant for this organization',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            db.session.add(assistant_role)
        
        # Receptionist role for this organization
        receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
        if not receptionist_role:
            receptionist_role = Role(
                name='Receptionist',
                description='Front desk receptionist for this organization',
                is_system_role=True,
                organization_id=org.id,
                is_default=False
            )
            db.session.add(receptionist_role)
    
    db.session.flush()
    
    # Assign all permissions to admin roles
    all_permissions = Permission.query.all()
    for org in self.organizations:
        admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
        if admin_role:
            admin_role.permissions = all_permissions
    
    print("   ✅ Roles and permissions seeded")


# Update the seed_users_and_staff function:

def seed_users_and_staff(self):
    """Seed users and staff members"""
    print("👨‍💼 Seeding users and staff...")
    
    for i, org in enumerate(self.organizations):
        # Get organization-specific roles
        admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
        dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
        assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
        receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
        
        # Create admin user for each organization
        admin_user = User(
            public_id=f"user_admin_{i+1}",
            email=self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com",
            password_hash=bcrypt.generate_password_hash(self.admin_password).decode('utf-8'),
            first_name="Soji" if i == 0 else self.fake.first_name(),
            last_name="Pariola" if i == 0 else self.fake.last_name(),
            phone=self.fake.phone_number(),
            date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=55),
            gender_id=Gender.query.filter_by(code='male').first().id,
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
            license_number=f"LIC-{fake.random_number(digits=6)}" if i == 0 else None,
            license_expiry=self.fake.future_date(end_date='+2y') if i == 0 else None,
            is_active=True
        )
        db.session.add(admin_staff)
        self.staff_members.append(admin_staff)
        
        # Assign admin role
        if admin_role:
            admin_user.roles.append(admin_role)
        
        # Create additional staff members with different roles
        staff_configs = [
            {'role': dentist_role, 'title': 'Senior Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry'},
            {'role': dentist_role, 'title': 'General Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry'},
            {'role': assistant_role, 'title': 'Dental Assistant', 'dept': 'Clinical', 'specialization': 'Chairside Assistance'},
            {'role': receptionist_role, 'title': 'Receptionist', 'dept': 'Front Desk', 'specialization': 'Patient Coordination'},
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
                gender_id=random.choice([g.id for g in Gender.query.all()]),
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
                license_number=f"LIC-{fake.random_number(digits=6)}" if config['role'] == dentist_role else None,
                license_expiry=self.fake.future_date(end_date='+2y') if config['role'] == dentist_role else None,
                is_active=True
            )
            db.session.add(staff_member)
            self.staff_members.append(staff_member)
            
            # Assign role
            if config['role']:
                staff_user.roles.append(config['role'])
        
        # Create a hygienist (additional staff member)
        hygienist_user = User(
            public_id=f"user_hyg_{i+1}",
            email=f"hygienist{i+1}@{org.name.lower().replace(' ', '')}.com",
            password_hash=bcrypt.generate_password_hash("Password123!").decode('utf-8'),
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name(),
            phone=self.fake.phone_number(),
            date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=45),
            gender_id=random.choice([g.id for g in Gender.query.all()]),
            address=self.fake.address(),
            city=self.fake.city(),
            state=self.fake.state(),
            country="USA",
            postal_code=self.fake.zipcode(),
            timezone="America/New_York",
            email_verified=True,
            is_active=True
        )
        db.session.add(hygienist_user)
        self.users.append(hygienist_user)
        
        hygienist_staff = Staff(
            user=hygienist_user,
            organization=org,
            employee_id=f"EMP{org.public_id.upper()}{i+1:03d}H",
            hire_date=self.fake.date_between(start_date='-2y', end_date='-6m'),
            job_title="Dental Hygienist",
            department="Clinical",
            specialization="Preventive Care",
            license_number=f"HYG-{fake.random_number(digits=6)}",
            license_expiry=self.fake.future_date(end_date='+2y'),
            is_active=True
        )
        db.session.add(hygienist_staff)
        self.staff_members.append(hygienist_staff)
    
    db.session.flush()
    print("   ✅ Users and staff seeded")
'''

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
                self.seed_roles_and_permissions()
                self.seed_tenants_and_organizations()
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
        
        # Define deletion order to respect foreign key constraints
        models_to_clear = [
            # Analytics models
            AnalyticsWidget, AnalyticsDashboard, KPIHistory, KPI, AnalyticsEvent,
            ReportRun, ReportSchedule, DataExport,
            Notification, AuditTrail, EmailLog, IntegrationLog, Integration,
            WebhookEvent, Webhook, FileRecord, AnalyticsReport,
            WidgetConfig, WidgetTemplate, Widget,
            
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
            TenantAuditLog, TenantInvitation, Subscription,
            
            # Role and permission associations (clear these before roles)
            # These might be many-to-many tables
        ]
        
        # Clear data in reverse dependency order
        for model in models_to_clear:
            try:
                db.session.query(model).delete()
                print(f"   🧹 Cleared {model.__name__}")
            except Exception as e:
                print(f"   ⚠️  Could not clear {model.__name__}: {e}")
        
        # Clear roles and users separately due to relationships
        try:
            # Clear user-role relationships first
            db.session.execute("DELETE FROM user_roles")
            db.session.execute("DELETE FROM staff_roles") 
            db.session.execute("DELETE FROM role_permissions")
        except Exception as e:
            print(f"   ⚠️  Could not clear role relationships: {e}")
        
        try:
            db.session.query(Role).delete()
            print("   🧹 Cleared Role")
        except Exception as e:
            print(f"   ⚠️  Could not clear Role: {e}")
        
        try:
            db.session.query(Permission).delete()
            print("   🧹 Cleared Permission")
        except Exception as e:
            print(f"   ⚠️  Could not clear Permission: {e}")
        
        try:
            db.session.query(User).delete()
            print("   🧹 Cleared User")
        except Exception as e:
            print(f"   ⚠️  Could not clear User: {e}")
        
        try:
            db.session.query(Patient).delete()
            print("   🧹 Cleared Patient")
        except Exception as e:
            print(f"   ⚠️  Could not clear Patient: {e}")
        
        try:
            db.session.query(Organization).delete()
            print("   🧹 Cleared Organization")
        except Exception as e:
            print(f"   ⚠️  Could not clear Organization: {e}")
        
        try:
            db.session.query(Tenant).delete()
            print("   🧹 Cleared Tenant")
        except Exception as e:
            print(f"   ⚠️  Could not clear Tenant: {e}")
        
        db.session.commit()
        print("✅ Existing demo data cleared")
        
            
    def seed_patients_and_families(self):
        """Seed patients and family relationships"""
        print("👥 Seeding patients and families...")
        
        for org in self.organizations:
            # Create 20-30 patients per organization
            num_patients = random.randint(20, 30)
            
            for i in range(num_patients):
                patient = Patient(
                    public_id=f"pat_{org.public_id}_{i+1:03d}",
                    organization=org,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    email=self.fake.email() if random.random() > 0.2 else None,  # 80% have email
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=1, maximum_age=85),
                    gender_id=random.choice([g.id for g in Gender.query.all()]),
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
                    insurance_policy_number=f"POL-{fake.random_number(digits=8)}" if random.random() > 0.3 else None,
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


    def seed_roles_and_permissions(self):
        """Seed roles and permissions"""
        print("👥 Seeding roles and permissions...")
        
        # Create permissions (these are global, not organization-specific)
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
        
        # Create roles for each organization
        for org in self.organizations:
            # Admin role for this organization
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            if not admin_role:
                admin_role = Role(
                    name='Administrator',
                    description='Full system access for this organization',
                    is_system_role=True,
                    organization_id=org.id,
                    is_default=False
                )
                db.session.add(admin_role)
            
            # Dentist role for this organization
            dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
            if not dentist_role:
                dentist_role = Role(
                    name='Dentist',
                    description='Dental practitioner for this organization',
                    is_system_role=True,
                    organization_id=org.id,
                    is_default=False
                )
                db.session.add(dentist_role)
            
            # Assistant role for this organization
            assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
            if not assistant_role:
                assistant_role = Role(
                    name='Dental Assistant',
                    description='Dental assistant for this organization',
                    is_system_role=True,
                    organization_id=org.id,
                    is_default=False
                )
                db.session.add(assistant_role)
            
            # Receptionist role for this organization
            receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
            if not receptionist_role:
                receptionist_role = Role(
                    name='Receptionist',
                    description='Front desk receptionist for this organization',
                    is_system_role=True,
                    organization_id=org.id,
                    is_default=False
                )
                db.session.add(receptionist_role)
        
        db.session.flush()
        
        # Assign all permissions to admin roles
        all_permissions = Permission.query.all()
        for org in self.organizations:
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            if admin_role:
                admin_role.permissions = all_permissions
        
        print("   ✅ Roles and permissions seeded")


    
    def seed_tenants_and_organizations(self):
        """Seed tenants and organizations"""
        print("🏢 Seeding tenants and organizations...")
        
        # Create main tenant
        tenant = Tenant(
            name="Dentaloist Demo Tenant",
            domain="demo.dentaloist.com",
            status='active',
            max_organizations=10,
            max_users=100
        )
        db.session.add(tenant)
        db.session.flush()
        
        # Create 3 organizations
        org_names = [
            "Bright Smile Dental Clinic",
            "Perfect Teeth Orthodontics", 
            "Family Dental Care Center"
        ]
        
        org_types = OrganizationType.query.all()
        subscription_plans = SubscriptionPlan.query.all()
        
        for i, org_name in enumerate(org_names):
            organization = Organization(
                public_id=f"org_{i+1}",
                name=org_name,
                legal_name=org_name,
                tax_id=f"TAX-{fake.random_number(digits=9)}",
                organization_type_id=org_types[0].id if org_types else 1,
                subscription_plan_id=subscription_plans[2].id if len(subscription_plans) > 2 else 1,  # Professional plan
                address=self.fake.address(),
                city=self.fake.city(),
                state=self.fake.state(),
                country="USA",
                postal_code=self.fake.zipcode(),
                phone=self.fake.phone_number(),
                email=f"info@{org_name.lower().replace(' ', '')}.com",
                website=f"www.{org_name.lower().replace(' ', '')}.com",
                timezone="America/New_York",
                currency_id=Currency.query.filter_by(code='USD').first().id,
                is_active=True
            )
            db.session.add(organization)
            self.organizations.append(organization)
        
        db.session.flush()
        print("   ✅ Tenants and organizations seeded")
        

    def seed_users_and_staff(self):
        """Seed users and staff members"""
        print("👨‍💼 Seeding users and staff...")
        
        for i, org in enumerate(self.organizations):
            # Get organization-specific roles
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
            assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
            receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
            
            # Create admin user for each organization
            admin_user = User(
                public_id=f"user_admin_{i+1}",
                email=self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com",
                password_hash=bcrypt.generate_password_hash(self.admin_password).decode('utf-8'),
                first_name="Soji" if i == 0 else self.fake.first_name(),
                last_name="Pariola" if i == 0 else self.fake.last_name(),
                phone=self.fake.phone_number(),
                date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=55),
                gender_id=Gender.query.filter_by(code='male').first().id,
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
                license_number=f"LIC-{fake.random_number(digits=6)}" if i == 0 else None,
                license_expiry=self.fake.future_date(end_date='+2y') if i == 0 else None,
                is_active=True
            )
            db.session.add(admin_staff)
            self.staff_members.append(admin_staff)
            
            # Assign admin role
            if admin_role:
                admin_user.roles.append(admin_role)
            
            # Create additional staff members with different roles
            staff_configs = [
                {'role': dentist_role, 'title': 'Senior Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry'},
                {'role': dentist_role, 'title': 'General Dentist', 'dept': 'Clinical', 'specialization': 'General Dentistry'},
                {'role': assistant_role, 'title': 'Dental Assistant', 'dept': 'Clinical', 'specialization': 'Chairside Assistance'},
                {'role': receptionist_role, 'title': 'Receptionist', 'dept': 'Front Desk', 'specialization': 'Patient Coordination'},
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
                    gender_id=random.choice([g.id for g in Gender.query.all()]),
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
                    license_number=f"LIC-{fake.random_number(digits=6)}" if config['role'] == dentist_role else None,
                    license_expiry=self.fake.future_date(end_date='+2y') if config['role'] == dentist_role else None,
                    is_active=True
                )
                db.session.add(staff_member)
                self.staff_members.append(staff_member)
                
                # Assign role
                if config['role']:
                    staff_user.roles.append(config['role'])
            
            # Create a hygienist (additional staff member)
            hygienist_user = User(
                public_id=f"user_hyg_{i+1}",
                email=f"hygienist{i+1}@{org.name.lower().replace(' ', '')}.com",
                password_hash=bcrypt.generate_password_hash("Password123!").decode('utf-8'),
                first_name=self.fake.first_name(),
                last_name=self.fake.last_name(),
                phone=self.fake.phone_number(),
                date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=45),
                gender_id=random.choice([g.id for g in Gender.query.all()]),
                address=self.fake.address(),
                city=self.fake.city(),
                state=self.fake.state(),
                country="USA",
                postal_code=self.fake.zipcode(),
                timezone="America/New_York",
                email_verified=True,
                is_active=True
            )
            db.session.add(hygienist_user)
            self.users.append(hygienist_user)
            
            hygienist_staff = Staff(
                user=hygienist_user,
                organization=org,
                employee_id=f"EMP{org.public_id.upper()}{i+1:03d}H",
                hire_date=self.fake.date_between(start_date='-2y', end_date='-6m'),
                job_title="Dental Hygienist",
                department="Clinical",
                specialization="Preventive Care",
                license_number=f"HYG-{fake.random_number(digits=6)}",
                license_expiry=self.fake.future_date(end_date='+2y'),
                is_active=True
            )
            db.session.add(hygienist_staff)
            self.staff_members.append(hygienist_staff)
        
        db.session.flush()
        print("   ✅ Users and staff seeded")


    def seed_clinical_data(self):
        """Seed clinical data (appointments, treatments, etc.)"""
        print("🏥 Seeding clinical data...")
        
        appointment_statuses = AppointmentStatus.query.all()
        appointment_types = AppointmentType.query.all()
        treatment_statuses = TreatmentStatus.query.all()
        treatment_types = TreatmentType.query.all()
        
        for org in self.organizations:
            org_patients = [p for p in self.patients if p.organization_id == org.id]
            org_staff = [s for s in self.staff_members if s.organization_id == org.id]
            
            # Create treatment rooms
            for i in range(5):
                room = TreatmentRoom(
                    organization=org,
                    room_number=f"Room {i+1}",
                    name=f"Treatment Room {i+1}",
                    description=f"Standard dental treatment room",
                    equipment=random.choice(["Basic dental chair", "Advanced imaging", "Surgical setup"]),
                    is_active=True
                )
                db.session.add(room)
            
            # Create appointments for the next 90 days
            for i in range(100):  # 100 appointments per org
                patient = random.choice(org_patients)
                staff = random.choice(org_staff)
                appointment_type = random.choice(appointment_types)
                status = random.choice(appointment_statuses)
                
                # Create appointment in the past or future
                if random.random() > 0.3:  # 70% in past, 30% in future
                    start_time = self.fake.date_time_between(start_date='-90d', end_date='today')
                else:
                    start_time = self.fake.date_time_between(start_date='today', end_date='+90d')
                
                duration = timedelta(minutes=appointment_type.default_duration or 30)
                end_time = start_time + duration
                
                appointment = Appointment(
                    organization=org,
                    patient=patient,
                    staff_id=staff.id,
                    appointment_type_id=appointment_type.id,
                    status_id=status.id,
                    title=f"{appointment_type.name} - {patient.first_name}",
                    description=f"Routine {appointment_type.name.lower()} appointment",
                    start_time=start_time,
                    end_time=end_time,
                    room_number=f"Room {random.randint(1, 5)}",
                    notes=random.choice([None, "Patient requires special attention", "Follow-up from previous treatment"]),
                    is_walk_in=random.random() > 0.9,  # 10% walk-ins
                    created_by=staff.user_id
                )
                db.session.add(appointment)
                
                # Create treatments for some appointments
                if random.random() > 0.5:  # 50% of appointments have treatments
                    treatment = Treatment(
                        organization=org,
                        patient=patient,
                        appointment=appointment,
                        staff_id=staff.id,
                        treatment_type_id=random.choice(treatment_types).id,
                        status_id=random.choice(treatment_statuses).id,
                        name=f"Treatment for {appointment_type.name}",
                        description=f"Standard treatment procedure",
                        procedure_code=f"DT{random.randint(1000, 9999)}",
                        tooth_numbers=random.choice([None, "3,4,5", "14,15", "19,20,21,22"]),
                        cost=round(random.uniform(50, 500), 2),
                        duration_minutes=appointment_type.default_duration or 30,
                        notes=random.choice([None, "Treatment completed successfully", "Patient tolerated well"]),
                        is_active=True
                    )
                    db.session.add(treatment)
            
            # Create vital signs for patients
            for patient in org_patients[:10]:  # First 10 patients get vital signs
                for i in range(random.randint(1, 3)):
                    vital_sign = VitalSign(
                        organization=org,
                        patient=patient,
                        recorded_by=random.choice(org_staff).user_id,
                        blood_pressure_systolic=random.randint(110, 140),
                        blood_pressure_diastolic=random.randint(70, 90),
                        heart_rate=random.randint(60, 100),
                        respiratory_rate=random.randint(12, 20),
                        temperature=round(random.uniform(36.5, 37.5), 1),
                        oxygen_saturation=random.randint(95, 100),
                        weight_kg=round(random.uniform(50, 100), 1),
                        height_cm=random.randint(150, 190),
                        notes=random.choice([None, "Within normal limits", "Stable vitals"])
                    )
                    db.session.add(vital_sign)
            
            # Create clinical notes
            for patient in org_patients[:15]:  # First 15 patients get clinical notes
                for i in range(random.randint(1, 2)):
                    clinical_note = ClinicalNote(
                        organization=org,
                        patient=patient,
                        created_by=random.choice(org_staff).user_id,
                        note_type_id=NoteType.query.filter_by(code='progress').first().id,
                        title=f"Progress Note - {self.fake.date_between(start_date='-60d', end_date='today').strftime('%Y-%m-%d')}",
                        content=self.fake.paragraph(nb_sentences=5),
                        subjective="Patient reports no pain or discomfort",
                        objective="Oral examination within normal limits",
                        assessment="Stable condition, no issues noted",
                        plan="Continue with regular checkups",
                        is_confidential=random.random() > 0.8  # 20% confidential
                    )
                    db.session.add(clinical_note)
        
        db.session.flush()
        print("   ✅ Clinical data seeded")
    
    def seed_financial_data(self):
        """Seed financial data (invoices, payments, insurance, etc.)"""
        print("💰 Seeding financial data...")
        
        invoice_statuses = InvoiceStatus.query.all()
        payment_statuses = PaymentStatus.query.all()
        payment_methods = PaymentMethod.query.all()
        claim_statuses = ClaimStatus.query.all()
        expense_categories = ExpenseCategory.query.all()
        currencies = Currency.query.all()
        transaction_types = TransactionType.query.all()
        
        for org in self.organizations:
            org_patients = [p for p in self.patients if p.organization_id == org.id]
            org_staff = [s for s in self.staff_members if s.organization_id == org.id]
            currency = currencies[0]  # USD
            
            # Create insurance plans for some patients
            for patient in org_patients[:10]:
                if random.random() > 0.3:  # 70% have insurance
                    insurance_plan = InsurancePlan(
                        organization=org,
                        patient=patient,
                        created_by=org_staff[0].user_id,
                        insurance_provider=random.choice(['Delta Dental', 'Cigna', 'Aetna', 'MetLife']),
                        plan_name=random.choice(['PPO Premier', 'Basic Plan', 'Gold Coverage']),
                        policy_number=f"POL-{fake.random_number(digits=8)}",
                        group_number=f"GRP-{fake.random_number(digits=6)}",
                        subscriber_name=patient.first_name + " " + patient.last_name,
                        subscriber_dob=patient.date_of_birth,
                        subscriber_relationship='Self',
                        coverage_type='Dental',
                        effective_date=self.fake.date_between(start_date='-2y', end_date='-6m'),
                        expiration_date=self.fake.date_between(start_date='+6m', end_date='+2y'),
                        is_primary=True,
                        is_active=True,
                        verification_status='verified',
                        annual_maximum=random.choice([1500, 2000, 2500, 3000]),
                        annual_used=random.randint(0, 1000),
                        benefits={
                            'preventive': {'covered': True, 'coverage_percentage': 100},
                            'basic': {'covered': True, 'coverage_percentage': 80},
                            'major': {'covered': True, 'coverage_percentage': 50}
                        }
                    )
                    db.session.add(insurance_plan)
            
            # Create invoices
            for i in range(50):  # 50 invoices per org
                patient = random.choice(org_patients)
                invoice_status = random.choice(invoice_statuses)
                
                # Generate line items
                line_items = []
                subtotal = 0
                for j in range(random.randint(1, 4)):
                    item_amount = round(random.uniform(50, 300), 2)
                    line_items.append({
                        'description': random.choice(['Dental Examination', 'Teeth Cleaning', 'X-Rays', 'Filling', 'Crown']),
                        'quantity': 1,
                        'unit_price': item_amount,
                        'total': item_amount,
                        'procedure_code': f"DT{random.randint(1000, 9999)}"
                    })
                    subtotal += item_amount
                
                tax_rate = 0.08  # 8% tax
                tax_amount = round(subtotal * tax_rate, 2)
                total_amount = subtotal + tax_amount
                
                # Determine amounts paid based on status
                if invoice_status.code in ['paid', 'partial']:
                    if invoice_status.code == 'paid':
                        amount_paid = total_amount
                    else:
                        amount_paid = round(total_amount * random.uniform(0.1, 0.8), 2)
                else:
                    amount_paid = 0
                
                balance_due = total_amount - amount_paid
                
                invoice = Invoice(
                    organization=org,
                    patient=patient,
                    status_id=invoice_status.id,
                    currency_id=currency.id,
                    invoice_number=f"INV-{org.public_id.upper()}-{i+1:04d}",
                    invoice_date=self.fake.date_between(start_date='-180d', end_date='today'),
                    due_date=self.fake.date_between(start_date='-150d', end_date='+30d'),
                    items=line_items,
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    total_amount=total_amount,
                    amount_paid=amount_paid,
                    balance_due=balance_due,
                    tax_rate=tax_rate,
                    payment_instructions="Please pay within 30 days",
                    notes=random.choice([None, "Insurance pending", "Payment plan arranged"])
                )
                db.session.add(invoice)
                
                # Create payments for paid/partial invoices
                if amount_paid > 0:
                    payment = Payment(
                        organization_id=org.id,
                        patient=patient,
                        invoice=invoice,
                        payment_method_id=random.choice(payment_methods).id,
                        status_id=PaymentStatus.query.filter_by(code='completed').first().id,
                        currency_id=currency.id,
                        amount=amount_paid,
                        payment_date=invoice.invoice_date + timedelta(days=random.randint(0, 30)),
                        reference_number=f"PMT-{fake.random_number(digits=8)}",
                        notes="Payment received"
                    )
                    db.session.add(payment)
                
                # Create financial transactions
                if random.random() > 0.5:  # 50% have financial transactions
                    transaction_type = random.choice(transaction_types)
                    financial_transaction = FinancialTransaction(
                        organization=org,
                        patient=patient,
                        invoice=invoice,
                        transaction_type_id=transaction_type.id,
                        currency_id=currency.id,
                        transaction_number=f"TRX-{fake.random_number(digits=10)}",
                        description=f"{transaction_type.name} - {invoice.invoice_number}",
                        debit_amount=total_amount if transaction_type.category == 'revenue' else 0,
                        credit_amount=0 if transaction_type.category == 'revenue' else total_amount,
                        net_amount=total_amount if transaction_type.category == 'revenue' else -total_amount,
                        account_type='asset' if transaction_type.category == 'revenue' else 'expense',
                        account_subtype='accounts_receivable',
                        source_module='billing',
                        source_reference=invoice.invoice_number,
                        posted_by=org_staff[0].user_id
                    )
                    db.session.add(financial_transaction)
            
            # Create expenses
            for i in range(20):  # 20 expenses per org
                expense = Expense(
                    organization=org,
                    category_id=random.choice(expense_categories).id,
                    amount=round(random.uniform(50, 2000), 2),
                    description=random.choice(['Office supplies', 'Dental equipment maintenance', 'Utility bill', 'Staff training']),
                    expense_date=self.fake.date_between(start_date='-90d', end_date='today'),
                    vendor_name=random.choice(['Dental Supply Co.', 'Office Depot', 'Local Utility Company']),
                    vendor_invoice_number=f"VINV-{fake.random_number(digits=6)}",
                    payment_method_id=random.choice(payment_methods).id,
                    is_tax_deductible=True,
                    status='paid',
                    incurred_by=org_staff[0].user_id
                )
                db.session.add(expense)
        
        db.session.flush()
        print("   ✅ Financial data seeded")
    
    def seed_inventory_data(self):
        """Seed inventory data"""
        print("📦 Seeding inventory data...")
        
        product_types = ProductType.query.all()
        transaction_types = InventoryTransactionType.query.all()
        po_statuses = PurchaseOrderStatus.query.all()
        
        for org in self.organizations:
            # Create product categories
            categories = ['Dental Supplies', 'Medications', 'Equipment', 'Office Supplies']
            product_categories = []
            
            for category_name in categories:
                category = ProductCategory(
                    organization=org,
                    name=category_name,
                    description=f"{category_name} for dental practice",
                    is_active=True
                )
                db.session.add(category)
                product_categories.append(category)
            
            db.session.flush()
            
            # Create suppliers
            suppliers = []
            for i in range(3):
                supplier = Supplier(
                    organization=org,
                    name=f"{self.fake.company()} Dental Supplies",
                    contact_name=self.fake.name(),
                    email=self.fake.email(),
                    phone=self.fake.phone_number(),
                    address=self.fake.address(),
                    city=self.fake.city(),
                    state=self.fake.state(),
                    country="USA",
                    postal_code=self.fake.zipcode(),
                    payment_terms="Net 30",
                    is_active=True
                )
                db.session.add(supplier)
                suppliers.append(supplier)
            
            db.session.flush()
            
            # Create products
            products = []
            dental_products = [
                ('Dental Floss', 'Waxed dental floss 50m', 2.50, 'consumable'),
                ('Toothpaste', 'Fluoride toothpaste 100ml', 3.75, 'consumable'),
                ('Dental Anesthetic', 'Lidocaine 2% 1.8ml', 8.99, 'medication'),
                ('Examination Gloves', 'Latex-free gloves medium', 12.50, 'supply'),
                ('Dental Mask', 'Surgical face masks', 15.00, 'supply'),
                ('X-Ray Film', 'Dental X-Ray film pack', 45.00, 'dental_material'),
                ('Dental Drill', 'High-speed dental handpiece', 450.00, 'equipment')
            ]
            
            for product_name, description, price, product_type_code in dental_products:
                product_type = ProductType.query.filter_by(code=product_type_code).first()
                category = random.choice(product_categories)
                
                product = Product(
                    organization=org,
                    name=product_name,
                    description=description,
                    sku=f"SKU-{fake.random_number(digits=6)}",
                    product_type_id=product_type.id if product_type else product_types[0].id,
                    category_id=category.id,
                    unit_price=price,
                    cost_price=round(price * 0.6, 2),  # 40% margin
                    reorder_level=random.randint(5, 20),
                    preferred_supplier_id=random.choice(suppliers).id,
                    is_active=True
                )
                db.session.add(product)
                products.append(product)
            
            db.session.flush()
            
            # Create inventory items and transactions
            for product in products:
                # Create inventory item
                inventory_item = InventoryItem(
                    organization=org,
                    product=product,
                    current_stock=random.randint(10, 100),
                    min_stock=product.reorder_level,
                    max_stock=product.reorder_level * 4,
                    location=random.choice(['Main Storage', 'Room 1 Cabinet', 'Supply Room']),
                    last_restocked=self.fake.date_between(start_date='-30d', end_date='today')
                )
                db.session.add(inventory_item)
                
                # Create inventory transactions
                for i in range(random.randint(2, 5)):
                    transaction_type = random.choice(transaction_types)
                    quantity = random.randint(1, 20)
                    
                    transaction = InventoryTransaction(
                        organization=org,
                        product=product,
                        transaction_type_id=transaction_type.id,
                        quantity=quantity,
                        unit_cost=product.cost_price,
                        total_cost=quantity * product.cost_price,
                        reference_number=f"INV-TRX-{fake.random_number(digits=8)}",
                        notes=random.choice([None, "Regular restock", "Patient procedure usage"]),
                        created_by=self.staff_members[0].user_id  # Use first staff member
                    )
                    db.session.add(transaction)
            
            # Create purchase orders
            for i in range(5):
                supplier = random.choice(suppliers)
                po_status = random.choice(po_statuses)
                
                purchase_order = PurchaseOrder(
                    organization=org,
                    supplier=supplier,
                    status_id=po_status.id,
                    po_number=f"PO-{org.public_id.upper()}-{i+1:03d}",
                    order_date=self.fake.date_between(start_date='-60d', end_date='today'),
                    expected_delivery=self.fake.date_between(start_date='-30d', end_date='+30d'),
                    subtotal=round(random.uniform(200, 1000), 2),
                    tax_amount=0,
                    total_amount=0,  # Will be calculated from items
                    notes=random.choice([None, "Urgent order", "Quarterly restock"])
                )
                db.session.add(purchase_order)
                
                # Create PO items
                po_items = []
                po_total = 0
                for j in range(random.randint(2, 4)):
                    product = random.choice(products)
                    quantity = random.randint(5, 20)
                    unit_price = product.cost_price
                    total_price = quantity * unit_price
                    po_total += total_price
                    
                    po_item = PurchaseOrderItem(
                        purchase_order=purchase_order,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price
                    )
                    db.session.add(po_item)
                    po_items.append(po_item)
                
                # Update PO totals
                purchase_order.subtotal = po_total
                purchase_order.tax_amount = round(po_total * 0.08, 2)  # 8% tax
                purchase_order.total_amount = purchase_order.subtotal + purchase_order.tax_amount
        
        db.session.flush()
        print("   ✅ Inventory data seeded")
    
    def seed_analytics_data(self):
        """Seed analytics and reporting data"""
        print("📊 Seeding analytics data...")
        
        widget_types = WidgetType.query.all()
        notification_types = NotificationType.query.all()
        report_types = ReportType.query.all()
        
        for org in self.organizations:
            org_staff = [s for s in self.staff_members if s.organization_id == org.id]
            
            # Create analytics dashboards
            for i in range(2):
                dashboard = AnalyticsDashboard(
                    organization=org,
                    name=random.choice(['Clinical Overview', 'Financial Dashboard', 'Operations Monitor']),
                    description=f"{org.name} analytics dashboard",
                    layout_config={'columns': 3, 'theme': 'light'},
                    is_default=i == 0,
                    is_public=False,
                    created_by=org_staff[0].user_id
                )
                db.session.add(dashboard)
            
            # Create KPIs
            kpis = [
                {'name': 'Monthly Revenue', 'target_value': 50000, 'unit': 'USD', 'category': 'financial'},
                {'name': 'Patient Satisfaction', 'target_value': 95, 'unit': '%', 'category': 'clinical'},
                {'name': 'Appointment Utilization', 'target_value': 85, 'unit': '%', 'category': 'operations'},
            ]
            
            for kpi_data in kpis:
                kpi = KPI(
                    organization=org,
                    name=kpi_data['name'],
                    description=f"Track {kpi_data['name'].lower()}",
                    target_value=kpi_data['target_value'],
                    unit=kpi_data['unit'],
                    category=kpi_data['category'],
                    is_active=True
                )
                db.session.add(kpi)
                
                # Create KPI history
                for j in range(12):  # 12 months of history
                    month_ago = datetime.now() - timedelta(days=30*j)
                    actual_value = kpi_data['target_value'] * random.uniform(0.8, 1.2)
                    
                    kpi_history = KPIHistory(
                        kpi=kpi,
                        recorded_date=month_ago,
                        actual_value=actual_value,
                        notes=random.choice([None, "Strong performance", "Seasonal variation"])
                    )
                    db.session.add(kpi_history)
            
            # Create notifications
            for i in range(10):
                notification = Notification(
                    organization=org,
                    user_id=org_staff[0].user_id,
                    notification_type_id=random.choice(notification_types).id,
                    title=random.choice(['Appointment Reminder', 'Payment Received', 'Inventory Alert']),
                    message=self.fake.sentence(),
                    is_read=random.random() > 0.3,  # 70% read
                    action_url=random.choice([None, '/appointments', '/invoices', '/inventory']),
                    expires_at=datetime.now() + timedelta(days=7)
                )
                db.session.add(notification)
            
            # Create analytics events
            for i in range(50):
                event = AnalyticsEvent(
                    organization=org,
                    event_type=random.choice(['page_view', 'user_login', 'report_generated', 'data_export']),
                    event_data={'page': random.choice(['/dashboard', '/patients', '/appointments'])},
                    user_id=random.choice([u.id for u in org_staff[:3]]),  # First 3 staff members
                    session_id=f"session_{fake.random_number(digits=10)}",
                    ip_address=self.fake.ipv4(),
                    user_agent=self.fake.user_agent()
                )
                db.session.add(event)
            
            # Create report schedules
            for i in range(3):
                report_schedule = ReportSchedule(
                    organization=org,
                    name=random.choice(['Weekly Financial Report', 'Monthly Clinical Summary', 'Quarterly Inventory']),
                    report_type_id=random.choice(report_types).id,
                    frequency=random.choice(['weekly', 'monthly', 'quarterly']),
                    schedule_config={'day_of_week': 'monday', 'time': '09:00'},
                    is_active=True,
                    created_by=org_staff[0].user_id
                )
                db.session.add(report_schedule)
        
        db.session.flush()
        print("   ✅ Analytics data seeded")

def seed_demo_data():
    """Main function to seed all demo data"""
    seeder = DemoDataSeeder()
    seeder.seed_all_data()

if __name__ == '__main__':
    seed_demo_data()