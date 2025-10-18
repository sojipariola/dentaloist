import pytest
import json
import tempfile
import os
from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

class TestAuthClean:
    """Clean authentication tests with proper database handling"""
    
    def setup_method(self):
        """Set up test database"""
        # Create temporary database
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        class TestConfig:
            TESTING = True
            SQLALCHEMY_DATABASE_URI = f'sqlite:///{self.db_path}'
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = 'test-secret'
            JWT_SECRET_KEY = 'test-jwt-secret'
            WTF_CSRF_ENABLED = False
        
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            # Drop all tables first to avoid conflicts
            db.drop_all()
            # Then create all tables
            db.create_all()
    
    def teardown_method(self):
        """Clean up test database"""
        with self.app.app_context():
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)
    
    def test_health_endpoint(self):
        """Test health endpoint - simplest test first"""
        response = self.client.get("/api/auth/health")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["status"] == "healthy"
        assert json_data["service"] == "auth"
    
    def test_register_user(self):
        """Test user registration"""
        data = {
            "email": "clean@example.com",
            "password": "TestPass123",
            "first_name": "Clean",
            "last_name": "User"
        }
        
        response = self.client.post(
            "/api/auth/register",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        # Should create user successfully
        assert response.status_code == 201
        
        # Verify user in database
        with self.app.app_context():
            user = User.query.filter_by(email="clean@example.com").first()
            assert user is not None
            assert user.first_name == "Clean"
    
    def test_login_user(self):
        """Test user login"""
        # Create user first
        with self.app.app_context():
            user = User(
                email="loginclean@example.com",
                password_hash=generate_password_hash("TestPass123"),
                first_name="Login",
                last_name="User",
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
        
        data = {
            "email": "loginclean@example.com",
            "password": "TestPass123"
        }
        
        response = self.client.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert "access_token" in json_data
    
    def test_invalid_login(self):
        """Test invalid login credentials"""
        data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = self.client.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        assert response.status_code == 401
