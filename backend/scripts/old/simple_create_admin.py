from app import create_app, db
from app.models import User, Organization, Role
from app.utils.encryption import hash_password

app = create_app()

with app.app_context():
    try:
        # Create organization
        print("Creating organization...")
        org = Organization(
            name="Default Dental Clinic",
            email="admin@dentaloist.com",
            type="CLINIC",
            status="active"
        )
        db.session.add(org)
        db.session.commit()
        print("✅ Organization created")
        
        # Create admin user
        print("Creating admin user...")
        pwd_hash = hash_password('admin123')
        admin = User(
            email='admin@dentaloist.com',
            password_hash=pwd_hash['hash'],
            password_salt=pwd_hash['salt'],
            first_name='Admin',
            last_name='User',
            role='admin',
            organization_id=org.id,
            is_active=True,
            email_verified=True
        )
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Email: admin@dentaloist.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
