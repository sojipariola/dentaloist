# backend/scripts/verify_fix.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    print("🔍 VERIFYING FIX")
    print("=" * 50)
    
    # Check if appointments table exists and can be queried
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    if 'appointments' in tables:
        print("✅ appointments table exists")
        
        # Check the problematic tables exist
        problem_tables = ['widgets', 'notifications']  # Tables that had ArrayOrJSON
        for table in problem_tables:
            if table in tables:
                print(f"✅ {table} table exists")
            else:
                print(f"❌ {table} table missing")
        
        # Try to query appointments
        try:
            from app.models.clinical import Appointment
            count = db.session.query(Appointment).count()
            print(f"✅ Can query appointments table - count: {count}")
        except Exception as e:
            print(f"❌ Cannot query appointments: {e}")
            
    else:
        print("❌ appointments table still missing")
        print("Available tables:")
        for table in sorted(tables)[:20]:
            print(f"   - {table}")