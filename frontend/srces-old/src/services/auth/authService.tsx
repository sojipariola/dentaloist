// src/services/auth/authService.ts
import { apiClient } from '../api';
import { API_ENDPOINTS } from '../api/config';
import { 
  LoginCredentials, 
  RegisterData, 
  AuthResponse, 
  User,
  RefreshTokenResponse,
  CurrentUserResponse 
} from './types';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (typeof err === 'string') return new Error(err);
  if (err?.message) return new Error(err.message);
  return new Error(fallbackMessage);
};

export const authService = {
  // Email/Password Auth
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      return await apiClient.post(API_ENDPOINTS.AUTH.LOGIN, credentials);
    } catch (err: any) {
      throw normalizeError(err, 'Login failed');
    }
  },

  async register(userData: RegisterData): Promise<AuthResponse> {
    try {
      const { confirmPassword, ...dataToSend } = userData;
      return await apiClient.post(API_ENDPOINTS.AUTH.REGISTER, dataToSend);
    } catch (err: any) {
      throw normalizeError(err, 'Registration failed');
    }
  },

  // ✅ Enhanced getCurrentUser with dev fallback
  async getCurrentUser(): Promise<User> {
    try {
      const response: CurrentUserResponse = await apiClient.get(API_ENDPOINTS.AUTH.ME);
      return response.user;
    } catch (err: any) {
      // Temporary fallback for development
      if (process.env.NODE_ENV === 'development') {
        console.warn('API unavailable, returning mock user');
        return {
          id: 1,
          email: 'demo@example.com',
          first_name: 'Demo',
          last_name: 'User',
          role: 'admin',
          roles: ['admin'],
          permissions: [],
          is_active: true,
          is_admin: true,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        } as User;
      }
      throw normalizeError(err, 'Failed to fetch user data');
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post(API_ENDPOINTS.AUTH.LOGOUT, {});
    } catch (err: any) {
      console.error('Logout error:', err);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  },

  async refreshToken(): Promise<RefreshTokenResponse> {
    try {
      const refreshToken = typeof window !== 'undefined' 
        ? localStorage.getItem('refresh_token') 
        : null;
      
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }
      
      return await apiClient.post(API_ENDPOINTS.AUTH.REFRESH, { refresh_token: refreshToken });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to refresh token');
    }
  },

  // Social Auth - Redirect methods
  googleLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}${API_ENDPOINTS.AUTH.GOOGLE}`;
    }
  },

  facebookLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}${API_ENDPOINTS.AUTH.FACEBOOK}`;
    }
  },

  githubLogin(): void {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}${API_ENDPOINTS.AUTH.GITHUB}`;
    }
  },

  // Password management
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
};

// Auth service index
export * from './types';