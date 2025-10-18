# scripts/final_setup.py
#!/usr/bin/env python3
import os
import sys

# Set environment first
os.environ['EVENTLET_NO_MONKEYPATCH'] = '1'

# Add project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def setup_database():
    print("🚀 Setting up database...")
    
    from app import create_app
    from app.models.models import db, User, Tenant, Organization, UserRole
    from werkzeug.security import generate_password_hash
    
    app = create_app()
    
    with app.app_context():
        # Create tables
        print("🔧 Creating tables...")
        db.create_all()
        print("✅ Tables created")
        
        # Seed data
        print("🌱 Seeding data...")
        
        # Create tenant
        tenant = Tenant(
            name="Pariola Dental Clinic",
            subdomain="pariola",
            is_active=True
        )
        db.session.add(tenant)
        db.session.flush()
        
        # Create organization
        organization = Organization(
            name="Pariola Dental Clinic",
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
        print("✅ Database setup completed successfully!")
        print("\n🔑 Admin credentials:")
        print("   Email: sojipariola@gmail.com")
        print("   Password: Soji1111")

if __name__ == "__main__":
    setup_database()