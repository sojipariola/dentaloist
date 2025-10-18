# backend/scripts/debug_database_files.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    print("🔍 DATABASE FILE INVESTIGATION")
    print("=" * 50)
    
    # Check which database file is being used
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    print(f"📊 Database URI: {db_uri}")
    
    if db_uri.startswith('sqlite:///'):
        db_path = db_uri.replace('sqlite:///', '')
        print(f"📁 Database file path: {db_path}")
        print(f"📁 File exists: {os.path.exists(db_path)}")
        print(f"📁 File size: {os.path.getsize(db_path) if os.path.exists(db_path) else 'N/A'} bytes")
    
    # Check current connection
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Tables in current connection: {len(tables)}")
    
    # Check if appointments exists in this connection
    if 'appointments' in tables:
        print("✅ appointments table FOUND in current connection")
    else:
        print("❌ appointments table NOT FOUND in current connection")
        print("Available tables:")
        for table in sorted(tables)[:20]:  # Show first 20
            print(f"   - {table}")
    
    # Try direct SQL query
    try:
        result = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='appointments'"))
        table_exists = result.fetchone()
        print(f"🔍 Direct SQL check: appointments table exists = {bool(table_exists)}")
    except Exception as e:
        print(f"❌ Direct SQL check failed: {e}")