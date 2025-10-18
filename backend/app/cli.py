import os
import shutil
import click
from flask.cli import with_appcontext
from sqlalchemy import inspect, text
# from werkzeug.security import generate_password_hash
from flask_bcrypt import generate_password_hash
from faker import Faker
import random
import datetime 

from app.models import (
    db, Organization, Tenant, User, Staff, Patient, Appointment, Treatment, Subscription
)
from app.models.lookups import (
    OrganizationType, TenantStatus, UserRole, SubscriptionPlan,
    AppointmentStatus, AppointmentType, TreatmentStatus, TreatmentType,
    PriorityLevel, Gender
)

# -----------------------------
# Helpers
# -----------------------------
def _ensure_instance_directory():
    """Ensure instance directory exists with proper permissions."""
    os.makedirs("instance", exist_ok=True)
    try:
        os.chmod("instance", 0o755)
    except Exception:
        pass

def _delete_database():
    """Delete SQLite database file."""
    db_path = "instance/app.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        click.echo(f"🗑️  Deleted database: {db_path}")

def _delete_folders():
    """Delete migrations folder only (keep instance)."""
    if os.path.exists("migrations"):
        shutil.rmtree("migrations")
        click.echo("🗑️  Deleted folder: migrations")

def _create_tables_safely():
    """Safely create database tables with proper error handling."""
    try:
        _ensure_instance_directory()
        db.create_all()
        click.echo("✅ Database tables created")
        return True
    except Exception as e:
        click.echo(f"❌ Error creating tables: {e}")
        return False

def _get_lookup_value(lookup_model, code):
    """Get lookup model instance by code."""
    lookup = lookup_model.query.filter_by(code=code, is_active=True).first()
    if not lookup:
        # Create default lookup if it doesn't exist
        lookup = _create_default_lookup(lookup_model, code)
    return lookup

def _create_default_lookup(lookup_model, code):
    """Create default lookup value if it doesn't exist."""
    defaults = {
        'tenant_statuses': {
            'active': {'name': 'Active', 'description': 'Active tenant'},
            'suspended': {'name': 'Suspended', 'description': 'Suspended tenant'},
            'inactive': {'name': 'Inactive', 'description': 'Inactive tenant'}
        },
        'organization_types': {
            'clinic': {'name': 'Clinic', 'description': 'Dental clinic'},
            'hospital': {'name': 'Hospital', 'description': 'Hospital'},
            'practice': {'name': 'Private Practice', 'description': 'Private dental practice'}
        },
        'user_roles': {
            'super_admin': {'name': 'Super Admin', 'description': 'System administrator'},
            'admin': {'name': 'Administrator', 'description': 'Organization administrator'},
            'dentist': {'name': 'Dentist', 'description': 'Dental practitioner'},
            'nurse': {'name': 'Dental Nurse', 'description': 'Dental nurse'},
            'staff': {'name': 'Staff', 'description': 'General staff'},
            'patient': {'name': 'Patient', 'description': 'Patient user'}
        },
        'subscription_plans': {
            'free': {'name': 'Free', 'description': 'Free plan', 'price_monthly': 0, 'max_users': 5, 'max_patients': 100},
            'professional': {'name': 'Professional', 'description': 'Professional plan', 'price_monthly': 199, 'max_users': 50, 'max_patients': 1000},
            'enterprise': {'name': 'Enterprise', 'description': 'Enterprise plan', 'price_monthly': 499, 'max_users': 500, 'max_patients': 10000}
        },
        'appointment_statuses': {
            'scheduled': {'name': 'Scheduled', 'description': 'Appointment scheduled'},
            'confirmed': {'name': 'Confirmed', 'description': 'Appointment confirmed'},
            'completed': {'name': 'Completed', 'description': 'Appointment completed', 'is_final_status': True},
            'cancelled': {'name': 'Cancelled', 'description': 'Appointment cancelled', 'is_final_status': True},
            'no_show': {'name': 'No Show', 'description': 'Patient did not show up', 'is_final_status': True}
        },
        'appointment_types': {
            'consultation': {'name': 'Consultation', 'description': 'Initial consultation', 'default_duration': 30},
            'checkup': {'name': 'Checkup', 'description': 'Regular checkup', 'default_duration': 30},
            'cleaning': {'name': 'Cleaning', 'description': 'Teeth cleaning', 'default_duration': 45},
            'filling': {'name': 'Filling', 'description': 'Dental filling', 'default_duration': 60},
            'extraction': {'name': 'Extraction', 'description': 'Tooth extraction', 'default_duration': 45},
            'crown': {'name': 'Crown', 'description': 'Dental crown', 'default_duration': 90},
            'root_canal': {'name': 'Root Canal', 'description': 'Root canal treatment', 'default_duration': 120},
            'emergency': {'name': 'Emergency', 'description': 'Emergency appointment', 'default_duration': 30}
        },
        'treatment_statuses': {
            'scheduled': {'name': 'Scheduled', 'description': 'Treatment scheduled'},
            'in_progress': {'name': 'In Progress', 'description': 'Treatment in progress'},
            'completed': {'name': 'Completed', 'description': 'Treatment completed', 'is_completed_status': True},
            'cancelled': {'name': 'Cancelled', 'description': 'Treatment cancelled', 'is_completed_status': True}
        },
        'treatment_types': {
            'preventive': {'name': 'Preventive', 'description': 'Preventive care', 'category': 'preventive', 'typical_duration': 30},
            'restorative': {'name': 'Restorative', 'description': 'Restorative treatment', 'category': 'restorative', 'typical_duration': 60},
            'surgical': {'name': 'Surgical', 'description': 'Surgical procedure', 'category': 'surgical', 'typical_duration': 90},
            'cosmetic': {'name': 'Cosmetic', 'description': 'Cosmetic dentistry', 'category': 'cosmetic', 'typical_duration': 120},
            'diagnostic': {'name': 'Diagnostic', 'description': 'Diagnostic procedure', 'category': 'diagnostic', 'typical_duration': 30}
        },
        'priority_levels': {
            'low': {'name': 'Low', 'description': 'Low priority'},
            'medium': {'name': 'Medium', 'description': 'Medium priority'},
            'high': {'name': 'High', 'description': 'High priority'},
            'urgent': {'name': 'Urgent', 'description': 'Urgent priority', 'requires_immediate_attention': True}
        },
        'genders': {
            'male': {'name': 'Male', 'description': 'Male gender', 'pronoun': 'he/him'},
            'female': {'name': 'Female', 'description': 'Female gender', 'pronoun': 'she/her'},
            'other': {'name': 'Other', 'description': 'Other gender', 'pronoun': 'they/them'},
            'prefer_not_to_say': {'name': 'Prefer not to say', 'description': 'Prefer not to specify gender'}
        }
    }
    
    table_name = lookup_model.__tablename__
    if table_name in defaults and code in defaults[table_name]:
        default_data = defaults[table_name][code]
        lookup = lookup_model(
            code=code,
            name=default_data['name'],
            description=default_data.get('description', ''),
            **{k: v for k, v in default_data.items() if k not in ['name', 'description']}
        )
        db.session.add(lookup)
        db.session.commit()
        return lookup
    
    return None

def _create_default_admin():
    """Create default tenant, organization, and super admin user."""
    try:
        # Get lookup values
        tenant_status = _get_lookup_value(TenantStatus, 'active')
        org_type = _get_lookup_value(OrganizationType, 'clinic')
        user_role = _get_lookup_value(UserRole, 'super_admin')
        subscription_plan = _get_lookup_value(SubscriptionPlan, 'professional')

        # Create tenant first
        tenant = Tenant(
            name="Dentaloist Main Tenant",
            subdomain="default",
            display_name="Dentaloist",
            contact_email="sojipariola@gmail.com",
            status=tenant_status.id,
            max_users=50,
            max_patients=10000,
            is_active=True
        )
        db.session.add(tenant)
        db.session.flush()

        # Create organization
        org = Organization(
            name="Dentaloist Clinic",
            type=org_type.id,
            email="info@dentaloist.com",
            phone="+1234567890",
            max_staff=50,
            max_patients=1000,
            status="active",
            is_verified=True,
            tenant_id=tenant.id
        )
        db.session.add(org)
        db.session.flush()

        # Create subscription for the organization
        subscription = Subscription(
            organization_id=org.public_id,
            plan=subscription_plan.id,
            price=199.00,
            start_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(subscription)
        db.session.flush()

        # Create admin user with direct password hash
        admin = User(
            email="sojipariola@gmail.com",
            first_name="Soji",
            last_name="Pariola",
            role=user_role.id,
            organization_id=org.public_id,
            tenant_id=tenant.id,
            is_active=True,
            is_admin=True,
            password_hash=generate_password_hash("Soji1111")
        )
        db.session.add(admin)
        db.session.flush()

        # Update tenant with admin info
        tenant.created_by = admin.id
        tenant.activated_by = admin.id
        tenant.activated_at = datetime.datetime.utcnow()

        db.session.commit()
        click.echo(f"✅ Admin created: {admin.email} / Soji1111")
        return True
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error creating admin: {e}")
        import traceback
        traceback.print_exc()
        return False

# -----------------------------
# Demo Data Generation
# -----------------------------

def _create_sample_data_for_organization(org_data, fake):
    """Create sample data for a specific organization"""
    # Create staff
    staff_members = _create_staff_for_organization(org_data, fake)
    
    # Create patients
    patients = _create_patients_for_organization(org_data, fake)
    
    # Create appointments
    click.echo("📅 Creating appointments...")
    appointments = _create_appointments_for_organization(org_data, patients, staff_members, fake, num_appointments=50)
    
    # Create treatments
    click.echo("🦷 Creating treatments...")
    treatments = _create_treatments_for_organization(org_data, patients, staff_members, fake, num_treatments=30)
    
    return {
        'staff': staff_members,
        'patients': patients,
        'appointments': appointments,
        'treatments': treatments
    }

def _create_staff_for_organization(org_data, fake):
    """Create staff members for an organization"""
    org = org_data['org']
    tenant = org_data['tenant']
    
    click.echo("👥 Creating staff...")
    
    # Get lookup values for roles
    admin_role = _get_lookup_value(UserRole, 'admin')
    dentist_role = _get_lookup_value(UserRole, 'dentist')
    nurse_role = _get_lookup_value(UserRole, 'nurse')
    staff_role = _get_lookup_value(UserRole, 'staff')
    
    job_titles = [
        ('Practice Administrator', admin_role),
        ('Dentist', dentist_role), 
        ('Dental Nurse', nurse_role),
        ('Receptionist', staff_role)
    ]
    
    staff_members = []
    
    for job_title, role in job_titles:
        try:
            # Create user
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@{org.name.lower().replace(' ', '')}.com"
            
            # Create user with direct password hash
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                role=role.id,
                organization_id=org.public_id,
                tenant_id=tenant.id,
                is_active=True,
                is_admin=(role.code == 'admin'),
                phone=fake.phone_number()[:15],
                date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=65),
                password_hash=generate_password_hash("Password123!")
            )
            db.session.add(user)
            db.session.flush()

            # Create staff record
            staff_data = {
                'user_id': user.id,
                'organization_id': org.public_id,
                'staff_number': f"EMP{random.randint(1000, 9999)}",
                'job_title': job_title,
                'department': "Dental",
                'hire_date': fake.date_between(start_date='-5y', end_date='today'),
                'status': 'active',
                'work_email': email,
                'work_phone': fake.phone_number()[:15],
                'employment_type': random.choice(['Full-time', 'Part-time']),
                'emergency_contact_name': fake.name(),
                'emergency_contact_phone': fake.phone_number()[:15],
                'emergency_contact_relationship': random.choice(['Spouse', 'Parent', 'Sibling']),
                'office_location': 'Main Office',
                'languages_spoken': 'English, Spanish'
            }
            
            # Add dentist-specific fields
            if role.code == 'dentist':
                staff_data['specialization'] = "General Dentistry"
                staff_data['license_number'] = f"DEN{random.randint(100000, 999999)}"
                staff_data['license_expiry'] = fake.date_between(start_date='today', end_date='+2y')
                staff_data['qualifications'] = "DDS, MBA"
                staff_data['certifications'] = "Cosmetic Dentistry, Orthodontics"
            
            # Add nurse-specific fields
            elif role.code == 'nurse':
                staff_data['specialization'] = "Dental Nursing"
                staff_data['qualifications'] = "Registered Dental Nurse"
                staff_data['certifications'] = "CPR, First Aid"
            
            staff = Staff(**staff_data)
            db.session.add(staff)
            staff_members.append(staff)
            
            click.echo(f"   👨‍💼 Created {job_title}: {first_name} {last_name}")
            
        except Exception as e:
            db.session.rollback()
            click.echo(f"   ❌ Error creating {job_title}: {e}")
            continue
    
    db.session.commit()
    return staff_members

def _create_patients_for_organization(org_data, fake, max_patients=100):
    """Create patients for an organization"""
    org = org_data['org']
    
    # Get lookup values for gender
    male_gender = _get_lookup_value(Gender, 'male')
    female_gender = _get_lookup_value(Gender, 'female')
    other_gender = _get_lookup_value(Gender, 'other')
    
    patients = []
    
    for i in range(max_patients):
        try:
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@patient.{org.name.lower().replace(' ', '')}.com" if random.random() > 0.3 else None
            
            # Random gender
            gender_choice = random.choice([male_gender, female_gender, other_gender])
            
            # Create patient
            patient_data = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': fake.phone_number()[:15],
                'date_of_birth': fake.date_of_birth(minimum_age=1, maximum_age=90),
                'gender': gender_choice.id,
                'address': fake.address().replace('\n', ', ')[:200],
                'emergency_contact': fake.name() + " - " + fake.phone_number()[:15],
                'medical_history': fake.text(max_nb_chars=200) if random.random() > 0.7 else None,
                'allergies': fake.text(max_nb_chars=100) if random.random() > 0.8 else None,
                'medications': fake.text(max_nb_chars=150) if random.random() > 0.6 else None,
                'dental_history': fake.text(max_nb_chars=180) if random.random() > 0.5 else None,
                'oral_hygiene': random.choice(['Good', 'Fair', 'Poor']),
                'last_dental_visit': fake.date_between(start_date='-2y', end_date='today') if random.random() > 0.3 else None,
                'status': 'active',
                'preferred_language': random.choice(['English', 'Spanish', 'French']),
                'organization_id': org.public_id,
                'is_active': True
            }
            
            # Remove None values
            patient_data = {k: v for k, v in patient_data.items() if v is not None}
            
            patient = Patient(**patient_data)
            db.session.add(patient)
            patients.append(patient)
            
            if (i + 1) % 20 == 0:
                click.echo(f"   👥 Created {i + 1} patients...")
                
        except Exception as e:
            db.session.rollback()
            click.echo(f"   ❌ Error creating patient {i + 1}: {e}")
            continue
    
    try:
        db.session.commit()
        click.echo(f"   ✅ Created {len(patients)} patients for {org.name}")
    except Exception as e:
        db.session.rollback()
        click.echo(f"   ❌ Error committing patients: {e}")
        return []
    
    return patients

def _create_demo_organizations():
    """Create 3 organizations with FREE subscription and populate with data."""
    fake = Faker()
    
    # Check if demo organizations already exist
    existing_orgs = Organization.query.filter(
        Organization.name.in_(['Smile Bright Dental', 'Perfect Smile Clinic', 'Healthy Teeth Center'])
    ).all()
    
    if existing_orgs:
        click.echo("⚠️ Demo organizations already exist. Using existing ones...")
        organizations = []
        for org in existing_orgs:
            tenant = Tenant.query.get(org.tenant_id)
            subscription = Subscription.query.filter_by(organization_id=org.public_id).first()
            organizations.append({
                'org': org,
                'tenant': tenant,
                'subscription': subscription
            })
            click.echo(f"✅ Using existing organization: {org.name}")
        return organizations
    
    # Get lookup values
    tenant_status = _get_lookup_value(TenantStatus, 'active')
    org_type = _get_lookup_value(OrganizationType, 'clinic')
    free_plan = _get_lookup_value(SubscriptionPlan, 'free')
    
    organizations_data = [
        {
            'name': 'Smile Bright Dental',
            'email': 'info@smilebrightdental.com',
            'phone': '+1-555-0101',
            'address': '123 Main Street, New York, NY 10001'
        },
        {
            'name': 'Perfect Smile Clinic', 
            'email': 'contact@perfectsmile.com',
            'phone': '+1-555-0102',
            'address': '456 Oak Avenue, Los Angeles, CA 90210'
        },
        {
            'name': 'Healthy Teeth Center',
            'email': 'hello@healthyteeth.com', 
            'phone': '+1-555-0103',
            'address': '789 Pine Road, Chicago, IL 60601'
        }
    ]
    
    organizations = []
    
    for org_data in organizations_data:
        try:
            # Generate unique subdomain with timestamp
            base_subdomain = org_data['name'].lower().replace(' ', '')
            timestamp = int(datetime.datetime.utcnow().timestamp() % 10000)
            subdomain = f"{base_subdomain}{timestamp}"
            
            # Create tenant for organization
            tenant = Tenant(
                name=f"{org_data['name']} Tenant",
                subdomain=subdomain,
                display_name=org_data['name'],
                contact_email=org_data['email'],
                status=tenant_status.id,
                max_users=5,  # FREE tier limit
                max_patients=100,  # FREE tier limit
                is_active=True
            )
            db.session.add(tenant)
            db.session.flush()

            # Create organization
            org = Organization(
                name=org_data['name'],
                type=org_type.id,
                email=org_data['email'],
                phone=org_data['phone'],
                address=org_data['address'],
                max_staff=5,  # FREE tier limit
                max_patients=100,  # FREE tier limit
                status="active",
                is_verified=True,
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.flush()

            # Create FREE subscription
            subscription = Subscription(
                organization_id=org.public_id,
                plan=free_plan.id,
                price=0.00,
                start_date=datetime.datetime.utcnow(),
                is_active=True
            )
            db.session.add(subscription)
            
            organizations.append({
                'org': org,
                'tenant': tenant,
                'subscription': subscription
            })
            
            click.echo(f"✅ Created organization: {org.name}")
            
        except Exception as e:
            db.session.rollback()
            click.echo(f"❌ Error creating organization {org_data['name']}: {e}")
            continue
    
    return organizations

def _clean_existing_demo_data():
    """Clean existing demo data before creating new demo data"""
    try:
        # Delete existing demo organizations and their related data
        demo_org_names = ['Smile Bright Dental', 'Perfect Smile Clinic', 'Healthy Teeth Center']
        
        for org_name in demo_org_names:
            org = Organization.query.filter_by(name=org_name).first()
            if org:
                # Delete related data first
                Patient.query.filter_by(organization_id=org.public_id).delete()
                Staff.query.filter_by(organization_id=org.public_id).delete()
                Appointment.query.filter_by(organization_id=org.public_id).delete()
                Treatment.query.filter_by(organization_id=org.public_id).delete()
                Subscription.query.filter_by(organization_id=org.public_id).delete()
                
                # Delete organization
                db.session.delete(org)
                
                # Delete tenant if it exists
                tenant = Tenant.query.get(org.tenant_id)
                if tenant:
                    db.session.delete(tenant)
                
                click.echo(f"🗑️  Deleted existing demo organization: {org_name}")
        
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error cleaning existing demo data: {e}")
        return False

def _create_appointments_for_organization(org_data, patients, staff_members, fake, num_appointments=50):
    """Create appointments for an organization"""
    org = org_data['org']
    
    # Get lookup values
    scheduled_status = _get_lookup_value(AppointmentStatus, 'scheduled')
    confirmed_status = _get_lookup_value(AppointmentStatus, 'confirmed')
    completed_status = _get_lookup_value(AppointmentStatus, 'completed')
    cancelled_status = _get_lookup_value(AppointmentStatus, 'cancelled')
    
    consultation_type = _get_lookup_value(AppointmentType, 'consultation')
    checkup_type = _get_lookup_value(AppointmentType, 'checkup')
    cleaning_type = _get_lookup_value(AppointmentType, 'cleaning')
    filling_type = _get_lookup_value(AppointmentType, 'filling')
    extraction_type = _get_lookup_value(AppointmentType, 'extraction')
    crown_type = _get_lookup_value(AppointmentType, 'crown')
    root_canal_type = _get_lookup_value(AppointmentType, 'root_canal')
    emergency_type = _get_lookup_value(AppointmentType, 'emergency')
    
    low_priority = _get_lookup_value(PriorityLevel, 'low')
    medium_priority = _get_lookup_value(PriorityLevel, 'medium')
    high_priority = _get_lookup_value(PriorityLevel, 'high')
    urgent_priority = _get_lookup_value(PriorityLevel, 'urgent')
    
    appointment_types = [consultation_type, checkup_type, cleaning_type, filling_type, 
                        extraction_type, crown_type, root_canal_type, emergency_type]
    appointment_statuses = [scheduled_status, confirmed_status, completed_status, cancelled_status]
    priorities = [low_priority, medium_priority, high_priority, urgent_priority]
    
    dentists = [s for s in staff_members if s.job_title == 'Dentist']
    if not dentists:
        click.echo("   ⚠️ No dentists found for appointments")
        return []
    
    appointments = []
    
    for i in range(num_appointments):
        try:
            patient = random.choice(patients)
            dentist = random.choice(dentists)
            appointment_type = random.choice(appointment_types)
            appointment_status = random.choice(appointment_statuses)
            priority = random.choice(priorities)
            
            # Create appointment in the future/past
            days_from_now = random.randint(-30, 60)
            appointment_datetime = datetime.datetime.utcnow() + datetime.timedelta(days=days_from_now)
            
            # Generate random time between 9 AM and 5 PM
            hour = random.randint(9, 16)
            minute = random.choice([0, 15, 30, 45])
            start_time = appointment_datetime.datetime.replace(hour=hour, minute=minute, second=0, microsecond=0)
            duration = appointment_type.default_duration or random.choice([30, 45, 60])
            end_time = start_time + datetime.timedelta(minutes=duration)
            
            appointment = Appointment(
                organization_id=org.public_id,
                patient_id=patient.id,
                dentist_id=dentist.id,
                staff_id=dentist.id,
                title=f"Appointment for {patient.first_name} {patient.last_name}",
                description=f"Regular dental appointment",
                type=appointment_type.id,
                status=appointment_status.id,
                priority=priority.id,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                treatment_room=random.choice(['Room 1', 'Room 2', 'Room 3']),
                location=org.address,
                equipment_needed=[],
                chief_complaint=fake.sentence() if random.random() > 0.7 else None,
                treatment_notes=f"Demo appointment notes for {patient.first_name} {patient.last_name}",
                prescribed_medications=[],
                follow_up_required=random.choice([True, False]),
                follow_up_date=start_time + datetime.timedelta(days=random.randint(30, 180)) if random.random() > 0.7 else None,
                estimated_cost=random.uniform(50, 300),
                insurance_covered=random.uniform(0, 200),
                patient_payment=random.uniform(0, 100),
                payment_status=random.choice(['pending', 'paid', 'partial']),
                reminder_sent=random.choice([True, False]),
                confirmation_sent=random.choice([True, False]),
                sms_reminder=random.choice([True, False]),
                email_reminder=random.choice([True, False]),
                is_active=True
            )
            
            db.session.add(appointment)
            appointments.append(appointment)
            
        except Exception as e:
            click.echo(f"   ❌ Error creating appointment {i+1}: {str(e)}")
    
    try:
        db.session.commit()
        click.echo(f"   ✅ Created {len(appointments)} appointments")
        return appointments
    except Exception as e:
        db.session.rollback()
        click.echo(f"   ❌ Error committing appointments: {str(e)}")
        return []

def _create_treatments_for_organization(org_data, patients, staff_members, fake, num_treatments=30):
    """Create treatments for an organization"""
    org = org_data['org']
    tenant = org_data['tenant']
    
    # Get lookup values
    scheduled_status = _get_lookup_value(TreatmentStatus, 'scheduled')
    in_progress_status = _get_lookup_value(TreatmentStatus, 'in_progress')
    completed_status = _get_lookup_value(TreatmentStatus, 'completed')
    
    preventive_type = _get_lookup_value(TreatmentType, 'preventive')
    restorative_type = _get_lookup_value(TreatmentType, 'restorative')
    surgical_type = _get_lookup_value(TreatmentType, 'surgical')
    cosmetic_type = _get_lookup_value(TreatmentType, 'cosmetic')
    diagnostic_type = _get_lookup_value(TreatmentType, 'diagnostic')
    
    low_priority = _get_lookup_value(PriorityLevel, 'low')
    medium_priority = _get_lookup_value(PriorityLevel, 'medium')
    high_priority = _get_lookup_value(PriorityLevel, 'high')
    
    treatment_types = [preventive_type, restorative_type, surgical_type, cosmetic_type, diagnostic_type]
    treatment_statuses = [scheduled_status, in_progress_status, completed_status]
    priorities = [low_priority, medium_priority, high_priority]
    
    dentists = [s for s in staff_members if s.job_title == 'Dentist']
    nurses = [s for s in staff_members if s.job_title == 'Dental Nurse']
    if not dentists:
        click.echo("   ⚠️ No dentists found for treatments")
        return []
    
    treatments = []
    procedures = [
        {'code': 'D1110', 'name': 'Adult Prophylaxis', 'fee': 75.00, 'type': preventive_type},
        {'code': 'D0274', 'name': 'Bitewing X-rays', 'fee': 65.00, 'type': diagnostic_type},
        {'code': 'D2140', 'name': 'Amalgam 1 Surface', 'fee': 110.00, 'type': restorative_type},
        {'code': 'D2750', 'name': 'Crown Porcelain', 'fee': 950.00, 'type': restorative_type},
        {'code': 'D7140', 'name': 'Tooth Extraction', 'fee': 150.00, 'type': surgical_type},
        {'code': 'D1206', 'name': 'Topical Fluoride', 'fee': 35.00, 'type': preventive_type}
    ]
    
    for i in range(num_treatments):
        try:
            patient = random.choice(patients)
            dentist = random.choice(dentists)
            assistant = random.choice(nurses) if nurses else None
            procedure = random.choice(procedures)
            treatment_status = random.choice(treatment_statuses)
            priority = random.choice(priorities)
            
            treatment_date = datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(1, 365))
            treatment_date = treatment_date.replace(hour=random.randint(8, 16), minute=0, second=0, microsecond=0)
            
            treatment = Treatment(
                tenant_id=tenant.id,
                patient_id=patient.id,
                dentist_id=dentist.id,
                assistant_id=assistant.id if assistant else None,
                name=procedure['name'],
                description=f"Treatment for {procedure['name']}",
                type=procedure['type'].id,
                procedure_code=procedure['code'],
                diagnosis_codes=[],
                status=treatment_status.id,
                priority=priority.id,
                scheduled_date=treatment_date,
                estimated_duration=procedure['type'].typical_duration or random.choice([30, 45, 60, 90]),
                actual_start_time=treatment_date if random.random() > 0.3 else None,
                actual_end_time=treatment_date + datetime.timedelta(minutes=random.choice([30, 45, 60])) if random.random() > 0.3 else None,
                actual_duration=random.choice([30, 45, 60]) if random.random() > 0.3 else None,
                tooth_numbers=[random.randint(1, 32) for _ in range(random.randint(1, 3))] if random.random() > 0.5 else [],
                surfaces=['occlusal', 'buccal', 'lingual'] if random.random() > 0.7 else [],
                anesthesia_used=['lidocaine'] if random.random() > 0.6 else [],
                complications=fake.sentence() if random.random() > 0.8 else None,
                post_treatment_instructions=f"Brush gently and avoid hard foods for 24 hours." if random.random() > 0.5 else None,
                cost_estimate=procedure['fee'],
                actual_cost=procedure['fee'] * random.uniform(0.8, 1.2),
                insurance_covered=procedure['fee'] * random.uniform(0, 0.8),
                patient_responsibility=procedure['fee'] * random.uniform(0.2, 1.0),
                duration=random.choice([30, 45, 60]),
                price=procedure['fee'],
                category=procedure['type'].category,
                is_active=True
            )
            
            db.session.add(treatment)
            treatments.append(treatment)
            
        except Exception as e:
            click.echo(f"   ❌ Error creating treatment {i+1}: {str(e)}")
    
    try:
        db.session.commit()
        click.echo(f"   ✅ Created {len(treatments)} treatments")
        return treatments
    except Exception as e:
        db.session.rollback()
        click.echo(f"   ❌ Error committing treatments: {str(e)}")
        return []

# -----------------------------
# CLI Commands
# -----------------------------
@click.command("init-db")
@with_appcontext
def init_db():
    """Initialize database with tables and default admin."""
    click.echo("🚀 Initializing database...")
    if _create_tables_safely():
        if _create_default_admin():
            click.echo("🎉 Database initialized successfully!")
        else:
            click.echo("❌ Failed to create default admin")
    else:
        click.echo("❌ Database initialization failed")

@click.command("reset-db")
@with_appcontext
def reset_db():
    """Reset database: delete db, delete migrations, recreate."""
    click.echo("🔄 Resetting database...")
    _delete_database()
    _delete_folders()
    if _create_tables_safely():
        if _create_default_admin():
            click.echo("✅ Default admin created")
    click.echo("🔁 Database reset complete.")

@click.command("demo-data")
@with_appcontext
def demo_data():
    """Create demo data with 3 FREE organizations and full data."""
    click.echo("🎪 Creating demo data...")
    
    fake = Faker()
    
    try:
        # Clean existing demo data first
        click.echo("🧹 Cleaning existing demo data...")
        _clean_existing_demo_data()
        
        # Create 3 organizations
        click.echo("🏢 Creating 3 organizations with FREE subscription...")
        organizations = _create_demo_organizations()
        
        if not organizations:
            click.echo("❌ No organizations created")
            return
        
        # Create sample data for each organization
        all_data = {}
        for org_data in organizations:
            org_name = org_data['org'].name
            click.echo(f"\n📊 Populating {org_name} with data...")
            all_data[org_name] = _create_sample_data_for_organization(org_data, fake)
        
        # Commit all changes
        db.session.commit()
        
        # Print summary
        click.echo("\n🎉 Demo data creation complete!")
        click.echo("=" * 50)
        
        for org_data in organizations:
            org_name = org_data['org'].name
            data = all_data[org_name]
            click.echo(f"\n📈 {org_name} Summary:")
            click.echo(f"   👨‍💼 Staff: {len(data['staff'])}")
            click.echo(f"   👤 Patients: {len(data['patients'])}")
            click.echo(f"   📅 Appointments: {len(data['appointments'])}")
            click.echo(f"   🦷 Treatments: {len(data['treatments'])}")
            click.echo(f"   💰 Subscription: FREE")
        
        click.echo(f"\n🔑 Default admin: sojipariola@gmail.com / Soji1111")
        click.echo("🔑 Staff passwords: Password123!")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error creating demo data: {e}")
        import traceback
        traceback.print_exc()

@click.command("check-db")
@with_appcontext
def check_db():
    """Check database tables and record counts."""
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if tables:
            click.echo(f"✅ Database exists with {len(tables)} tables")
            click.echo(f"📊 Tables: {', '.join(sorted(tables))}")
            
            # Check key tables
            key_tables = ['users', 'organizations', 'tenants', 'patients', 'staff', 'appointments', 'treatments']
            for table in key_tables:
                if table in tables:
                    try:
                        count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                        click.echo(f"   {table}: {count} records")
                    except Exception as e:
                        click.echo(f"   {table}: error counting - {e}")
        else:
            click.echo("❌ No tables found")
    except Exception as e:
        click.echo(f"❌ Error checking database: {e}")

@click.command("create-admin")
@click.option('--email', default='sojipariola@gmail.com', help='Admin email')
@click.option('--password', default='Soji1111', help='Admin password')
@with_appcontext
def create_admin_command(email, password):
    """Create or update an admin user."""
    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            click.echo(f"⚠️ User {email} already exists! Updating password...")
            existing_user.password_hash = generate_password_hash(password)
            db.session.commit()
            click.echo("✅ Password updated")
            return

        # Get lookup values - FIXED: Use the actual model instances
        tenant_status = _get_lookup_value(TenantStatus, 'active')
        org_type = _get_lookup_value(OrganizationType, 'clinic')
        user_role = _get_lookup_value(UserRole, 'super_admin')

        # Get or create tenant and organization
        tenant = Tenant.query.first()
        org = Organization.query.first()
        
        if not tenant:
            tenant = Tenant(
                name="Default Tenant",
                contact_email=email,
                status=tenant_status.id  # This should be the ID, not the instance
            )
            db.session.add(tenant)
            db.session.flush()

        if not org:
            org = Organization(
                name="Default Clinic",
                type=org_type.id,  # This should be the ID, not the instance
                email=email,
                tenant_id=tenant.id  # This should be the ID, not the instance
            )
            db.session.add(org)
            db.session.flush()

        # Create admin - FIXED: Use IDs for foreign keys, not instances
        admin = User(
            email=email,
            first_name="Admin",
            last_name="User",
            role=user_role.id,  # Use the ID, not the instance
            organization_id=org.public_id,  # Use the ID, not the instance
            tenant_id=tenant.id,  # Use the ID, not the instance
            is_active=True,
            is_admin=True,
            password_hash=generate_password_hash(password)
        )
        db.session.add(admin)
        db.session.commit()
        click.echo(f"✅ Admin user created: {email} / {password}")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error creating admin: {e}")
        import traceback
        traceback.print_exc()


@click.command("init-lookups")
@with_appcontext
def init_lookups():
    """Initialize all lookup tables with default values."""
    click.echo("📚 Initializing lookup tables...")
    
    try:
        # Import all lookup models
        from app.models.lookups import (
            AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
            TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
            MedicationRoute, VitalSignsUnit, WidgetType, NotificationType,
            IntegrationStatus, WebhookEventStatus, ReportType, UserRole,
            OrganizationType, Gender, SubscriptionPlan, TenantStatus,
            IndustryType, SecurityEventType, PermissionCategory,
            PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus,
            ExpenseCategory, Currency, ProductType, InventoryTransactionType,
            PurchaseOrderStatus, InventoryAdjustmentType
        )
        
        # Define all lookup models and their default values
        lookup_models = [
            (TenantStatus, 'tenant_statuses'),
            (OrganizationType, 'organization_types'),
            (UserRole, 'user_roles'),
            (SubscriptionPlan, 'subscription_plans'),
            (AppointmentStatus, 'appointment_statuses'),
            (AppointmentType, 'appointment_types'),
            (TreatmentStatus, 'treatment_statuses'),
            (TreatmentType, 'treatment_types'),
            (PriorityLevel, 'priority_levels'),
            (Gender, 'genders')
        ]
        
        total_created = 0
        for lookup_model, table_name in lookup_models:
            click.echo(f"📋 Initializing {table_name}...")
            
            # Get existing codes to avoid duplicates
            existing_codes = {lookup.code for lookup in lookup_model.query.all()}
            
            # Create default lookups for this model
            defaults = _get_default_lookup_values(table_name)
            for code, data in defaults.items():
                if code not in existing_codes:
                    lookup = lookup_model(
                        code=code,
                        name=data['name'],
                        description=data.get('description', ''),
                        **{k: v for k, v in data.items() if k not in ['name', 'description']}
                    )
                    db.session.add(lookup)
                    total_created += 1
                    click.echo(f"   ✅ Created {code}")
        
        db.session.commit()
        click.echo(f"🎉 Lookup tables initialized! Created {total_created} new lookup values.")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error initializing lookups: {e}")
        import traceback
        traceback.print_exc()

def _get_default_lookup_values(table_name):
    """Get default values for lookup tables."""
    defaults = {
        'tenant_statuses': {
            'active': {'name': 'Active', 'description': 'Active tenant', 'allows_login': True},
            'suspended': {'name': 'Suspended', 'description': 'Suspended tenant', 'allows_login': False, 'requires_action': True},
            'inactive': {'name': 'Inactive', 'description': 'Inactive tenant', 'allows_login': False},
            'trial': {'name': 'Trial', 'description': 'Trial period', 'allows_login': True, 'is_trial_status': True}
        },
        'organization_types': {
            'clinic': {'name': 'Clinic', 'description': 'Dental clinic'},
            'hospital': {'name': 'Hospital', 'description': 'Hospital'},
            'practice': {'name': 'Private Practice', 'description': 'Private dental practice'}
        },
        'user_roles': {
            'super_admin': {'name': 'Super Admin', 'description': 'System administrator', 'is_system_role': True, 'access_level': 'admin', 'can_manage_users': True, 'can_access_reports': True},
            'admin': {'name': 'Administrator', 'description': 'Organization administrator', 'access_level': 'admin', 'can_manage_users': True, 'can_access_reports': True},
            'dentist': {'name': 'Dentist', 'description': 'Dental practitioner', 'access_level': 'staff'},
            'nurse': {'name': 'Dental Nurse', 'description': 'Dental nurse', 'access_level': 'staff'},
            'staff': {'name': 'Staff', 'description': 'General staff', 'access_level': 'staff'},
            'patient': {'name': 'Patient', 'description': 'Patient user', 'access_level': 'user'}
        },
        'subscription_plans': {
            'free': {'name': 'Free', 'description': 'Free plan', 'price_monthly': 0, 'max_users': 5, 'max_patients': 100},
            'professional': {'name': 'Professional', 'description': 'Professional plan', 'price_monthly': 199, 'max_users': 50, 'max_patients': 1000},
            'enterprise': {'name': 'Enterprise', 'description': 'Enterprise plan', 'price_monthly': 499, 'max_users': 500, 'max_patients': 10000}
        },
        'appointment_statuses': {
            'scheduled': {'name': 'Scheduled', 'description': 'Appointment scheduled', 'allows_editing': True},
            'confirmed': {'name': 'Confirmed', 'description': 'Appointment confirmed', 'allows_editing': True},
            'completed': {'name': 'Completed', 'description': 'Appointment completed', 'is_final_status': True},
            'cancelled': {'name': 'Cancelled', 'description': 'Appointment cancelled', 'is_final_status': True},
            'no_show': {'name': 'No Show', 'description': 'Patient did not show up', 'is_final_status': True}
        },
        'appointment_types': {
            'consultation': {'name': 'Consultation', 'description': 'Initial consultation', 'default_duration': 30, 'category': 'consultation'},
            'checkup': {'name': 'Checkup', 'description': 'Regular checkup', 'default_duration': 30, 'category': 'examination'},
            'cleaning': {'name': 'Cleaning', 'description': 'Teeth cleaning', 'default_duration': 45, 'category': 'preventive'},
            'filling': {'name': 'Filling', 'description': 'Dental filling', 'default_duration': 60, 'category': 'restorative'},
            'extraction': {'name': 'Extraction', 'description': 'Tooth extraction', 'default_duration': 45, 'category': 'surgical'},
            'crown': {'name': 'Crown', 'description': 'Dental crown', 'default_duration': 90, 'category': 'restorative'},
            'root_canal': {'name': 'Root Canal', 'description': 'Root canal treatment', 'default_duration': 120, 'category': 'endodontic'},
            'emergency': {'name': 'Emergency', 'description': 'Emergency appointment', 'default_duration': 30, 'category': 'emergency'}
        },
        'treatment_statuses': {
            'scheduled': {'name': 'Scheduled', 'description': 'Treatment scheduled', 'allows_modification': True},
            'in_progress': {'name': 'In Progress', 'description': 'Treatment in progress', 'allows_modification': True},
            'completed': {'name': 'Completed', 'description': 'Treatment completed', 'is_completed_status': True},
            'cancelled': {'name': 'Cancelled', 'description': 'Treatment cancelled', 'is_completed_status': True}
        },
        'treatment_types': {
            'preventive': {'name': 'Preventive', 'description': 'Preventive care', 'category': 'preventive', 'complexity_level': 'simple', 'typical_duration': 30},
            'restorative': {'name': 'Restorative', 'description': 'Restorative treatment', 'category': 'restorative', 'complexity_level': 'moderate', 'typical_duration': 60},
            'surgical': {'name': 'Surgical', 'description': 'Surgical procedure', 'category': 'surgical', 'complexity_level': 'complex', 'typical_duration': 90},
            'cosmetic': {'name': 'Cosmetic', 'description': 'Cosmetic dentistry', 'category': 'cosmetic', 'complexity_level': 'complex', 'typical_duration': 120},
            'diagnostic': {'name': 'Diagnostic', 'description': 'Diagnostic procedure', 'category': 'diagnostic', 'complexity_level': 'simple', 'typical_duration': 30}
        },
        'priority_levels': {
            'low': {'name': 'Low', 'description': 'Low priority'},
            'medium': {'name': 'Medium', 'description': 'Medium priority'},
            'high': {'name': 'High', 'description': 'High priority'},
            'urgent': {'name': 'Urgent', 'description': 'Urgent priority', 'requires_immediate_attention': True}
        },
        'genders': {
            'male': {'name': 'Male', 'description': 'Male gender', 'pronoun': 'he/him'},
            'female': {'name': 'Female', 'description': 'Female gender', 'pronoun': 'she/her'},
            'other': {'name': 'Other', 'description': 'Other gender', 'pronoun': 'they/them'},
            'prefer_not_to_say': {'name': 'Prefer not to say', 'description': 'Prefer not to specify gender'}
        }
    }
    
    return defaults.get(table_name, {})


@click.command("inspect-db")
@click.option('--format', 'output_format', type=click.Choice(['table', 'markdown', 'csv', 'detailed']), 
              default='table', help='Output format')
@click.option('--database-url', help='Specific database URL (uses app config if not provided)')
@with_appcontext
def inspect_db(output_format, database_url):
    """Inspect database schema - tables, columns, relationships."""
    from sqlalchemy import inspect, text, MetaData
    from collections import defaultdict
    
    click.echo("🔍 Database Schema Inspection")
    click.echo("=" * 60)
    
    try:
        # Use provided database URL or app database
        if database_url:
            from sqlalchemy import create_engine
            engine = create_engine(database_url)
            db_name = database_url.split('/')[-1] if '/' in database_url else "external_db"
        else:
            engine = db.engine
            db_name = "app_db"
        
        inspector = inspect(engine)
        
        # Get all tables
        tables = inspector.get_table_names()
        
        if not tables:
            click.echo("❌ No tables found in database")
            return
        
        click.echo(f"📊 Database: {db_name}")
        click.echo(f"📈 Total Tables: {len(tables)}")
        click.echo()
        
        if output_format == 'table':
            _print_db_schema_table(inspector, tables)
        elif output_format == 'markdown':
            _print_db_schema_markdown(inspector, tables)
        elif output_format == 'csv':
            _print_db_schema_csv(inspector, tables)
        elif output_format == 'detailed':
            _print_db_schema_detailed(inspector, tables, engine)
        
    except Exception as e:
        click.echo(f"❌ Error inspecting database: {e}")
        import traceback
        traceback.print_exc()

def _print_db_schema_table(inspector, tables):
    """Print database schema in table format"""
    total_columns = 0
    
    for table_name in sorted(tables):
        columns = inspector.get_columns(table_name)
        total_columns += len(columns)
        
        click.echo(f"🏷️  Table: {table_name}")
        click.echo(f"   📋 Columns: {len(columns)}")
        
        # Get primary keys
        pk_info = inspector.get_pk_constraint(table_name)
        if pk_info and 'constrained_columns' in pk_info:
            click.echo(f"   🔑 Primary Key: {', '.join(pk_info['constrained_columns'])}")
        
        # Get foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            click.echo(f"   🔗 Foreign Keys: {len(fks)}")
            for fk in fks:
                click.echo(f"     - {', '.join(fk['constrained_columns'])} → {fk['referred_table']}.{', '.join(fk['referred_columns'])}")
        
        # Print columns with details
        click.echo("   📝 Column Details:")
        for col in columns:
            constraints = []
            if not col['nullable']:
                constraints.append("NOT NULL")
            if col.get('default'):
                constraints.append(f"DEFAULT: {col['default']}")
            
            constraint_str = f" [{', '.join(constraints)}]" if constraints else ""
            click.echo(f"     - {col['name']}: {col['type']}{constraint_str}")
        
        click.echo()
    
    click.echo(f"📊 SUMMARY: {len(tables)} tables, {total_columns} columns")

def _print_db_schema_markdown(inspector, tables):
    """Print database schema in markdown format"""
    click.echo("# Database Schema\n")
    
    for table_name in sorted(tables):
        columns = inspector.get_columns(table_name)
        
        click.echo(f"## Table: `{table_name}`\n")
        click.echo(f"**Columns:** {len(columns)}\n")
        
        # Primary keys
        pk_info = inspector.get_pk_constraint(table_name)
        if pk_info and 'constrained_columns' in pk_info:
            click.echo(f"**Primary Key:** `{', '.join(pk_info['constrained_columns'])}`\n")
        
        # Foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            click.echo("**Foreign Keys:**")
            for fk in fks:
                click.echo(f"- `{', '.join(fk['constrained_columns'])}` → `{fk['referred_table']}.{', '.join(fk['referred_columns'])}`")
            click.echo()
        
        # Columns table
        click.echo("| Column | Type | Nullable | Default |")
        click.echo("|--------|------|----------|---------|")
        
        for col in columns:
            nullable = "NO" if not col['nullable'] else "YES"
            default = str(col['default']) if col['default'] else ""
            click.echo(f"| `{col['name']}` | `{col['type']}` | {nullable} | {default} |")
        
        click.echo()

def _print_db_schema_csv(inspector, tables):
    """Print database schema in CSV format"""
    click.echo("table,column,type,nullable,default,primary_key,foreign_key")
    
    for table_name in sorted(tables):
        columns = inspector.get_columns(table_name)
        
        # Get primary keys
        pk_info = inspector.get_pk_constraint(table_name)
        pk_columns = pk_info.get('constrained_columns', []) if pk_info else []
        
        # Get foreign keys
        fks = inspector.get_foreign_keys(table_name)
        fk_columns = {}
        for fk in fks:
            for col in fk['constrained_columns']:
                fk_columns[col] = f"{fk['referred_table']}.{fk['referred_columns'][0]}"
        
        for col in columns:
            is_pk = "YES" if col['name'] in pk_columns else "NO"
            is_fk = fk_columns.get(col['name'], "")
            nullable = "NO" if not col['nullable'] else "YES"
            default = str(col['default']) if col['default'] else ""
            
            click.echo(f"{table_name},{col['name']},{col['type']},{nullable},{default},{is_pk},{is_fk}")

def _print_db_schema_detailed(inspector, tables, engine):
    """Print detailed database schema with relationships"""
    from sqlalchemy import MetaData
    
    # Reflect the entire database
    metadata = MetaData()
    metadata.reflect(bind=engine)
    
    click.echo("🔍 DETAILED DATABASE SCHEMA ANALYSIS")
    click.echo("=" * 70)
    
    # Table relationships analysis
    click.echo("\n📊 TABLE RELATIONSHIPS:")
    click.echo("-" * 40)
    
    relationship_map = defaultdict(list)
    
    for table_name in sorted(tables):
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            relationship_map[fk['referred_table']].append({
                'from_table': table_name,
                'from_columns': fk['constrained_columns'],
                'to_columns': fk['referred_columns']
            })
    
    # Print relationships
    for parent_table, relationships in sorted(relationship_map.items()):
        click.echo(f"\n🏷️  {parent_table} (parent)")
        for rel in relationships:
            click.echo(f"   ← {rel['from_table']} ({', '.join(rel['from_columns'])})")
    
    # Detailed table info
    click.echo("\n📋 DETAILED TABLE INFORMATION:")
    click.echo("-" * 40)
    
    for table_name in sorted(tables):
        table = metadata.tables[table_name]
        columns = inspector.get_columns(table_name)
        indexes = inspector.get_indexes(table_name)
        
        click.echo(f"\n🏷️  TABLE: {table_name}")
        click.echo(f"   📊 Columns: {len(columns)}")
        click.echo(f"   📈 Indexes: {len(indexes)}")
        
        # Column details
        click.echo("   📝 Columns:")
        for col in columns:
            col_info = f"     - {col['name']}: {col['type']}"
            if not col['nullable']:
                col_info += " [NOT NULL]"
            if col.get('default'):
                col_info += f" [DEFAULT: {col['default']}]"
            click.echo(col_info)
        
        # Index details
        if indexes:
            click.echo("   🔍 Indexes:")
            for idx in indexes:
                unique = "UNIQUE" if idx.get('unique') else "INDEX"
                click.echo(f"     - {unique}: {', '.join(idx['column_names'])}")

@click.command("compare-models-db")
@with_appcontext
def compare_models_db():
    """Compare SQLAlchemy models with actual database schema."""
    from sqlalchemy import MetaData, inspect
    from app.models import get_models
    
    click.echo("🔍 COMPARING MODELS WITH DATABASE")
    click.echo("=" * 60)
    
    try:
        # Reflect database schema
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        inspector = inspect(db.engine)
        
        models = get_models()
        db_tables = set(metadata.tables.keys())
        
        click.echo(f"📊 Models: {len(models)}, Database Tables: {len(db_tables)}")
        click.echo()
        
        # Check for tables in models but not in database
        model_tables = set()
        for model in models:
            if hasattr(model, '__tablename__'):
                model_tables.add(model.__tablename__)
        
        missing_in_db = model_tables - db_tables
        extra_in_db = db_tables - model_tables
        
        if missing_in_db:
            click.echo("❌ TABLES IN MODELS BUT MISSING IN DATABASE:")
            for table in sorted(missing_in_db):
                click.echo(f"   - {table}")
            click.echo()
        
        if extra_in_db:
            click.echo("⚠️  TABLES IN DATABASE BUT NOT IN MODELS:")
            for table in sorted(extra_in_db):
                click.echo(f"   - {table}")
            click.echo()
        
        # Check common tables for column mismatches
        common_tables = model_tables.intersection(db_tables)
        if common_tables:
            click.echo("🔍 CHECKING COLUMN MISMATCHES:")
            click.echo("-" * 40)
            
            mismatch_count = 0
            for table_name in sorted(common_tables):
                model = next((m for m in models if hasattr(m, '__tablename__') and m.__tablename__ == table_name), None)
                if not model:
                    continue
                
                db_table = metadata.tables[table_name]
                model_columns = set(model.__table__.columns.keys())
                db_columns = set(db_table.columns.keys())
                
                missing_in_db_cols = model_columns - db_columns
                extra_in_db_cols = db_columns - model_columns
                
                if missing_in_db_cols or extra_in_db_cols:
                    click.echo(f"\n🏷️  Table: {table_name}")
                    if missing_in_db_cols:
                        click.echo(f"   ❌ Missing in DB: {', '.join(sorted(missing_in_db_cols))}")
                        mismatch_count += len(missing_in_db_cols)
                    if extra_in_db_cols:
                        click.echo(f"   ⚠️  Extra in DB: {', '.join(sorted(extra_in_db_cols))}")
                        mismatch_count += len(extra_in_db_cols)
                else:
                    click.echo(f"   ✅ {table_name}: Columns match")
            
            click.echo(f"\n📊 Total column mismatches: {mismatch_count}")
        
        # Summary
        click.echo(f"\n🎯 SUMMARY:")
        click.echo(f"   ✅ Common tables: {len(common_tables)}")
        click.echo(f"   ❌ Missing tables: {len(missing_in_db)}")
        click.echo(f"   ⚠️  Extra tables: {len(extra_in_db)}")
        
    except Exception as e:
        click.echo(f"❌ Error comparing models with database: {e}")
        import traceback
        traceback.print_exc()

@click.command("db-stats")
@with_appcontext
def db_stats():
    """Show comprehensive database statistics."""
    from sqlalchemy import inspect, text
    from collections import Counter
    
    click.echo("📊 DATABASE STATISTICS")
    click.echo("=" * 50)
    
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if not tables:
            click.echo("❌ No tables found")
            return
        
        # Basic stats
        total_tables = len(tables)
        total_columns = 0
        column_types = Counter()
        
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            total_columns += len(columns)
            for col in columns:
                col_type = str(col['type'])
                column_types[col_type] += 1
        
        click.echo(f"📈 Basic Statistics:")
        click.echo(f"   • Tables: {total_tables}")
        click.echo(f"   • Columns: {total_columns}")
        click.echo(f"   • Avg columns per table: {total_columns/total_tables:.1f}")
        
        # Table sizes (by column count)
        table_sizes = []
        for table_name in tables:
            columns = inspector.get_columns(table_name)
            table_sizes.append((table_name, len(columns)))
        
        table_sizes.sort(key=lambda x: x[1], reverse=True)
        
        click.echo(f"\n📋 Largest Tables (by column count):")
        for table_name, col_count in table_sizes[:10]:
            click.echo(f"   • {table_name}: {col_count} columns")
        
        # Column type distribution
        click.echo(f"\n🔧 Column Type Distribution (top 10):")
        for col_type, count in column_types.most_common(10):
            percentage = (count / total_columns) * 100
            click.echo(f"   • {col_type}: {count} ({percentage:.1f}%)")
        
        # Record counts for key tables
        click.echo(f"\n📊 Record Counts for Key Tables:")
        key_tables = ['users', 'patients', 'appointments', 'treatments', 'organizations', 'tenants']
        
        for table in key_tables:
            if table in tables:
                try:
                    count = db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                    click.echo(f"   • {table}: {count} records")
                except Exception as e:
                    click.echo(f"   • {table}: error - {e}")
        
        # Database size (for PostgreSQL)
        try:
            result = db.session.execute(text("SELECT pg_size_pretty(pg_database_size(current_database()))"))
            db_size = result.scalar()
            click.echo(f"\n💾 Database Size: {db_size}")
        except:
            pass  # Not PostgreSQL or not supported
        
    except Exception as e:
        click.echo(f"❌ Error getting database statistics: {e}")

@click.command("table-info")
@click.argument('table_name')
@with_appcontext
def table_info(table_name):
    """Show detailed information about a specific table."""
    from sqlalchemy import inspect
    
    click.echo(f"🔍 Detailed Table Analysis: {table_name}")
    click.echo("=" * 50)
    
    try:
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if table_name not in tables:
            click.echo(f"❌ Table '{table_name}' not found in database")
            click.echo(f"Available tables: {', '.join(sorted(tables))}")
            return
        
        # Basic table info
        columns = inspector.get_columns(table_name)
        click.echo(f"📋 Columns ({len(columns)}):")
        
        for col in columns:
            col_info = f"   • {col['name']} ({col['type']})"
            if not col['nullable']:
                col_info += " [NOT NULL]"
            if col.get('default'):
                col_info += f" [DEFAULT: {col['default']}]"
            if col.get('autoincrement') == True:
                col_info += " [AUTOINCREMENT]"
            click.echo(col_info)
        
        # Primary keys
        pk_info = inspector.get_pk_constraint(table_name)
        if pk_info and 'constrained_columns' in pk_info:
            click.echo(f"\n🔑 Primary Key: {', '.join(pk_info['constrained_columns'])}")
        
        # Foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            click.echo(f"\n🔗 Foreign Keys ({len(fks)}):")
            for fk in fks:
                click.echo(f"   • {', '.join(fk['constrained_columns'])} → {fk['referred_table']}.{', '.join(fk['referred_columns'])}")
                if fk.get('name'):
                    click.echo(f"     Constraint: {fk['name']}")
        
        # Indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            click.echo(f"\n📊 Indexes ({len(indexes)}):")
            for idx in indexes:
                unique = "UNIQUE" if idx.get('unique') else "INDEX"
                click.echo(f"   • {unique}: {', '.join(idx['column_names'])}")
                if idx.get('name'):
                    click.echo(f"     Name: {idx['name']}")
        
        # Record count
        try:
            from sqlalchemy import text
            count = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            click.echo(f"\n📈 Record Count: {count}")
        except Exception as e:
            click.echo(f"\n📈 Record Count: Unable to count - {e}")
        
    except Exception as e:
        click.echo(f"❌ Error analyzing table: {e}")

@click.command("reset-password")
@click.argument("email")
@click.argument("new_password")
@with_appcontext
def reset_password(email, new_password):
    """Reset a user's password via CLI"""
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            click.echo(f"❌ No user found with email: {email}")
            click.echo("💡 Available users:")
            users = User.query.with_entities(User.email).all()
            for user_email in users:
                click.echo(f"   - {user_email[0]}")
            return
        
        # ✅ Hash the new password correctly (decode before saving)
        hashed_pw = generate_password_hash(new_password).decode("utf-8")
        user.password_hash = hashed_pw
        user.updated_at = datetime.datetime.utcnow()
        
        db.session.commit()
        
        click.echo(f"✅ Password for {email} has been reset successfully!")
        click.echo(f"📧 Email: {email}")
        click.echo(f"🔑 New password: {new_password}")
        click.echo("⚠️  Inform the user of their new password safely.")
        click.echo(f"🧩 Hash preview: {hashed_pw[:25]}...")
        
    except Exception as e:
        db.session.rollback()
        click.echo(f"❌ Error resetting password: {e}")
        import traceback
        traceback.print_exc()


@click.command("validate-data")
@with_appcontext
def validate_data():
    """Validate data integrity across relationships"""
    click.echo("🔍 Validating data integrity...")
    
    # Check for orphaned records
    issues = []
    
    # Orphaned patients without organization
    orphaned_patients = db.session.execute(text("""
        SELECT p.id FROM patients p 
        LEFT JOIN organizations o ON p.organization_id = o.public_id 
        WHERE o.public_id IS NULL
    """)).fetchall()
    
    if orphaned_patients:
        issues.append(f"❌ {len(orphaned_patients)} orphaned patients")
    
    # Print results
    if issues:
        click.echo("🚨 Data integrity issues found:")
        for issue in issues:
            click.echo(f"   {issue}")
    else:
        click.echo("✅ All data relationships are valid")

@click.command("backup-db")
@click.option('--backup-dir', default='backups', help='Backup directory')
@with_appcontext
def backup_db(backup_dir):
    """Create database backup"""
    import sqlite3
    import datetime
    
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/backup_{timestamp}.db"
    
    # For SQLite - copy the file
    if os.path.exists("instance/app.db"):
        shutil.copy2("instance/app.db", backup_file)
        click.echo(f"✅ Backup created: {backup_file}")
    else:
        click.echo("❌ No database file found")

@click.command("optimize-db")
@with_appcontext
def optimize_db():
    """Optimize database performance"""
    try:
        # SQLite specific optimizations
        db.session.execute(text("PRAGMA optimize"))
        db.session.execute(text("VACUUM"))
        db.session.commit()
        click.echo("✅ Database optimized")
    except Exception as e:
        click.echo(f"⚠️  Optimization notes: {e}")


@click.command("export-data")
@click.option('--format', type=click.Choice(['json', 'csv']), default='json')
@click.option('--tables', help='Comma-separated table names')
@with_appcontext
def export_data(format, tables):
    """Export data to JSON or CSV"""
    import json
    import csv
    
    table_list = tables.split(',') if tables else ['patients', 'appointments', 'treatments']
    
    for table_name in table_list:
        try:
            result = db.session.execute(text(f"SELECT * FROM {table_name}"))
            columns = result.keys()
            data = [dict(zip(columns, row)) for row in result]
            
            if format == 'json':
                filename = f"export_{table_name}.json"
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            else:
                filename = f"export_{table_name}.csv"
                with open(filename, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=columns)
                    writer.writeheader()
                    writer.writerows(data)
            
            click.echo(f"✅ Exported {len(data)} records from {table_name} to {filename}")
            
        except Exception as e:
            click.echo(f"❌ Error exporting {table_name}: {e}")

@click.command("audit-users")
@with_appcontext
def audit_users():
    """Audit user accounts and security"""
    click.echo("🔒 User Account Audit")
    
    # Check for inactive users
    inactive_users = User.query.filter_by(is_active=False).count()
    click.echo(f"📊 Inactive users: {inactive_users}")
    
    # Check for users without recent login
    thirty_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=30)
    # Assuming you have last_login field
    # stale_users = User.query.filter(User.last_login < thirty_days_ago).count()
    # click.echo(f"📊 Users inactive for 30+ days: {stale_users}")
    
    # Check admin users
    admin_users = User.query.filter_by(is_admin=True).count()
    click.echo(f"👑 Admin users: {admin_users}")


@click.command("migration-helper")
@click.argument('migration_name')
@with_appcontext
def migration_helper(migration_name):
    """Helper for creating complex migrations"""
    click.echo(f"🛠️  Migration Helper: {migration_name}")
    
    # Generate migration template based on common patterns
    templates = {
        'add_column': "ALTER TABLE {table} ADD COLUMN {column} {type};",
        'drop_column': "ALTER TABLE {table} DROP COLUMN {column};",
        'create_index': "CREATE INDEX idx_{table}_{column} ON {table}({column});"
    }
    
    # This would interact with your migration system
    click.echo("📝 Use this command after making model changes")
    click.echo("💡 Run: flask db migrate -m 'your message'")

@click.command('seed-lookups-db')
@with_appcontext
def seed_lookups_db_command():
    """Seed the database with initial data"""
    seed_all()

# -----------------------------
# Register Commands
# -----------------------------
def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(demo_data)
    app.cli.add_command(init_lookups) 

    app.cli.add_command(check_db)
    app.cli.add_command(create_admin_command)
 
    app.cli.add_command(inspect_db)
    app.cli.add_command(compare_models_db)
    app.cli.add_command(db_stats)
    app.cli.add_command(table_info)
    app.cli.add_command(reset_password)

    app.cli.add_command(validate_data)
    app.cli.add_command(backup_db)
    app.cli.add_command(optimize_db)
    app.cli.add_command(export_data)
    app.cli.add_command(audit_users)
    app.cli.add_command(migration_helper)

    app.cli.add_command(seed_lookups_db_command)

    click.echo("✅ CLI commands registered.")


'''
sudo pkill -f "flask run" || true
sudo pkill -f "python" || true
rm -f instance/dentaloist.db
rm -f instance/dentaloist.db-journal
rm -rf migrations/
rm -rf __pycache__
rm -rf app/__pycache__
rm -rf app/models/__pycache__
rm -rf app/models/clinical/__pycache__
sleep 2
python3 scripts/fix_migration_file.py
sleep 2
python3 scripts/force_create_tables.py
python3 scripts/verify_fix.py
sleep 2
python3 -m flask db init
sleep 2
python3 -m flask db migrate -m "Initial migration"
python3 -m flask db upgrade
sleep 2
python3 setup_database.py
sleep 2
python3 scripts/seed_demo_data.py
sleep 2
python3 scripts/fix_seeder_imports.py
sleep 2
python scripts/debug_import_issue.py
sleep 2
python3 wsgi.py


python3 -m flask reset-password sojipariola@gmail.com Soji1111
'''
# backend/scripts/debug_admin_auth_logic.py