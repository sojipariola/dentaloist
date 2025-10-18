# create_db_simple.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Disable eventlet monkey patching for this script
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

def create_database_simple():
    # Import after setting environment variable
    from app import create_app, db
    
    app = create_app()
    
    with app.app_context():
        print("🚀 Creating database tables...")
        
        try:
            # First, let's check what tables exist
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            print(f"📋 Found {len(existing_tables)} existing tables")
            
            if existing_tables:
                print("🗑️  Dropping existing tables...")
                # Drop tables one by one to avoid issues
                for table_name in existing_tables:
                    try:
                        db.engine.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
                        print(f"  - Dropped {table_name}")
                    except Exception as e:
                        print(f"  - Could not drop {table_name}: {e}")
            
            print("📊 Creating new tables...")
            
            # Create all tables
            db.create_all()
            
            # Verify creation
            inspector = inspect(db.engine)
            new_tables = inspector.get_table_names()
            print(f"✅ Created {len(new_tables)} tables successfully!")
            
            # List the tables
            for table in sorted(new_tables):
                print(f"  - {table}")
                
            return True
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = create_database_simple()
    if success:
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1)
