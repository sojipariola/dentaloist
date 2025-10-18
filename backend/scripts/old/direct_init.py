#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def direct_db_init():
    print("🚀 Direct database initialization for SQLite...")
    
    from app import create_app, db
    
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables
            print("Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("Creating tables...")
            db.create_all()
            
            # Verify creation
            from sqlalchemy import text
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            
            print(f"✅ Successfully created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"   - {table}")
            
            # Create a test user
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
            print("✅ Test admin user created: admin@example.com / admin123")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if direct_db_init():
        print("🎉 Database initialization completed successfully!")
        sys.exit(0)
    else:
        print("💥 Database initialization failed!")
        sys.exit(1)
