from app import create_app, db
from app.models import User, Organization, Role
from app.utils.encryption import hash_password
import sys

app = create_app()

with app.app_context():
    try:
        # Check if organizations table exists and create one if needed
        org = Organization.query.first()
        if not org:
            print("Creating default organization...")
            # Use only the fields that actually exist in Organization model
            org = Organization(
                name="Default Organization",
                email="admin@dentaloist.com",
                type="dental_clinic",
                status="active"
                # Remove subscription_plan if it doesn't exist
            )
            db.session.add(org)
            db.session.commit()
            print("✅ Default organization created")
        
        # Check if admin role exists
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            print("Creating admin role...")
            admin_role = Role(
                name='admin',
                description='System Administrator',
                organization_id=org.id,
                is_system_role=True
            )
            db.session.add(admin_role)
            db.session.commit()
            print("✅ Admin role created")
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(email='admin@dentaloist.com').first()
        if admin_user:
            print("⚠️ Admin user already exists")
            print(f"Admin email: {admin_user.email}")
            sys.exit(0)
        
        # Create admin user
        print("Creating admin user...")
        password_hash = hash_password('admin123')
        admin_user = User(
            email='admin@dentaloist.com',
            password_hash=password_hash['hash'],
            password_salt=password_hash['salt'],
            first_name='System',
            last_name='Administrator',
            role='admin',
            organization_id=org.id,
            is_active=True,
            email_verified=True
        )
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Email: admin@dentaloist.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        sys.exit(1)
