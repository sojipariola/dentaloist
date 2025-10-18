# create_db_final_fixed.py
import os
import sys

# Completely disable eventlet before ANY imports
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'
os.environ['EVENTLET_DISABLE_PATCHING'] = 'yes'

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_final_fixed():
    print("🚀 Creating database with Eventlet completely disabled...")
    
    try:
        # Import your Flask app factory
        from app import create_app, db
        
        # Create app - this should avoid eventlet now
        app = create_app()
        
        with app.app_context():
            print("📋 Tables in metadata:", len(db.metadata.tables))
            
            # Use raw SQL to drop tables to avoid eventlet issues
            print("🗑️  Dropping tables with raw SQL...")
            try:
                with db.engine.connect() as conn:
                    # Get list of tables
                    result = conn.execute(db.text("""
                        SELECT tablename 
                        FROM pg_tables 
                        WHERE schemaname = 'public'
                        AND tablename != 'alembic_version'
                    """))
                    tables = [row[0] for row in result]
                    result.close()
                    
                    print(f"Found {len(tables)} tables to drop")
                    
                    # Drop each table individually
                    for table in tables:
                        try:
                            conn.execute(db.text(f'DROP TABLE IF EXISTS "{table}" CASCADE'))
                            print(f"  - Dropped {table}")
                        except Exception as e:
                            print(f"  - Could not drop {table}: {e}")
                    
                    # Commit the transaction
                    conn.commit()
                    
            except Exception as e:
                print(f"⚠️  Could not drop tables with SQL: {e}")
            
            print("📊 Creating tables...")
            
            # Create tables - this should work now
            db.create_all()
            print("✅ Tables created!")
            
            # Verify
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
    success = create_db_final_fixed()
    if success:
        print("\n🎉 Database creation completed successfully!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
