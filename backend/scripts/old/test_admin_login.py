# backend/scripts/test_admin_login.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User
from werkzeug.security import check_password_hash

def test_admin_login():
    app = create_app()
    
    with app.app_context():
        print("🔐 TESTING ADMIN LOGIN")
        print("=" * 50)
        
        # Test credentials
        test_credentials = [
            ('sojipariola@gmail.com', 'Soji1111'),
            ('superadmin@dentaloist.com', 'SuperAdmin123!')
        ]
        
        for email, password in test_credentials:
            user = User.query.filter_by(email=email).first()
            if user:
                print(f"\n📧 Testing: {email}")
                print(f"   User exists: ✅")
                print(f"   Active: {user.is_active}")
                print(f"   Email verified: {user.email_verified}")
                
                # Check password
                password_correct = check_password_hash(user.password_hash, password)
                print(f"   Password correct: {password_correct}")
                
                if user.is_active and user.email_verified and password_correct:
                    print("   ✅ LOGIN SHOULD WORK!")
                else:
                    print("   ❌ Login issues detected")
            else:
                print(f"\n❌ User not found: {email}")

if __name__ == '__main__':
    test_admin_login()