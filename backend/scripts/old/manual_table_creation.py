# backend/scripts/manual_table_creation.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
import sqlite3

def manual_table_creation():
    app = create_app()
    
    with app.app_context():
        print("💥 MANUAL TABLE CREATION")
        print("=" * 50)
        
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        db_path = db_uri.replace('sqlite:///', '')
        print(f"Database: {db_path}")
        
        # Close all connections
        db.session.close_all()
        db.engine.dispose()
        
        # Remove database file completely
        if os.path.exists(db_path):
            os.remove(db_path)
            print("🗑️  Database file removed")
        
        # Create new database with SQLAlchemy
        print("📦 Creating all tables with db.create_all()...")
        db.create_all()
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Created {len(tables)} tables")
        
        # Check critical tables
        critical_tables = ['appointments', 'patients', 'staff', 'users', 'organizations']
        created_critical = [t for t in critical_tables if t in tables]
        missing_critical = [t for t in critical_tables if t not in tables]
        
        print(f"🔑 Critical tables created: {len(created_critical)}/{len(critical_tables)}")
        for table in created_critical:
            print(f"   ✅ {table}")
        for table in missing_critical:
            print(f"   ❌ {table}")
        
        if 'appointments' in tables:
            print("\n🎉 APPOINTMENTS TABLE SUCCESSFULLY CREATED!")
            
            # Test inserting an appointment
            print("\n🧪 Testing appointment insertion...")
            try:
                # First create minimal required data
                from app.models import Organization, User, Staff, Patient, AppointmentType, AppointmentStatus
                
                # Create a test organization
                org = Organization(
                    public_id='test_org_001',
                    name='Test Clinic',
                    address='123 Test St',
                    city='Test City',
                    state='TS',
                    country='USA',
                    postal_code='12345',
                    phone='555-1234',
                    email='test@clinic.com',
                    is_active=True
                )
                db.session.add(org)
                
                # Create test user
                user = User(
                    public_id='test_user_001',
                    email='doctor@test.com',
                    password_hash='test',
                    first_name='Test',
                    last_name='Doctor',
                    organization_id='test_org_001',
                    is_active=True
                )
                db.session.add(user)
                db.session.flush()
                
                # Create test staff
                staff = Staff(
                    user_id=user.id,
                    organization_id='test_org_001',
                    staff_number='EMP001',
                    job_title='Dentist',
                    department='Clinical',
                    employment_type='Full-time',
                    status='Active',
                    work_email='doctor@test.com'
                )
                db.session.add(staff)
                
                # Create test patient
                patient = Patient(
                    public_id='test_patient_001',
                    organization_id='test_org_001',
                    first_name='Test',
                    last_name='Patient',
                    email='patient@test.com',
                    phone='555-5678',
                    status='active',
                    is_active=True
                )
                db.session.add(patient)
                db.session.flush()
                
                # Create test appointment type and status if they don't exist
                appt_type = AppointmentType.query.first()
                if not appt_type:
                    appt_type = AppointmentType(
                        code='checkup',
                        name='Dental Checkup',
                        description='Routine dental examination',
                        default_duration=30,
                        color='#3498db'
                    )
                    db.session.add(appt_type)
                
                appt_status = AppointmentStatus.query.first()
                if not appt_status:
                    appt_status = AppointmentStatus(
                        code='scheduled',
                        name='Scheduled',
                        description='Appointment is scheduled',
                        color='#2ecc71'
                    )
                    db.session.add(appt_status)
                
                db.session.flush()
                
                # Now create test appointment
                from app.models.clinical.appointment import Appointment
                from datetime import datetime, timedelta
                
                test_appt = Appointment(
                    organization_id='test_org_001',
                    patient_id=patient.id,
                    dentist_id=staff.id,  # This is the required field
                    staff_id=staff.id,
                    appointment_type_id=appt_type.id,
                    status_id=appt_status.id,
                    title='Test Appointment',
                    description='Test appointment description',
                    start_time=datetime.now(),
                    end_time=datetime.now() + timedelta(hours=1),
                    treatment_room='Room 1'
                )
                db.session.add(test_appt)
                db.session.commit()
                
                print("✅ Test appointment created successfully!")
                print(f"   Appointment ID: {test_appt.id}")
                print(f"   Public ID: {test_appt.public_id}")
                
                # Count appointments
                count = db.session.query(Appointment).count()
                print(f"   Total appointments: {count}")
                
            except Exception as e:
                db.session.rollback()
                print(f"❌ Test appointment failed: {e}")
                import traceback
                traceback.print_exc()
        
        return 'appointments' in tables

if __name__ == '__main__':
    success = manual_table_creation()
    if success:
        print("\n🎉 Manual table creation successful!")
        print("📝 Next: Run the full seeder")
        print("python backend/scripts/seed_demo_data.py")
    else:
        print("\n❌ Manual table creation failed!")
        sys.exit(1)