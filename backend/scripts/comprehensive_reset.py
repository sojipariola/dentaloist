#!/usr/bin/env python3
"""
COMPREHENSIVE DATABASE RESET
Resets database and seeds all tables based on schema
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
import random


# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# def seed_product

from app.models import Organization, User, Staff, Patient
from app.models import Treatment, Patient, Staff, TreatmentType, TreatmentStatus, TreatmentPriority
from datetime import datetime, date

def comprehensive_reset():
    """Complete database reset with comprehensive seeding"""
    print("🔄 COMPREHENSIVE DATABASE RESET")
    print("=" * 50)
    
    # Confirm reset
    response = input("❓ Are you sure you want to reset everything? (yes/NO): ")
    if response.lower() != 'yes':
        print("❌ Reset cancelled.")
        return
    
    # Step 1: Reset database
    print("\n1️⃣  STEP 1: Resetting database...")
    reset_database()
    
    # Step 2: Seed lookups
    print("\n2️⃣  STEP 2: Seeding lookup data...")
    seed_lookup_data()
    
    # Step 3: Seed core data based on schema
    print("\n3️⃣  STEP 3: Seeding core data...")
    seed_core_data()
    
    # Step 4: Verify
    print("\n4️⃣  STEP 4: Verifying data...")
    verify_data()
    
    print("\n🎉 COMPREHENSIVE RESET COMPLETE!")

def seed_lookup_data():
    """Seed lookup tables using the unified seeder"""
    try:
        from scripts.seed_lookups_unified import seed_all_lookups
        seed_all_lookups()
    except Exception as e:
        print(f"❌ Error seeding lookup data: {e}")
        raise

def reset_database():
    """Reset database completely"""
    print("🗑️  Resetting database...")
    
    # Remove migrations
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
        print("✅ Removed migrations directory")
    
    # Remove database
    db_path = Path('instance/dentaloist.db')
    if db_path.exists():
        os.remove(db_path)
        print("✅ Removed database file")
    
    # Create instance directory
    instance_dir = Path('instance')
    if not instance_dir.exists():
        instance_dir.mkdir(parents=True)
        print("✅ Created instance directory")
    
    # Recreate database using emergency fix approach
    create_database_directly()

def create_database_directly():
    """Create database directly using SQLAlchemy"""
    print("🔄 Creating database directly...")
    
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    # Create minimal app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'reset-key'
    
    db = SQLAlchemy(app)
    
    # Import and create all models
    try:
        # Set environment first
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_APP'] = 'app:create_app()'
        
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app import db
            db.create_all()
            print("✅ All tables created successfully")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        # Fallback to simple tables
        create_minimal_tables(db, app)

def create_minimal_tables(db, app):
    """Create minimal tables as fallback"""
    print("🔄 Creating minimal tables (fallback)...")
    
    # Define minimal essential models
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(255), nullable=False)
        is_active = db.Column(db.Boolean, default=True)
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(255), nullable=False)
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
    
    class Patient(db.Model):
        __tablename__ = 'patients'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50))
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
    
    with app.app_context():
        db.create_all()
        print("✅ Minimal tables created")

def seed_lookups():
    """Seed all lookup data"""
    print("📋 Seeding lookup data...")
    
    try:
        result = subprocess.run([
            sys.executable, 'scripts/seed_lookups.py'
        ], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Lookup seeding issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Lookup seeding failed: {e}")

def seed_core_data():
    """Seed all core data based on schema analysis"""
    print("🌱 Seeding core data...")
    
    # Set environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'app:create_app()'
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Import all models
            from app.models import (
                # Core models
                Organization, User, Staff, 
                # Clinical models
                Patient, Appointment, Treatment, ClinicalNote, Allergy,
                Prescription, VitalSign, TreatmentPlan,
                # Financial models
                Invoice, Payment, InsurancePlan, Expense, FinancialTransaction,
                # Inventory models
                Product, ProductCategory, Supplier,
                # Analytics models
                Widget, AnalyticsDashboard
            )
            
            # Check if we already have data
            org_count = Organization.query.count()
            if org_count > 0:
                print("ℹ️  Database already has data. Skipping seeding.")
                return
            
            print("📊 Starting comprehensive data seeding...")
            
            # Seed in dependency order
            seed_organizations_and_users(db)
            seed_patients(db) 
            seed_staff(db)
            seed_appointments(db)
            seed_treatments(db)
            seed_invoices(db)
            seed_products(db)
            seed_analytics(db)
            
            print("✅ All core data seeded successfully")
            
    except Exception as e:
        print(f"❌ Error seeding core data: {e}")
        import traceback
        traceback.print_exc()

def seed_organizations_and_users(db):
    """Seed organizations and users"""
    from app.models import Organization, User
    
    print("\n🏢 Seeding organizations and users...")
    
    organizations = [
        {
            'public_id': 'org_001',
            'name': 'Bright Smile Dental Clinic',
            'email': 'info@brightsmiledental.com',
            'phone': '+1-555-0101',
            'address': '123 Dental Street, Springfield, IL 62701, USA',
            'city': 'Springfield',
            'state': 'IL',
            'postal_code': '62701',
            'country': 'USA',
            'website': 'https://brightsmiledental.com',
            'timezone': 'America/Chicago',
            'organization_type_id': 1,
        },
        {
            'public_id': 'org_002', 
            'name': 'Perfect Teeth Orthodontics',
            'email': 'contact@perfectteeth.com',
            'phone': '+1-555-0102',
            'address': '456 Ortho Avenue, Shelbyville, IL 62702, USA',
            'city': 'Shelbyville',
            'state': 'IL', 
            'postal_code': '62702',
            'country': 'USA',
            'website': 'https://perfectteeth.com',
            'timezone': 'America/Chicago',
            'organization_type_id': 1,
        },
        {
            'public_id': 'org_003',
            'name': 'Family Dental Care Center',
            'email': 'hello@familydental.com', 
            'phone': '+1-555-0103',
            'address': '789 Care Boulevard, Capital City, IL 62703, USA',
            'city': 'Capital City',
            'state': 'IL',
            'postal_code': '62703',
            'country': 'USA',
            'website': 'https://familydental.com',
            'timezone': 'America/Chicago',
            'organization_type_id': 1,
        }
    ]
    
    # Create organizations
    org_objects = []
    for org_data in organizations:
        org = Organization(**org_data)
        db.session.add(org)
        org_objects.append(org)
    
    db.session.commit()
    print(f"✅ Created {len(org_objects)} organizations")
    
    # Create users for each organization
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia']
    
    user_count = 0
    for org in org_objects:
        # Admin user
        admin_user = User(
            public_id=f'user_{org.public_id}_admin',
            email=f'admin@{org.public_id}.com',
            password_hash='$2b$12$hashed_password',
            first_name='Admin',
            last_name='User',
            phone=f'+1-555-{random.randint(1000,9999)}',
            organization_id=org.public_id,
            user_role_id=1,
            email_verified=True
        )
        db.session.add(admin_user)
        user_count += 1
        
        # Staff users
        for i in range(3):
            staff_user = User(
                public_id=f'user_{org.public_id}_staff{i+1}',
                email=f'staff{i+1}@{org.public_id}.com',
                password_hash='$2b$12$hashed_password',
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                phone=f'+1-555-{random.randint(1000,9999)}',
                organization_id=org.public_id,
                user_role_id=2,
                email_verified=True
            )
            db.session.add(staff_user)
            user_count += 1
    
    db.session.commit()
    print(f"✅ Created {user_count} users")

def seed_patients(db):
    """Seed patients"""
    from app.models import Patient, Organization
    import json
    
    print("👤 Seeding patients...")
    
    organizations = Organization.query.all()
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    
    patient_count = 0
    for org in organizations:
        for i in range(8):  # 8 patients per org
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            patient = Patient(
                public_id=f'patient_{org.public_id}_{i+1:03d}',
                first_name=first_name,
                last_name=last_name,
                email=f'{first_name.lower()}.{last_name.lower()}@example.com',
                phone=f'+1-555-{random.randint(1000,9999)}',
                date_of_birth=datetime(1980 + random.randint(0, 40), random.randint(1, 12), random.randint(1, 28)),
                gender=random.choice(['Male', 'Female']),
                organization_id=org.public_id,
                address=json.dumps({
                    'street': f'{random.randint(100, 999)} Main St',
                    'city': org.city,
                    'state': org.state,
                    'postal_code': org.postal_code,
                    'country': org.country
                })
            )
            db.session.add(patient)
            patient_count += 1
    
    db.session.commit()
    print(f"✅ Created {patient_count} patients")

def seed_staff(db):
    """Seed staff records for all organizations"""
    
    organizations = Organization.query.all()
    
    for org in organizations:
        # Use no_autoflush to prevent premature flushing
        with db.session.no_autoflush:
            users = User.query.filter_by(organization_id=org.public_id).all()
            
            for i, user in enumerate(users):
                staff = Staff(
                    organization_id=org.public_id,
                    user_id=user.id,
                    staff_number=f"STAFF-{org.public_id}-{i+1:03d}",
                    job_title="Dentist" if i == 0 else "Dental Assistant",
                    department="Dentistry",
                    hire_date=date.today(),  # Required field
                    employment_type="full_time",
                    status="active",
                    public_id=f"staff_{user.public_id}"
                )
                
                db.session.add(staff)
    
    try:
        db.session.commit()
        print(f"✅ Created staff records for {len(organizations)} organizations")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating staff: {e}")
        raise

def seed_appointments(db): # seed_treatment
    """Seed appointments"""
    from app.models import Appointment, Patient, User, Organization
    
    print("📅 Seeding appointments...")
    
    organizations = Organization.query.all()
    appointment_count = 0
    base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    for org in organizations:
        patients = Patient.query.filter_by(organization_id=org.public_id).all()
        users = User.query.filter_by(organization_id=org.public_id).all()
        
        for i in range(5):  # 5 appointments per org
            if patients and users:
                patient = random.choice(patients)
                user = random.choice(users)
                start_time = base_date + timedelta(days=i*3, hours=random.randint(0, 6))
                end_time = start_time + timedelta(hours=1)
                
                appointment = Appointment(
                    public_id=f'appt_{org.public_id}_{i+1:03d}',
                    title=f'Dental Checkup - {patient.first_name} {patient.last_name}',
                    description='Routine dental examination and cleaning',
                    start_time=start_time,
                    end_time=end_time,
                    duration=60,
                    organization_id=org.public_id,
                    patient_id=patient.id,
                    dentist_id=user.id,
                    appointment_type_id=1,
                    status_id=1
                )
                db.session.add(appointment)
                appointment_count += 1
    
    db.session.commit()
    print(f"✅ Created {appointment_count} appointments")

def seed_treatments(db):
    """Seed treatment records with proper lookup relationships"""
    
    from datetime import datetime, timedelta
    import random
    
    print("🦷 Seeding treatments...")
    
    # Clear any existing transactions
    db.session.rollback()
    
    patients = Patient.query.all()
    
    if not patients:
        print("❌ No patients found for treatment seeding")
        return
    
    # Get lookup values (should now exist)
    treatment_types = TreatmentType.query.all()
    statuses = TreatmentStatus.query.all()
    priorities = TreatmentPriority.query.all()
    
    if not treatment_types:
        print("❌ No treatment types found - lookup seeding may have failed")
        return
    
    treatment_counter = 1
    created_count = 0
    
    for patient in patients:
        # Get staff from the same organization
        staff_members = Staff.query.filter_by(organization_id=patient.organization_id).all()
        
        if not staff_members:
            print(f"⚠️  No staff found for organization {patient.organization_id}")
            continue
        
        # Get dentists and assistants
        dentists = [s for s in staff_members if s.job_title == "Dentist"]
        if not dentists:
            dentists = staff_members  # Fallback to any staff
        
        assistants = [s for s in staff_members if s.job_title == "Dental Assistant"]
        
        for i in range(random.randint(1, 2)):  # 1-2 treatments per patient
            try:
                dentist = random.choice(dentists)
                assistant = random.choice(assistants) if assistants else None
                
                # Create scheduled date
                scheduled_date = datetime.now() + timedelta(days=random.randint(1, 30))
                
                treatment = Treatment()
                
                # Set required relationships
                treatment.tenant_id = getattr(patient, 'tenant_id', 1)  # Fallback if needed
                treatment.patient_id = patient.id
                treatment.dentist_id = dentist.id
                treatment.assistant_id = assistant.id if assistant else None
                treatment.treatment_type_id = random.choice(treatment_types).id
                treatment.status_id = random.choice(statuses).id
                treatment.priority_id = random.choice(priorities).id
                
                # Set basic info
                treatment_type = TreatmentType.query.get(treatment.treatment_type_id)
                treatment.name = f"{treatment_type.name}"
                treatment.description = f"{treatment_type.name} for {patient.first_name} {patient.last_name}"
                treatment.scheduled_date = scheduled_date
                treatment.estimated_duration = random.choice([30, 45, 60, 90])
                
                # Set optional fields
                treatment.procedure_code = f"CDT-{random.randint(1000, 9999)}"
                treatment.cost_estimate = random.uniform(50, 500)
                treatment.public_id = f"treatment_{treatment_counter:03d}"
                treatment.is_active = True
                
                db.session.add(treatment)
                created_count += 1
                treatment_counter += 1
                
            except Exception as e:
                print(f"⚠️  Warning: Could not create treatment for patient {patient.id}: {e}")
                continue
    
    try:
        db.session.commit()
        print(f"✅ Created {created_count} treatments")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating treatments: {e}")
        raise


def seed_invoices(db):
    """Seed invoices"""
    from app.models import Invoice, Patient, Organization
    import json
    
    print("🧾 Seeding invoices...")
    
    organizations = Organization.query.all()
    invoice_count = 0
    
    for org in organizations:
        patients = Patient.query.filter_by(organization_id=org.public_id).all()
        
        for i in range(4):  # 4 invoices per org
            if patients:
                patient = random.choice(patients)
                
                items = [
                    {
                        'description': 'Dental Examination',
                        'quantity': 1,
                        'unit_price': 85.00,
                        'total': 85.00
                    },
                    {
                        'description': 'Teeth Cleaning',
                        'quantity': 1, 
                        'unit_price': 65.00,
                        'total': 65.00
                    }
                ]
                
                invoice = Invoice(
                    public_id=f'inv_{org.public_id}_{i+1:03d}',
                    invoice_number=f'INV-{org.public_id.upper()}-{i+1:04d}',
                    invoice_date=datetime.now(),
                    due_date=datetime.now() + timedelta(days=30),
                    organization_id=org.public_id,
                    patient_id=patient.id,
                    status_id=1,
                    currency_id=1,
                    items=json.dumps(items),
                    subtotal=150.00,
                    tax_amount=12.00,
                    total_amount=162.00,
                    balance_due=162.00,
                    payment_terms='Net 30'
                )
                db.session.add(invoice)
                invoice_count += 1
    
    db.session.commit()
    print(f"✅ Created {invoice_count} invoices")

def seed_products(db):
    """Seed product records with centralized imports"""
    
    print("📦 Seeding products...")
    
    try:
        # CORRECT: Import everything from app.models
        from app.models import Product, Organization, ProductType, ExpenseCategory
        
        print("✅ All imports successful from app.models")
        
        organizations = Organization.query.all()
        product_types = ProductType.query.all()
        categories = ExpenseCategory.query.all()
        
        print(f"   Found {len(organizations)} organizations, {len(product_types)} product types, {len(categories)} categories")
        
        if not organizations:
            print("❌ No organizations found for product seeding")
            return
            
        if not product_types:
            print("❌ No product types found")
            return
        
        product_counter = 1
        created_count = 0
        
        for org in organizations:
            print(f"   Creating products for {org.name}...")
            
            sample_products = [
                {
                    'name': 'Toothbrush',
                    'description': 'Soft-bristle toothbrush for daily oral care',
                    'cost_price': 2.5,
                    'selling_price': 5.0,
                    'product_type_code': 'MEDICAL_SUPPLY',
                    'category_code': 'MEDICAL_SUPPLIES',
                    'current_stock': 100,
                },
                {
                    'name': 'Toothpaste',
                    'description': 'Fluoride toothpaste for cavity protection',
                    'cost_price': 1.5, 
                    'selling_price': 3.0,
                    'product_type_code': 'MEDICAL_SUPPLY',
                    'category_code': 'MEDICAL_SUPPLIES',
                    'current_stock': 80,
                },
                {
                    'name': 'Dental Floss',
                    'description': 'Waxed dental floss for interdental cleaning',
                    'cost_price': 0.8,
                    'selling_price': 2.0,
                    'product_type_code': 'MEDICAL_SUPPLY',
                    'category_code': 'MEDICAL_SUPPLIES', 
                    'current_stock': 150,
                }
            ]
            
            for product_data in sample_products:
                try:
                    # Find the product type by code
                    product_type = next((pt for pt in product_types if pt.code == product_data['product_type_code']), None)
                    if not product_type:
                        available_codes = [pt.code for pt in product_types]
                        print(f"      ❌ Product type '{product_data['product_type_code']}' not found. Available: {available_codes}")
                        continue
                    
                    # Find the category by code
                    category = next((cat for cat in categories if cat.code == product_data['category_code']), None)
                    if not category:
                        available_categories = [cat.code for cat in categories]
                        print(f"      ❌ Category '{product_data['category_code']}' not found. Available: {available_categories}")
                        continue
                    
                    # Create the product
                    product = Product(
                        organization_id=org.public_id,
                        product_type_id=product_type.id,
                        category_id=category.id,
                        name=product_data['name'],
                        description=product_data['description'],
                        cost_price=product_data['cost_price'],
                        selling_price=product_data['selling_price'],
                        current_stock=product_data['current_stock'],
                        status='active',
                        is_active=True,
                        public_id=f"product_{org.public_id}_{product_counter:03d}"
                    )
                    
                    db.session.add(product)
                    created_count += 1
                    product_counter += 1
                    
                    print(f"      ✅ Created: {product_data['name']}")
                    
                except Exception as e:
                    print(f"      ❌ Failed to create {product_data['name']}: {e}")
                    continue
        
        db.session.commit()
        print(f"✅ Successfully created {created_count} products")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in products seeding: {e}")


def seed_analytics(db):
    """Seed analytics data"""
    from app.models import AnalyticsDashboard, Widget, Organization, User
    import json
    
    print("📊 Seeding analytics...")
    
    organizations = Organization.query.all()
    
    for org in organizations:
        users = User.query.filter_by(organization_id=org.public_id).all()
        
        if users:
            # Create dashboard
            dashboard = AnalyticsDashboard(
                public_id=f'dash_{org.public_id}',
                name=f'{org.name} Analytics',
                description=f'Main analytics dashboard for {org.name}',
                organization_id=org.public_id,
                layout_type='grid',
                is_default=True,
                is_public=False
            )
            db.session.add(dashboard)
            
            # Create widget
            widget = Widget(
                public_id=f'widget_{org.public_id}_main',
                user_id=users[0].id,
                organization_id=org.public_id,
                widget_type_id=1,
                title='Patient Overview',
                description='Key patient metrics',
                size='medium',
                config=json.dumps({'metrics': ['total_patients', 'new_this_month']}),
                data_source=json.dumps({'type': 'patient_metrics'}),
                is_visible=True
            )
            db.session.add(widget)
    
    db.session.commit()
    print("✅ Created analytics dashboards and widgets")

def verify_data():
    """Verify all data was seeded correctly"""
    print("🔍 Verifying data...")
    
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'app:create_app()'
    
    from app import create_app
    from app.models import (
        Organization, User, Staff, Patient, Appointment, 
        Treatment, Invoice, Product, AnalyticsDashboard
    )
    
    app = create_app()
    
    with app.app_context():
        print("\n📈 DATA VERIFICATION SUMMARY")
        print("=" * 40)
        
        counts = {
            'Organizations': Organization.query.count(),
            'Users': User.query.count(),
            'Staff': Staff.query.count(),
            'Patients': Patient.query.count(),
            'Appointments': Appointment.query.count(),
            'Treatments': Treatment.query.count(),
            'Invoices': Invoice.query.count(),
            'Products': Product.query.count(),
            'Analytics Dashboards': AnalyticsDashboard.query.count()
        }
        
        for model_name, count in counts.items():
            print(f"📊 {model_name}: {count}")
        
        # Check tenant isolation
        print(f"\n🔒 TENANT ISOLATION CHECK:")
        organizations = Organization.query.all()
        for org in organizations:
            patients = Patient.query.filter_by(organization_id=org.public_id).count()
            users = User.query.filter_by(organization_id=org.public_id).count()
            print(f"   {org.name}: {patients} patients, {users} users")

if __name__ == '__main__':
    comprehensive_reset()


# def main():