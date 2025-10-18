#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def fresh_db_init():
    print("🔄 Fresh database initialization...")
    
    from app import create_app, db
    
    app = create_app()
    
    with app.app_context():
        try:
            # First, let's check if database file exists and remove it
            import sqlite3
            db_path = app.instance_path + '/app.db'
            if os.path.exists(db_path):
                print(f"Removing existing database: {db_path}")
                os.remove(db_path)
            
            # Now create all tables from scratch
            print("Creating all tables...")
            db.create_all()
            
            # Verify creation
            from sqlalchemy import text
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result]
            
            print(f"✅ Successfully created {len(tables)} tables")
            
            # Create essential test data
            from app.models.user import User
            from app.models.tenant import Tenant
            from app.models.organization import Organization
            
            # Create a default tenant
            default_tenant = Tenant(
                name="Development Tenant",
                contact_email="admin@example.com",
                status="ACTIVE"
            )
            db.session.add(default_tenant)
            db.session.flush()  # Get the ID without committing
            
            # Create a default organization
            default_org = Organization(
                name="Development Clinic",
                type="CLINIC",
                email="clinic@example.com",
                tenant_id=default_tenant.id
            )
            db.session.add(default_org)
            db.session.flush()
            
            # Create admin user
            admin_user = User(
                email="admin@example.com",
                first_name="Admin",
                last_name="User",
                role="admin",
                organization_id=default_org.public_id,
                tenant_id=default_tenant.id
            )
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            
            # Create dentist user
            dentist_user = User(
                email="dentist@example.com",
                first_name="John",
                last_name="Dentist",
                role="dentist",
                organization_id=default_org.public_id,
                tenant_id=default_tenant.id
            )
            dentist_user.set_password("dentist123")
            db.session.add(dentist_user)
            
            # Commit all
            db.session.commit()
            
            print("✅ Default tenant created")
            print("✅ Default organization created")
            print("✅ Test users created:")
            print("   - admin@example.com / admin123 (Admin)")
            print("   - dentist@example.com / dentist123 (Dentist)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during initialization: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    if fresh_db_init():
        print("🎉 Fresh database initialization completed successfully!")
        sys.exit(0)
    else:
        print("💥 Database initialization failed!")
        sys.exit(1)
