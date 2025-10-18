#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def fixed_setup():
    print("🚀 Fixed database setup...")
    
    try:
        from app import create_app, db
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ App context created")
            
            # Create all tables
            db.create_all()
            print("✅ Tables created")
            
            # Verify tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Created {len(tables)} tables")
            
            # Check login_attempts specifically
            if 'login_attempts' in tables:
                columns = [col['name'] for col in inspector.get_columns('login_attempts')]
                print(f"Login attempts columns: {columns}")
                if 'failure_reason' in columns:
                    print("✅ failure_reason column exists!")
                else:
                    print("❌ failure_reason column missing")
            
            print("🎉 Database setup complete!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fixed_setup()
