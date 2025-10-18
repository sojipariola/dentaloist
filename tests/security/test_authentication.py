import pytest
import requests
import jwt
from datetime import datetime, timedelta

class TestAuthenticationSecurity:
    """Test authentication security measures"""
    
    def test_jwt_token_security(self, backend_url, test_credentials):
        """Test JWT token security features"""
        
        # Login to get token
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['super_admin']
        )
        auth_data = auth_response.json()
        access_token = auth_data['access_token']
        
        # Decode token without verification to inspect contents
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        
        # Verify token contents
        assert 'sub' in decoded  # Subject (user ID)
        assert 'exp' in decoded  # Expiration
        assert 'iat' in decoded  # Issued at
        assert 'user_id' in decoded  # Custom claim
        
        # Verify token expiration (should be reasonable)
        exp_time = datetime.fromtimestamp(decoded['exp'])
        iat_time = datetime.fromtimestamp(decoded['iat'])
        token_lifetime = exp_time - iat_time
        
        assert token_lifetime < timedelta(days=1), "Token lifetime too long"
        assert token_lifetime > timedelta(hours=1), "Token lifetime too short"
        
        print("✅ JWT token security test passed")
    
    def test_authentication_brute_force_protection(self, backend_url):
        """Test brute force protection"""
        
        failed_attempts = []
        
        # Make multiple failed login attempts
        for i in range(6):  # More than typical rate limit
            response = requests.post(
                f"{backend_url}/api/auth/login",
                json={'email': 'nonexistent@test.com', 'password': 'wrongpassword'}
            )
            failed_attempts.append(response.status_code)
            
            # Add small delay between requests
            import time
            time.sleep(0.1)
        
        # Should eventually get rate limited
        assert 429 in failed_attempts, "No rate limiting detected"
        
        print("✅ Brute force protection test passed")
    
    def test_cross_tenant_access_prevention(self, backend_url, test_credentials, test_tenants):
        """Test that users cannot access other tenants' data"""
        
        # Login as practice admin (regular user)
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['practice_admin']
        )
        access_token = auth_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Try to access other tenants' data directly
        for tenant_id in test_tenants.values():
            if tenant_id != 'org_001':  # This user should only have org_001
                # Try to switch to other tenant (should fail)
                switch_response = requests.post(
                    f"{backend_url}/api/switch-tenant",
                    headers=headers,
                    json={'tenant_id': tenant_id}
                )
                
                # Should be forbidden
                assert switch_response.status_code in [403, 400], \
                    f"Unauthorized tenant switch allowed to {tenant_id}"
        
        print("✅ Cross-tenant access prevention test passed")