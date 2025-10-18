import pytest
import json
from app.models import User, Organization, UserRole
from werkzeug.security import generate_password_hash

class TestAuthSimple:
    """Simple authentication tests"""
    
    def test_register_user(self, client, db):
        """Test user registration"""
        data = {
            "email": "simple@example.com",
            "password": "TestPass123",
            "first_name": "Simple",
            "last_name": "User"
        }
        
        response = client.post(
            "/api/auth/register",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        # Should create user successfully
        assert response.status_code == 201
        
        # Verify user in database
        user = User.query.filter_by(email="simple@example.com").first()
        assert user is not None
        assert user.first_name == "Simple"
    
    def test_login_user(self, client, db):
        """Test user login"""
        # Create user first
        user = User(
            email="login@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Login",
            last_name="User",
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        data = {
            "email": "login@example.com",
            "password": "TestPass123"
        }
        
        response = client.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert "access_token" in json_data
        assert json_data["user"]["email"] == "login@example.com"
    
    def test_invalid_login(self, client):
        """Test invalid login credentials"""
        data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post(
            "/api/auth/login",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        assert response.status_code == 401

class TestTenancySimple:
    """Simple tenancy tests"""
    
    def test_get_tenants_unauthorized(self, client):
        """Test getting tenants without auth"""
        response = client.get("/api/auth/api/tenants")
        assert response.status_code == 401  # Unauthorized
    
    def test_switch_tenant_unauthorized(self, client):
        """Test switching tenant without auth"""
        data = {"tenant_id": "test-org"}
        response = client.post(
            "/api/auth/api/switch-tenant",
            data=json.dumps(data),
            content_type="application/json"
        )
        assert response.status_code == 401  # Unauthorized
