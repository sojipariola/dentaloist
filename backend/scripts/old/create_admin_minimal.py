from app import create_app, db
from app.models import User, Organization, Role
from app.utils.encryption import hash_password
from sqlalchemy import text
import sys

app = create_app()

with app.app_context():
    try:
        # Check if organizations exist
        result = db.session.execute(text("SELECT id, name, type, status FROM organizations LIMIT 1"))
        org_row = result.fetchone()
        
        org = None
        if org_row:
            print(f"Found existing organization: {org_row}")
            org = Organization.query.get(org_row[0])
        else:
            print("Creating default organization...")
            org = Organization(
                name="Default Organization",
                email="admin@dentaloist.com",
                type="CLINIC",
                status="active"
            )
            db.session.add(org)
            db.session.commit()
            print("✅ Default organization created")
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(email='admin@dentaloist.com').first()
        if admin_user:
            print("⚠️ Admin user already exists")
            print(f"Admin email: {admin_user.email}")
            sys.exit(0)
        
        # Create admin user - with absolute minimum fields
        print("Creating admin user...")
        password_hash = hash_password('admin123')
        
        # Create user with only the most basic required fields
        admin_user = User(
            email='admin@dentaloist.com',
            password_hash=password_hash['hash'],
            first_name='System',
            last_name='Administrator',
            organization_id=org.id
            # Only include fields that are definitely required
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
