#!/usr/bin/env python3
"""
Complete Database Reset Script
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def reset_database():
    print("🚀 Starting complete database reset...")
    
    # Ensure instance directory exists
    os.makedirs("instance", exist_ok=True)
    
    try:
        from app import create_app, db
        from app.models import (
            User, Organization, Tenant, Staff, 
            UserRole, OrganizationType, SubscriptionPlan, TenantStatus
        )
        from datetime import datetime, date
        
        # Create Flask app context
        app = create_app()
        
        with app.app_context():
            print("🧹 Dropping all tables...")
            db.drop_all()
            
            print("📦 Creating all tables...")
            db.create_all()
            
            # Verify tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Created {len(tables)} tables")
            
            # Create tenant
            print("🏢 Creating tenant...")
            tenant = Tenant(
                name="Dentaloist Main Tenant",
                subdomain="default",
                display_name="Dentaloist",
                contact_email="sojipariola@gmail.com",
                subscription_plan=SubscriptionPlan.PROFESSIONAL,
                status=TenantStatus.ACTIVE,
                max_users=50,
                max_patients=10000,
                is_active=True
            )
            db.session.add(tenant)
            db.session.flush()
            
            # Create organization
            print("🏥 Creating organization...")
            org = Organization(
                name="Dentaloist Clinic",
                type=OrganizationType.CLINIC,
                max_staff=50,
                max_patients=1000,
                is_active=True,
                is_verified=True,
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.flush()
            
            # Create admin user
            print("👤 Creating admin user...")
            admin = User(
                email="sojipariola@gmail.com",
                first_name="Soji",
                last_name="Pariola",
                role=UserRole.SUPER_ADMIN,
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
            
            # Create staff record
            print("👨‍💼 Creating staff record...")
            staff = Staff(
                organization_id=org.public_id,
                user_id=admin.id,
                staff_number="ADM001",
                job_title="System Administrator",
                department="Administration",
                employment_type="full-time",
                hire_date=date.today(),
                status="active"
            )
            db.session.add(staff)
            
            # Commit everything
            db.session.commit()
            print("💾 All changes committed")
            
            # Final verification
            print("\n📊 Final verification:")
            tables = inspector.get_table_names()
            print(f"Total tables: {len(tables)}")
            
            # Check login_attempts has failure_reason
            if 'login_attempts' in tables:
                columns = [col['name'] for col in inspector.get_columns('login_attempts')]
                if 'failure_reason' in columns:
                    print("✅ failure_reason column exists in login_attempts")
                else:
                    print("❌ failure_reason column missing")
            
            # Verify admin user
            admin_check = User.query.filter_by(email="sojipariola@gmail.com").first()
            if admin_check and admin_check.check_password("Soji1111"):
                print("✅ Admin user created and password works")
            else:
                print("❌ Admin user issue")
            
            print("\n🎉 Database reset complete!")
            print("📧 Login: sojipariola@gmail.com")
            print("🔑 Password: Soji1111")
            
    except Exception as e:
        print(f"❌ Error during reset: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    reset_database()
