import { describe, it, expect, beforeEach, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import { useAuthStore } from '@/stores/auth';
import { createPinia, setActivePinia } from 'pinia';

// Mock API calls
vi.mock('@/services/api', () => ({
  authAPI: {
    login: vi.fn(),
    logout: vi.fn(),
    getCurrentUser: vi.fn(),
    refreshToken: vi.fn(),
    getTenants: vi.fn(),
    switchTenant: vi.fn(),
  },
}));

describe('Auth Store', () => {
  let authStore;
  
  beforeEach(() => {
    setActivePinia(createPinia());
    authStore = useAuthStore();
  });

  it('should login successfully', async () => {
    const mockUser = {
      id: 1,
      email: 'test@example.com',
      first_name: 'Test',
      last_name: 'User',
      role: 'admin'
    };
    
    const mockTokens = {
      access_token: 'mock-access-token',
      refresh_token: 'mock-refresh-token'
    };
    
    // Mock successful API response
    const { authAPI } = await import('@/services/api');
    authAPI.login.mockResolvedValue({
      data: {
        ...mockTokens,
        user: mockUser
      }
    });
    
    await authStore.login('test@example.com', 'password');
    
    expect(authStore.isAuthenticated).toBe(true);
    expect(authStore.user).toEqual(mockUser);
    expect(authAPI.login).toHaveBeenCalledWith('test@example.com', 'password');
  });

  it('should handle login failure', async () => {
    const { authAPI } = await import('@/services/api');
    authAPI.login.mockRejectedValue(new Error('Invalid credentials'));
    
    await expect(authStore.login('test@example.com', 'wrongpassword'))
      .rejects.toThrow('Invalid credentials');
    
    expect(authStore.isAuthenticated).toBe(false);
    expect(authStore.user).toBeNull();
  });

  it('should logout successfully', async () => {
    // First login
    authStore.$patch({
      isAuthenticated: true,
      user: { id: 1, email: 'test@example.com' }
    });
    
    const { authAPI } = await import('@/services/api');
    authAPI.logout.mockResolvedValue({});
    
    await authStore.logout();
    
    expect(authStore.isAuthenticated).toBe(false);
    expect(authStore.user).toBeNull();
    expect(authAPI.logout).toHaveBeenCalled();
  });

  it('should fetch available tenants for super admin', async () => {
    const mockTenants = [
      { id: 'org1', name: 'Organization 1', is_current: true },
      { id: 'org2', name: 'Organization 2', is_current: false }
    ];
    
    const { authAPI } = await import('@/services/api');
    authAPI.getTenants.mockResolvedValue({
      data: {
        tenants: mockTenants,
        is_super_admin: true,
        current_tenant: 'org1'
      }
    });
    
    await authStore.fetchTenants();
    
    expect(authStore.availableTenants).toEqual(mockTenants);
    expect(authStore.isSuperAdmin).toBe(true);
    expect(authStore.currentTenant).toBe('org1');
  });

  it('should switch tenant for super admin', async () => {
    const { authAPI } = await import('@/services/api');
    authAPI.switchTenant.mockResolvedValue({
      data: {
        message: 'Switched to Organization 2',
        tenant: { id: 'org2', name: 'Organization 2' }
      }
    });
    
    await authStore.switchTenant('org2');
    
    expect(authAPI.switchTenant).toHaveBeenCalledWith('org2');
    // You might want to verify the current tenant is updated
  });
});