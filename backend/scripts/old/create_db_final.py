# create_db_final.py
import os
import sys

# Add the current directory to Python path user
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_database_final():
    print("🚀 Creating database with correct SQLAlchemy syntax...")
    
    try:
        # Import Flask and SQLAlchemy
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from sqlalchemy import text
        
        # Use the database URL from environment or with password
        database_url = os.environ.get('DATABASE_URL', 'postgresql://soji:password123@localhost/dentaloist')
        
        print(f"🔗 Using database: {database_url}")
        
        # Create app configuration
        class Config:
            SQLALCHEMY_DATABASE_URI = database_url
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = 'temp-secret-key'
        
        app = Flask(__name__)
        app.config.from_object(Config)
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            print("🗑️  Cleaning database...")
            
            # Test connection first
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("SELECT version()"))
                    version = result.scalar()
                    print(f"✅ Database connection successful: {version}")
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                return False
            
            # Drop all tables using raw SQL
            try:
                with db.engine.connect() as conn:
                    # Start a transaction
                    trans = conn.begin()
                    
                    # Drop all tables in public schema
                    conn.execute(text("""
                        DO $$ DECLARE
                            r RECORD;
                        BEGIN
                            -- Drop all tables
                            FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                            END LOOP;
                            
                            -- Drop all sequences  
                            FOR r IN (SELECT sequence_name FROM information_schema.sequences WHERE sequence_schema = 'public') LOOP
                                EXECUTE 'DROP SEQUENCE IF EXISTS ' || quote_ident(r.sequence_name) || ' CASCADE';
                            END LOOP;
                            
                            -- Drop all types
                            FOR r IN (SELECT typname FROM pg_type t JOIN pg_namespace n ON n.oid = t.typnamespace WHERE n.nspname = 'public' AND t.typtype = 'e') LOOP
                                EXECUTE 'DROP TYPE IF EXISTS ' || quote_ident(r.typname) || ' CASCADE';
                            END LOOP;
                        END $$;
                    """))
                    
                    trans.commit()
                    print("✅ Database cleaned successfully")
                    
            except Exception as e:
                print(f"⚠️  Could not clean database: {e}")
                # Continue anyway
            
            print("📊 Creating tables...")
            
            # Import your actual models to create tables
            try:
                from .app.models import db as actual_db
                actual_db.create_all()
                print("✅ Tables created using actual models!")
            except Exception as e:
                print(f"❌ Could not create tables with actual models: {e}")
                # Fall back to simple creation
                try:
                    db.create_all()
                    print("✅ Tables created using simple db!")
                except Exception as e2:
                    print(f"❌ Could not create tables at all: {e2}")
                    return False
            
            # Verify creation
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
                
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_database_final()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)