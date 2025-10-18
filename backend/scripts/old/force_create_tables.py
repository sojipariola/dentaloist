# backend/scripts/force_create_tables.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def force_create_tables():
    app = create_app()
    
    with app.app_context():
        print("💥 FORCE CREATING ALL TABLES")
        print("=" * 50)
        
        # Drop all existing tables
        print("🗑️  Dropping all tables...")
        db.drop_all()
        
        # Create all tables
        print("📦 Creating all tables...")
        db.create_all()
        
        # Verify
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Created {len(tables)} tables")
        
        # Check for appointments table specifically
        if 'appointments' in tables:
            print("🎉 APPOINTMENTS TABLE CREATED!")
            
            # Count appointments
            from app.models.clinical import Appointment
            count = db.session.query(Appointment).count()
            print(f"📊 Appointments count: {count}")
        else:
            print("❌ appointments table still missing")
            print("Available tables:")
            for table in sorted(tables)[:30]:
                print(f"   - {table}")
        
        return 'appointments' in tables

if __name__ == '__main__':
    success = force_create_tables()
    if success:
        print("\n🎉 Table creation successful!")
        print("📝 Now run the seeder:")
        print("python scripts/seed_demo_data.py")
    else:
        print("\n❌ Table creation failed!")
        sys.exit(1)