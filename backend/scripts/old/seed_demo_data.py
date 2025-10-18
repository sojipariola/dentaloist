# backend/scripts/seed_demo_data.py
import os
import sys
import json
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
        """Seed core demo data with comprehensive error handling"""
        with self.app.app_context():
            print("🚀 Starting demo data seeding...")
            
            try:
                # First, check if core tables exist
                if not self.check_tables_exist():
                    print("❌ Database tables not found. Please run 'flask db upgrade' first.")
                    return
                
                # Clear existing data first 
                self.clear_existing_data()
                
                # Create core infrastructure
                self.seed_user_roles()
                self.seed_roles_and_permissions()
                self.seed_tenants_and_organizations()
                self.seed_users_and_staff()
                
                # Debug staff organizations
                self.debug_staff_organizations()
                
                self.seed_patients_and_families()
                
                # Try to seed other data with individual error handling
                self.seed_with_error_handling('clinical_data', self.seed_clinical_data)
                self.seed_with_error_handling('financial_data', self.seed_financial_data)
                self.seed_with_error_handling('inventory_data', self.seed_inventory_data)
                self.seed_with_error_handling('analytics_data', self.seed_analytics_data)
                
                db.session.commit()
                print("✅ Demo data seeding completed!")
                
                # Final summary
                self.print_final_summary()
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error seeding demo data: {e}")
                import traceback
                print(f"🔍 Detailed traceback: {traceback.format_exc()}")
                raise

    def check_tables_exist(self):
        """Check if required tables exist"""
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        required_tables = ['users', 'organizations', 'patients', 'staff']
        existing_tables = inspector.get_table_names()
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        print("✅ All required tables exist")
        return True

    def seed_with_error_handling(self, data_type, seed_function):
        """Helper function to seed data with error handling"""
        try:
            seed_function()
        except Exception as e:
            print(f"⚠️  Could not seed {data_type}: {e}")
            db.session.rollback()  # Rollback any partial changes
            # Continue with next seeding function

    def print_final_summary(self):
        """Print final summary of what was created with error handling"""
        print("\n📋 FINAL SEEDING SUMMARY:")
        print(f"   🏢 Organizations: {len(self.organizations)}")
        print(f"   👥 Users: {len(self.users)}")
        
        # Count various data with error handling
        from app.models import Patient, Staff
        
        try:
            patient_count = Patient.query.count()
            print(f"   👥 Patients: {patient_count}")
        except Exception as e:
            print(f"   👥 Patients: ERROR - {e}")
        
        try:
            staff_count = Staff.query.count()
            print(f"   👨‍💼 Staff: {staff_count}")
        except Exception as e:
            print(f"   👨‍💼 Staff: ERROR - {e}")
        
        # Try to count other tables, but handle missing tables gracefully
        try:
            from app.models import Appointment
            appointment_count = Appointment.query.count()
            print(f"   🏥 Appointments: {appointment_count}")
        except Exception as e:
            print(f"   🏥 Appointments: 0 (table doesn't exist)")
        
        try:
            from app.models import Invoice
            invoice_count = Invoice.query.count()
            print(f"   💰 Invoices: {invoice_count}")
        except Exception as e:
            print(f"   💰 Invoices: 0 (table doesn't exist)")
        
        try:
            from app.models import Product
            product_count = Product.query.count()
            print(f"   📦 Products: {product_count}")
        except Exception as e:
            print(f"   📦 Products: 0 (table doesn't exist)")
        
        try:
            from app.models import KPI
            kpi_count = KPI.query.count()
            print(f"   📊 KPIs: {kpi_count}")
        except Exception as e:
            print(f"   📊 KPIs: 0 (table doesn't exist)")

    def seed_user_roles(self):
        """Seed user roles if they don't exist"""
        print("🎭 Seeding user roles...")
        
        user_roles_data = [
            {
                'code': 'admin',
                'name': 'Administrator', 
                'description': 'System administrator with full access',
                'is_system_role': True,
                'access_level': 'admin',
                'can_manage_users': True,
                'can_access_reports': True
            },
            {
                'code': 'dentist',
                'name': 'Dentist',
                'description': 'Dental practitioner',
                'is_system_role': True,
                'access_level': 'provider',
                'can_manage_users': False,
                'can_access_reports': True
            },
            {
                'code': 'staff', 
                'name': 'Staff',
                'description': 'General staff member',
                'is_system_role': True,
                'access_level': 'staff',
                'can_manage_users': False,
                'can_access_reports': False
            },
            {
                'code': 'patient',
                'name': 'Patient',
                'description': 'Patient user',
                'is_system_role': True,
                'access_level': 'patient',
                'can_manage_users': False,
                'can_access_reports': False
            }
        ]
        
        for role_data in user_roles_data:
            role = UserRole.query.filter_by(code=role_data['code']).first()
            if not role:
                role = UserRole(**role_data)
                db.session.add(role)
        
        db.session.flush()
        print("   ✅ User roles seeded")
        
    def clear_existing_data(self):
        """Clear existing demo data to avoid conflicts"""
        print("🧹 Clearing existing demo data...")
        
        try:
            # Clear in reverse dependency order
            # Start with analytics and reporting
            try:
                db.session.query(AnalyticsWidget).delete()
            except: pass
            try:
                db.session.query(AnalyticsDashboard).delete()
            except: pass
            try:
                db.session.query(KPIHistory).delete()
            except: pass
            try:
                db.session.query(KPI).delete()
            except: pass
            
            # Clear inventory
            try:
                db.session.query(InventoryAdjustment).delete()
            except: pass
            try:
                db.session.query(InventoryTransaction).delete()
            except: pass
            try:
                db.session.query(InventoryItem).delete()
            except: pass
            try:
                db.session.query(PurchaseOrderItem).delete()
            except: pass
            try:
                db.session.query(PurchaseOrder).delete()
            except: pass
            try:
                db.session.query(Product).delete()
            except: pass
            try:
                db.session.query(ProductCategory).delete()
            except: pass
            try:
                db.session.query(Supplier).delete()
            except: pass
            
            # Clear financial data
            try:
                db.session.query(FinancialTransaction).delete()
            except: pass
            try:
                db.session.query(Expense).delete()
            except: pass
            try:
                db.session.query(FinancialReport).delete()
            except: pass
            try:
                db.session.query(InsuranceClaim).delete()
            except: pass
            try:
                db.session.query(InsurancePlan).delete()
            except: pass
            try:
                db.session.query(Payment).delete()
            except: pass
            try:
                db.session.query(Invoice).delete()
            except: pass
            
            # Clear clinical data - use correct table names
            try:
                # Use Notes instead of ClinicalNote if that's your actual model
                db.session.query(Note).delete()
            except: pass
            try:
                db.session.query(Allergy).delete()
            except: pass
            try:
                db.session.query(VitalSign).delete()
            except: pass
            try:
                db.session.query(Prescription).delete()
            except: pass
            try:
                db.session.query(Treatment).delete()
            except: pass
            try:
                db.session.query(Appointment).delete()
            except: pass
            try:
                db.session.query(Patient).delete()
            except: pass
            try:
                db.session.query(TreatmentRoom).delete()
            except: pass
            
            # Clear core data - use proper SQLAlchemy queries
            try:
                # Clear many-to-many relationships first
                db.session.execute(db.text("DELETE FROM user_roles_association"))
            except: pass
            try:
                db.session.execute(db.text("DELETE FROM role_permissions"))
            except: pass
            
            try:
                db.session.query(Staff).delete()
            except: pass
            try:
                db.session.query(User).delete()
            except: pass
            try:
                db.session.query(Role).delete()
            except: pass
            try:
                db.session.query(Permission).delete()
            except: pass
            try:
                db.session.query(Organization).delete()
            except: pass
            try:
                db.session.query(Tenant).delete()
            except: pass
            
            db.session.commit()
            print("✅ Existing demo data cleared")
            
        except Exception as e:
            db.session.rollback()
            print(f"⚠️  Error during cleanup: {e}")
        
    def debug_staff_organizations(self):
        """Debug staff organization assignments"""
        print("🔍 Debugging staff organization assignments...")
        
        from app.models import Staff, Organization
        
        all_staff = Staff.query.all()
        print(f"Total staff in database: {len(all_staff)}")
        
        for staff in all_staff:
            # Use filter_by instead of get for VARCHAR organization_id
            org = Organization.query.filter_by(public_id=staff.organization_id).first() if staff.organization_id else None
            org_name = org.name if org else "NO ORGANIZATION"
            print(f"  Staff {staff.id}: user_id={staff.user_id}, org_id='{staff.organization_id}', org_name='{org_name}'")
        
        # Check if we have any staff with organization assignments
        staff_with_org = [s for s in all_staff if s.organization_id]
        print(f"Staff with organization assignments: {len(staff_with_org)}")
        
                    
    def seed_patients_and_families(self):
        """Seed patients using the corrected Patient model"""
        print("👥 Seeding patients and families...")
        
        for org in self.organizations:
            num_patients = random.randint(20, 30)
            
            for i in range(num_patients):
                # Create patient with proper JSON data
                patient = Patient(
                    public_id=f"pat_{org.public_id}_{i+1:03d}",
                    organization_id=org.public_id,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    email=self.fake.email() if random.random() > 0.2 else None,
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=1, maximum_age=85),
                    gender=random.choice(['Male', 'Female', 'Other']),
                    
                    # Use JSON fields instead of separate columns
                    address={
                        "street": self.fake.street_address(),
                        "city": self.fake.city(),
                        "state": self.fake.state(),
                        "postal_code": self.fake.zipcode(),
                        "country": "USA"
                    },
                    emergency_contact={
                        "name": self.fake.name(),
                        "phone": self.fake.phone_number(),
                        "relationship": random.choice(['Spouse', 'Parent', 'Child'])
                    },
                    medical_history={
                        "conditions": random.choice(["None", "Hypertension", "Diabetes", "Asthma"]),
                        "medications": random.choice(["None", "Blood pressure medication", "Insulin"]),
                        "allergies": random.choice(["No known allergies", "Penicillin", "Latex"])
                    },
                    allergies=random.choice([["No known allergies"], ["Penicillin"], ["Latex", "Iodine"]]),
                    medications=random.choice([["None"], ["Lisinopril 10mg daily"], ["Metformin 500mg twice daily"]]),
                    insurance_info={
                        "provider": random.choice(['Delta Dental', 'Cigna', 'Aetna', 'MetLife']),
                        "policy_number": f"POL-{fake.random_number(digits=8)}",
                        "group_number": f"GRP-{fake.random_number(digits=6)}"
                    } if random.random() > 0.3 else None,
                    dental_history={
                        "last_visit": self.fake.date_between(start_date='-2y', end_date='-3m').isoformat(),
                        "regular_visits": random.choice([True, False]),
                        "previous_treatments": random.choice(["Cleanings only", "Fillings", "Crowns"])
                    },
                    oral_hygiene=random.choice(['Good', 'Fair', 'Poor']),
                    last_dental_visit=self.fake.date_between(start_date='-2y', end_date='-1m') if random.random() > 0.2 else None,
                    next_recall_date=self.fake.date_between(start_date='+3m', end_date='+1y') if random.random() > 0.5 else None,
                    status='active',
                    preferred_language=random.choice(['English', 'Spanish', 'French']),
                    communication_preferences={
                        "email_notifications": random.choice([True, False]),
                        "sms_reminders": random.choice([True, False]),
                        "preferred_contact_method": random.choice(['email', 'sms', 'phone'])
                    },
                    is_active=True
                )
                db.session.add(patient)
                self.patients.append(patient)
        
        db.session.flush()
        print(f"   ✅ Created {len(self.patients)} patients using corrected model")
        

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
        
        # First, ensure we have the required lookup data
        industry_types = IndustryType.query.all()
        subscription_plans = SubscriptionPlan.query.all()
        tenant_statuses = TenantStatus.query.all()
        organization_types = OrganizationType.query.all()
        currencies = Currency.query.all()
        
        # Create default lookup data if it doesn't exist
        if not industry_types:
            print("   ⚠️  Creating default industry type...")
            industry_type = IndustryType(
                code='healthcare',
                name='Healthcare',
                description='Healthcare industry',
                category='Medical',
                requires_license=True
            )
            db.session.add(industry_type)
            db.session.flush()
            industry_types = [industry_type]
        
        if not subscription_plans:
            print("   ⚠️  Creating default subscription plan...")
            subscription_plan = SubscriptionPlan(
                code='professional',
                name='Professional',
                description='Professional subscription plan',
                price_monthly=199.00,
                price_yearly=1990.00,
                max_users=10,
                max_patients=1000,
                features={'basic_features': True, 'advanced_features': True},
                is_active=True
            )
            db.session.add(subscription_plan)
            db.session.flush()
            subscription_plans = [subscription_plan]
        
        if not tenant_statuses:
            print("   ⚠️  Creating default tenant status...")
            tenant_status = TenantStatus(
                code='active',
                name='Active',
                description='Active tenant',
                allows_login=True,
                requires_action=False
            )
            db.session.add(tenant_status)
            db.session.flush()
            tenant_statuses = [tenant_status]
        
        if not organization_types:
            print("   ⚠️  Creating default organization type...")
            org_type = OrganizationType(
                code='dental_clinic',
                name='Dental Clinic',
                description='Dental clinic organization',
                max_users=20,
                max_patients=5000,
                features_available=['appointments', 'billing', 'inventory']
            )
            db.session.add(org_type)
            db.session.flush()
            organization_types = [org_type]
        
        if not currencies:
            print("   ⚠️  Creating default currency...")
            currency = Currency(
                code='USD',
                name='US Dollar',
                symbol='$',
                decimal_places=2,
                is_active=True
            )
            db.session.add(currency)
            db.session.flush()
            currencies = [currency]
        
        # Create main tenant
        tenant = Tenant(
            name="Dentaloist Demo Tenant",
            domain="demo.dentaloist.com",
            subdomain="demo",
            display_name="Dentaloist Demo",
            description="Demo tenant for Dentaloist application",
            industry_id=industry_types[0].id,
            contact_email="demo@dentaloist.com",
            contact_phone=self.fake.phone_number(),
            website="https://demo.dentaloist.com",
            address_line1=self.fake.street_address(),
            city=self.fake.city(),
            state=self.fake.state(),
            postal_code=self.fake.zipcode(),
            country="USA",
            timezone="America/New_York",
            subscription_plan_id=subscription_plans[0].id,
            status_id=tenant_statuses[0].id,
            max_organizations=10,
            max_users=100,
            max_patients=10000,
            is_active=True
        )
        db.session.add(tenant)
        db.session.flush()
        
        # Create 3 organizations
        org_names = [
            "Bright Smile Dental Clinic",
            "Perfect Teeth Orthodontics", 
            "Family Dental Care Center"
        ]
        
        for i, org_name in enumerate(org_names):
            organization = Organization(
                public_id=f"org_{i+1:03d}",
                name=org_name,
                description=f"{org_name} - providing quality dental care",
                address=self.fake.street_address(),
                city=self.fake.city(),
                state=self.fake.state(),
                country="USA",
                postal_code=self.fake.zipcode(),
                phone=self.fake.phone_number(),
                email=f"info@{org_name.lower().replace(' ', '')}.com",
                website=f"https://www.{org_name.lower().replace(' ', '')}.com",
                organization_type_id=organization_types[0].id,
                tax_id=f"TAX-{fake.random_number(digits=9)}" if i == 0 else None,
                timezone="America/New_York",
                currency_id=currencies[0].id,
                is_active=True
            )
            db.session.add(organization)
            self.organizations.append(organization)
        
        db.session.flush()
        print("   ✅ Tenants and organizations seeded")
    
    ''' 
    def seed_users_and_staff(self):
        """Seed users and staff using correct staff schema"""
        print("👨‍💼 Seeding users and staff...")
        
        # Get user roles
        admin_user_role = UserRole.query.filter_by(code='admin').first()
        dentist_user_role = UserRole.query.filter_by(code='dentist').first()
        staff_user_role = UserRole.query.filter_by(code='staff').first()
        
        for i, org in enumerate(self.organizations):
            print(f"   👥 Creating staff for {org.name}...")
            
            # Get organization-specific roles
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
            assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
            receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()
            
            # Create admin user for each organization
            admin_user = User()
            admin_user.public_id = f"user_admin_{i+1}"
            admin_user.email = self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com"
            admin_user.password_hash = bcrypt.generate_password_hash(self.admin_password).decode('utf-8')
            admin_user.first_name = "Soji" if i == 0 else self.fake.first_name()
            admin_user.last_name = "Pariola" if i == 0 else self.fake.last_name()
            admin_user.phone = self.fake.phone_number()
            admin_user.date_of_birth = self.fake.date_of_birth(minimum_age=25, maximum_age=55)
            admin_user.gender_id = Gender.query.filter_by(code='male').first().id
            admin_user.user_role_id = admin_user_role.id
            admin_user.organization_id = org.public_id
            admin_user.email_verified = True
            admin_user.is_active = True
            
            db.session.add(admin_user)
            self.users.append(admin_user)
            db.session.flush()
            
            # Create staff record for admin - use correct column names from schema
            current_time = datetime.now()
            admin_staff_sql = """
            INSERT INTO staff (
                user_id, organization_id, staff_number, job_title, 
                department, specialization, hire_date, employment_type, status,
                work_email, work_phone, public_id, created_at, updated_at
            ) VALUES (
                :user_id, :org_id, :staff_number, :job_title,
                :department, :specialization, :hire_date, :employment_type, :status,
                :work_email, :work_phone, :public_id, :created_at, :updated_at
            )
            """
            
            admin_staff_params = {
                'user_id': admin_user.id,
                'org_id': org.public_id,  # Use public_id (VARCHAR) not org.id (INTEGER)
                'staff_number': f"EMP{org.public_id.upper()}{i+1:03d}",
                'job_title': "Practice Administrator",
                'department': "Administration",
                'specialization': "Practice Management",
                'hire_date': self.fake.date_between(start_date='-5y', end_date='-1y'),
                'employment_type': "Full-time",
                'status': "Active",
                'work_email': admin_user.email,
                'work_phone': self.fake.phone_number(),
                'public_id': f"staff_admin_{i+1}",
                'created_at': current_time,
                'updated_at': current_time
            }
            
            try:
                db.session.execute(db.text(admin_staff_sql), admin_staff_params)
                print(f"   ✅ Created admin staff for {org.name}")
            except Exception as e:
                print(f"   ❌ Error creating admin staff: {e}")
                continue
            
            # Assign admin role
            if admin_role:
                admin_user.roles.append(admin_role)
            
            # Create additional staff members
            staff_configs = [
                {'role': dentist_role, 'user_role': dentist_user_role, 'title': 'Senior Dentist', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': dentist_role, 'user_role': dentist_user_role, 'title': 'General Dentist', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': assistant_role, 'user_role': staff_user_role, 'title': 'Dental Assistant', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': receptionist_role, 'user_role': staff_user_role, 'title': 'Receptionist', 'dept': 'Front Desk', 'employment_type': 'Full-time'},
            ]
            
            for j, config in enumerate(staff_configs):
                staff_user = User()
                staff_user.public_id = f"user_staff_{i+1}_{j+1}"
                staff_user.email = f"staff{i+1}_{j+1}@{org.name.lower().replace(' ', '')}.com"
                staff_user.password_hash = bcrypt.generate_password_hash("Password123!").decode('utf-8')
                staff_user.first_name = self.fake.first_name()
                staff_user.last_name = self.fake.last_name()
                staff_user.phone = self.fake.phone_number()
                staff_user.date_of_birth = self.fake.date_of_birth(minimum_age=22, maximum_age=65)
                staff_user.gender_id = random.choice([g.id for g in Gender.query.all()])
                staff_user.user_role_id = config['user_role'].id
                staff_user.organization_id = org.public_id
                staff_user.email_verified = True
                staff_user.is_active = True
                
                db.session.add(staff_user)
                self.users.append(staff_user)
                db.session.flush()
                
                # Create staff record using correct schema
                staff_sql = """
                INSERT INTO staff (
                    user_id, organization_id, staff_number, job_title, 
                    department, specialization, license_number, license_expiry,
                    hire_date, employment_type, status, work_email, work_phone,
                    public_id, created_at, updated_at
                ) VALUES (
                    :user_id, :org_id, :staff_number, :job_title,
                    :department, :specialization, :license_number, :license_expiry,
                    :hire_date, :employment_type, :status, :work_email, :work_phone,
                    :public_id, :created_at, :updated_at
                )
                """
                
                staff_params = {
                    'user_id': staff_user.id,
                    'org_id': org.public_id,  # Use public_id (VARCHAR) not org.id (INTEGER)
                    'staff_number': f"EMP{org.public_id.upper()}{i+1:03d}{j+1:02d}",
                    'job_title': config['title'],
                    'department': config['dept'],
                    'specialization': config.get('specialization', ''),
                    'license_number': f"LIC-{fake.random_number(digits=6)}" if config['role'] == dentist_role else None,
                    'license_expiry': self.fake.future_date(end_date='+2y') if config['role'] == dentist_role else None,
                    'hire_date': self.fake.date_between(start_date='-3y', end_date='today'),
                    'employment_type': config['employment_type'],
                    'status': "Active",
                    'work_email': staff_user.email,
                    'work_phone': self.fake.phone_number(),
                    'public_id': f"staff_{i+1}_{j+1}",
                    'created_at': current_time,
                    'updated_at': current_time
                }
                
                try:
                    db.session.execute(db.text(staff_sql), staff_params)
                    print(f"   ✅ Created {config['title']} for {org.name}")
                except Exception as e:
                    print(f"   ❌ Error creating staff: {e}")
                    continue
                
                # Assign role
                if config['role']:
                    staff_user.roles.append(config['role'])
        
        db.session.flush()
        print("   ✅ Users and staff seeded")
        '''

    def seed_users_and_staff(self):
        """Seed users and staff using correct staff schema with enforced password hashing"""
        print("👨‍💼 Seeding users and staff...")

        # Fetch lookup roles safely
        def get_role_or_fail(model, code, name):
            role = model.query.filter_by(code=code).first()
            if not role:
                raise ValueError(f"❌ Missing {model.__name__} with code='{code}' ({name})")
            return role

        admin_user_role = get_role_or_fail(UserRole, 'admin', 'Admin User Role')
        dentist_user_role = get_role_or_fail(UserRole, 'dentist', 'Dentist User Role')
        staff_user_role = get_role_or_fail(UserRole, 'staff', 'Staff User Role')

        # Ensure bcrypt is available
        from app.models import bcrypt

        for i, org in enumerate(self.organizations):
            print(f"   👥 Creating staff for {org.name}...")

            # Organization-level roles
            admin_role = Role.query.filter_by(name='Administrator', organization_id=org.id).first()
            dentist_role = Role.query.filter_by(name='Dentist', organization_id=org.id).first()
            assistant_role = Role.query.filter_by(name='Dental Assistant', organization_id=org.id).first()
            receptionist_role = Role.query.filter_by(name='Receptionist', organization_id=org.id).first()

            # --- Admin User ---
            admin_password = self.admin_password or "Admin123!"
            hashed_admin_pw = bcrypt.generate_password_hash(admin_password).decode("utf-8")

            admin_user = User(
                public_id=f"user_admin_{i+1}",
                email=self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com",
                password_hash=hashed_admin_pw,
                first_name="Soji" if i == 0 else self.fake.first_name(),
                last_name="Pariola" if i == 0 else self.fake.last_name(),
                phone=self.fake.phone_number(),
                date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=55),
                gender_id=Gender.query.filter_by(code='male').first().id,
                user_role_id=admin_user_role.id,
                organization_id=org.public_id,
                email_verified=True,
                is_active=True
            )

            db.session.add(admin_user)
            db.session.flush()
            self.users.append(admin_user)

            # Staff Record for Admin
            current_time = datetime.now()
            try:
                db.session.execute(
                    db.text("""
                        INSERT INTO staff (
                            user_id, organization_id, staff_number, job_title,
                            department, specialization, hire_date, employment_type, status,
                            work_email, work_phone, public_id, created_at, updated_at
                        ) VALUES (
                            :user_id, :org_id, :staff_number, :job_title,
                            :department, :specialization, :hire_date, :employment_type, :status,
                            :work_email, :work_phone, :public_id, :created_at, :updated_at
                        )
                    """),
                    {
                        'user_id': admin_user.id,
                        'org_id': org.public_id,
                        'staff_number': f"EMP{org.public_id.upper()}{i+1:03d}",
                        'job_title': "Practice Administrator",
                        'department': "Administration",
                        'specialization': "Practice Management",
                        'hire_date': self.fake.date_between(start_date='-5y', end_date='-1y'),
                        'employment_type': "Full-time",
                        'status': "Active",
                        'work_email': admin_user.email,
                        'work_phone': self.fake.phone_number(),
                        'public_id': f"staff_admin_{i+1}",
                        'created_at': current_time,
                        'updated_at': current_time
                    }
                )
                print(f"   ✅ Created admin staff for {org.name}")
            except Exception as e:
                print(f"   ❌ Error creating admin staff: {e}")
                db.session.rollback()
                continue

            if admin_role:
                admin_user.roles.append(admin_role)

            # --- Other Staff ---
            staff_configs = [
                {'role': dentist_role, 'user_role': dentist_user_role, 'title': 'Senior Dentist', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': dentist_role, 'user_role': dentist_user_role, 'title': 'General Dentist', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': assistant_role, 'user_role': staff_user_role, 'title': 'Dental Assistant', 'dept': 'Clinical', 'employment_type': 'Full-time'},
                {'role': receptionist_role, 'user_role': staff_user_role, 'title': 'Receptionist', 'dept': 'Front Desk', 'employment_type': 'Full-time'},
            ]

            for j, config in enumerate(staff_configs):
                # Always enforce valid bcrypt hash
                password_plain = "Password123!"
                hashed_pw = bcrypt.generate_password_hash(password_plain).decode("utf-8")

                staff_user = User(
                    public_id=f"user_staff_{i+1}_{j+1}",
                    email=f"staff{i+1}_{j+1}@{org.name.lower().replace(' ', '')}.com",
                    password_hash=hashed_pw,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=22, maximum_age=65),
                    gender_id=random.choice([g.id for g in Gender.query.all()]),
                    user_role_id=config['user_role'].id,
                    organization_id=org.public_id,
                    email_verified=True,
                    is_active=True
                )

                db.session.add(staff_user)
                db.session.flush()
                self.users.append(staff_user)

                # Staff record insert
                try:
                    db.session.execute(
                        db.text("""
                            INSERT INTO staff (
                                user_id, organization_id, staff_number, job_title,
                                department, specialization, license_number, license_expiry,
                                hire_date, employment_type, status, work_email, work_phone,
                                public_id, created_at, updated_at
                            ) VALUES (
                                :user_id, :org_id, :staff_number, :job_title,
                                :department, :specialization, :license_number, :license_expiry,
                                :hire_date, :employment_type, :status, :work_email, :work_phone,
                                :public_id, :created_at, :updated_at
                            )
                        """),
                        {
                            'user_id': staff_user.id,
                            'org_id': org.public_id,
                            'staff_number': f"EMP{org.public_id.upper()}{i+1:03d}{j+1:02d}",
                            'job_title': config['title'],
                            'department': config['dept'],
                            'specialization': config.get('specialization', ''),
                            'license_number': f"LIC-{self.fake.random_number(digits=6)}"
                                if config['role'] == dentist_role else None,
                            'license_expiry': self.fake.future_date(end_date='+2y')
                                if config['role'] == dentist_role else None,
                            'hire_date': self.fake.date_between(start_date='-3y', end_date='today'),
                            'employment_type': config['employment_type'],
                            'status': "Active",
                            'work_email': staff_user.email,
                            'work_phone': self.fake.phone_number(),
                            'public_id': f"staff_{i+1}_{j+1}",
                            'created_at': current_time,
                            'updated_at': current_time
                        }
                    )
                    print(f"   ✅ Created {config['title']} for {org.name}")
                except Exception as e:
                    print(f"   ❌ Error creating staff: {e}")
                    db.session.rollback()
                    continue

                if config['role']:
                    staff_user.roles.append(config['role'])

        db.session.commit()
        print("   ✅ Users and staff seeded successfully")



    def seed_clinical_data(self):
        """Seed clinical data with all required fields"""
        print("🏥 Seeding clinical data...")
        
        from app.models import Patient, Staff
        
        total_patients = Patient.query.count()
        if total_patients == 0:
            print("   ⚠️  No patients found - skipping clinical data")
            return
        
        print(f"   📊 Found {total_patients} patients in database")
        
        appointment_statuses = AppointmentStatus.query.all()
        appointment_types = AppointmentType.query.all()
        
        clinical_data_created = 0
        
        for org in self.organizations:
            # Get staff for this organization
            org_staff = Staff.query.filter(Staff.organization_id == org.public_id).all()
            if not org_staff:
                print(f"   ⚠️  No staff for {org.name}")
                continue
            
            # Get patients for this organization
            org_patients = Patient.query.filter_by(organization_id=org.public_id).all()
            if not org_patients:
                print(f"   ⚠️  No patients for {org.name}")
                continue
            
            print(f"   🏥 Creating clinical data for {org.name} ({len(org_patients)} patients, {len(org_staff)} staff)")
            
            # Create appointments
            appointments_created = 0
            num_appointments = min(5, len(org_patients))
            
            for i in range(num_appointments):
                try:
                    patient = random.choice(org_patients)
                    staff = random.choice(org_staff)
                    appointment_type = random.choice(appointment_types)
                    status = random.choice(appointment_statuses)
                    
                    # Create appointment with proper datetime objects
                    if random.random() > 0.3:
                        start_time = self.fake.date_time_between(start_date='-90d', end_date='now')
                    else:
                        start_time = self.fake.future_datetime(end_date='+90d')
                    
                    duration = timedelta(minutes=appointment_type.default_duration or 30)
                    end_time = start_time + duration
                    
                    # Create appointment with ALL required fields including duration
                    appointment = Appointment()
                    appointment.organization_id = org.public_id
                    appointment.patient_id = patient.id
                    appointment.dentist_id = staff.id  # REQUIRED FIELD
                    appointment.staff_id = staff.id
                    appointment.appointment_type_id = appointment_type.id
                    appointment.status_id = status.id
                    appointment.title = f"{appointment_type.name} - {patient.first_name}"
                    appointment.description = f"Routine {appointment_type.name.lower()} appointment"
                    appointment.start_time = start_time
                    appointment.end_time = end_time
                    appointment.duration = duration.total_seconds() // 60  # Convert to minutes ← ADD THIS LINE
                    appointment.treatment_room = f"Room {random.randint(1, 3)}"
                    appointment.is_walk_in = random.random() > 0.9
                    
                    db.session.add(appointment)
                    appointments_created += 1
                    
                    # Commit in small batches
                    if appointments_created % 3 == 0:
                        db.session.flush()
                    
                except Exception as e:
                    print(f"   ⚠️  Error creating appointment {i+1}: {e}")
                    db.session.rollback()  # Rollback the failed transaction
                    continue
            
            clinical_data_created += appointments_created
            print(f"   ✅ Created {appointments_created} appointments for {org.name}")
        
        # Commit all appointments
        try:
            db.session.commit()
            print(f"   ✅ Clinical data committed successfully ({clinical_data_created} appointments)")
        except Exception as e:
            db.session.rollback()
            print(f"   ❌ Error committing clinical data: {e}")
            raise

    
    def seed_financial_data(self):
        """Seed financial data using fixed staff lookup"""
        print("💰 Seeding financial data...")
        
        from app.models import Patient, Staff
        total_patients = Patient.query.count()
        if total_patients == 0:
            print("   ⚠️  No patients found - skipping financial data")
            return
        
        print(f"   📊 Found {total_patients} patients in database")
        
        invoice_statuses = InvoiceStatus.query.all()
        payment_statuses = PaymentStatus.query.all()
        payment_methods = PaymentMethod.query.all()
        currencies = Currency.query.all()  # Get available currencies
        
        financial_data_created = 0
        
        for org in self.organizations:
            # Get staff for this organization - use public_id (VARCHAR)
            org_staff = Staff.query.filter_by(organization_id=org.public_id).all()
            if not org_staff:
                print(f"   ⚠️  No staff for {org.name} (looking for org_id: {org.public_id})")
                continue
            
            # Get patients for this organization
            org_patients = Patient.query.filter_by(organization_id=org.public_id).all()
            if not org_patients:
                print(f"   ⚠️  No patients for {org.name}")
                continue
            
            print(f"   💰 Creating financial data for {org.name} ({len(org_patients)} patients, {len(org_staff)} staff)")
            
            # Create invoices
            invoices_created = 0
            num_invoices = min(10, len(org_patients))
            
            for i in range(num_invoices):
                try:
                    patient = random.choice(org_patients)
                    staff = random.choice(org_staff)
                    invoice_status = random.choice(invoice_statuses)
                    currency = random.choice(currencies) if currencies else None  # Get a random currency
                    
                    if not currency:
                        print(f"   ⚠️  No currencies available - creating default USD currency")
                        currency = Currency(
                            code='USD',
                            name='US Dollar',
                            symbol='$',
                            decimal_places=2,
                            is_active=True
                        )
                        db.session.add(currency)
                        db.session.flush()
                    
                    # Generate line items
                    line_items = []
                    subtotal = 0
                    for j in range(random.randint(1, 3)):
                        item_amount = round(random.uniform(50, 300), 2)
                        line_items.append({
                            'description': random.choice(['Dental Examination', 'Teeth Cleaning', 'X-Rays', 'Filling']),
                            'quantity': 1,
                            'unit_price': item_amount,
                            'total': item_amount
                        })
                        subtotal += item_amount
                    
                    tax_rate = 0.08
                    tax_amount = round(subtotal * tax_rate, 2)
                    total_amount = subtotal + tax_amount
                    
                    # Create invoice with ALL required fields including currency_id
                    invoice = Invoice()
                    invoice.organization_id = org.public_id
                    invoice.patient_id = patient.id
                    invoice.status_id = invoice_status.id
                    invoice.currency_id = currency.id  # REQUIRED FIELD ← ADD THIS
                    invoice.invoice_number = f"INV-{org.public_id.upper()}-{i+1:04d}"
                    invoice.invoice_date = self.fake.date_between(start_date='-180d', end_date='today')
                    invoice.due_date = invoice.invoice_date + timedelta(days=30)
                    invoice.items = line_items
                    invoice.subtotal = subtotal
                    invoice.tax_amount = tax_amount
                    invoice.total_amount = total_amount
                    invoice.tax_rate = tax_rate
                    invoice.payment_terms = "Net 30"
                    invoice.payment_instructions = "Please pay within 30 days"
                    
                    db.session.add(invoice)
                    invoices_created += 1
                    
                    # Commit in small batches to avoid session issues
                    if invoices_created % 5 == 0:
                        db.session.flush()
                    
                except Exception as e:
                    print(f"   ⚠️  Error creating invoice: {e}")
                    db.session.rollback()
                    continue
            
            # Commit invoices for this organization
            try:
                db.session.commit()
                financial_data_created += invoices_created
                print(f"   ✅ Created {invoices_created} invoices for {org.name}")
            except Exception as e:
                db.session.rollback()
                print(f"   ❌ Error committing invoices for {org.name}: {e}")
        
        print(f"   ✅ Financial data seeded successfully ({financial_data_created} records)")


    def seed_inventory_data(self):
        """Seed inventory data using fixed staff lookup"""
        print("📦 Seeding inventory data...")
        
        from app.models import Staff
        
        product_types = ProductType.query.all()
        transaction_types = InventoryTransactionType.query.all()
        
        inventory_data_created = 0
        
        for org in self.organizations:
            # Get staff for this organization - use public_id (VARCHAR)
            org_staff = Staff.query.filter_by(organization_id=org.public_id).all()
            if not org_staff:
                print(f"   ⚠️  No staff for {org.name} (looking for org_id: {org.public_id})")
                continue
                
            print(f"   📦 Creating inventory data for {org.name} ({len(org_staff)} staff)")
            
            # Create product categories
            categories = ['Dental Supplies', 'Medications', 'Equipment', 'Office Supplies']
            product_categories = []
            
            for category_name in categories:
                category = ProductCategory()
                category.organization_id = org.public_id
                category.name = category_name
                category.description = f"{category_name} for dental practice"
                category.is_active = True
                db.session.add(category)
                product_categories.append(category)
            
            db.session.flush()
            
            # Create suppliers
            suppliers = []
            for i in range(3):
                supplier = Supplier()
                supplier.organization_id = org.public_id
                supplier.name = f"{self.fake.company()} Dental Supplies"
                supplier.contact_name = self.fake.name()
                supplier.contact_email = self.fake.email()
                supplier.contact_phone = self.fake.phone_number()
                supplier.address = self.fake.street_address()
                supplier.city = self.fake.city()
                supplier.state = self.fake.state()
                supplier.country = "USA"
                supplier.postal_code = self.fake.zipcode()
                supplier.payment_terms = "Net 30"
                supplier.is_active = True
                
                db.session.add(supplier)
                suppliers.append(supplier)
            
            db.session.flush()
            
            # Create products with all required fields
            products_created = 0
            dental_products = [
                ('Dental Floss', 'Waxed dental floss 50m', 1.50, 2.50, 'roll'),
                ('Toothpaste', 'Fluoride toothpaste 100ml', 2.25, 3.75, 'tube'),
                ('Examination Gloves', 'Latex-free gloves medium', 7.50, 12.50, 'box'),
                ('Disposable Masks', 'Surgical masks 50pc', 5.39, 8.99, 'box'),
                ('Dental Bibs', 'Disposable dental bibs', 9.45, 15.75, 'pack'),
                ('Mouthwash', 'Antiseptic mouthwash 500ml', 4.20, 7.00, 'bottle'),
                ('Dental Probes', 'Sterile dental probes', 8.00, 13.33, 'pack'),
                ('Cotton Rolls', 'Sterile cotton rolls 100pc', 6.75, 11.25, 'box'),
            ]
            
            for product_name, description, cost_price, selling_price, unit_of_measure in dental_products:
                product_type = product_types[0] if product_types else None
                category = random.choice(product_categories)
                supplier = random.choice(suppliers)
                
                product = Product()
                product.organization_id = org.public_id
                product.name = product_name
                product.description = description
                product.sku = f"SKU-{fake.random_number(digits=6)}"
                product.product_type_id = product_type.id if product_type else 1
                product.category_id = category.id
                product.unit_of_measure = unit_of_measure
                product.cost_price = cost_price
                product.selling_price = selling_price  # REQUIRED FIELD ← ADD THIS
                product.current_price = selling_price  # Also set current_price
                product.reorder_level = random.randint(5, 20)
                product.preferred_supplier_id = supplier.id
                product.is_active = True
                
                db.session.add(product)
                products_created += 1
            
            # Commit products for this organization
            try:
                db.session.commit()
                inventory_data_created += products_created
                print(f"   ✅ Created {products_created} products for {org.name}")
            except Exception as e:
                db.session.rollback()
                print(f"   ❌ Error committing products for {org.name}: {e}")
        
        print(f"   ✅ Inventory data seeded successfully ({inventory_data_created} products)")


    def seed_analytics_data(self):
        """Seed analytics data with required fields"""
        print("📊 Seeding analytics data...")
        
        analytics_data_created = 0
        
        for org in self.organizations:
            try:
                # Get any user from this organization for created_by field
                org_users = [u for u in self.users if u.organization_id == org.public_id]
                if not org_users:
                    print(f"   ⚠️  No users for {org.name} - skipping analytics data")
                    continue
                
                created_by_user = org_users[0]
                
                # Create a simple KPI with required calculation_query
                kpi = KPI()
                kpi.organization_id = org.public_id
                kpi.name = "Monthly Patient Visits"
                kpi.description = "Track monthly patient visits"
                kpi.category = "clinical"
                kpi.calculation_query = "SELECT COUNT(*) FROM appointments WHERE organization_id = :org_id AND start_time BETWEEN :start_date AND :end_date"  # Required field
                kpi.target_value = 100
                kpi.unit = "visits"
                kpi.format_type = "number"
                kpi.decimal_places = 0
                kpi.alert_enabled = False
                kpi.is_active = True
                
                db.session.add(kpi)
                analytics_data_created += 1
                
            except Exception as e:
                print(f"   ⚠️  Error creating analytics data for {org.name}: {e}")
        
        db.session.flush()
        print(f"   ✅ Analytics data seeded successfully ({analytics_data_created} records)")




def seed_demo_data():
    """Main function to seed all demo data"""
    seeder = DemoDataSeeder()
    seeder.seed_all_data()

if __name__ == '__main__':
    seed_demo_data()