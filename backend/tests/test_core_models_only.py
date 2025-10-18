# tests/test_core_models_only.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class TestCoreModelsOnly:
    """Test only core models without problematic analytics models"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_user_creation_basic(self, app):
        """Test basic user creation without analytics dependencies"""
        with app.app_context():
            # Import only core models
            from app.models import User, Organization
            
            # Clear any existing data
            User.query.delete()
            Organization.query.delete()
            db.session.commit()
            
            # Create organization
            org = Organization(
                name="Basic Test Clinic",
                code="BASIC_TEST"
            )
            db.session.add(org)
            db.session.flush()
            
            # Create user
            user = User(
                email="basic@test.com",
                first_name="Basic",
                last_name="User"
            )
            user.set_password("basic123")
            user.organizations.append(org)
            
            db.session.add(user)
            db.session.commit()
            
            # Verify basic attributes
            assert user.id is not None
            assert org.id is not None
            assert user.email == "basic@test.com"
            assert user.check_password("basic123")
            
            print("✅ Basic user creation test passed!")
    
    def test_organization_operations(self, app):
        """Test organization operations"""
        with app.app_context():
            from app.models import Organization
            
            # Clear organizations
            Organization.query.delete()
            db.session.commit()
            
            # Create multiple organizations
            org1 = Organization(name="Clinic One", code="CLINIC_1")
            org2 = Organization(name="Clinic Two", code="CLINIC_2")
            org3 = Organization(name="Clinic Three", code="CLINIC_3")
            
            db.session.add_all([org1, org2, org3])
            db.session.commit()
            
            # Test queries
            organizations = Organization.query.all()
            assert len(organizations) == 3
            
            org_codes = [org.code for org in organizations]
            assert "CLINIC_1" in org_codes
            assert "CLINIC_2" in org_codes
            assert "CLINIC_3" in org_codes
            
            # Test filtering
            clinic_two = Organization.query.filter_by(code="CLINIC_2").first()
            assert clinic_two.name == "Clinic Two"
            
            print("✅ Organization operations test passed!")