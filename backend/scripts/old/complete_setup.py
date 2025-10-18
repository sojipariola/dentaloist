#!/usr/bin/env python3
"""
Complete Database Setup Script
"""

import os
import sys
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def setup_database():
    print("🚀 Starting complete database setup...")
    
    # Ensure instance directory exists
    instance_dir = current_dir / "instance"
    instance_dir.mkdir(exist_ok=True)
    
    # Create database file manually
    db_path = instance_dir / "app.db"
    if db_path.exists():
        db_path.unlink()
    
    # Create empty database file
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    conn.close()
    print("✅ Database file created")
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print("✅ App context created")
            
            # Create all tables
            db.create_all()
            print("✅ Tables created")
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📊 Created {len(tables)} tables")
            
            # Check login_attempts
            if 'login_attempts' in tables:
                columns = [col['name'] for col in inspector.get_columns('login_attempts')]
                print(f"Login attempts columns: {columns}")
                if 'failure_reason' in columns:
                    print("✅ failure_reason column exists!")
            
            print("🎉 Database setup complete!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_database()
