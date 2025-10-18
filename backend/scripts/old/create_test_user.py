# create_test_user.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, Organization
from werkzeug.security import generate_password_hash

def create_test_data():
    app = create_app()
    
    with app.app_context():
        print("🚀 Starting test data creation...")
        
        # Check if organization exists
        org = Organization.query.filter_by(id="test-tenant-001").first()
        if not org:
            print("🏥 Creating organization...")
            org = Organization(
                id="test-tenant-001",
                name="Test Dental Clinic",
                email="test@clinic.com",
                phone="+1234567890",
                is_active=True
            )
            db.session.add(org)
            db.session.commit()
            print("✅ Organization created")
        else:
            print("✅ Organization already exists")
        
        # Check if user exists
        user = User.query.filter_by(email="doctor@test.com").first()
        if not user:
            print("👤 Creating user...")
            user = User(
                email="doctor@test.com",
                first_name="Test",
                last_name="Doctor",
                organization_id="test-tenant-001",
                role="doctor",
                is_active=True
            )
            # Set password using the proper method
            user.set_password("test123")
            db.session.add(user)
            db.session.commit()
            print("✅ User created: doctor@test.com / test123")
        else:
            print("✅ User already exists")
            # Update password just in case
            user.set_password("test123")
            db.session.commit()
            print("✅ Password reset to: test123")
        
        # Verify everything works
        verify_user = User.query.filter_by(email="doctor@test.com").first()
        if verify_user and verify_user.check_password("test123"):
            print(f"✅ Verification successful!")
            print(f"   User ID: {verify_user.id}")
            print(f"   Email: {verify_user.email}")
            print(f"   Organization: {verify_user.organization_id}")
            print(f"   Role: {verify_user.role}")
            print(f"   Is Active: {verify_user.is_active}")
        else:
            print("❌ Verification failed!")
        
        # Show all users
        print("\n📊 All users in database:")
        users = User.query.all()
        for u in users:
            print(f"   - {u.id}: {u.email} (Org: {u.organization_id})")

if __name__ == "__main__":
    create_test_data()