# scripts/reset_database_safe.py
#!/usr/bin/env python3
import os
import sys
import warnings

# Disable eventlet warnings and prevent monkey patching
os.environ['EVENTLET_NO_MONKEYPATCH'] = '1'
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def reset_database():
    """Safe database reset without eventlet interference"""
    print("🚀 Starting safe database reset...")
    
    # Import after setting environment variables
    from app import create_app
    from app.models import db, Organization, User, Tenant, UserRole
    from werkzeug.security import generate_password_hash
    
    # Create app with minimal configuration
    app = create_app()
    
    with app.app_context():
        try:
            print("🗑️  Dropping all tables...")
            
            # Use raw SQL to drop tables to avoid eventlet issues
            with db.engine.connect() as conn:
                # Get all table names
                result = conn.execute("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public'
                """)
                tables = [row[0] for row in result]
                
                # Disable foreign key constraints
                conn.execute("SET session_replication_role = 'replica';")
                
                # Drop tables
                for table in tables:
                    try:
                        conn.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                        print(f"   Dropped table: {table}")
                    except Exception as e:
                        print(f"   Warning: Could not drop {table}: {e}")
                
                # Re-enable foreign key constraints
                conn.execute("SET session_replication_role = 'origin';")
            
            print("✅ Tables dropped")
            
            # Create tables
            print("🔧 Creating tables...")
            db.create_all()
            print("✅ Tables created")
            
            # Seed data
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
            db.session.rollback()
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    reset_database()