// src/services/api/index.ts
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
    
    // Enhanced logging for debugging
    console.log('API Request:', {
      url,
      method: options.method || 'GET',
      headers: Object.fromEntries(Object.entries(headers).filter(([key]) => key !== 'Authorization')),
      hasToken: !!token,
      body: options.body ? JSON.parse(options.body as string) : undefined,
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
        headers: Object.fromEntries(response.headers.entries()),
      });

      // Handle non-2xx responses
      if (!response.ok) {
        let errorData;
        try {
          errorData = await response.json();
        } catch (e) {
          errorData = { message: `HTTP error ${response.status}: ${response.statusText}` };
        }
        
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      // Handle 204 No Content responses
      if (response.status === 204) {
        return null;
      }

      const responseData = await response.json();
      console.log('API Response Data:', responseData);
      return responseData;

    } catch (error) {
      console.error('API Request Failed:', {
        url,
        error: error instanceof Error ? error.message : 'Unknown error',
        errorObject: error,
      });
      
      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        throw new Error('Network error: Could not connect to server. Please check if the backend is running.');
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