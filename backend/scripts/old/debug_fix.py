#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path

def debug_and_fix():
    print("🔍 Debugging database issue...")
    
    current_dir = Path(__file__).parent
    instance_dir = current_dir / "instance"
    db_path = instance_dir / "app.db"
    
    print(f"Current directory: {current_dir}")
    print(f"Instance directory: {instance_dir}")
    print(f"Database path: {db_path}")
    print(f"Instance exists: {instance_dir.exists()}")
    print(f"Database exists: {db_path.exists()}")
    
    if instance_dir.exists():
        print(f"Instance permissions: {oct(instance_dir.stat().st_mode)}")
    
    if db_path.exists():
        print(f"Database permissions: {oct(db_path.stat().st_mode)}")
        print(f"Database size: {db_path.stat().st_size} bytes")
        
        # Test direct SQLite access
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✅ Direct SQLite access: {result}")
            conn.close()
        except Exception as e:
            print(f"❌ Direct SQLite error: {e}")
    
    # Check Flask configuration
    try:
        from app import create_app
        app = create_app()
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"Flask DB URI: {db_uri}")
        
        # Test Flask database connection
        with app.app_context():
            from app import db
            try:
                result = db.session.execute("SELECT 1").scalar()
                print(f"✅ Flask SQLAlchemy connection: {result}")
            except Exception as e:
                print(f"❌ Flask SQLAlchemy error: {e}")
    except Exception as e:
        print(f"❌ Flask app error: {e}")

if __name__ == "__main__":
    debug_and_fix()
