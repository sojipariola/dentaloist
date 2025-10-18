# backend/scripts/debug_admin_auth_logic.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, UserRole

def debug_admin_auth_logic():
    app = create_app()
    
    with app.app_context():
        print("🔍 DEBUGGING ADMIN AUTH LOGIC")
        print("=" * 50)
        
        # Test the admin user
        admin_user = User.query.filter_by(email='sojipariola@gmail.com').first()
        
        if admin_user:
            print(f"👤 Admin User: {admin_user.email}")
            print(f"   ID: {admin_user.id}")
            print(f"   Active: {admin_user.is_active}")
            print(f"   Email Verified: {admin_user.email_verified}")
            print(f"   Organization: {admin_user.organization_id}")
            
            # Check user role
            user_role = UserRole.query.get(admin_user.user_role_id)
            if user_role:
                print(f"   User Role: {user_role.name} (code: {user_role.code})")
                print(f"   Is Admin: {user_role.code == 'admin'}")
                print(f"   Access Level: {user_role.access_level}")
                print(f"   Can Manage Users: {user_role.can_manage_users}")
            else:
                print("   ❌ No user role assigned!")
            
            # Simulate the admin check that your app is doing
            is_admin_user = (
                admin_user.is_active and 
                admin_user.email_verified and 
                user_role and 
                user_role.code == 'admin'
            )
            
            print(f"\n🔑 WOULD PASS ADMIN CHECK: {is_admin_user}")
            
            if not is_admin_user:
                print("\n❌ REASONS FOR FAILURE:")
                if not admin_user.is_active:
                    print("   - User is not active")
                if not admin_user.email_verified:
                    print("   - Email not verified")
                if not user_role:
                    print("   - No user role assigned")
                if user_role and user_role.code != 'admin':
                    print(f"   - User role is '{user_role.code}' not 'admin'")
                    
        else:
            print("❌ Admin user not found!")

if __name__ == '__main__':
    debug_admin_auth_logic()