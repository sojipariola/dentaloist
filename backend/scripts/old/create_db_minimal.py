# create_db_minimal.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Completely avoid eventlet
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def create_database_minimal():
    # Import Flask and SQLAlchemy directly
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from config import Config
    
    # Create a minimal app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize db without eventlet
    db = SQLAlchemy(app)
    
    with app.app_context():
        print("🚀 Creating database with minimal setup...")
        
        try:
            # Drop all tables
            print("🗑️  Dropping tables...")
            db.drop_all()
            
            # Create all tables
            print("📊 Creating tables...")
            db.create_all()
            
            # Check results
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Success! Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
                
            return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = create_database_minimal()
    if success:
        print("\n🎉 Minimal database setup completed!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
