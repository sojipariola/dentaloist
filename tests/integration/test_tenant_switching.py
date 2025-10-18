import pytest
import requests
from playwright.sync_api import sync_playwright

class TestTenantSwitching:
    """Test tenant switching functionality"""
    
    def test_tenant_data_isolation(self, backend_url, frontend_url, test_credentials, test_tenants):
        """Test that data is properly isolated between tenants"""
        
        # Login as super admin
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['super_admin']
        )
        access_token = auth_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Get patients for different tenants
        patients_by_tenant = {}
        
        for tenant_name, tenant_id in test_tenants.items():
            # Switch tenant context
            switch_response = requests.post(
                f"{backend_url}/api/switch-tenant",
                headers=headers,
                json={'tenant_id': tenant_id}
            )
            assert switch_response.status_code == 200
            
            # Get patients for this tenant
            patients_response = requests.get(
                f"{backend_url}/api/patients",
                headers=headers
            )
            assert patients_response.status_code == 200
            
            patients_by_tenant[tenant_id] = patients_response.json()
        
        # Verify data isolation
        tenant_ids = list(test_tenants.values())
        for i, tenant_a in enumerate(tenant_ids):
            for tenant_b in tenant_ids[i+1:]:
                # Patients should be different between tenants
                patients_a = {p['public_id'] for p in patients_by_tenant[tenant_a]}
                patients_b = {p['public_id'] for p in patients_by_tenant[tenant_b]}
                
                # No overlapping patients between different tenants
                assert patients_a.isdisjoint(patients_b), \
                    f"Data leak between {tenant_a} and {tenant_b}"
        
        print("✅ Tenant data isolation test passed")
    
    def test_tenant_switching_persists_session(self, backend_url, frontend_url, test_credentials):
        """Test that tenant switching persists during user session"""
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Set to True for CI
            context = browser.new_context()
            page = context.new_page()
            
            try:
                # Login as super admin
                page.goto(f"{frontend_url}/login")
                page.fill('input[type="email"]', test_credentials['super_admin']['email'])
                page.fill('input[type="password"]', test_credentials['super_admin']['password'])
                page.click('button[type="submit"]')
                
                # Wait for dashboard
                page.wait_for_selector('[data-testid="dashboard"]')
                
                # Switch tenant
                page.click('[data-testid="tenant-switcher"]')
                page.wait_for_selector('[data-testid="tenant-option"]')
                tenant_options = page.query_selector_all('[data-testid="tenant-option"]')
                tenant_options[1].click()
                
                selected_tenant = page.text_content('[data-testid="current-tenant"]')
                
                # Refresh page and verify tenant persists
                page.reload()
                page.wait_for_selector('[data-testid="current-tenant"]')
                
                persisted_tenant = page.text_content('[data-testid="current-tenant"]')
                assert selected_tenant == persisted_tenant, "Tenant selection didn't persist"
                
                # Test multiple switches
                for _ in range(3):
                    page.click('[data-testid="tenant-switcher"]')
                    page.wait_for_selector('[data-testid="tenant-option"]')
                    options = page.query_selector_all('[data-testid="tenant-option"]')
                    options[-1].click()  # Switch to last tenant
                    page.wait_for_timeout(1000)  # Brief pause
                
                # Verify still functional after multiple switches
                page.click('[data-testid="navigation-patients"]')
                page.wait_for_selector('[data-testid="patients-list"]')
                
            finally:
                browser.close()
        
        print("✅ Tenant switching persistence test passed")