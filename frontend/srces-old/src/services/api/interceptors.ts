// src/services/api/interceptors.ts
import { API_BASE_URL } from './config';

export const setupRequestInterceptors = (request: Request): Request => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  if (token) {
    request.headers.set('Authorization', `Bearer ${token}`);
  }
  
  return request;
};

export const handleResponse = async (response: Response): Promise<any> => {
  if (response.status === 401) {
    // Token expired or invalid
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

  if (response.status === 404) {
    throw new Error('Resource not found');
  }

  if (response.status === 422) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || 'Validation failed');
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

export const handleError = (error: any): never => {
  if (error.name === 'AbortError') {
    throw new Error('Request timeout');
  }
  
  if (error instanceof TypeError) {
    throw new Error('Network error: Could not connect to server');
  }
  
  throw error;
};