# create_with_real_app.py
import os
import sys

# Disable eventlet
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_with_real_app():
    print("🚀 Using your real Flask app...")
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print("📋 Checking tables in metadata...")
            print(f"Total tables: {len(db.metadata.tables)}")
            
            for table_name in sorted(db.metadata.tables.keys()):
                print(f"  - {table_name}")
            
            print("🗑️  Dropping tables...")
            db.drop_all()
            
            print("📊 Creating tables...")
            db.create_all()
            
            # Verify
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"✅ Created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_with_real_app()
    if success:
        print("\n🎉 Database creation completed!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
