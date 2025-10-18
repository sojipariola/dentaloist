#!/usr/bin/env python3
"""
Seed database with proper tenant isolation using actual models
REQUIRES: Lookup data to be seeded first
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from datetime import datetime, timedelta
import random
import json

def create_app():
    """Create Flask app for seeding"""
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    return app

def seed_tenants():
    """Seed tenant data (requires lookups to be seeded first)"""
    app = create_app()
    
    # Initialize with your app's db
    from app import db
    db.init_app(app)
    
    with app.app_context():
        print("🌱 SEEDING TENANT DATA")
        print("=" * 50)
        
        # Verify lookups exist
        if not verify_lookups_exist():
            print("❌ Lookup data not found. Please run seed_lookups.py first.")
            return
        
        # Import models
        from app.models import (
            Organization, Tenant, User, Staff, 
            Patient, Appointment, Treatment, ClinicalNote, Allergy,
            Prescription, VitalSign, TreatmentPlan, AvailabilitySlot,
            Invoice, Payment, InsurancePlan, Expense, FinancialReport,
            FinancialTransaction, Widget, AnalyticsDashboard
        )
        
        # Create tenants (top-level multi-tenant containers)
        print("\n🏢 Creating tenants...")
        
        # Get tenant status lookup
        from app.models import TenantStatus
        active_status = TenantStatus.query.filter_by(name='Active').first()
        if not active_status:
            print("❌ TenantStatus 'Active' not found in lookups")
            return
        
        tenants_data = [
            {
                'public_id': 'tenant_001',
                'name': 'Dental Health Group',
                'domain': 'dentalhealthgroup.com',
                'status_id': active_status.id,
                'max_organizations': 10,
                'max_users': 100,
                'max_patients': 5000
            },
            {
                'public_id': 'tenant_002',
                'name': 'Smile Care Network', 
                'domain': 'smilecarenetwork.com',
                'status_id': active_status.id,
                'max_organizations': 8,
                'max_users': 80,
                'max_patients': 4000
            }
        ]
        
        tenant_objects = []
        for tenant_data in tenants_data:
            tenant = Tenant(**tenant_data)
            db.session.add(tenant)
            tenant_objects.append(tenant)
            print(f"   ✅ {tenant.name} ({tenant.public_id})")
        
        db.session.commit()
        
        # Create organizations (each belongs to a tenant)
        print("\n🏥 Creating organizations...")
        
        # Get organization type lookup
        from app.models import OrganizationType
        dental_clinic_type = OrganizationType.query.filter_by(name='Dental Clinic').first()
        if not dental_clinic_type:
            print("❌ OrganizationType 'Dental Clinic' not found in lookups")
            return
        
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
                'organization_type_id': dental_clinic_type.id,
                'tenant_id': tenant_objects[0].id if tenant_objects else None
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
                'organization_type_id': dental_clinic_type.id,
                'tenant_id': tenant_objects[0].id if tenant_objects else None
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
                'organization_type_id': dental_clinic_type.id,
                'tenant_id': tenant_objects[1].id if len(tenant_objects) > 1 else None
            }
        ]
        
        org_objects = []
        for org_data in organizations_data:
            org = Organization(**org_data)
            db.session.add(org)
            org_objects.append(org)
            print(f"   ✅ {org.name} ({org.public_id})")
        
        db.session.commit()
        
        # Seed data for each organization
        seed_organization_data(org_objects, db)
        
        print(f"\n🎉 TENANT SEEDING COMPLETE!")
        print("=" * 50)
        
        # Show summary
        show_seeding_summary(db)

def verify_lookups_exist():
    """Verify that required lookup data exists"""
    from app.models import (
        UserRole, OrganizationType, Gender, AppointmentStatus, AppointmentType,
        PaymentStatus, InvoiceStatus, PaymentMethod, TenantStatus
    )
    
    required_lookups = [
        (UserRole, 'UserRole'),
        (OrganizationType, 'OrganizationType'), 
        (Gender, 'Gender'),
        (AppointmentStatus, 'AppointmentStatus'),
        (AppointmentType, 'AppointmentType'),
        (TenantStatus, 'TenantStatus')
    ]
    
    for model, name in required_lookups:
        if model.query.count() == 0:
            print(f"❌ {name} lookup table is empty")
            return False
    
    return True

def seed_organization_data(org_objects, db):
    """Seed data for each organization"""
    from app.models import (
        User, Staff, Patient, Appointment, AvailabilitySlot,
        Invoice, FinancialTransaction, Widget, AnalyticsDashboard
    )
    
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
    
    # Get lookup data
    from app.models import UserRole, AppointmentStatus, AppointmentType, InvoiceStatus, PaymentStatus
    
    admin_role = UserRole.query.filter_by(name='Administrator').first()
    staff_role = UserRole.query.filter_by(name='Staff').first()
    scheduled_status = AppointmentStatus.query.filter_by(name='Scheduled').first()
    checkup_type = AppointmentType.query.filter_by(name='Checkup').first()
    draft_invoice = InvoiceStatus.query.filter_by(name='Draft').first()
    
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
                'user_role_id': admin_role.id if admin_role else 1,
                'email_verified': True
            }
        ]
        
        # Add staff users
        for i in range(3):
            users_data.append({
                'public_id': f'user_{org.public_id}_staff{i+1}',
                'email': f'staff{i+1}@{org.public_id}.com',
                'password_hash': '$2b$12$hashed_password_for_dev',
                'first_name': first_names[random.randint(0, 4)],
                'last_name': last_names[random.randint(0, 4)],
                'phone': f'+1-555-{random.randint(1000,9999)}',
                'organization_id': org.public_id,
                'user_role_id': staff_role.id if staff_role else 2,
                'email_verified': True
            })
        
        user_objects = []
        for user_data in users_data:
            user = User(**user_data)
            db.session.add(user)
            user_objects.append(user)
        print(f"   👥 Created {len(users_data)} users")
        
        # Create staff records for users
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
        print(f"   💼 Created {len(staff_objects)} staff records")
        
        # Create patients for this organization (8 per org)
        patients_data = []
        for i in range(8):
            first_name = first_names[random.randint(0, len(first_names)-1)]
            last_name = last_names[random.randint(0, len(last_names)-1)]
            
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
        print(f"   👤 Created {len(patients_data)} patients")
        
        # Create availability slots for staff
        print("   🕒 Creating availability slots...")
        base_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        for staff in staff_objects:
            for day in range(5):  # Monday to Friday
                slot_date = base_date + timedelta(days=day)
                slot = AvailabilitySlot(
                    public_id=f'slot_{org.public_id}_{staff.id}_{day}',
                    staff_id=staff.id,
                    organization_id=org.public_id,
                    date=slot_date.date(),
                    start_time=datetime.strptime('09:00', '%H:%M').time(),
                    end_time=datetime.strptime('17:00', '%H:%M').time(),
                    slot_type='working_hours',
                    status='available'
                )
                db.session.add(slot)
        
        # Create appointments for this organization (3 per org)
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
                    'appointment_type_id': checkup_type.id if checkup_type else 1,
                    'status_id': scheduled_status.id if scheduled_status else 1
                })
        
        for appointment_data in appointments_data:
            appointment = Appointment(**appointment_data)
            db.session.add(appointment)
        print(f"   📅 Created {len(appointments_data)} appointments")
        
        # Create invoices for this organization (4 per org)
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
                    'status_id': draft_invoice.id if draft_invoice else 1,
                    'currency_id': 1,  # USD
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
        print(f"   🧾 Created {len(invoices_data)} invoices")
        
        # Create financial transactions
        print("   💰 Creating financial transactions...")
        for invoice_data in invoices_data:
            transaction = FinancialTransaction(
                public_id=f'trans_{org.public_id}_{invoice_data["public_id"]}',
                organization_id=org.public_id,
                transaction_type_id=1,  # Invoice
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
        
        # Create analytics dashboard for organization
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
        print("   📊 Created analytics dashboard")
        
        # Create sample widgets for dashboard
        widget = Widget(
            public_id=f'widget_{org.public_id}_main',
            user_id=user_objects[0].id,  # Admin user
            organization_id=org.public_id,
            widget_type_id=1,  # Assuming 1 = stats widget
            title='Patient Overview',
            description='Key patient metrics',
            size='medium',
            config=json.dumps({'metrics': ['total_patients', 'new_this_month']}),
            data_source=json.dumps({'type': 'patient_metrics'}),
            is_visible=True
        )
        db.session.add(widget)
        print("   📈 Created sample widget")
    
    # Commit all changes
    db.session.commit()

def show_seeding_summary(db):
    """Show summary of seeded data"""
    from app.models import (
        Organization, User, Patient, Appointment, Invoice, 
        FinancialTransaction, Widget, AnalyticsDashboard
    )
    
    print("\n📈 SEEDING SUMMARY")
    print("=" * 30)
    
    org_count = Organization.query.count()
    user_count = User.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    invoice_count = Invoice.query.count()
    transaction_count = FinancialTransaction.query.count()
    widget_count = Widget.query.count()
    dashboard_count = AnalyticsDashboard.query.count()
    
    print(f"🏢 Organizations: {org_count}")
    print(f"👥 Users: {user_count}")
    print(f"👤 Patients: {patient_count}")
    print(f"📅 Appointments: {appointment_count}")
    print(f"🧾 Invoices: {invoice_count}")
    print(f"💰 Financial Transactions: {transaction_count}")
    print(f"📊 Analytics Dashboards: {dashboard_count}")
    print(f"📈 Widgets: {widget_count}")
    
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
    seed_tenants()