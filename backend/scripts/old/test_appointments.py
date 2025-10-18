# backend/scripts/test_appointments.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Appointment

app = create_app()

with app.app_context():
    print("🧪 Testing appointments table access...")
    
    try:
        # Test 1: Count appointments
        count = Appointment.query.count()
        print(f"✅ Current appointments in database: {count}")
        
        # Test 2: Try to create one appointment
        from app.models import Patient, Staff, AppointmentType, AppointmentStatus
        
        # Get first available records
        patient = Patient.query.first()
        staff = Staff.query.first()
        appt_type = AppointmentType.query.first()
        status = AppointmentStatus.query.first()
        
        if all([patient, staff, appt_type, status]):
            test_appt = Appointment(
                organization_id=patient.organization_id,
                patient_id=patient.id,
                staff_id=staff.id,
                appointment_type_id=appt_type.id,
                status_id=status.id,
                title="Test Appointment",
                start_time=db.func.now(),
                end_time=db.func.now()
            )
            
            db.session.add(test_appt)
            db.session.commit()
            print("✅ Successfully created test appointment!")
            
            # Clean up
            db.session.delete(test_appt)
            db.session.commit()
            print("✅ Test appointment cleaned up")
        else:
            print("❌ Missing required data for test")
            
    except Exception as e:
        print(f"❌ Error accessing appointments: {e}")
        import traceback
        traceback.print_exc()