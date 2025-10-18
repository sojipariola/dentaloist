# backend/scripts/create_super_admin.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, UserRole, Role, Permission
from werkzeug.security import generate_password_hash

def create_super_admin():
    app = create_app()
    
    with app.app_context():
        print("👑 CREATING SUPER ADMIN USER")
        print("=" * 50)
        
        # Check if super admin already exists
        super_admin = User.query.filter_by(email='superadmin@dentaloist.com').first()
        
        if super_admin:
            print("✅ Super admin already exists")
            return True
        
        # Get or create admin user role
        admin_role = UserRole.query.filter_by(code='admin').first()
        if not admin_role:
            print("❌ Admin user role not found!")
            return False
        
        # Create super admin user
        super_admin = User(
            public_id='super_admin_001',
            email='superadmin@dentaloist.com',
            password_hash=generate_password_hash('SuperAdmin123!'),
            first_name='Super',
            last_name='Admin',
            user_role_id=admin_role.id,
            organization_id='org_001',  # Assign to first organization
            email_verified=True,
            is_active=True
        )
        
        db.session.add(super_admin)
        
        try:
            db.session.commit()
            print("✅ Super admin created successfully!")
            print("   📧 Email: superadmin@dentaloist.com")
            print("   🔑 Password: SuperAdmin123!")
            print("   🏢 Organization: Bright Smile Dental Clinic")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating super admin: {e}")
            return False

if __name__ == '__main__':
    success = create_super_admin()
    if success:
        print("\n🎉 Try logging in with superadmin@dentaloist.com / SuperAdmin123!")
    else:
        print("\n❌ Failed to create super admin!")