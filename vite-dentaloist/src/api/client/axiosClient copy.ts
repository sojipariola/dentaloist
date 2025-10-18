// src/api/client/axiosClient.ts

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const axiosClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // ✅ Add this for session cookies
})

// Request interceptor - Only add token if it exists
axiosClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    // Only add Authorization header if token exists
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - Handle both session and token auth
axiosClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If it's a 401 error and we have a token, try to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      const token = localStorage.getItem('access_token')
      const refreshToken = localStorage.getItem('refresh_token')
      
      // Only attempt token refresh if we have tokens
      if (token && refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          }, {
            withCredentials: true // Include credentials for refresh
          })
          
          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)
          
          // Retry with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return axiosClient(originalRequest)
        } catch (refreshError) {
          // Token refresh failed, clear tokens
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
          return Promise.reject(refreshError)
        }
      } else {
        // No tokens, redirect to login
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
) 