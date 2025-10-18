#!/usr/bin/env python3
"""
One-time admin setup script for Dentaloist
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models import User, Organization
from app.models.lookups import UserRole, OrganizationType, Currency

def setup_admin():
    print("🚀 Starting admin setup...")
    
    app = create_app()
    with app.app_context():
        try:
            # Use no_autoflush to prevent premature flushing
            with db.session.no_autoflush:
                # 1. Create or get required lookup values first
                
                # Get or create organization type
                org_type = OrganizationType.query.filter_by(name='Dental Clinic').first()
                if not org_type:
                    org_type = OrganizationType(
                        name='Dental Clinic',
                        code='dental_clinic',
                        description='Dental practice or clinic',
                        is_active=True
                    )
                    db.session.add(org_type)
                    print("✅ Created Dental Clinic organization type")
                else:
                    print("✅ Dental Clinic organization type already exists")
                
                # Get or create currency (USD)
                currency = Currency.query.filter_by(code='USD').first()
                if not currency:
                    currency = Currency(
                        code='USD',
                        name='US Dollar',
                        symbol='$',
                        is_active=True
                    )
                    db.session.add(currency)
                    print("✅ Created USD currency")
                else:
                    print("✅ USD currency already exists")
                
                # 2. Get or create admin role - FIXED: Check if it exists first
                admin_role = UserRole.query.filter_by(code='admin').first()
                if not admin_role:
                    admin_role = UserRole(
                        name='admin',
                        code='admin',
                        description='System Administrator',
                        is_system_role=True,
                        access_level=100,
                        can_manage_users=True,
                        can_access_reports=True,
                        is_active=True
                    )
                    db.session.add(admin_role)
                    print("✅ Created admin role")
                else:
                    print("✅ Admin role already exists")
                
                # 3. Create default organization with all required fields
                default_org = Organization.query.filter_by(public_id='default_org').first()
                if not default_org:
                    default_org = Organization(
                        name='Default Dental Clinic',
                        description='Default dental practice for system administration',
                        address='123 Main Street',
                        city='Anytown',
                        state='CA',
                        postal_code='12345',
                        country='USA',
                        phone='+1-555-0123',
                        email='info@dentaloist.com',
                        website='https://dentaloist.com',
                        timezone='America/Los_Angeles',
                        currency_id=currency.id,
                        organization_type_id=org_type.id,
                        tax_id='12-3456789',
                        business_type='private_practice',
                        industry='healthcare_dental',
                        max_staff=10,
                        max_patients=1000,
                        status='active',
                        is_verified=True,
                        public_id='default_org',
                        is_active=True
                    )
                    db.session.add(default_org)
                    print("✅ Created default organization with all required fields")
                else:
                    print("✅ Default organization already exists")
                
                # 4. Create admin user
                admin_user = User.query.filter_by(email='admin@dentaloist.com').first()
                if not admin_user:
                    # Make sure we have the admin_role ID
                    if not admin_role.id:
                        # If admin_role was just created, we need to flush to get the ID
                        db.session.flush()
                    
                    admin_user = User(
                        email='admin@dentaloist.com',
                        first_name='System',
                        last_name='Administrator',
                        user_role_id=admin_role.id,
                        organization_id='default_org',
                        is_admin=True,
                        is_active=True,
                        email_verified=True
                    )
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)
                    print("✅ Created admin user: admin@dentaloist.com / admin123")
                else:
                    # Update existing user to ensure admin permissions
                    admin_user.user_role_id = admin_role.id
                    admin_user.is_admin = True
                    admin_user.is_active = True
                    admin_user.email_verified = True
                    print("✅ Updated existing admin user")
            
            # Commit all changes at once
            db.session.commit()
            print("🎉 Admin setup completed successfully!")
            
            # Verify the setup
            admin_count = User.query.filter_by(user_role_id=admin_role.id, is_active=True).count()
            print(f"📊 Active admin users: {admin_count}")
            
            # Print login information
            print("\n🔑 Login Information:")
            print(f"   Email: admin@dentaloist.com")
            print(f"   Password: admin123")
            print(f"   Admin URL: http://localhost:5000/admin/")
            print(f"   API Login: http://localhost:5000/api/auth/admin-direct-login")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Admin setup failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    setup_admin()