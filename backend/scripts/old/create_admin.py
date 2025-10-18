# create_admin.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime
from sqlalchemy import text  # Import text wrapper

def create_admin_direct_sql_complete():
    app = create_app()
    
    with app.app_context():
        try:
            # Check if organization exists with all required fields
            org_result = db.session.execute(
                text("SELECT id FROM organizations WHERE name = 'Main Dental Clinic'")
            ).fetchone()
            
            if not org_result:
                # Create organization with all required fields
                org_public_id = str(uuid.uuid4())
                db.session.execute(
                    text("""INSERT INTO organizations 
                    (name, type, email, country, subscription, status, 
                     business_type, industry, max_staff, max_patients,
                     is_verified, is_active, public_id, created_at, updated_at) 
                    VALUES (:name, :type, :email, :country, :subscription, :status,
                            :business_type, :industry, :max_staff, :max_patients,
                            :is_verified, :is_active, :public_id, :created_at, :updated_at)"""),
                    {
                        'name': 'Main Dental Clinic',
                        'type': 'CLINIC',
                        'email': 'admin@dentaloist.com',
                        'country': 'USA',
                        'subscription': 'FREE',
                        'status': 'active',
                        'business_type': 'PRIVATE_PRACTICE',
                        'industry': 'HEALTHCARE',
                        'max_staff': 10,
                        'max_patients': 1000,
                        'is_verified': True,
                        'is_active': True,
                        'public_id': org_public_id,
                        'created_at': datetime.utcnow(),
                        'updated_at': datetime.utcnow()
                    }
                )
                db.session.commit()
                
                # Get the new organization ID
                org_result = db.session.execute(
                    text("SELECT id FROM organizations WHERE public_id = :public_id"),
                    {'public_id': org_public_id}
                ).fetchone()
            
            org_id = org_result[0]
            
            # Check if admin exists
            admin_result = db.session.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {'email': 'sojipariola@gmail.com'}
            ).fetchone()
            
            if admin_result:
                print("⚠️ Admin user already exists!")
                return
            
            # Create admin user
            password_hash = generate_password_hash('Soji1111')
            user_public_id = str(uuid.uuid4())
            
            db.session.execute(
                text("""INSERT INTO users 
                (email, password_hash, first_name, last_name, organization_id, role, 
                 is_admin, is_active, public_id, created_at, updated_at) 
                VALUES (:email, :password_hash, :first_name, :last_name, :org_id, :role, 
                        :is_admin, :is_active, :public_id, :created_at, :updated_at)"""),
                {
                    'email': 'sojipariola@gmail.com',
                    'password_hash': password_hash,
                    'first_name': 'Soji',
                    'last_name': 'Pariola',
                    'org_id': org_id,
                    'role': 'ADMIN',
                    'is_admin': True,
                    'is_active': True,
                    'public_id': user_public_id,
                    'created_at': datetime.utcnow(),
                    'updated_at': datetime.utcnow()
                }
            )
            db.session.commit()
            print("✅ Admin user created via direct SQL!")
            print("📧 Email: sojipariola@gmail.com")
            print("🔑 Password: Soji1111")
            print("👤 Name: Soji Omopariola")
            print("🏢 Organization: Main Dental Clinic")
            print("💼 Role: ADMIN")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ SQL error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_admin_direct_sql_complete()