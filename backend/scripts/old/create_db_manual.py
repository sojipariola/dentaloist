# create_db_manual.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_db_manual():
    print("🚀 Creating database with manual index management...")
    
    try:
        from app import create_app, db
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("📊 Creating tables without indexes first...")
            
            # Get the metadata
            metadata = db.metadata
            
            # Create a new connection for manual control
            with db.engine.connect() as connection:
                with connection.begin() as transaction:
                    try:
                        # Create all tables (without indexes)
                        print("Creating tables...")
                        for table in metadata.sorted_tables:
                            # Create table without indexes
                            create_stmt = table.__class__.create(table, bind=connection)
                            connection.execute(create_stmt)
                            print(f"  - Created table: {table.name}")
                        
                        # Now create indexes separately
                        print("Creating indexes...")
                        for table in metadata.sorted_tables:
                            for index in table.indexes:
                                try:
                                    create_index_stmt = index.__class__.create(index, bind=connection)
                                    connection.execute(create_index_stmt)
                                    print(f"  - Created index: {index.name}")
                                except Exception as e:
                                    print(f"  - Could not create index {index.name}: {e}")
                        
                        transaction.commit()
                        print("✅ All tables and indexes created successfully!")
                        
                    except Exception as e:
                        print(f"❌ Error: {e}")
                        transaction.rollback()
                        raise
            
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
    success = create_db_manual()
    if success:
        print("\n🎉 Database creation completed successfully!")
    else:
        print("\n💥 Database creation failed!")
        sys.exit(1)
