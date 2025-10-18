#!/usr/bin/env python3
import os
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def direct_setup():
    print("🚀 Direct database setup (no migrations)...")
    
    from app import create_app, db
    from sqlalchemy import text, inspect
    
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            
            # Verify
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Successfully created {len(tables)} tables")
            
            # Create test data
            from app.models.core import User, Tenant, Organization
            
            # Create tenant
            tenant = Tenant(
                name="Dentaloist Clinic",
                contact_email="admin@dentaloist.com",
                status="ACTIVE"
            )
            db.session.add(tenant)
            db.session.flush()
            
            # Create organization
            org = Organization(
                name="Main Dental Practice",
                type="CLINIC",
                email="info@dentaloist.com",
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.flush()
            
            # Create users
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
            
            dentist = User(
                email="dr.smith@dentaloist.com",
                first_name="John",
                last_name="Smith",
                role="dentist",
                organization_id=org.public_id,
                tenant_id=tenant.id
            )
            dentist.set_password("dentist123")
            db.session.add(dentist)
            
            db.session.commit()
            
            print("✅ Database setup complete!")
            print("👥 Users created:")
            print("   - admin@dentaloist.com / admin123")
            print("   - dr.smith@dentaloist.com / dentist123")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    if direct_setup():
        print("🎉 Database ready!")
        sys.exit(0)
    else:
        print("💥 Setup failed!")
        sys.exit(1)
