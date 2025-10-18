# tests/test_final_fix_validation.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def test_final_fix_validation():
    """Final validation after fixing widget models"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        print("🎯 Final validation after widget model fixes...")
        
        try:
            # Try to create all tables
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Test that we can instantiate core models
            from app.models import User, Organization
            
            org = Organization(name="Final Test Org", code="FINAL")
            user = User(email="final@test.com", first_name="Final", last_name="Test")
            user.set_password("final123")
            
            db.session.add_all([org, user])
            db.session.commit()
            
            print("✅ Core models work!")
            return True
            
        except Exception as e:
            print(f"❌ Still having issues: {e}")
            return False

if __name__ == '__main__':
    success = test_final_fix_validation()
    sys.exit(0 if success else 1)
