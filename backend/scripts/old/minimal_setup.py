#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def minimal_setup():
    print("🚀 Minimal database setup...")
    
    # Use absolute path
    db_path = current_dir / "instance" / "app.db"
    print(f"Database path: {db_path}")
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print("✅ App context created")
            
            # Just create tables - no data
            db.create_all()
            print("✅ Tables created")
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Created {len(tables)} tables")
            
            if 'users' in tables:
                print("✅ Users table exists")
            if 'login_attempts' in tables:
                columns = [col['name'] for col in inspector.get_columns('login_attempts')]
                print(f"Login attempts columns: {columns}")
                if 'failure_reason' in columns:
                    print("✅ failure_reason column exists!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    minimal_setup()
