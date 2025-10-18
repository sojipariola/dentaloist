# backend/scripts/fix_all_admin_passwords.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def fix_all_admin_passwords():
    app = create_app()
    
    with app.app_context():
        print("🔧 FIXING ALL ADMIN PASSWORDS")
        print("=" * 50)
        
        admin_users = [
            {'email': 'sojipariola@gmail.com', 'password': 'Soji1111'},
            {'email': 'superadmin@dentaloist.com', 'password': 'SuperAdmin123!'},
            {'email': 'admin1@brightsmiledentalclinic.com', 'password': 'Password123!'},
            {'email': 'admin2@perfectteethorthodontics.com', 'password': 'Password123!'},
            {'email': 'admin3@familydentalcarecenter.com', 'password': 'Password123!'}
        ]
        
        fixed_count = 0
        
        for admin_info in admin_users:
            user = User.query.filter_by(email=admin_info['email']).first()
            
            if user:
                print(f"🔧 Fixing: {admin_info['email']}")
                
                # Generate proper password hash
                new_password_hash = generate_password_hash(admin_info['password'])
                user.password_hash = new_password_hash
                
                fixed_count += 1
                print(f"   ✅ Password hash updated")
            else:
                print(f"   ⚠️  User not found: {admin_info['email']}")
        
        try:
            db.session.commit()
            print(f"\n✅ Fixed {fixed_count} admin passwords!")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error fixing passwords: {e}")
            return False

if __name__ == '__main__':
    success = fix_all_admin_passwords()
    if success:
        print("\n🎉 All admin passwords fixed!")
        print("📝 Login credentials:")
        print("   sojipariola@gmail.com / Soji1111")
        print("   superadmin@dentaloist.com / SuperAdmin123!")
    else:
        print("\n❌ Failed to fix passwords!")