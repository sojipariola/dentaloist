# tests/find_duplicate_relationships.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def find_duplicate_relationships():
    """Find duplicate relationship names"""
    app = create_app()
    
    with app.app_context():
        from app.models import Organization
        
        print("🔍 Checking Organization model relationships...")
        
        # Get all relationships on Organization
        relationships = {}
        for attr_name in dir(Organization):
            attr = getattr(Organization, attr_name)
            if hasattr(attr, 'property') and hasattr(attr.property, 'direction'):
                relationships[attr_name] = {
                    'target': attr.property.mapper.class_.__name__,
                    'direction': str(attr.property.direction)
                }
        
        print("\n📋 All relationships on Organization model:")
        for rel_name, rel_info in relationships.items():
            print(f"  - {rel_name} -> {rel_info['target']}")
        
        # Check for analytics_dashboards
        if 'analytics_dashboards' in relationships:
            print(f"\n❌ Found analytics_dashboards relationship")
            print(f"   This is conflicting with a new relationship definition")

if __name__ == '__main__':
    find_duplicate_relationships()
