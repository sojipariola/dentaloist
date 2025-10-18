# scripts/simple_reset_fixed.py
#!/usr/bin/env python3
import os
import sys

# Set environment first
os.environ['EVENTLET_NO_MONKEYPATCH'] = '1'

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def reset_database():
    print("🚀 Starting database reset...")
    
    try:
        # Import after setting path and environment
        from app import create_app
        from app.models.models import db  # Import db from models
        from app.models.models import User, Tenant, Organization, UserRole
        from werkzeug.security import generate_password_hash
        
        # Create app
        app = create_app()
        
        with app.app_context():
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
            print("✅ Database reset and seed completed successfully!")
            print("\n🔑 Admin credentials:")
            print("   Email: sojipariola@gmail.com")
            print("   Password: Soji1111")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_database()