# create_soji_complete.py
from app import create_app, db
from werkzeug.security import generate_password_hash
from sqlalchemy import text
import uuid
from datetime import datetime

app = create_app()

with app.app_context():
    try:
        print("🔄 Creating admin with ALL required fields...")
        
        # Check if admin already exists
        existing_admin = db.session.execute(
            text("SELECT id FROM users WHERE email = :email"),
            {"email": "sojipariola@gmail.com"}
        ).first()
        
        if existing_admin:
            print("✅ Admin user already exists")
        else:
            print("📚 Setting up required data...")
            
            # We know super_admin role exists (ID: 1)
            role_id = 1
            
            # Check if industry types exist, create one if not
            industry = db.session.execute(
                text("SELECT id FROM industry_types LIMIT 1")
            ).first()
            
            if industry:
                industry_id = industry[0]
                print(f"🏭 Using existing industry ID: {industry_id}")
            else:
                print("🏭 Creating default industry type...")
                # Create a default industry type with ALL required fields
                industry_public_id = str(uuid.uuid4())
                industry_id = db.session.execute(
                    text("""
                        INSERT INTO industry_types (
                            code, name, description, public_id, is_active, created_at
                        ) 
                        VALUES (:code, :name, :desc, :public_id, :active, :created_at) 
                        RETURNING id
                    """),
                    {
                        "code": "healthcare", 
                        "name": "Healthcare", 
                        "desc": "Healthcare industry",
                        "public_id": industry_public_id,
                        "active": True,
                        "created_at": datetime.utcnow()
                    }
                ).scalar()
                print(f"🏭 Created industry ID: {industry_id}")
            
            # Check if tenant status exists, create one if not
            tenant_status = db.session.execute(
                text("SELECT id FROM tenant_statuses WHERE code = 'active'")
            ).first()
            
            if tenant_status:
                status_id = tenant_status[0]
                print(f"📊 Using existing tenant status ID: {status_id}")
            else:
                print("📊 Creating default tenant status...")
                status_public_id = str(uuid.uuid4())
                status_id = db.session.execute(
                    text("""
                        INSERT INTO tenant_statuses (
                            code, name, description, public_id, is_active, created_at
                        ) 
                        VALUES (:code, :name, :desc, :public_id, :active, :created_at) 
                        RETURNING id
                    """),
                    {
                        "code": "active",
                        "name": "Active", 
                        "desc": "Active tenant",
                        "public_id": status_public_id,
                        "active": True,
                        "created_at": datetime.utcnow()
                    }
                ).scalar()
                print(f"📊 Created tenant status ID: {status_id}")
            
            # Check if subscription plan exists, create one if not
            subscription_plan = db.session.execute(
                text("SELECT id FROM subscription_plans LIMIT 1")
            ).first()
            
            if subscription_plan:
                subscription_plan_id = subscription_plan[0]
                print(f"💰 Using existing subscription plan ID: {subscription_plan_id}")
            else:
                print("💰 Creating default subscription plan...")
                plan_public_id = str(uuid.uuid4())
                subscription_plan_id = db.session.execute(
                    text("""
                        INSERT INTO subscription_plans (
                            code, name, description, price_monthly, max_users, max_patients, 
                            public_id, is_active, created_at
                        ) 
                        VALUES (:code, :name, :desc, :price, :max_users, :max_patients, 
                                :public_id, :active, :created_at) 
                        RETURNING id
                    """),
                    {
                        "code": "professional",
                        "name": "Professional", 
                        "desc": "Professional plan",
                        "price": 199.00,
                        "max_users": 50,
                        "max_patients": 1000,
                        "public_id": plan_public_id,
                        "active": True,
                        "created_at": datetime.utcnow()
                    }
                ).scalar()
                print(f"💰 Created subscription plan ID: {subscription_plan_id}")
            
            # Check if organization type exists
            org_type = db.session.execute(
                text("SELECT id FROM organization_types LIMIT 1")
            ).first()
            
            if org_type:
                org_type_id = org_type[0]
                print(f"🏥 Using existing organization type ID: {org_type_id}")
            else:
                print("🏥 Creating default organization type...")
                org_type_public_id = str(uuid.uuid4())
                org_type_id = db.session.execute(
                    text("""
                        INSERT INTO organization_types (
                            code, name, description, public_id, is_active, created_at
                        ) 
                        VALUES (:code, :name, :desc, :public_id, :active, :created_at) 
                        RETURNING id
                    """),
                    {
                        "code": "clinic", 
                        "name": "Clinic", 
                        "desc": "Dental clinic",
                        "public_id": org_type_public_id,
                        "active": True,
                        "created_at": datetime.utcnow()
                    }
                ).scalar()
                print(f"🏥 Created organization type ID: {org_type_id}")
            
            # Create tenant with ALL required columns including subscription_plan_id
            tenant = db.session.execute(text("SELECT id FROM tenants LIMIT 1")).first()
            if not tenant:
                print("🏢 Creating default tenant...")
                tenant_public_id = str(uuid.uuid4())
                tenant_id = db.session.execute(
                    text("""
                        INSERT INTO tenants (
                            name, subdomain, display_name, contact_email, status_id, industry_id,
                            subscription_plan_id, max_users, max_patients, is_active, activated_at, 
                            public_id, created_at
                        ) 
                        VALUES (:name, :subdomain, :display_name, :email, :status_id, :industry_id,
                                :subscription_plan_id, :max_users, :max_patients, :is_active, :activated_at, 
                                :public_id, :created_at) 
                        RETURNING id
                    """),
                    {
                        "name": "Default Tenant",
                        "subdomain": "default", 
                        "display_name": "Default",
                        "email": "admin@example.com",
                        "status_id": status_id,
                        "industry_id": industry_id,
                        "subscription_plan_id": subscription_plan_id,  # New required field
                        "max_users": 50,
                        "max_patients": 1000,
                        "is_active": True,
                        "activated_at": datetime.utcnow(),
                        "public_id": tenant_public_id,
                        "created_at": datetime.utcnow()
                    }
                ).scalar()
                print(f"🏢 Created tenant ID: {tenant_id}")
            else:
                tenant_id = tenant[0]
                print(f"🏢 Using existing tenant ID: {tenant_id}")
            
            # Create organization with ALL required columns
            org = db.session.execute(text("SELECT public_id FROM organizations LIMIT 1")).first()
            if not org:
                print("🏥 Creating default organization...")
                org_public_id = str(uuid.uuid4())
                db.session.execute(
                    text("""
                        INSERT INTO organizations (
                            public_id, name, email, phone, tenant_id, organization_type_id,
                            max_staff, max_patients, status, is_verified, is_active, created_at
                        ) 
                        VALUES (:public_id, :name, :email, :phone, :tenant_id, :org_type_id,
                                :max_staff, :max_patients, :status, :is_verified, :is_active, :created_at)
                    """),
                    {
                        "public_id": org_public_id,
                        "name": "Default Clinic",
                        "email": "info@example.com",
                        "phone": "+1234567890",
                        "tenant_id": tenant_id,
                        "org_type_id": org_type_id,
                        "max_staff": 50,
                        "max_patients": 1000,
                        "status": "active",
                        "is_verified": True,
                        "is_active": True,
                        "created_at": datetime.utcnow()
                    }
                )
                print(f"🏥 Created organization with ID: {org_public_id}")
            else:
                org_public_id = org[0]
                print(f"🏥 Using existing organization ID: {org_public_id}")
            
            # Create admin user with ALL required columns
            print("👤 Creating admin user...")
            user_public_id = str(uuid.uuid4())
            db.session.execute(
                text("""
                    INSERT INTO users (
                        email, password_hash, first_name, last_name, user_role_id, 
                        organization_id, tenant_id, is_active, is_admin, public_id, created_at
                    ) 
                    VALUES (:email, :password_hash, :first_name, :last_name, :user_role_id, 
                            :organization_id, :tenant_id, :is_active, :is_admin, :public_id, :created_at)
                """),
                {
                    "email": "sojipariola@gmail.com",
                    "password_hash": generate_password_hash("Soji1111"),
                    "first_name": "Soji",
                    "last_name": "Pariola", 
                    "user_role_id": role_id,
                    "organization_id": org_public_id,
                    "tenant_id": tenant_id,
                    "is_active": True,
                    "is_admin": True,
                    "public_id": user_public_id,
                    "created_at": datetime.utcnow()
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