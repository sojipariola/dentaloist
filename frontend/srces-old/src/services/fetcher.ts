// src/services/fetcher.ts
import { API_BASE_URL } from './api';

export const fetcher = async (url: string, options?: RequestInit) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options?.headers,
  };

  const response = await fetch(`${API_BASE_URL}${url}`, {
    headers,
    ...options,
  });

  if (response.status === 401) {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth/login';
    }
    throw new Error('Authentication required');
  }

  if (response.status === 403) {
    throw new Error('Access denied');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};