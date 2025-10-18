# tests/validate_models.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def validate_models():
    """Validate all model relationships"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        print("🔧 Validating model relationships...")
        
        # List of core models to validate
        core_models = [
            'User', 'Organization', 'Role', 'Permission',
            'AnalyticsDashboard', 'AnalyticsWidget', 'Widget'
        ]
        
        success_count = 0
        error_count = 0
        
        for model_name in core_models:
            try:
                # Dynamically import model
                module = __import__('app.models', fromlist=[model_name])
                model_class = getattr(module, model_name)
                
                # Try to create table
                model_class.__table__.create(db.engine)
                print(f"✅ {model_name}: OK")
                model_class.__table__.drop(db.engine)
                success_count += 1
                
            except Exception as e:
                print(f"❌ {model_name}: {str(e)}")
                error_count += 1
        
        print(f"\n📊 Summary: {success_count} passed, {error_count} failed")
        return error_count == 0

if __name__ == '__main__':
    validate_models()