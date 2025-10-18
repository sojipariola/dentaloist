#!/usr/bin/env python3
"""
Seed tenant data - fixed user.id issue
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random
import json

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def seed_tenants_fixed():
    """Seed tenant data - fixed user.id issue"""
    print("🌱 SEEDING TENANT DATA (FIXED USER.ID)")
    print("=" * 50)
    
    # Set environment
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'app:create_app()'
    
    try:
        from app import create_app, db
        app = create_app()
        
        with app.app_context():
            # Import models
            from app.models import (
                Organization, User, Staff, Patient, Appointment, 
                AvailabilitySlot, Invoice, FinancialTransaction, Widget, AnalyticsDashboard
            )
            
            # Check if we already have data
            org_count = Organization.query.count()
            if org_count > 0:
                print(f"ℹ️  Database already has {org_count} organizations. Skipping seeding.")
                return
            
            print("📊 Starting tenant data seeding...")
            
            # Create organizations
            print("\n🏢 Creating organizations...")
            organizations_data = [
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
                    'tenant_id': None
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
                    'tenant_id': None
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
                    'tenant_id': None
                }
            ]
            
            org_objects = []
            for org_data in organizations_data:
                org = Organization(**org_data)
                db.session.add(org)
                org_objects.append(org)
                print(f"   ✅ {org.name}")
            
            db.session.commit()
            print("✅ Organizations committed to database")
            
            # Seed data for each organization
            seed_organization_data(org_objects, db)
            
            print(f"\n🎉 TENANT SEEDING COMPLETE!")
            
    except Exception as e:
        print(f"❌ Error in tenant seeding: {e}")
        import traceback
        traceback.print_exc()

def seed_organization_data(org_objects, db):
    """Seed data for each organization - fixed user.id issue"""
    from app.models import User, Staff, Patient, Appointment, AvailabilitySlot, Invoice, FinancialTransaction, Widget, AnalyticsDashboard
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    for org in org_objects:
        print(f"\n📊 Seeding data for {org.name}...")
        
        # Create users for this organization
        users_data = [
            {
                'public_id': f'user_{org.public_id}_admin',
                'email': f'admin@{org.public_id}.com',
                'password_hash': '$2b$12$hashed_password_for_dev',
                'first_name': 'Admin',
                'last_name': 'User',
                'phone': f'+1-555-{random.randint(1000,9999)}',
                'organization_id': org.public_id,
                'user_role_id': 1,
                'email_verified': True
            }
        ]
        
        # Add staff users
        for i in range(3):
            users_data.append({
                'public_id': f'user_{org.public_id}_staff{i+1}',
                'email': f'staff{i+1}@{org.public_id}.com',
                'password_hash': '$2b$12$hashed_password_for_dev',
                'first_name': random.choice(first_names),
                'last_name': random.choice(last_names),
                'phone': f'+1-555-{random.randint(1000,9999)}',
                'organization_id': org.public_id,
                'user_role_id': 2,
                'email_verified': True
            })
        
        # Create users and commit to get their IDs
        user_objects = []
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            user_objects.append(user)
        
        # Commit users to get their IDs
        db.session.commit()
        print(f"   👥 Created {len(users_data)} users")
        
        # Now create staff records with valid user IDs
        staff_objects = []
        for user in user_objects:
            staff = Staff(
                public_id=f'staff_{user.public_id}',
                organization_id=org.public_id,
                user_id=user.id,
                staff_number=f'STAFF-{org.public_id}-{user.id:03d}',
                job_title='Dental Professional',
                department='Dentistry',
                status='active'
            )
            db.session.add(staff)
            staff_objects.append(staff)
        
        db.session.commit()
        print(f"   💼 Created {len(staff_objects)} staff records")
        
        # Create patients (8 per org)
        patients_data = []
        for i in range(8):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            patients_data.append({
                'public_id': f'patient_{org.public_id}_{i+1:03d}',
                'first_name': first_name,
                'last_name': last_name,
                'email': f'{first_name.lower()}.{last_name.lower()}@example.com',
                'phone': f'+1-555-{random.randint(1000,9999)}',
                'date_of_birth': datetime(1980 + random.randint(0, 40), random.randint(1, 12), random.randint(1, 28)),
                'gender': random.choice(['Male', 'Female']),
                'organization_id': org.public_id,
                'address': json.dumps({
                    'street': f'{random.randint(100, 999)} Main St',
                    'city': org.city,
                    'state': org.state,
                    'postal_code': org.postal_code,
                    'country': org.country
                })
            })
        
        patient_objects = []
        for patient_data in patients_data:
            patient = Patient(**patient_data)
            db.session.add(patient)
            patient_objects.append(patient)
        
        db.session.commit()
        print(f"   👤 Created {len(patients_data)} patients")
        
        # Create appointments (3 per org)
        appointments_data = []
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        for i in range(3):
            if patient_objects and staff_objects:
                patient = random.choice(patient_objects)
                staff = random.choice(staff_objects)
                start_time = base_date + timedelta(days=i*7, hours=random.randint(0, 6))
                end_time = start_time + timedelta(hours=1)
                
                appointments_data.append({
                    'public_id': f'appt_{org.public_id}_{i+1:03d}',
                    'title': f'Dental Checkup - {patient.first_name} {patient.last_name}',
                    'description': f'Routine dental examination and cleaning',
                    'start_time': start_time,
                    'end_time': end_time,
                    'duration': 60,
                    'organization_id': org.public_id,
                    'patient_id': patient.id,
                    'dentist_id': staff.user_id,
                    'staff_id': staff.id,
                    'appointment_type_id': 1,
                    'status_id': 1
                })
        
        for appointment_data in appointments_data:
            appointment = Appointment(**appointment_data)
            db.session.add(appointment)
        
        db.session.commit()
        print(f"   📅 Created {len(appointments_data)} appointments")
        
        # Create invoices (4 per org)
        invoices_data = []
        for i in range(4):
            if patient_objects:
                patient = random.choice(patient_objects)
                
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
                
                invoices_data.append({
                    'public_id': f'inv_{org.public_id}_{i+1:03d}',
                    'invoice_number': f'INV-{org.public_id.upper()}-{i+1:04d}',
                    'invoice_date': datetime.now(),
                    'due_date': datetime.now() + timedelta(days=30),
                    'organization_id': org.public_id,
                    'patient_id': patient.id,
                    'status_id': 1,
                    'currency_id': 1,
                    'items': json.dumps(items),
                    'subtotal': 150.00,
                    'tax_amount': 12.00,
                    'total_amount': 162.00,
                    'balance_due': 162.00,
                    'payment_terms': 'Net 30'
                })
        
        for invoice_data in invoices_data:
            invoice = Invoice(**invoice_data)
            db.session.add(invoice)
        
        db.session.commit()
        print(f"   🧾 Created {len(invoices_data)} invoices")
        
        # Create financial transactions
        for invoice_data in invoices_data:
            transaction = FinancialTransaction(
                public_id=f'trans_{org.public_id}_{invoice_data["public_id"]}',
                organization_id=org.public_id,
                transaction_type_id=1,
                transaction_number=f'TRX-{org.public_id.upper()}-{random.randint(1000,9999)}',
                transaction_date=datetime.now(),
                effective_date=datetime.now().date(),
                description=f'Invoice {invoice_data["invoice_number"]}',
                debit_amount=0,
                credit_amount=invoice_data['total_amount'],
                net_amount=invoice_data['total_amount'],
                account_type='accounts_receivable',
                status='posted'
            )
            db.session.add(transaction)
        
        db.session.commit()
        print(f"   💰 Created {len(invoices_data)} financial transactions")
        
        # Create analytics dashboard
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
        
        # Create sample widget
        widget = Widget(
            public_id=f'widget_{org.public_id}_main',
            user_id=user_objects[0].id,
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
        print(f"   📊 Created analytics dashboard and widget")

def show_summary():
    """Show summary of seeded data"""
    print("\n📈 SEEDING SUMMARY")
    print("=" * 30)
    
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_APP'] = 'app:create_app()'
    
    from app import create_app
    from app.models import Organization, User, Patient, Appointment, Invoice
    
    app = create_app()
    
    with app.app_context():
        org_count = Organization.query.count()
        user_count = User.query.count()
        patient_count = Patient.query.count()
        appointment_count = Appointment.query.count()
        invoice_count = Invoice.query.count()
        
        print(f"🏢 Organizations: {org_count}")
        print(f"👥 Users: {user_count}")
        print(f"👤 Patients: {patient_count}")
        print(f"📅 Appointments: {appointment_count}")
        print(f"🧾 Invoices: {invoice_count}")
        
        # Show distribution per organization
        print(f"\n📊 Distribution per organization:")
        organizations = Organization.query.all()
        for org in organizations:
            patients = Patient.query.filter_by(organization_id=org.public_id).count()
            users = User.query.filter_by(organization_id=org.public_id).count()
            appointments = Appointment.query.filter_by(organization_id=org.public_id).count()
            invoices = Invoice.query.filter_by(organization_id=org.public_id).count()
            
            print(f"   {org.name}:")
            print(f"     👤 {patients} patients")
            print(f"     👥 {users} users")
            print(f"     📅 {appointments} appointments") 
            print(f"     🧾 {invoices} invoices")

if __name__ == '__main__':
    seed_tenants_fixed()
    show_summary()