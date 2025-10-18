import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import Treatment

app = create_app()
with app.app_context():
    print("🔍 Treatment Model Structure:")
    print(f"Table name: {Treatment.__tablename__}")
    print("\n📋 Columns:")
    for column in Treatment.__table__.columns:
        print(f"  - {column.name}: {column.type} (nullable={column.nullable})")
    
    print("\n🔗 Relationships:")
    for rel_name in dir(Treatment):
        if not rel_name.startswith('_'):
            attr = getattr(Treatment, rel_name)
            if hasattr(attr, 'property') and hasattr(attr.property, 'direction'):
                print(f"  - {rel_name}: {attr.property}")
    
    print("\n🎯 Available attributes:")
    treatment_instance = Treatment()
    for attr in dir(treatment_instance):
        if not attr.startswith('_') and not callable(getattr(treatment_instance, attr)):
            print(f"  - {attr}")
