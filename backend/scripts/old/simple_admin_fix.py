# simple_admin_fix.py
from app import create_app, db
from werkzeug.security import generate_password_hash
from sqlalchemy import text
import uuid

app = create_app()

with app.app_context():
    try:
        print("🔄 Creating admin with minimal dependencies...")
        
        # Check if admin already exists
        existing_admin = db.session.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": "sojipariola@gmail.com"}
        ).first()
        
        if existing_admin:
            print("✅ Admin user already exists")
        else:
            print("📚 Setting up required data...")
            
            # We already know super_admin role exists (ID: 1)
            role_id = 1
            print(f"🔑 Using role ID: {role_id}")
            
            # Check if tenant exists, create if not
            tenant = db.session.execute(
                text("SELECT id FROM tenants LIMIT 1")
            ).first()
            
            if tenant:
                tenant_id = tenant[0]
                print(f"🏢 Using existing tenant ID: {tenant_id}")
            else:
                print("🏢 Creating default tenant...")
                tenant_id = db.session.execute(
                    text("""
                        INSERT INTO tenants (name, subdomain, display_name, contact_email, status, max_users, max_patients, is_active) 
                        VALUES (:name, :subdomain, :display_name, :email, :status, :max_users, :max_patients, :is_active) 
                        RETURNING id
                    """),
                    {
                        "name": "Default Tenant",
                        "subdomain": "default", 
                        "display_name": "Default",
                        "email": "admin@example.com",
                        "status": 1,
                        "max_users": 50,
                        "max_patients": 1000,
                        "is_active": True
                    }
                ).scalar()
                print(f"🏢 Created tenant ID: {tenant_id}")
            
            # Check if organization exists, create if not
            org = db.session.execute(
                text("SELECT public_id FROM organizations LIMIT 1")
            ).first()
            
            if org:
                org_public_id = org[0]
                print(f"🏥 Using existing organization ID: {org_public_id}")
            else:
                print("🏥 Creating default organization...")
                org_public_id = str(uuid.uuid4())
                db.session.execute(
                    text("""
                        INSERT INTO organizations (public_id, name, type, email, tenant_id, max_staff, max_patients, status, is_verified, is_active) 
                        VALUES (:public_id, :name, :type, :email, :tenant_id, :max_staff, :max_patients, :status, :is_verified, :is_active)
                    """),
                    {
                        "public_id": org_public_id,
                        "name": "Default Clinic",
                        "type": 1,
                        "email": "info@example.com", 
                        "tenant_id": tenant_id,
                        "max_staff": 50,
                        "max_patients": 1000,
                        "status": "active",
                        "is_verified": True,
                        "is_active": True
                    }
                )
                print(f"🏥 Created organization with ID: {org_public_id}")
            
            # Create admin user
            print("👤 Creating admin user...")
            db.session.execute(
                text("""
                    INSERT INTO users (email, password_hash, first_name, last_name, role, organization_id, tenant_id, is_active, is_admin) 
                    VALUES (:email, :password_hash, :first_name, :last_name, :role, :organization_id, :tenant_id, :is_active, :is_admin)
                """),
                {
                    "email": "sojipariola@gmail.com",
                    "password_hash": generate_password_hash("Soji1111"),
                    "first_name": "Soji",
                    "last_name": "Pariola", 
                    "role": role_id,
                    "organization_id": org_public_id,
                    "tenant_id": tenant_id,
                    "is_active": True,
                    "is_admin": True
                }
            )
            
            db.session.commit()
            print("✅ Admin user created successfully!")
            print("🔑 Login: sojipariola@gmail.com / Soji1111")
            
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
