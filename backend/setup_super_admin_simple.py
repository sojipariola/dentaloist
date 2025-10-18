import os
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import User, Organization, UserRole
from werkzeug.security import generate_password_hash

def setup_super_admin_simple():
    app = create_app()
    
    with app.app_context():
        print("👑 Simple Super Admin Setup (Using user_role_id only)...")
        
        # Get the SUPER_ADMIN role
        super_admin_role = UserRole.query.filter_by(code='SUPER_ADMIN').first()
        if not super_admin_role:
            print("❌ SUPER_ADMIN role not found!")
            return
        
        print(f"✅ SUPER_ADMIN role ID: {super_admin_role.id}")
        
        # Check if user exists
        existing_user = User.query.filter_by(email='sojipariola@gmail.com').first()
        
        if existing_user:
            print("✅ User exists, updating...")
            existing_user.password_hash = generate_password_hash('Soji1111')
            existing_user.user_role_id = super_admin_role.id
            
            db.session.commit()
            print("✅ User updated successfully")
            
        else:
            print("🆕 Creating new user...")
            
            first_org = Organization.query.first()
            if not first_org:
                print("❌ No organizations found!")
                return
            
            # Create user with only the required user_role_id
            super_admin = User(
                first_name='Soji',
                last_name='Pariola', 
                email='sojipariola@gmail.com',
                password_hash=generate_password_hash('Soji1111'),
                organization_id=first_org.public_id,
                user_role_id=super_admin_role.id,  # This is the key field
                public_id='super_admin_soji',
                is_active=True,
                email_verified=True
            )
            
            db.session.add(super_admin)
            db.session.commit()
            
            print("✅ Super admin created successfully!")
        
        # Final verification
        print("\n🔍 Final Verification:")
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        if user:
            print(f"   ✅ User: {user.first_name} {user.last_name}")
            print(f"   ✅ Email: {user.email}")
            print(f"   ✅ Organization: {user.organization_id}")
            print(f"   ✅ User Role ID: {user.user_role_id}")
            
            role = UserRole.query.get(user.user_role_id)
            if role:
                print(f"   ✅ Role: {role.name} (Code: {role.code})")
            
            print(f"\\n🎉 Login credentials:")
            print(f"   Email: sojipariola@gmail.com")
            print(f"   Password: Soji1111")
            print(f"\\n💡 Note: Using user_role_id={super_admin_role.id} for super admin access")

if __name__ == '__main__':
    setup_super_admin_simple()
