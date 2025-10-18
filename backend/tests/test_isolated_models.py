# tests/test_isolated_models.py

import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create a minimal app for testing"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


class TestIsolatedModels:
    """Test models in isolation to avoid relationship conflicts"""
    
    def test_user_creation(self, app):
        with app.app_context():
            # Import inside context to avoid circular imports
            from app.models import User
            
            # Create tables only for User
            User.__table__.create(db.engine)
            
            user = User(
                email="test@example.com",
                first_name="John", 
                last_name="Doe"
            )
            user.set_password("password123")
            
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.check_password("password123")
            
            # Cleanup
            User.__table__.drop(db.engine)
    
    def test_organization_creation(self, app):
        with app.app_context():
            from app.models import Organization
            
            Organization.__table__.create(db.engine)
            
            org = Organization(
                name="Test Clinic",
                code="TEST_CLINIC"
            )
            
            db.session.add(org)
            db.session.commit()
            
            assert org.id is not None
            assert org.name == "Test Clinic"
            
            Organization.__table__.drop(db.engine)