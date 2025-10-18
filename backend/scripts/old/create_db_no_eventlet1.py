# create_db_no_eventlet.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_clean():
    print("🚀 Creating database without Eventlet...")
    
    try:
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            print(f"📋 Tables in metadata: {len(db.metadata.tables)}")
            
            # Drop all tables
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            
            # Create all tables
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
    success = create_db_clean()
    if success:
        print("\n🎉 Database creation completed successfully!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
