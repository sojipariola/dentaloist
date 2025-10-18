# create_db_fixed.py
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_database_fixed():
    print("🚀 Creating database with fixed imports...")
    
    try:
        # Import Flask and SQLAlchemy directly
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Get database URL from environment or use default
        database_url = os.environ.get('DATABASE_URL', 'postgresql://soji@localhost/dentaloist')
        
        # Create a minimal app configuration
        class SimpleConfig:
            SQLALCHEMY_DATABASE_URI = database_url
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = 'temp-secret-key-for-db-creation'
        
        app = Flask(__name__)
        app.config.from_object(SimpleConfig)
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            print("🗑️  Dropping existing tables...")
            
            # Use raw SQL to drop all tables (more reliable)
            connection = db.engine.connect()
            connection.execute("""
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
            """)
            connection.close()
            print("✅ Database cleaned")
            
            print("📊 Creating tables...")
            
            # Now import your actual models to create the tables
            # This will import all models through the __init__ files
            from models import db as actual_db
            
            # Use the actual db instance from your models
            actual_db.create_all()
            
            print("✅ Tables created successfully!")
            
            # Verify by counting tables
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
    success = create_database_fixed()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
