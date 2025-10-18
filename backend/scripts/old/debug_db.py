#!/usr/bin/env python3
import os
import sqlite3
from pathlib import Path

def debug_database():
    print("🔍 Debugging database connection...")
    
    # Check instance directory
    instance_path = "instance"
    db_path = "instance/app.db"
    
    print(f"Instance directory: {instance_path}")
    print(f"Database path: {db_path}")
    print(f"Instance exists: {os.path.exists(instance_path)}")
    print(f"Database exists: {os.path.exists(db_path)}")
    
    if os.path.exists(instance_path):
        print(f"Instance permissions: {oct(os.stat(instance_path).st_mode)[-3:]}")
    
    if os.path.exists(db_path):
        print(f"Database permissions: {oct(os.stat(db_path).st_mode)[-3:]}")
        print(f"Database size: {os.path.getsize(db_path)} bytes")
    
    # Test direct SQLite connection
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Direct SQLite connection works: {result}")
        conn.close()
    except Exception as e:
        print(f"❌ Direct SQLite connection failed: {e}")
    
    # Test Flask SQLAlchemy connection
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            print("✅ Flask app created successfully")
            try:
                # Try a simple query
                result = db.session.execute("SELECT 1").scalar()
                print(f"✅ Flask SQLAlchemy connection works: {result}")
            except Exception as e:
                print(f"❌ Flask SQLAlchemy connection failed: {e}")
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")

if __name__ == "__main__":
    debug_database()
