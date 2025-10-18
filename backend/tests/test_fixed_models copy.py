# tests/test_fixed_models.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class TestFixedModels:
    """Test models after fixing relationships"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_user_and_organization(self, app):
        """Test basic User and Organization models"""
        with app.app_context():
            # Import inside context
            from app.models import User, Organization
            
            # Create only these tables
            User.__table__.create(db.engine)
            Organization.__table__.create(db.engine)
            
            # Create organization
            org = Organization(
                name="Test Dental Clinic",
                code="TEST_DENTAL"
            )
            db.session.add(org)
            db.session.flush()
            
            # Create user
            user = User(
                email="dentist@test.com",
                first_name="Jane",
                last_name="Smith"
            )
            user.set_password("secure123")
            user.organizations.append(org)
            
            db.session.add(user)
            db.session.commit()
            
            # Verify
            assert user.id is not None
            assert org.id is not None
            assert len(user.organizations) == 1
            assert user.organizations[0].name == "Test Dental Clinic"
            assert user.check_password("secure123")
            
            # Cleanup
            User.__table__.drop(db.engine)
            Organization.__table__.drop(db.engine)
    
    def test_analytics_dashboard_basic(self, app):
        """Test AnalyticsDashboard with fixed relationships"""
        with app.app_context():
            from app.models import AnalyticsDashboard, User, Organization
            
            # Create required tables
            User.__table__.create(db.engine)
            Organization.__table__.create(db.engine)
            AnalyticsDashboard.__table__.create(db.engine)
            
            # Create org and user first
            org = Organization(name="Test Org", code="TEST")
            user = User(email="user@test.com", first_name="Test", last_name="User")
            user.set_password("pass123")
            
            db.session.add_all([org, user])
            db.session.flush()
            
            # Create dashboard
            dashboard = AnalyticsDashboard(
                name="Clinical Dashboard",
                description="Clinical metrics overview",
                user_id=user.id,
                organization_id=org.id,
                layout_config={"grid": "fluid"},
                is_public=False
            )
            
            db.session.add(dashboard)
            db.session.commit()
            
            # Verify
            assert dashboard.id is not None
            assert dashboard.name == "Clinical Dashboard"
            assert dashboard.organization_id == org.id
            assert dashboard.user_id == user.id
            
            # Cleanup
            AnalyticsDashboard.__table__.drop(db.engine)
            User.__table__.drop(db.engine)
            Organization.__table__.drop(db.engine)