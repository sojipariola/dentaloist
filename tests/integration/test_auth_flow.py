import pytest
import requests
from playwright.sync_api import sync_playwright
import json

class TestAuthFlow:
    """Test complete authentication flow across backend and frontend"""
    
    def test_super_admin_login_and_tenant_switching(self, backend_url, frontend_url, test_credentials):
        """Test super admin can login and switch tenants"""
        
        # Step 1: Backend API login
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['super_admin']
        )
        
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        
        # Verify super admin status
        assert auth_data['user']['is_super_admin'] == True
        assert 'tenants' in auth_data
        assert len(auth_data['tenants']) > 1
        
        access_token = auth_data['access_token']
        
        # Step 2: Frontend login simulation
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Navigate to login page
                page.goto(f"{frontend_url}/login")
                
                # Fill login form
                page.fill('input[type="email"]', test_credentials['super_admin']['email'])
                page.fill('input[type="password"]', test_credentials['super_admin']['password'])
                
                # Submit form
                page.click('button[type="submit"]')
                
                # Wait for navigation and check for tenant switcher
                page.wait_for_selector('[data-testid="tenant-switcher"]', timeout=10000)
                
                # Verify super admin UI elements
                tenant_switcher = page.query_selector('[data-testid="tenant-switcher"]')
                assert tenant_switcher is not None
                
                # Test tenant switching
                tenant_switcher.click()
                page.wait_for_selector('[data-testid="tenant-option"]')
                
                tenant_options = page.query_selector_all('[data-testid="tenant-option"]')
                assert len(tenant_options) >= 3  # Should see all organizations
                
                # Switch to different tenant
                tenant_options[1].click()
                
                # Verify context changed
                page.wait_for_selector('[data-testid="current-tenant"]')
                current_tenant = page.query_selector('[data-testid="current-tenant"]')
                assert current_tenant is not None
                
            finally:
                browser.close()
        
        # Step 3: Verify backend tenant context
        headers = {'Authorization': f'Bearer {access_token}'}
        tenants_response = requests.get(f"{backend_url}/api/tenants", headers=headers)
        assert tenants_response.status_code == 200
        
        print("✅ Super admin auth flow test passed")
    
    def test_regular_user_restricted_access(self, backend_url, frontend_url, test_credentials):
        """Test regular users can only access their own tenant"""
        
        # Backend API login for practice admin
        auth_response = requests.post(
            f"{backend_url}/api/auth/login", 
            json=test_credentials['practice_admin']
        )
        
        assert auth_response.status_code == 200
        auth_data = auth_response.json()
        
        # Verify NOT super admin
        assert auth_data['user']['is_super_admin'] == False
        assert len(auth_data['tenants']) == 1  # Only their organization
        
        access_token = auth_data['access_token']
        
        # Frontend test
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                # Login
                page.goto(f"{frontend_url}/login")
                page.fill('input[type="email"]', test_credentials['practice_admin']['email'])
                page.fill('input[type="password"]', test_credentials['practice_admin']['password'])
                page.click('button[type="submit"]')
                
                # Wait for dashboard
                page.wait_for_selector('[data-testid="dashboard"]', timeout=10000)
                
                # Verify NO tenant switcher for regular users
                tenant_switcher = page.query_selector('[data-testid="tenant-switcher"]')
                assert tenant_switcher is None
                
            finally:
                browser.close()
        
        print("✅ Regular user restricted access test passed")