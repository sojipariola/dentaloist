// services/authService.ts
import { 
  LoginCredentials, 
  RegisterData, 
  User, 
  AuthResponse, 
  CurrentUserResponse,
  RefreshTokenResponse
} from '@/types';
import { apiClient } from './api';

// Normalize all errors into proper Error objects
const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) {
    return err;
  }
  if (typeof err === 'string') {
    return new Error(err);
  }
  if (err?.message) {
    return new Error(err.message);
  }
  return new Error(fallbackMessage);
};

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/api/auth/login', credentials);
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Login failed');
    }
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/api/auth/register', userData);
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Registration failed');
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response: CurrentUserResponse = await apiClient.get('/api/auth/me'); // ✅ Fixed: added /api/
      return response.user;
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch user data');
    }
  },

  async refreshToken(): Promise<RefreshTokenResponse> {
    try {
      const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await apiClient.post('/api/auth/refresh', { refresh_token: refreshToken });
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Failed to refresh token');
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/auth/logout', {});
    } catch (err: any) {
      // Even if the API call fails, we should clear local storage
      console.error('Logout API error:', err);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  },

  async requestPasswordReset(email: string): Promise<void> {
    try {
      await apiClient.post('/api/auth/forgot-password', { email });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to request password reset');
    }
  },

  async resetPassword(token: string, password: string): Promise<void> {
    try {
      await apiClient.post('/api/auth/reset-password', { token, password });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to reset password');
    }
  },

  async verifyEmail(token: string): Promise<void> {
    try {
      await apiClient.post('/api/auth/verify-email', { token });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to verify email');
    }
  },

  async resendVerificationEmail(): Promise<void> {
    try {
      await apiClient.post('/api/auth/resend-verification', {});
    } catch (err: any) {
      throw normalizeError(err, 'Failed to resend verification email');
    }
  },

  googleLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/google/login`;
    }
  },

  facebookLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/facebook/login`;
    }
  },

  githubLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/github/login`;
    }
  },

  async handleOAuthCallback(): Promise<AuthResponse> {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const code = urlParams.get('code');
      
      if (code) {
        const response = await apiClient.post('/api/auth/oauth/callback', { code });
        return response;
      }
      
      throw new Error('No authorization code found');
    } catch (err: any) {
      throw normalizeError(err, 'OAuth authentication failed');
    }
  }
};




// Add this to your authService temporarily
export const debugAuth = async (): Promise<void> => {
  console.group('Auth Debug Information');
  
  // Check environment variables
  console.log('NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
  
  // Check tokens
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  console.log('Access token exists:', !!token);
  if (token) {
    console.log('Token length:', token.length);
    // Basic JWT validation (should have 3 parts)
    const parts = token.split('.');
    console.log('Token parts:', parts.length);
  }
  
  // Test API connectivity
  try {
    console.log('Testing API connectivity...');
    const testResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}/health`, {
      method: 'GET',
    });
    console.log('Health check status:', testResponse.status);
    
    if (testResponse.ok) {
      const healthData = await testResponse.json();
      console.log('Health check response:', healthData);
    }
  } catch (error) {
    console.error('Health check failed:', error);
  }
  
  console.groupEnd();
};

// Call this function in your component to debug
// debugAuth();