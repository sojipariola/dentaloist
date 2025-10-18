# create_db_with_auth.py
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_database_with_auth():
    print("🚀 Creating database with authentication...")
    
    try:
        # Import Flask and SQLAlchemy
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Use the database URL from environment or with password
        database_url = os.environ.get('DATABASE_URL', 'postgresql://soji:Soji1111@localhost/dentaloist')
        
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
            
            # First, let's just try to connect and see what happens
            try:
                # Test connection
                result = db.engine.execute("SELECT version()")
                print("✅ Database connection successful")
                result.close()
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                return False
            
            # Now drop all tables
            try:
                db.drop_all()
                print("✅ Dropped all tables")
            except Exception as e:
                print(f"⚠️  Could not drop tables: {e}")
            
            print("📊 Creating tables...")
            
            # Import your actual models
            try:
                from app.models import db as actual_db
                actual_db.create_all()
                print("✅ Tables created successfully!")
            except Exception as e:
                print(f"❌ Could not create tables: {e}")
                # Try with the simple db instance
                db.create_all()
                print("✅ Tables created with simple db!")
            
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
    success = create_database_with_auth()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
