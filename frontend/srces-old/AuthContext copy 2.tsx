'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User } from '@/../types/auth';
import useAuth from '@/../hooks/useAuth';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (userData: any) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const auth = useAuth();

  useEffect(() => {
    // Check authentication status on mount
    auth.checkAuth();
  }, []);

  const value = {
    user: auth.user,
    isLoading: auth.isLoading,
    error: auth.error,
    login: async (email: string, password: string) => {
      return auth.login({ email, password });
    },
    register: async (userData: any) => {
      return auth.register(userData);
    },
    logout: auth.logout,
    isAuthenticated: auth.isAuthenticated
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};