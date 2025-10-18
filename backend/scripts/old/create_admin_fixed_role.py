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
        
        # Check if there are any users with invalid roles using raw SQL
        result = db.session.execute(text("SELECT id, email, role FROM users WHERE email = 'admin@dentaloist.com'"))
        existing_user = result.fetchone()
        
        if existing_user:
            print(f"Found existing user: {existing_user}")
            # Check if the role is invalid
            if existing_user[2] not in ['SUPER_ADMIN', 'ORG_ADMIN', 'DENTIST', 'LAB_TECHNICIAN', 'ASSISTANT', 'NURSE', 'BILLING_STAFF', 'RESEARCHER', 'FAMILY_MEMBER', 'VISITOR', 'STAFF', 'USER', 'ADMIN', 'RECEPTIONIST', 'PATIENT']:
                print("Fixing invalid user role...")
                # Update the user with correct role
                db.session.execute(
                    text("UPDATE users SET role = 'SUPER_ADMIN' WHERE id = :id"),
                    {'id': existing_user[0]}
                )
                db.session.commit()
                print("✅ User role fixed")
            print("⚠️ Admin user already exists")
            sys.exit(0)
        
        # Create admin user with correct role enum value
        print("Creating admin user...")
        password_hash = hash_password('admin123')
        
        # Use SUPER_ADMIN as the role (highest privilege)
        admin_user = User(
            email='admin@dentaloist.com',
            password_hash=password_hash['hash'],
            first_name='System',
            last_name='Administrator',
            role='SUPER_ADMIN',  # Use valid enum value
            organization_id=org.id,
            is_active=True
        )
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print("Email: admin@dentaloist.com")
        print("Password: admin123")
        print("Role: SUPER_ADMIN")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        sys.exit(1)
