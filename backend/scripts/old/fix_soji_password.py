# backend/scripts/fix_soji_password.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

Email = 'sojipariola@gmail.com'
Password = 'Soji1111'

admin_users = [
    {'email': 'sojipariola@gmail.com', 'password': 'Soji1111'},
    {'email': 'superadmin@dentaloist.com', 'password': 'SuperAdmin123!'},
    {'email': 'admin1@brightsmiledentalclinic.com', 'password': 'Password123!'},
    {'email': 'admin2@perfectteethorthodontics.com', 'password': 'Password123!'},
    {'email': 'admin3@familydentalcarecenter.com', 'password': 'Password123!'}
]

def fix_admin_password():
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING ADMIN PASSWORD")
        print("=" * 50)
        
        # Find the admin user
        admin_user = User.query.filter_by(email=Email).first()
        
        if not admin_user:
            print("❌ Admin user not found!")
            return False
        
        print(f"🔧 Fixing password for: {admin_user.email}")
        
        # Generate proper password hash
        new_password_hash = generate_password_hash(Password)
        admin_user.password_hash = new_password_hash
        
        try:
            db.session.commit()
            print("✅ Admin password fixed successfully!")
            print(f"   New hash: {new_password_hash[:50]}...")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error fixing password: {e}")
            return False

if __name__ == '__main__':
    success = fix_admin_password()
    if success:
        print("\n🎉 Password fixed! Try logging in again.")
    else:
        print("\n❌ Failed to fix password!")