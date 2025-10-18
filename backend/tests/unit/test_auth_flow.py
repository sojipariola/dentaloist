import pytest
import json
from app.models import User, Organization, UserRole, db

class TestAuthIntegration:
    """Integration tests for authentication flow"""
    
    def test_complete_auth_flow(self, client, session):
        """Test complete authentication flow: register -> login -> get user -> logout"""
        # Step 1: Register
        register_data = {
            "email": "flow@example.com",
            "password": "TestPass123",
            "first_name": "Flow",
            "last_name": "User"
        }
        
        register_response = client.post(
            "/api/auth/register",
            data=json.dumps(register_data),
            content_type="application/json"
        )
        assert register_response.status_code == 201
        
        register_json = register_response.get_json()
        access_token = register_json["access_token"]
        refresh_token = register_json["refresh_token"]
        
        # Step 2: Get current user with token
        me_response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert me_response.status_code == 200
        me_json = me_response.get_json()
        assert me_json["user"]["email"] == "flow@example.com"
        
        # Step 3: Refresh token
        refresh_response = client.post(
            "/api/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        assert refresh_response.status_code == 200
        new_access_token = refresh_response.get_json()["access_token"]
        
        # Step 4: Use new token
        me_response2 = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        assert me_response2.status_code == 200
        
        # Step 5: Logout
        logout_response = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {new_access_token}"}
        )
        assert logout_response.status_code == 200

    def test_password_change_flow(self, client, session):
        """Test password change flow"""
        # Create user
        user = User(
            email="changepass@example.com",
            password_hash=generate_password_hash("OldPass123"),
            first_name="Change",
            last_name="Password",
            is_active=True
        )
        db.session.add(user)
        db.session.commit()
        
        # Login
        login_data = {
            "email": "changepass@example.com",
            "password": "OldPass123"
        }
        
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps(login_data),
            content_type="application/json"
        )
        token = login_response.get_json()["access_token"]
        
        # Change password
        change_data = {
            "current_password": "OldPass123",
            "new_password": "NewPass123"
        }
        
        change_response = client.post(
            "/api/auth/change-password",
            data=json.dumps(change_data),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert change_response.status_code == 200
        
        # Verify old password no longer works
        old_login_response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "changepass@example.com", "password": "OldPass123"}),
            content_type="application/json"
        )
        assert old_login_response.status_code == 401
        
        # Verify new password works
        new_login_response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "changepass@example.com", "password": "NewPass123"}),
            content_type="application/json"
        )
        assert new_login_response.status_code == 200