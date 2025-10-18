// src/services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export const api = {
  get: (url: string) => fetch(`${API_BASE_URL}${url}`).then(res => res.json()),
  post: (url: string, data: any) => 
    fetch(`${API_BASE_URL}${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json()),
  put: (url: string, data: any) => 
    fetch(`${API_BASE_URL}${url}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(res => res.json()),
  delete: (url: string) => 
    fetch(`${API_BASE_URL}${url}`, { method: 'DELETE' }).then(res => res.json()),
};

// Add auth token to requests
export const setAuthToken = (token: string) => {
  // You can use axios interceptors or fetch wrappers for this
};