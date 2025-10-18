'use client'

import { useState, useCallback } from 'react';
import { LoginCredentials, RegisterData, User } from '@/./types/auth';
import { authService } from '@/./services/authService';

interface UseAuthReturn {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  register: (userData: RegisterData) => Promise<boolean>;
  logout: () => void;
  checkAuth: () => Promise<boolean>;
  clearError: () => void;
  isAuthenticated: boolean;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (credentials: LoginCredentials): Promise<boolean> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await authService.login(credentials);
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', response.access_token);
        localStorage.setItem('isLoggedIn', 'true');
      }
      setUser(response.user);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (userData: RegisterData): Promise<boolean> => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await authService.register(userData);
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', response.access_token);
        localStorage.setItem('isLoggedIn', 'true');
      }
      setUser(response.user);
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    authService.logout();
    setUser(null);
  }, []);

  const checkAuth = useCallback(async (): Promise<boolean> => {
    if (!authService.isAuthenticated()) {
      return false;
    }

    setIsLoading(true);
    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
      return true;
    } catch (err) {
      authService.logout();
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    user,
    isLoading,
    error,
    login,
    register,
    logout,
    checkAuth,
    clearError,
    isAuthenticated: !!user
  };
};