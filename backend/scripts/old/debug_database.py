# backend/scripts/debug_database.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

app = create_app()

with app.app_context():
    print("🔍 COMPREHENSIVE DATABASE DIAGNOSTIC")
    print("=" * 50)
    
    # Check all tables
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"📋 Total tables in database: {len(tables)}")
    
    # Group tables by type
    core_tables = [t for t in tables if t in ['users', 'organizations', 'patients', 'staff']]
    clinical_tables = [t for t in tables if t in ['appointments', 'treatments', 'clinical_notes']]
    lookup_tables = [t for t in tables if 'lookup' in t or t.endswith('_types') or t.endswith('_statuses')]
    other_tables = [t for t in tables if t not in core_tables + clinical_tables + lookup_tables]
    
    print(f"🏢 Core tables: {len(core_tables)}")
    for table in sorted(core_tables):
        print(f"   ✅ {table}")
    
    print(f"🏥 Clinical tables: {len(clinical_tables)}")
    for table in sorted(clinical_tables):
        print(f"   {'✅' if table in tables else '❌'} {table}")
    
    print(f"📚 Lookup tables: {len(lookup_tables)}")
    print(f"📦 Other tables: {len(other_tables)}")
    
    # Check if Appointment model is properly registered
    print("\n🔧 MODEL REGISTRATION CHECK:")
    try:
        from app.models import Appointment
        print(f"✅ Appointment model imported successfully")
        print(f"   Table name: {Appointment.__tablename__}")
        print(f"   Has table object: {hasattr(Appointment, '__table__')}")
        if hasattr(Appointment, '__table__'):
            print(f"   Table columns: {[c.name for c in Appointment.__table__.columns]}")
    except Exception as e:
        print(f"❌ Error importing Appointment model: {e}")
    
    # Check BaseModel
    print("\n🔧 BASE MODEL CHECK:")
    from app.models.base import BaseModel
    print(f"BaseModel is abstract: {BaseModel.__abstract__}")
    print(f"BaseModel bases: {BaseModel.__bases__}")

if __name__ == '__main__':
    pass