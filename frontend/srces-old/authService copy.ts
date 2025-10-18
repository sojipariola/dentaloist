import { LoginCredentials, RegisterData, AuthResponse, User } from '@/./types/auth';
import { apiClient } from './api';

export const authService = {
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.login(credentials);
    if (response.error) {
      throw new Error(response.error);
    }
    return response.data!;
  },

  async register(userData: Omit<RegisterData, 'confirmPassword'>): Promise<AuthResponse> {
    const response = await apiClient.register(userData);
    if (response.error) {
      throw new Error(response.error);
    }
    return response.data!;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.getCurrentUser();
    if (response.error) {
      throw new Error(response.error);
    }
    return response.data!.user;
  },

  async logout(): Promise<void> {
    // Clear local storage
    localStorage.removeItem('authToken');
    localStorage.setItem('isLoggedIn', 'false');
  },

  isAuthenticated(): boolean {
    if (typeof window === 'undefined') return false;
    return !!localStorage.getItem('authToken');
  },

  getToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('authToken');
  }
};