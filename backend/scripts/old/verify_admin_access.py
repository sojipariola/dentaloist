# backend/scripts/verify_admin_access.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Organization

app = create_app()

with app.app_context():
    print("🔐 ADMIN ACCESS VERIFICATION")
    print("=" * 50)
    
    # Find the admin user
    admin_user = User.query.filter_by(email='sojipariola@gmail.com').first()
    
    if admin_user:
        print(f"✅ Admin user found:")
        print(f"   📧 Email: {admin_user.email}")
        print(f"   👤 Name: {admin_user.first_name} {admin_user.last_name}")
        print(f"   🏢 Organization ID: {admin_user.organization_id}")
        
        # Get organization details
        org = Organization.query.filter_by(public_id=admin_user.organization_id).first()
        if org:
            print(f"   🏥 Organization: {org.name}")
        
        print(f"   ✅ Email verified: {admin_user.email_verified}")
        print(f"   ✅ Account active: {admin_user.is_active}")
        
        print(f"\n🎯 Ready to login at: http://localhost:5000/admin")
        print(f"   Use: sojipariola@gmail.com / Soji1111")
        
    else:
        print("❌ Admin user not found!")