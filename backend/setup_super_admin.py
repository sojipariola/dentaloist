import os
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import User, Organization, UserRole
from werkzeug.security import generate_password_hash

def setup_super_admin():
    app = create_app()
    
    with app.app_context():
        print("👑 Setting up Super Admin account...")
        
        # Check if super admin role exists
        super_admin_role = UserRole.query.filter_by(code='SUPER_ADMIN').first()
        if not super_admin_role:
            print("❌ SUPER_ADMIN role not found! Please seed user roles first.")
            return
        
        # Check if user already exists
        existing_user = User.query.filter_by(email='sojipariola@gmail.com').first()
        
        if existing_user:
            print("✅ Super admin user already exists:")
            print(f"   Name: {existing_user.first_name} {existing_user.last_name}")
            print(f"   Email: {existing_user.email}")
            print(f"   Organization: {existing_user.organization_id}")
            
            # Update password and ensure super admin role
            existing_user.password_hash = generate_password_hash('Soji1111')
            if super_admin_role not in existing_user.roles:
                existing_user.roles.append(super_admin_role)
                print("   Added SUPER_ADMIN role")
            
            db.session.commit()
            print("✅ Password updated and role verified")
            
        else:
            # Create new super admin user
            print("🆕 Creating new super admin user...")
            
            # Get first organization or create a dummy one for super admin
            first_org = Organization.query.first()
            if not first_org:
                print("❌ No organizations found! Please seed organizations first.")
                return
            
            super_admin = User(
                first_name='Soji',
                last_name='Pariola',
                email='sojipariola@gmail.com',
                password_hash=generate_password_hash('Soji1111'),
                organization_id=first_org.public_id,  # Associate with an org for data structure
                public_id='super_admin_soji',
                is_active=True,
                email_verified=True
            )
            
            super_admin.roles.append(super_admin_role)
            db.session.add(super_admin)
            db.session.commit()
            
            print("✅ Super admin created successfully!")
            print(f"   Name: Soji Pariola")
            print(f"   Email: sojipariola@gmail.com")
            print(f"   Password: Soji1111")
            print(f"   Organization: {first_org.name}")
        
        # Verify setup
        print("\n🔍 Verification:")
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        roles = [role.name for role in user.roles]
        print(f"   Roles: {roles}")
        print(f"   Is Super Admin: {'SUPER_ADMIN' in roles}")

if __name__ == '__main__':
    setup_super_admin()
