#!/usr/bin/env python3
"""
Database Seeding Script
"""

import sys
from pathlib import Path
from datetime import datetime, date

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def seed_database():
    print("🌱 Seeding database...")
    
    try:
        from app import create_app, db
        from app.models import User, Organization, Tenant, Staff, LoginAttempt
        
        app = create_app()
        
        with app.app_context():
            # Check if we already have data
            if User.query.first():
                print("⚠️ Database already has data. Skipping seeding.")
                return
            
            # 1. Create Tenant
            print("🏢 Creating tenant...")
            tenant = Tenant(
                name="Dentaloist Main Tenant",
                subdomain="default",
                display_name="Dentaloist",
                contact_email="sojipariola@gmail.com",
                subscription_plan="PROFESSIONAL",
                status="ACTIVE",
                max_users=50,
                max_patients=10000,
                is_active=True
            )
            db.session.add(tenant)
            db.session.flush()
            
            # 2. Create Organization
            print("🏥 Creating organization...")
            org = Organization(
                name="Dentaloist Clinic",
                type="CLINIC",
                max_staff=50,
                max_patients=1000,
                is_active=True,
                is_verified=True,
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.flush()
            
            # 3. Create Admin User
            print("👑 Creating admin user...")
            admin = User(
                email="sojipariola@gmail.com",
                first_name="Soji",
                last_name="Pariola",
                role="SUPER_ADMIN",
                organization_id=org.public_id,
                tenant_id=tenant.id,
                is_active=True,
                is_admin=True
            )
            admin.set_password("Soji1111")
            db.session.add(admin)
            db.session.flush()
            
            # Update tenant with admin info
            tenant.created_by = admin.id
            tenant.activated_by = admin.id
            tenant.activated_at = datetime.utcnow()
            
            # 4. Create Admin Staff Record
            print("👨‍💼 Creating admin staff record...")
            admin_staff = Staff(
                organization_id=org.public_id,
                user_id=admin.id,
                staff_number="ADM001",
                job_title="System Administrator",
                department="Administration",
                employment_type="full-time",
                hire_date=date.today(),
                status="active"
            )
            db.session.add(admin_staff)
            
            # 5. Create Sample Login Attempts
            print("🔐 Creating sample login attempts...")
            # Successful login
            success_attempt = LoginAttempt(
                username="sojipariola@gmail.com",
                ip_address="192.168.1.100",
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                success=True,
                user_id=admin.id,
                failure_reason=None
            )
            db.session.add(success_attempt)
            
            # Failed login
            failed_attempt = LoginAttempt(
                username="test@example.com",
                ip_address="192.168.1.101",
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                success=False,
                user_id=None,
                failure_reason="invalid_password"
            )
            db.session.add(failed_attempt)
            
            # Commit everything
            db.session.commit()
            print("💾 All data committed")
            
            # Final verification
            print("\n📊 Final verification:")
            user_count = User.query.count()
            staff_count = Staff.query.count()
            login_attempts_count = LoginAttempt.query.count()
            
            print(f"Users: {user_count}")
            print(f"Staff: {staff_count}")
            print(f"Login attempts: {login_attempts_count}")
            
            # Verify admin login
            admin_check = User.query.filter_by(email="sojipariola@gmail.com").first()
            if admin_check and admin_check.check_password("Soji1111"):
                print("✅ Admin user can login successfully")
            else:
                print("❌ Admin user login issue")
            
            print("\n🎉 Database seeding completed!")
            print("=" * 50)
            print("�� Admin Login: sojipariola@gmail.com")
            print("🔑 Admin Password: Soji1111")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        
        # Rollback on error
        try:
            db.session.rollback()
            print("🔄 Session rolled back due to error")
        except:
            pass

if __name__ == "__main__":
    seed_database()
