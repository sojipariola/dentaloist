# backend/scripts/test_appointment_direct.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Appointment

app = create_app()

with app.app_context():
    print("🧪 DIRECT APPOINTMENT TEST")
    print("=" * 50)
    
    # Try to create the table directly
    try:
        # This creates ONLY the appointments table
        Appointment.__table__.create(db.engine)
        print("✅ appointments table created directly")
    except Exception as e:
        print(f"❌ Failed to create appointments table: {e}")
    
    # Verify
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'appointments' in tables:
        print("🎉 APPOINTMENTS TABLE EXISTS!")
        
        # Try to insert a test record
        try:
            test_appt = Appointment(
                organization_id='test_org',
                patient_id=1,
                staff_id=1,
                appointment_type_id=1,
                status_id=1,
                title="Test Appointment",
                start_time=db.func.now(),
                end_time=db.func.now()
            )
            db.session.add(test_appt)
            db.session.commit()
            print("✅ Test appointment inserted successfully!")
            
            # Clean up
            db.session.delete(test_appt)
            db.session.commit()
            print("✅ Test appointment cleaned up")
            
        except Exception as e:
            print(f"❌ Failed to insert test appointment: {e}")
    else:
        print("❌ appointments table still missing")