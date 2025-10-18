// src/api/client/axiosClient.ts — FINAL VERSION with Tenant + Debug Logs

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'

// 🌍 Environment-aware API base URL
const API_BASE_URL =
  import.meta.env?.VITE_API_URL?.replace(/\/$/, '') || 'http://localhost:5000/api'

console.log('🚀 [Axios] Initialized with base URL:', API_BASE_URL)

// ✅ Create axios instance
export const axiosClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // 🔒 Needed for cookies/JWT cookies if Flask uses them
})

// ✅ Request Interceptor — Adds Bearer + X-Tenant-ID headers
axiosClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    const tenantId = localStorage.getItem('tenant_id')

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('🔑 [Axios] Added Authorization header')
    }

    if (tenantId) {
      config.headers['X-Tenant-ID'] = tenantId
      console.log('🏢 [Axios] Added X-Tenant-ID header:', tenantId)
    }

    console.log('📤 [Axios] Sending Request:', {
      method: config.method?.toUpperCase(),
      url: config.url,
      baseURL: config.baseURL,
      data: config.data,
      headers: config.headers,
    })

    return config
  },
  (error) => {
    console.error('❌ [Axios] Request Interceptor Error:', error)
    return Promise.reject(error)
  }
)

// ✅ Response Interceptor — Handles refresh logic and tenant sync
axiosClient.interceptors.response.use(
  (response) => {
    console.log('✅ [Axios] Response OK:', {
      status: response.status,
      url: response.config.url,
      data: response.data,
    })

    // 🔄 Capture Tenant-ID from headers (server → client)
    const tenantHeader =
      response.headers['x-tenant-id'] || response.headers['X-Tenant-ID']
    if (tenantHeader) {
      console.log('🏢 [Axios] Synced Tenant-ID from response headers:', tenantHeader)
      localStorage.setItem('tenant_id', tenantHeader)
    }

    return response
  },
  async (error: AxiosError) => {
    console.error('❌ [Axios] Response Error:', {
      status: error.response?.status,
      url: error.config?.url,
      data: error.response?.data,
      message: error.message,
    })

    const originalRequest: any = error.config
    if (!error.response || originalRequest._retry) {
      return Promise.reject(error)
    }

    // ⚠️ Handle 401 → Try Refresh
    if (error.response.status === 401) {
      console.warn('🔄 [Axios] 401 detected — attempting token refresh')
      originalRequest._retry = true
      const refreshToken = localStorage.getItem('refresh_token')

      if (!refreshToken) {
        console.error('❌ [Axios] No refresh token found, redirecting to login')
        localStorage.removeItem('access_token')
        localStorage.removeItem('tenant_id')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      try {
        // 🔄 Token refresh request
        const refreshResponse = await axios.post(
          `${API_BASE_URL}/auth/refresh`,
          {},
          {
            headers: { Authorization: `Bearer ${refreshToken}` },
            withCredentials: true,
          }
        )

        const { access_token, tenant_id } = refreshResponse.data
        if (!access_token) throw new Error('Invalid refresh response')

        console.log('✅ [Axios] Token refreshed successfully')
        localStorage.setItem('access_token', access_token)
        if (tenant_id) localStorage.setItem('tenant_id', tenant_id)

        // Retry the failed request
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return axiosClient(originalRequest)
      } catch (refreshError) {
        console.error('❌ [Axios] Refresh failed, forcing logout:', refreshError)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('tenant_id')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)
