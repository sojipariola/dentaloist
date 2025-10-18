// src/services/authService.ts
import { apiClient } from './api';
import { 
  LoginCredentials, 
  RegisterData, 
  AuthResponse, 
  User,
  RefreshTokenResponse 
} from '@/types';

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
      const response = await apiClient.post('/auth/login', credentials);
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Login failed. Please check your credentials and try again.');
    }
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/register', userData);
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Registration failed. Please try again.');
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      // Check if we have a token first
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await apiClient.get('/auth/me');
      return response.user;
    } catch (err: any) {
      console.error('Failed to fetch user data:', err);
      
      // Clear invalid tokens
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
      
      throw normalizeError(err, 'Failed to fetch user data. Please login again.');
    }
  },

  async refreshToken(): Promise<RefreshTokenResponse> {
    try {
      const refreshToken = typeof window !== 'undefined' ? localStorage.getItem('refresh_token') : null;
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      const response = await apiClient.post('/auth/refresh', { refresh_token: refreshToken });
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Failed to refresh token. Please login again.');
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/auth/logout', {});
    } catch (err: any) {
      console.error('Logout API error:', err);
      // Even if the API call fails, we should clear local storage
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  },

  async requestPasswordReset(email: string): Promise<void> {
    try {
      await apiClient.post('/auth/forgot-password', { email });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to request password reset');
    }
  },

  async resetPassword(token: string, password: string): Promise<void> {
    try {
      await apiClient.post('/auth/reset-password', { token, password });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to reset password');
    }
  },

  async verifyEmail(token: string): Promise<void> {
    try {
      await apiClient.post('/auth/verify-email', { token });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to verify email');
    }
  },

  async resendVerificationEmail(): Promise<void> {
    try {
      await apiClient.post('/auth/resend-verification', {});
    } catch (err: any) {
      throw normalizeError(err, 'Failed to resend verification email');
    }
  },

  googleLogin(): void {
    if (typeof window !== 'undefined') {
      const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
      window.location.href = `${apiBaseUrl}/auth/google/login`;
    }
  },

  async handleGoogleCallback(code: string): Promise<AuthResponse> {
    try {
      const response = await apiClient.post('/auth/google/callback', { code });
      return response;
    } catch (err: any) {
      throw normalizeError(err, 'Google authentication failed');
    }
  }
};