import os
import sys
sys.path.insert(0, '.')

from app import create_app, db
from app.models.organization_models import Organization
from app.models.user_models import User
from app.models.lookups import UserRole

app = create_app()
with app.app_context():
    print("🔍 Checking Admin Tenant Isolation...")
    print("=" * 50)
    
    # Check organizations
    organizations = Organization.query.all()
    print("🏢 Organizations:")
    for org in organizations:
        print(f"   • {org.name} (ID: {org.public_id})")
    
    # Check users and their roles per organization
    print("\n👥 Users by Organization:")
    for org in organizations:
        users = User.query.filter_by(organization_id=org.public_id).all()
        print(f"\\n   {org.name}:")
        for user in users:
            role_name = "Unknown"
            if user.roles:
                role_name = user.roles[0].name if user.roles else "No role"
            print(f"      - {user.first_name} {user.last_name} ({user.email}) - Role: {role_name}")
    
    # Check if there are any super admins across tenants
    print("\n👑 Super Admins Check:")
    super_admin_role = UserRole.query.filter_by(code='SUPER_ADMIN').first()
    if super_admin_role:
        super_admins = User.query.filter(User.roles.any(id=super_admin_role.id)).all()
        print(f"   Super Admins found: {len(super_admins)}")
        for admin in super_admins:
            print(f"      - {admin.first_name} {admin.last_name} (Org: {admin.organization_id})")
    else:
        print("   ❌ SUPER_ADMIN role not found")
    
    # Check cross-tenant data access potential
    print("\n🔒 Cross-Tenant Data Check:")
    for org in organizations:
        other_orgs = [o for o in organizations if o.public_id != org.public_id]
        if other_orgs:
            # Try to find if any user from this org can see other org's data
            users = User.query.filter_by(organization_id=org.public_id).all()
            print(f"   {org.name} users should NOT see:")
            for other_org in other_orgs[:2]:  # Show first 2 others
                print(f"      - {other_org.name} data")
