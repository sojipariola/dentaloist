# bypass_encryption.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_without_encryption():
    print("🚀 Creating database without encryption initialization...")
    
    try:
        # Import Flask and SQLAlchemy directly
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        
        # Get database URL from environment
        database_url = os.environ.get('DATABASE_URL', 'postgresql://soji@localhost/dentaloist')
        
        # Create minimal app without encryption
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SECRET_KEY'] = 'temp-secret-key-for-db-creation'
        
        db = SQLAlchemy(app)
        
        with app.app_context():
            # Import your models to register them
            from app.models import core, clinical, financial, analytics, inventory
            
            print("📊 Creating tables...")
            db.create_all()
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Successfully created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_db_without_encryption()
    if success:
        print("\n🎉 Database creation completed successfully!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
