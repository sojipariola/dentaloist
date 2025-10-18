#!/usr/bin/env python3
import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def create_fresh_database():
    print("🔄 Creating fresh database after fixing indexes...")
    
    from app import create_app, db
    from sqlalchemy import text
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            
            # Verify creation
            tables = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            table_names = [t[0] for t in tables]
            
            print(f"✅ Successfully created {len(table_names)} tables")
            print("Sample tables:")
            for table in sorted(table_names)[:10]:  # Show first 10 tables
                print(f"  - {table}")
            if len(table_names) > 10:
                print(f"  ... and {len(table_names) - 10} more tables")
            
            # Create test admin user
            from app.models.user import User
            from app.models.tenant import Tenant
            from app.models.organization import Organization
            
            # Create default tenant
            tenant = Tenant(
                name="Development Tenant",
                contact_email="admin@dentaloist.com",
                status="ACTIVE"
            )
            db.session.add(tenant)
            db.session.flush()
            
            # Create default organization
            org = Organization(
                name="Main Dental Clinic",
                type="CLINIC", 
                email="clinic@dentaloist.com",
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.flush()
            
            # Create admin user
            admin = User(
                email="admin@dentaloist.com",
                first_name="Admin",
                last_name="User",
                role="admin",
                organization_id=org.public_id,
                tenant_id=tenant.id
            )
            admin.set_password("admin123")
            db.session.add(admin)
            
            # Create dentist user
            dentist = User(
                email="dentist@dentaloist.com",
                first_name="John",
                last_name="Dentist", 
                role="dentist",
                organization_id=org.public_id,
                tenant_id=tenant.id
            )
            dentist.set_password("dentist123")
            db.session.add(dentist)
            
            db.session.commit()
            
            print("✅ Default data created:")
            print("   Tenant: Development Tenant")
            print("   Organization: Main Dental Clinic") 
            print("   Users:")
            print("     - admin@dentaloist.com / admin123 (Admin)")
            print("     - dentist@dentaloist.com / dentist123 (Dentist)")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if create_fresh_database():
        print("🎉 Database creation successful!")
        sys.exit(0)
    else:
        print("💥 Database creation failed!")
        sys.exit(1)
