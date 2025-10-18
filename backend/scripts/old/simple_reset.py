# scripts/simple_reset.py
#!/usr/bin/env python3
import os
import sys
import psycopg2
from werkzeug.security import generate_password_hash

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def simple_reset():
    """Simple database reset using raw SQL"""
    print("🚀 Starting simple database reset...")
    
    # Database connection parameters from your config
    db_params = {
        'dbname': 'dentaloist',  # Replace with your actual database name
        'user': 'postgres',      # Replace with your username
        'password': 'password',  # Replace with your password
        'host': 'localhost',
        'port': '5432'
    }
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Drop all tables
        print("🗑️  Dropping all tables...")
        cur.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
        print("✅ Tables dropped")
        
        # Close connection
        cur.close()
        conn.close()
        
        # Now use Flask to create tables and seed data
        os.environ['EVENTLET_NO_MONKEYPATCH'] = '1'
        
        from app import create_app, db
        from app.models import Organization, User, Tenant, UserRole
        
        app = create_app()
        
        with app.app_context():
            print("🔧 Creating tables...")
            db.create_all()
            print("✅ Tables created")
            
            print("🌱 Seeding data...")
            
            # Create tenant
            tenant = Tenant(
                name="Pariola Dental Clinic",
                subdomain="pariola", 
                email="admin@parioladental.com",
                is_active=True
            )
            db.session.add(tenant)
            db.session.flush()
            
            # Create organization  
            organization = Organization(
                name="Pariola Dental Clinic",
                email="info@parioladental.com", 
                is_active=True
            )
            db.session.add(organization)
            db.session.flush()
            
            # Create admin user
            admin = User(
                email="sojipariola@gmail.com",
                first_name="Soji",
                last_name="Pariola", 
                password_hash=generate_password_hash("Soji1111"),
                role=UserRole.SUPER_ADMIN,
                is_active=True,
                is_admin=True,
                tenant_id=tenant.id,
                organization_id=organization.id
            )
            db.session.add(admin)
            
            db.session.commit()
            print("✅ Database seeded successfully!")
            print("\n🔑 Admin credentials:")
            print("   Email: sojipariola@gmail.com")
            print("   Password: Soji1111")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_reset()