import os
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models import User, Organization, UserRole
from werkzeug.security import generate_password_hash

def setup_super_admin_complete():
    app = create_app()
    
    with app.app_context():
        print("👑 Complete Super Admin Setup...")
        
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
            
            # Also add to many-to-many roles if not already there
            if super_admin_role not in existing_user.roles:
                existing_user.roles.append(super_admin_role)
                print("   Added to many-to-many roles")
            
        else:
            print("🆕 Creating new user...")
            
            first_org = Organization.query.first()
            if not first_org:
                print("❌ No organizations found!")
                return
            
            # Create user with required user_role_id
            super_admin = User(
                first_name='Soji',
                last_name='Pariola', 
                email='sojipariola@gmail.com',
                password_hash=generate_password_hash('Soji1111'),
                organization_id=first_org.public_id,
                user_role_id=super_admin_role.id,  # Required field
                public_id='super_admin_soji',
                is_active=True,
                email_verified=True
            )
            
            db.session.add(super_admin)
            db.session.flush()  # Get ID without commit
            
            # Add to many-to-many roles
            super_admin.roles.append(super_admin_role)
            
        db.session.commit()
        print("✅ Super admin setup completed!")
        
        # Final verification
        print("\n�� Final Verification:")
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        if user:
            print(f"   ✅ User: {user.first_name} {user.last_name}")
            print(f"   ✅ Email: {user.email}")
            print(f"   ✅ Organization: {user.organization_id}")
            print(f"   ✅ User Role ID: {user.user_role_id}")
            
            role = UserRole.query.get(user.user_role_id)
            if role:
                print(f"   ✅ Primary Role: {role.name}")
            
            m2m_roles = [r.name for r in user.roles]
            print(f"   ✅ Many-to-many Roles: {m2m_roles}")
            
            print(f"\\n🎉 Login credentials:")
            print(f"   Email: sojipariola@gmail.com")
            print(f"   Password: Soji1111")

if __name__ == '__main__':
    setup_super_admin_complete()
