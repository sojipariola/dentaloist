import { 
  LoginCredentials, 
  RegisterData, 
  AuthTokenResponse, 
  User,
  RefreshTokenResponse
} from '@/types/auth';
import { apiClient } from './api';

// Normalize base URL so `/api` is only added once
const rawBaseUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000";
const API_BASE_URL = rawBaseUrl.endsWith("/api")
  ? rawBaseUrl
  : `${rawBaseUrl}/api`;

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthTokenResponse> => {
    const response = await apiClient.login(credentials);
    if (response.data) {
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      return response.data;
    } else {
      throw new Error(response.error || 'Login failed');
    }
  },

  register: async (userData: RegisterData): Promise<AuthTokenResponse> => {
    const response = await apiClient.register(userData);
    if (response.data) {
      if (typeof window !== 'undefined') {
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);
      }
      return response.data;
    } else {
      throw new Error(response.error || 'Registration failed');
    }
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.getCurrentUser();
    if (response.data) {
      return response.data.user;
    } else {
      throw new Error(response.error || 'Failed to fetch user');
    }
  },

  logout: async (): Promise<void> => {
    try {
      await apiClient.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      }
    }
  },

  refreshToken: async (): Promise<RefreshTokenResponse> => {
    if (typeof window === 'undefined') {
      throw new Error('Cannot refresh token on server side');
    }

    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${refreshToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Token refresh failed: ${response.status}`);
      }

      const data: RefreshTokenResponse = await response.json();
      localStorage.setItem('access_token', data.access_token);
      return data;
    } catch (error) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw error;
    }
  },

  googleLogin: (): void => {
    if (typeof window !== 'undefined') {
      window.location.href = `${API_BASE_URL}/auth/google/login`;
    }
  },

  isAuthenticated: (): boolean => {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('access_token');
  },

  getToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('access_token');
  },

  getRefreshToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('refresh_token');
  },

  setTokens: (accessToken: string, refreshToken: string): void => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', accessToken);
      localStorage.setItem('refresh_token', refreshToken);
    }
  },

  clearTokens: (): void => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    }
  }
};
