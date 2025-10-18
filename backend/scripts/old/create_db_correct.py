# create_db_correct.py
import os
import sys

# Disable eventlet
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_correct():
    print("🚀 Creating database with correct model structure...")
    
    try:
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        database_url = 'postgresql://soji:password123@localhost/dentaloist'
        
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'temp-secret-key'
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            print("📥 Importing your model modules...")
            
            # Import all your model modules
            from app.models import core, clinical, financial, analytics, inventory
            
            print("✅ All model modules imported")
            
            # Check what tables are registered
            print(f"📋 Tables in metadata: {len(db.metadata.tables)}")
            for table_name in sorted(db.metadata.tables.keys()):
                print(f"  - {table_name}")
            
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
    success = create_db_correct()
    if success:
        print("\n🎉 Database creation completed!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
