# backend/scripts/check_migration_status.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    print("🔍 MIGRATION STATUS CHECK")
    print("=" * 50)
    
    # Check current database state
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Current tables: {tables}")
    
    # Check alembic version
    try:
        result = db.session.execute(db.text("SELECT version_num FROM alembic_version"))
        current_version = result.scalar()
        print(f"Current alembic version: {current_version}")
    except Exception as e:
        print(f"Error checking alembic version: {e}")
    
    # Try to create tables directly
    print("\n🔄 Attempting direct table creation...")
    try:
        db.create_all()
        
        # Check again
        inspector = inspect(db.engine)
        new_tables = inspector.get_table_names()
        print(f"Tables after direct creation: {len(new_tables)}")
        
        if 'appointments' in new_tables:
            print("✅ APPOINTMENTS TABLE CREATED!")
        else:
            print("❌ appointments still missing")
            print("Available tables:")
            for table in sorted(new_tables)[:30]:
                print(f"   - {table}")
                
    except Exception as e:
        print(f"❌ Direct creation failed: {e}")