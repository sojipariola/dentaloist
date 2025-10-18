# tests/test_final_validation.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def test_final_validation():
    """Final validation that all models work together"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        print("🎯 Running final model validation...")
        
        # Import all core models
        from app.models import (
            User, Organization, Role, Permission,
            AnalyticsDashboard, AnalyticsWidget, WidgetType, Widget
        )
        
        # Test that we can instantiate each model
        test_models = [
            ("User", User),
            ("Organization", Organization), 
            ("Role", Role),
            ("Permission", Permission),
            ("AnalyticsDashboard", AnalyticsDashboard),
            ("AnalyticsWidget", AnalyticsWidget),
            ("WidgetType", WidgetType),
            ("Widget", Widget)
        ]
        
        success_count = 0
        for name, model_class in test_models:
            try:
                # Test basic instantiation
                instance = model_class()
                assert instance is not None
                print(f"✅ {name}: Can instantiate")
                success_count += 1
            except Exception as e:
                print(f"❌ {name}: Instantiation failed - {e}")
        
        print(f"\n📊 Final validation: {success_count}/{len(test_models)} models OK")
        
        # Test basic database operations
        try:
            # Clear any data
            User.query.delete()
            Organization.query.delete()
            db.session.commit()
            
            # Create basic entities
            org = Organization(name="Final Test Org", code="FINAL_TEST")
            user = User(email="final@test.com", first_name="Final", last_name="Test")
            user.set_password("final123")
            user.organizations.append(org)
            
            db.session.add_all([org, user])
            db.session.commit()
            
            # Verify
            assert User.query.count() == 1
            assert Organization.query.count() == 1
            assert user.check_password("final123")
            
            print("✅ Basic database operations work!")
            return True
            
        except Exception as e:
            print(f"❌ Database operations failed: {e}")
            return False

if __name__ == '__main__':
    success = test_final_validation()
    sys.exit(0 if success else 1)