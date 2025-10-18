import pytest
import json
from flask import url_for
from app.models import User, Organization, UserRole, db
from werkzeug.security import generate_password_hash

class TestAuthRoutes:
    """Test authentication and tenancy routes"""
    
    def test_register_new_user(self, client, session):
        """Test user registration"""
        data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = client.post(
            "/api/auth/register",
            data=json.dumps(data),
            content_type="application/json"
        )
        
        assert response.status_code == 201
        json_data = response.get_json()
        assert "access_token" in json_data
        assert "refresh_token" in json_data
        assert json_data["user"]["email"] == "test@example.com"
        
        # Verify user was created in database
        user = User.query.filter_by(email="test@example.com").first()
        assert user is not None
        assert user.first_name == "Test"
        assert user.is_active == True

    def test_login_success(self, client, session):
        """Test successful login"""
        # Create a test user first
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
        assert "refresh_token" in json_data
        assert json_data["user"]["email"] == "login@example.com"

    def test_login_invalid_credentials(self, client, session):
        """Test login with invalid credentials"""
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
        json_data = response.get_json()
        assert "error" in json_data

    def test_get_current_user_with_token(self, client, session):
        """Test getting current user with valid JWT token"""
        # Create a test user
        user = User(
            email="current@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Current",
            last_name="User",
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Login to get token
        login_data = {
            "email": "current@example.com",
            "password": "TestPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        
        token = login_response.get_json()["access_token"]
        
        # Use token to get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["user"]["email"] == "current@example.com"

    def test_refresh_token(self, client, session):
        """Test token refresh"""
        # Create user and login
        user = User(
            email="refresh@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Refresh",
            last_name="User",
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        login_data = {
            "email": "refresh@example.com",
            "password": "TestPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        
        refresh_token = login_response.get_json()["refresh_token"]
        
        # Refresh token
        response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert "access_token" in json_data

class TestTenancyRoutes:
    """Test tenancy-related routes"""
    
    def test_get_available_tenants_super_admin(self, client, session):
        """Test super admin can see all tenants"""
        # Create organizations
        org1 = Organization(name="Org 1", public_id="org1")
        org2 = Organization(name="Org 2", public_id="org2")
        db.session.add_all([org1, org2])
        
        # Create super admin user
        super_admin_role = UserRole(name="SUPER_ADMIN", code="SUPER_ADMIN")
        db.session.add(super_admin_role)
        db.session.commit()
        
        user = User(
            email="superadmin@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Super",
            last_name="Admin",
            is_active=True
        )
        user.roles.append(super_admin_role)
        db.session.add(user)
        db.session.commit()
        
        # Login as super admin
        login_data = {
            "email": "superadmin@example.com",
            "password": "TestPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        
        token = login_response.get_json()["access_token"]
        
        # Get available tenants
        response = client.get(
            "/api/auth/api/tenants",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert len(json_data["tenants"]) == 2
        assert json_data["is_super_admin"] == True

    def test_switch_tenant_super_admin(self, client, session):
        """Test super admin can switch tenants"""
        # Create organizations
        org1 = Organization(name="Org 1", public_id="org1")
        org2 = Organization(name="Org 2", public_id="org2")
        db.session.add_all([org1, org2])
        
        # Create super admin user
        super_admin_role = UserRole(name="SUPER_ADMIN", code="SUPER_ADMIN")
        db.session.add(super_admin_role)
        db.session.commit()
        
        user = User(
            email="superadmin2@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Super",
            last_name="Admin",
            is_active=True
        )
        user.roles.append(super_admin_role)
        db.session.add(user)
        db.session.commit()
        
        # Login as super admin
        login_data = {
            "email": "superadmin2@example.com",
            "password": "TestPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        
        token = login_response.get_json()["access_token"]
        
        # Switch tenant
        switch_data = {"tenant_id": "org2"}
        response = client.post(
            "/api/auth/api/switch-tenant",
            data=json.dumps(switch_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data["tenant"]["id"] == "org2"
        assert json_data["tenant"]["name"] == "Org 2"

    def test_switch_tenant_regular_user(self, client, session):
        """Test regular user cannot switch tenants"""
        # Create organization and regular user
        org = Organization(name="Regular Org", public_id="regular_org")
        db.session.add(org)
        
        user_role = UserRole(name="USER", code="USER")
        db.session.add(user_role)
        db.session.commit()
        
        user = User(
            email="regular@example.com",
            password_hash=generate_password_hash("TestPass123"),
            first_name="Regular",
            last_name="User",
            organization_id="regular_org",
            is_active=True
        )
        user.roles.append(user_role)
        db.session.add(user)
        db.session.commit()
        
        # Login as regular user
        login_data = {
            "email": "regular@example.com",
            "password": "TestPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        
        token = login_response.get_json()["access_token"]
        
        # Try to switch tenant (should fail)
        switch_data = {"tenant_id": "other_org"}
        response = client.post(
            "/api/auth/api/switch-tenant",
            data=json.dumps(switch_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 403
        json_data = response.get_json()
        assert "error" in json_data