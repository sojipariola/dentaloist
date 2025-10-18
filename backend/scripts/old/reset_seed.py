# scripts/reset_seed.py
#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import db, Organization, User, Tenant, UserRole
from werkzeug.security import generate_password_hash

def main():
    print("🚀 Starting database reset and seed...")
    
    # Create app instance
    app = create_app()
    
    with app.app_context():
        try:
            # Drop all tables
            print("🗑️  Dropping all tables...")
            db.drop_all()
            print("✅ Tables dropped")
            
            # Create all tables
            print("🔧 Creating tables...")
            db.create_all()
            print("✅ Tables created")
            
            # Seed data
            print("🌱 Seeding data...")
            
            # Create tenant
            tenant = Tenant(
                name="Pariola Dental Clinic",
                subdomain="pariola",
                email="admin@parioladental.com",
                is_active=True
            )
            db.session.add(tenant)
            db.session.flush()
            
            # Create organization
            organization = Organization(
                name="Pariola Dental Clinic",
                email="info@parioladental.com",
                is_active=True
            )
            db.session.add(organization)
            db.session.flush()
            
            # Create admin user
            admin = User(
                email="sojipariola@gmail.com",
                first_name="Soji",
                last_name="Pariola",
                password_hash=generate_password_hash("Soji1111"),
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_admin=True,
                tenant_id=tenant.id,
                organization_id=organization.id
            )
            db.session.add(admin)
            
            db.session.commit()
            print("✅ Database seeded successfully!")
            print("\n🔑 Admin credentials:")
            print("   Email: sojipariola@gmail.com")
            print("   Password: Soji1111")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error: {e}")
            raise

if __name__ == "__main__":
    main()