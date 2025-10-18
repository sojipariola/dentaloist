#!/usr/bin/env python3
import sys
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def add_admin():
    print("👤 Adding admin user...")
    
    try:
        from app import create_app, db
        from app.models import User, Organization, Tenant, Staff
        from datetime import datetime, date
        
        app = create_app()
        
        with app.app_context():
            # Check if admin already exists
            admin = User.query.filter_by(email="sojipariola@gmail.com").first()
            if admin:
                print("⚠️ Admin already exists, updating password...")
                admin.set_password("Soji1111")
                db.session.commit()
                print("✅ Admin password updated")
                return
            
            # Get or create tenant and organization
            tenant = Tenant.query.first()
            org = Organization.query.first()
            
            if not tenant:
                print("❌ No tenant found")
                return
            if not org:
                print("❌ No organization found")  
                return
            
            # Create admin user
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
            
            # Create staff record
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
            
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("📧 Email: sojipariola@gmail.com")
            print("🔑 Password: Soji1111")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_admin()
