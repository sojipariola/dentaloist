# tests/examine_widget_config.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def examine_widget_config():
    """Examine the current WidgetConfig model"""
    app = create_app()
    
    with app.app_context():
        from app.models import WidgetConfig
        
        print("🔍 Examining WidgetConfig model...")
        print(f"Table name: {WidgetConfig.__tablename__}")
        print("Columns:")
        for column in WidgetConfig.__table__.columns:
            print(f"  - {column.name} ({column.type})")
        
        # Check if it has the required fields
        column_names = [col.name for col in WidgetConfig.__table__.columns]
        required_fields = ['user_id', 'organization_id']
        
        missing_fields = [field for field in required_fields if field not in column_names]
        
        if missing_fields:
            print(f"❌ Missing fields: {missing_fields}")
        else:
            print("✅ All required fields present")

if __name__ == '__main__':
    examine_widget_config()
