# debug_create_admin_db.py

from app import create_app, db
from app.models import User, Organization, Tenant, UserRole

app = create_app()

with app.app_context():
    try:
        print("🔍 Checking database state...")
        
        # Check existing records
        print(f"📊 Users: {User.query.count()}")
        print(f"📊 Organizations: {Organization.query.count()}")
        print(f"📊 Tenants: {Tenant.query.count()}")
        print(f"📊 UserRoles: {UserRole.query.count()}")
        
        # Check if we have the required lookup values
        super_admin_role = UserRole.query.filter_by(code='super_admin').first()
        print(f"🔑 Super Admin Role: {super_admin_role}")
        
        if super_admin_role:
            print(f"   - ID: {super_admin_role.id}")
            print(f"   - Code: {super_admin_role.code}")
            print(f"   - Name: {super_admin_role.name}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
