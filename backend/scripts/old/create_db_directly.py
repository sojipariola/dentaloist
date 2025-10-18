# create_db_directly.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db

def create_database():
    app = create_app()
    
    with app.app_context():
        print("🚀 Creating database tables...")
        
        try:
            # Drop all existing tables
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
            print("📊 Creating tables...")
            db.create_all()
            
            print("✅ Database created successfully!")
            
            # Verify by counting tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"📋 Created {len(tables)} tables")
            
            # List the tables
            for table in sorted(tables):
                print(f"  - {table}")
                
            return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = create_database()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
