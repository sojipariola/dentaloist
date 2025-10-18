#!/usr/bin/env python3
import os
import sys
import sqlite3
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def nuclear_reset():
    print("💥 NUCLEAR RESET - Complete database cleanup...")
    
    # Remove any existing database files
    instance_path = current_dir / "instance"
    db_path = instance_path / "app.db"
    
    if db_path.exists():
        print(f"Removing database file: {db_path}")
        os.remove(db_path)
    
    # Also check for any other SQLite files
    for sqlite_file in current_dir.glob("*.db"):
        print(f"Removing SQLite file: {sqlite_file}")
        os.remove(sqlite_file)
    
    for sqlite_file in current_dir.glob("*.sqlite"):
        print(f"Removing SQLite file: {sqlite_file}")
        os.remove(sqlite_file)
    
    # Create a brand new empty database
    print("Creating fresh database...")
    conn = sqlite3.connect(str(db_path))
    conn.execute("VACUUM;")  # This creates a clean database file
    conn.close()
    
    print("✅ Database file reset complete")
    
    # Now initialize with Flask
    from app import create_app, db
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Creating database tables...")
            
            # First, let's try to create tables one by one to identify the problem
            from sqlalchemy import inspect
            
            # Drop all existing tables if any
            try:
                db.drop_all()
            except:
                pass  # Ignore errors if no tables exist
            
            # Create all tables
            db.create_all()
            
            # Verify
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Successfully created {len(tables)} tables")
            
            # Create minimal test data
            from app.models.user import User
            
            test_user = User(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                role="admin"
            )
            test_user.set_password("admin123")
            db.session.add(test_user)
            db.session.commit()
            
            print("✅ Test user created: admin@example.com / admin123")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if nuclear_reset():
        print("�� Nuclear reset completed successfully!")
        sys.exit(0)
    else:
        print("💥 Nuclear reset failed!")
        sys.exit(1)
