# create_db_no_eventlet.py
import os
import sys

# Disable eventlet before any imports
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_no_eventlet():
    print("🚀 Creating database without Eventlet interference...")
    
    try:
        # Import Flask and SQLAlchemy directly (avoid eventlet)
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Use database URL
        database_url = 'postgresql://soji:password123@localhost/dentaloist'
        
        # Create minimal app
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'temp-secret-key'
        
        # Create db instance
        db = SQLAlchemy(app)
        
        with app.app_context():
            print("🔗 Testing database connection...")
            
            # Test connection
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(db.text("SELECT version()"))
                    version = result.scalar()
                    print(f"✅ Connected to: {version}")
            except Exception as e:
                print(f"❌ Connection failed: {e}")
                return False
            
            print("📥 Loading your models...")
            
            # Import your actual models to register them with SQLAlchemy
            try:
                # Import all your model files
                from app.models import BaseModel
                # This should import all models through the __init__ chain
                print("✅ Models imported successfully")
            except Exception as e:
                print(f"❌ Could not import models: {e}")
                return False
            
            # Check what tables are in metadata
            print(f"📋 Tables in metadata: {len(db.metadata.tables)}")
            for table_name in sorted(db.metadata.tables.keys()):
                print(f"  - {table_name}")
            
            if len(db.metadata.tables) <= 1:
                print("⚠️  Not enough tables in metadata. Manually importing models...")
                # Try to manually import specific models
                try:
                    from app.models.user import User
                    from app.models.tenant import Tenant
                    from app.models.organization import Organization
                    print("✅ Manually imported key models")
                except Exception as e:
                    print(f"❌ Manual import failed: {e}")
                    return False
            
            print("🗑️  Dropping existing tables...")
            try:
                db.drop_all()
                print("✅ Tables dropped")
            except Exception as e:
                print(f"⚠️  Could not drop tables: {e}")
            
            print("📊 Creating tables...")
            db.create_all()
            print("✅ Tables created!")
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Created {len(tables)} tables in database:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_db_no_eventlet()
    if success:
        print("\n🎉 Database creation completed!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
