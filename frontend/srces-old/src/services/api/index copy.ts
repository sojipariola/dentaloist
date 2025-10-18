// src/services/api/index.ts
import { API_CONFIG, API_BASE_URL } from './config';
import { setupRequestInterceptors, handleResponse, handleError } from './interceptors';

class ApiClient {
  private baseURL: string;

  constructor(baseURL?: string) {
    this.baseURL = baseURL || API_BASE_URL;
  }

  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);

    try {
      const url = `${this.baseURL}${endpoint}`;
      let request = new Request(url, {
        ...options,
        signal: controller.signal,
      });

      request = setupRequestInterceptors(request);
      
      const response = await fetch(request);
      clearTimeout(timeoutId);
      
      return await handleResponse(response);
    } catch (error) {
      clearTimeout(timeoutId);
      return handleError(error);
    }
  }

  async get(endpoint: string, params?: Record<string, string>): Promise<any> {
    const queryString = params ? `?${new URLSearchParams(params)}` : '';
    return this.request(`${endpoint}${queryString}`);
  }

  async post(endpoint: string, data?: any): Promise<any> {
    return this.request(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put(endpoint: string, data?: any): Promise<any> {
    return this.request(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async patch(endpoint: string, data?: any): Promise<any> {
    return this.request(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete(endpoint: string): Promise<any> {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }

  async upload(endpoint: string, file: File, fieldName = 'file'): Promise<any> {
    const formData = new FormData();
    formData.append(fieldName, file);
    
    return this.request(endpoint, {
      method: 'POST',
      body: formData,
      headers: {
        // Let browser set Content-Type for FormData
      },
    });
  }
}

// Singleton instance
export const apiClient = new ApiClient();