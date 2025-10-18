// src/services/auth.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  organization: {
    id: number;
    name: string;
    type: string;
    subscription_plan: string;
  };
}

export interface RegisterData {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  organization_name: string;
  organization_type: 'clinic' | 'laboratory' | 'family';
}

export const authService = {
  register: async (data: RegisterData): Promise<{ token: string; user: User }> => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },

  login: async (email: string, password: string): Promise<{ token: string; user: User }> => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    return response.json();
  },
};

// src/hooks/useAuth.ts
import { useState, useEffect } from 'react';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and get user info
      authService.getProfile().then(setUser).finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  return { user, loading };
};