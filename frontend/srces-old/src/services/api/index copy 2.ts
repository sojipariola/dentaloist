// services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

class ApiClient {
  private baseURL: string;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || API_BASE_URL;
  }

  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    };

    const url = `${this.baseURL}${endpoint}`;
    
    console.log('API Request:', {
      url,
      method: options.method || 'GET',
      headers: Object.fromEntries(Object.entries(headers).filter(([key]) => key !== 'Authorization')),
      hasToken: !!token,
    });

    try {
      const response = await fetch(url, {
        headers,
        ...options,
      });

      console.log('API Response:', {
        url,
        status: response.status,
        statusText: response.statusText,
      });

      if (response.status === 401) {
        if (typeof window !== 'undefined') {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
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
    } catch (error) {
      console.error('API Request Failed:', {
        url,
        error: error instanceof Error ? error.message : 'Unknown error',
      });
      
      if (error instanceof TypeError) {
        throw new Error('Network error: Could not connect to server');
      }
      
      throw error;
    }
  }

  async get(endpoint: string): Promise<any> {
    return this.request(endpoint);
  }

  async post(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async put(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async patch(endpoint: string, data: any): Promise<any> {
    return this.request(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  async delete(endpoint: string): Promise<any> {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();
export { API_BASE_URL };