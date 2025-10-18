import os
import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import User, Organization, UserRole

def test_super_admin_access():
    app = create_app()
    
    with app.app_context():
        print("🧪 Testing Super Admin Tenant Access...")
        print("=" * 50)
        
        # Find user
        user = User.query.filter_by(email='sojipariola@gmail.com').first()
        if not user:
            print("❌ User not found!")
            return
        
        print(f"✅ Found user: {user.first_name} {user.last_name}")
        
        # Check user_role_id
        print(f"📋 User Role ID: {user.user_role_id}")
        primary_role = UserRole.query.get(user.user_role_id)
        if primary_role:
            print(f"   Primary Role: {primary_role.name} (Code: {primary_role.code})")
            is_super_admin = (primary_role.code == 'SUPER_ADMIN')
            print(f"   Is Super Admin: {is_super_admin}")
        else:
            print("❌ No primary role found!")
            return
        
        # Check what organizations are available
        organizations = Organization.query.all()
        print(f"\\n🏢 All Organizations ({len(organizations)} total):")
        for org in organizations:
            print(f"   • {org.name} (ID: {org.public_id})")
        
        # Simulate tenant switching logic
        print(f"\\n🔄 Tenant Switching Capability:")
        if is_super_admin:
            print("   ✅ CAN switch between all tenants")
            print("   ✅ CAN access all organization data")
            print("   ✅ CAN manage users across organizations")
        else:
            print("   ❌ CANNOT switch tenants (not super admin)")
            print("   ❌ Limited to own organization only")
        
        # Show current user context
        current_org = Organization.query.filter_by(public_id=user.organization_id).first()
        if current_org:
            print(f"\\n📍 Current Context:")
            print(f"   Organization: {current_org.name}")
            print(f"   User's assigned org: {user.organization_id}")
        
        print(f"\\n🎯 For tenant switching, check if user_role_id == SUPER_ADMIN role ID")

if __name__ == '__main__':
    test_super_admin_access()
