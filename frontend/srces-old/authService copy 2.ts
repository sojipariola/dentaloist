import { 
  LoginCredentials, 
  RegisterData, 
  AuthResponse, 
  User,
  RefreshTokenResponse
} from '@/types/auth';
import api from './api'; // your axios instance

export const authService = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/login', credentials);
    const data = response.data;
    
    // Store tokens
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    
    return data;
  },

  register: async (userData: RegisterData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/register', userData);
    const data = response.data;
    
    // Store tokens
    if (typeof window !== 'undefined') {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    
    return data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<{ user: User }>('/api/auth/me');
    return response.data.user;
  },

  logout: async (): Promise<void> => {
    try {
      await api.post('/api/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Always clear local storage
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
      const response = await api.post<RefreshTokenResponse>(
        '/api/auth/refresh', 
        {},
        {
          headers: {
            'Authorization': `Bearer ${refreshToken}`
          }
        }
      );
      
      localStorage.setItem('access_token', response.data.access_token);
      return response.data;
    } catch (error) {
      // Clear tokens if refresh fails
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      throw error;
    }
  },

  googleLogin: (): void => {
    if (typeof window !== 'undefined') {
      window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/google/login`;
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
  }
};