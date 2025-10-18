import { test, expect } from '@playwright/test';

test.describe('Authentication and Tenant Switching', () => {
  let superAdminEmail = 'sojipariola@gmail.com';
  let superAdminPassword = 'your_password'; // You'll need to set this
  let regularUserEmail = 'admin@brightsmile.com';
  let regularUserPassword = 'user_password'; // You'll need to set this

  test('super admin can login and switch tenants', async ({ page }) => {
    // Navigate to login page
    await page.goto('/login');
    
    // Fill login form
    await page.fill('input[type="email"]', superAdminEmail);
    await page.fill('input[type="password"]', superAdminPassword);
    
    // Click login button
    await page.click('button[type="submit"]');
    
    // Wait for navigation and check if login was successful
    await page.waitForURL('**/dashboard**', { timeout: 10000 });
    
    // Check if tenant switcher is visible for super admin
    const tenantSwitcher = page.locator('[data-testid="tenant-switcher"]');
    await expect(tenantSwitcher).toBeVisible();
    
    // Open tenant switcher
    await tenantSwitcher.click();
    
    // Check if multiple tenants are available
    const tenantOptions = page.locator('[data-testid="tenant-option"]');
    await expect(tenantOptions).toHaveCount(2);
    
    // Switch to different tenant
    await tenantOptions.nth(1).click();
    
    // Verify tenant switch (check for success message or URL change)
    await expect(page.locator('[data-testid="current-tenant"]')).toHaveText(/Org 2|BrightSmile/);
  });

  test('regular user cannot see tenant switcher', async ({ page }) => {
    await page.goto('/login');
    
    // Login as practice admin (regular user)
    await page.fill('input[type="email"]', regularUserEmail);
    await page.fill('input[type="password"]', regularUserPassword);
    await page.click('button[type="submit"]');
    
    // Wait for navigation
    await page.waitForURL('**/dashboard**', { timeout: 10000 });
    
    // Verify tenant switcher is NOT visible for regular users
    const tenantSwitcher = page.locator('[data-testid="tenant-switcher"]');
    await expect(tenantSwitcher).toBeHidden();
  });

  test('user can logout', async ({ page }) => {
    await page.goto('/login');
    
    // Login
    await page.fill('input[type="email"]', superAdminEmail);
    await page.fill('input[type="password"]', superAdminPassword);
    await page.click('button[type="submit"]');
    
    // Wait for login
    await page.waitForURL('**/dashboard**', { timeout: 10000 });
    
    // Click logout
    await page.click('[data-testid="user-menu"]');
    await page.click('[data-testid="logout-button"]');
    
    // Verify redirected to login page
    await page.waitForURL('**/login**');
    await expect(page.locator('input[type="email"]')).toBeVisible();
  });

  test('protected routes require authentication', async ({ page }) => {
    // Try to access dashboard without login
    await page.goto('/dashboard');
    
    // Should be redirected to login page
    await page.waitForURL('**/login**');
    await expect(page.locator('input[type="email"]')).toBeVisible();
  });
});