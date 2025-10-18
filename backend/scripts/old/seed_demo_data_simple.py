# backend/scripts/seed_demo_data_simple.py
import os
import sys
from datetime import datetime, timedelta
import random
from faker import Faker
from sqlalchemy import text

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import (db, bcrypt,
    Tenant, Organization, User, Staff, Role, Permission,
    Patient, Gender, OrganizationType, SubscriptionPlan, Currency,
    IndustryType, TenantStatus
)

fake = Faker()

class SimpleDemoDataSeeder:
    def __init__(self):
        self.app = create_app()
        self.fake = Faker()
        self.admin_email = "sojipariola@gmail.com"
        self.admin_password = "Soji1111"
        
    def seed_all_data(self):
        """Seed minimal demo data"""
        with self.app.app_context():
            print("🚀 Starting simple demo data seeding...")
            
            try:
                # Clear minimal data first
                self.clear_minimal_data()
                
                # Create basic structure
                self.seed_lookup_data()
                self.seed_tenant_and_orgs()
                self.seed_users_and_roles()
                self.seed_patients()
                
                db.session.commit()
                print("✅ Simple demo data seeded successfully!")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error seeding demo data: {e}")
                import traceback
                print(f"🔍 Detailed traceback: {traceback.format_exc()}")
                raise
    
    def clear_minimal_data(self):
        """Clear minimal existing data"""
        print("🧹 Clearing minimal existing data...")
        
        try:
            # Clear in dependency order
            models_to_clear = [
                Patient, Staff, User, Role, Organization, Tenant
            ]
            
            for model in models_to_clear:
                try:
                    count = db.session.query(model).delete()
                    print(f"   🧹 Cleared {count} records from {model.__name__}")
                except Exception as e:
                    print(f"   ⚠️  Could not clear {model.__name__}: {e}")
            
            # Clear relationship tables with proper text()
            try:
                db.session.execute(text("DELETE FROM user_roles"))
                print("   🧹 Cleared user_roles table")
            except Exception as e:
                print(f"   ⚠️  Could not clear user_roles: {e}")
            
            db.session.commit()
            print("✅ Minimal data cleared")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error clearing data: {e}")
            raise
    
    def seed_lookup_data(self):
        """Ensure basic lookup data exists"""
        print("📋 Ensuring lookup data exists...")
        
        # Check and create essential lookup data
        if not Gender.query.first():
            print("   ⚠️  Creating default genders...")
            genders = [
                Gender(code='male', name='Male', sort_order=1),
                Gender(code='female', name='Female', sort_order=2),
                Gender(code='other', name='Other', sort_order=3)
            ]
            for gender in genders:
                db.session.add(gender)
        
        if not OrganizationType.query.first():
            print("   ⚠️  Creating default organization type...")
            org_type = OrganizationType(
                code='clinic',
                name='Dental Clinic',
                description='Dental practice clinic'
            )
            db.session.add(org_type)
        
        if not SubscriptionPlan.query.first():
            print("   ⚠️  Creating default subscription plan...")
            subscription_plan = SubscriptionPlan(
                code='professional',
                name='Professional Plan',
                description='Professional subscription plan',
                price_monthly=99,
                price_yearly=990,
                max_users=25,
                max_patients=5000
            )
            db.session.add(subscription_plan)
        
        if not Currency.query.first():
            print("   ⚠️  Creating default currency...")
            currency = Currency(
                code='USD',
                name='US Dollar',
                symbol='$',
                decimal_places=2
            )
            db.session.add(currency)
        
        # CRITICAL: Add IndustryType for Tenant
        if not IndustryType.query.first():
            print("   ⚠️  Creating default industry type...")
            industry_type = IndustryType(
                code='dental',
                name='Dental',
                description='Dental healthcare industry',
                category='healthcare'
            )
            db.session.add(industry_type)
        
        # CRITICAL: Add TenantStatus for Tenant
        if not TenantStatus.query.first():
            print("   ⚠️  Creating default tenant status...")
            tenant_status = TenantStatus(
                code='active',
                name='Active',
                description='Active tenant status'
            )
            db.session.add(tenant_status)
        
        db.session.flush()
        print("   ✅ Lookup data ensured")
    
    def seed_tenant_and_orgs(self):
        """Seed tenant and organizations with correct fields"""
        print("🏢 Seeding tenant and organizations...")
        
        # Get required lookup values
        industry_type = IndustryType.query.first()
        tenant_status = TenantStatus.query.first()
        subscription_plan = SubscriptionPlan.query.first()
        org_type = OrganizationType.query.first()
        currency = Currency.query.first()
        
        if not industry_type:
            print("   ❌ No industry type found - cannot create tenant")
            return
        if not tenant_status:
            print("   ❌ No tenant status found - cannot create tenant")
            return
        if not org_type:
            print("   ❌ No organization type found - cannot create organizations")
            return
        
        # Create tenant with correct fields
        tenant = Tenant(
            name="Dentaloist Demo Tenant",
            domain="demo.dentaloist.com",
            display_name="Dentaloist Demo",
            description="Demo tenant for Dentaloist application",
            industry_id=industry_type.id,
            status_id=tenant_status.id,
            contact_email="admin@dentaloistdemo.com",
            contact_phone=self.fake.phone_number(),
            website="https://demo.dentaloist.com",
            address_line1=self.fake.street_address(),
            city=self.fake.city(),
            state=self.fake.state(),
            postal_code=self.fake.zipcode(),
            country="USA",
            timezone="America/New_York",
            subscription_plan_id=subscription_plan.id if subscription_plan else None,
            max_organizations=10,
            max_users=100,
            max_patients=10000,
            max_storage_mb=1024,
            features_enabled={},
            theme_settings={},
            settings={},
            business_hours={},
            holiday_schedule={},
            data_retention_days=1095,
            compliance_settings={},
            is_active=True
        )
        db.session.add(tenant)
        db.session.flush()
        print(f"   ✅ Created tenant: {tenant.name}")
        
        # Create organizations with ACTUAL field names from the error message
        org_names = [
            "Bright Smile Dental Clinic",
            "Perfect Teeth Orthodontics", 
            "Family Dental Care Center"
        ]
        
        self.organizations = []
        for i, org_name in enumerate(org_names):
            # Use only the fields that actually exist in your Organization model
            organization = Organization(
                public_id=f"org_{i+1}",
                name=org_name,
                description=f"Dental practice - {org_name}",
                address=self.fake.address(),
                city=self.fake.city(),
                state=self.fake.state(),
                postal_code=self.fake.zipcode(),
                country="USA",
                phone=self.fake.phone_number(),
                email=f"info@{org_name.lower().replace(' ', '')}.com",
                website=f"www.{org_name.lower().replace(' ', '')}.com",
                organization_type_id=org_type.id,  # REQUIRED field
                tax_id=f"TAX-{self.fake.random_number(digits=9)}",
                business_type="Dental Practice",
                industry="Healthcare",
                max_staff=20,
                max_patients=1000,
                status="active",
                is_verified=True,
                is_active=True
            )
            db.session.add(organization)
            self.organizations.append(organization)
            print(f"   ✅ Created organization: {org_name}")
        
        db.session.flush()
        print("   ✅ Tenant and organizations seeded")
    
    def seed_users_and_roles(self):
        """Seed users and roles"""
        print("👥 Seeding users and roles...")
        
        gender_male = Gender.query.filter_by(code='male').first()
        
        # Create global permissions first
        permissions = [
            Permission(name='user_read', description='View users', category='user_management'),
            Permission(name='patient_read', description='View patients', category='patient_management'),
            Permission(name='appointment_read', description='View appointments', category='clinical_operations'),
        ]
        
        for perm in permissions:
            if not Permission.query.filter_by(name=perm.name).first():
                db.session.add(perm)
        
        db.session.flush()
        
        self.users = []
        self.staff_members = []
        
        for i, org in enumerate(self.organizations):
            # Create organization-specific admin role
            admin_role = Role(
                name='Administrator',
                description='Organization administrator',
                organization_id=org.id,
                is_system_role=True
            )
            db.session.add(admin_role)
            db.session.flush()
            
            # Assign permissions to admin role
            all_permissions = Permission.query.all()
            admin_role.permissions = all_permissions
            
            # Create admin user
            admin_user = User(
                public_id=f"user_admin_{i+1}",
                email=self.admin_email if i == 0 else f"admin{i+1}@{org.name.lower().replace(' ', '')}.com",
                password_hash=bcrypt.generate_password_hash(self.admin_password).decode('utf-8'),
                first_name="Soji" if i == 0 else self.fake.first_name(),
                last_name="Pariola" if i == 0 else self.fake.last_name(),
                phone=self.fake.phone_number(),
                date_of_birth=self.fake.date_of_birth(minimum_age=25, maximum_age=55),
                gender_id=gender_male.id if gender_male else None,
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
            
            # Assign admin role to user
            admin_user.roles.append(admin_role)
            
            # Create staff record - FIXED: use employee_id instead of organization_id
            admin_staff = Staff(
                user=admin_user,
                organization=org,
                employee_id=f"EMP{org.public_id.upper()}{i+1:03d}",  # FIXED: employee_id not organization_id
                hire_date=self.fake.date_between(start_date='-2y', end_date='today'),
                job_title="Practice Administrator",
                department="Administration",
                is_active=True
            )
            db.session.add(admin_staff)
            self.staff_members.append(admin_staff)
            
            print(f"   ✅ Created admin user for {org.name}: {admin_user.email}")
        
        db.session.flush()
        print("   ✅ Users and roles seeded")
    
    def seed_patients(self):
        """Seed patients"""
        print("👥 Seeding patients...")
        
        genders = Gender.query.all()
        if not genders:
            print("   ⚠️  No genders found, skipping patients")
            return
        
        patient_count = 0
        for org in self.organizations:
            num_patients = random.randint(5, 10)  # Start with fewer patients
            
            for i in range(num_patients):
                # Use only fields that exist in your Patient model
                patient = Patient(
                    public_id=f"pat_{org.public_id}_{i+1:03d}",
                    organization=org,
                    first_name=self.fake.first_name(),
                    last_name=self.fake.last_name(),
                    email=self.fake.email(),
                    phone=self.fake.phone_number(),
                    date_of_birth=self.fake.date_of_birth(minimum_age=5, maximum_age=80),
                    gender_id=random.choice(genders).id,
                    address=self.fake.address(),
                    city=self.fake.city(),
                    state=self.fake.state(),
                    country="USA",
                    postal_code=self.fake.zipcode(),
                    is_active=True
                )
                db.session.add(patient)
                patient_count += 1
        
        db.session.flush()
        print(f"   ✅ Seeded {patient_count} patients")

def seed_simple_demo_data():
    """Main function to seed simple demo data"""
    seeder = SimpleDemoDataSeeder()
    seeder.seed_all_data()

if __name__ == '__main__':
    seed_simple_demo_data()