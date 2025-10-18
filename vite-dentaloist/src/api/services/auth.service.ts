// src/api/services/auth.service.ts

import { axiosClient } from '@/api/client/axiosClient'
import type { AxiosError } from 'axios'

export interface LoginCredentials {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  session_token: string
  user: {
    id: number
    email: string
    first_name: string
    last_name: string
    organization_id: string
    organization_name?: string
    roles: string[]
    permissions: string[]
    is_active: boolean
    created_at?: string
    updated_at?: string
  }
}

export interface BaseUser {
  id: number
  email: string
  first_name: string
  last_name: string
  organization_id: string
  organization_name?: string
  roles: string[]           // This should contain role names like ['admin', 'user']
  permissions: string[]     // This should contain permission strings
  is_active: boolean
  is_admin: boolean         // This is the admin flag from your backend
  created_at?: string
  updated_at?: string
}

export interface RegisterData {
  email: string
  password: string
  first_name: string
  last_name: string
  organization_id?: string
}

// API Endpoints
const AUTH_ENDPOINTS = {
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
  REGISTER: '/auth/register',
  ME: '/auth/me',
  REFRESH: '/auth/refresh',
  ADMIN_DIRECT_LOGIN: '/auth/admin-login'
}

// Improved error handler with proper typing
const handleApiError = (error: AxiosError): Error => {
  console.error('API Error:', error)
  
  // Handle different error response formats
  const errorData = error.response?.data as any
  
  if (errorData?.message) {
    return new Error(errorData.message)
  }
  
  if (errorData?.error) {
    return new Error(errorData.error)
  }
  
  if (typeof errorData === 'string') {
    return new Error(errorData)
  }
  
  if (error.response?.status === 401) {
    return new Error('Unauthorized - Please log in again')
  }
  
  if (error.response?.status === 403) {
    return new Error('Access denied')
  }
  
  if (error.response?.status === 404) {
    return new Error('Resource not found')
  }
  
  if (error.code === 'NETWORK_ERROR') {
    return new Error('Network error - Please check your connection')
  }
  
  return new Error(error.message || 'An unexpected error occurred')
}

class AuthService {
  /**
   * 🔐 User Login
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      console.log('🔐 Attempting login...', { email: credentials.email })
      
      const { data } = await axiosClient.post<AuthResponse>(AUTH_ENDPOINTS.LOGIN, credentials)

      // 🎯 CRITICAL: Store all tokens from your backend response
      this.storeAuthData({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        session_token: data.session_token,
        user: data.user
      })

      console.log('✅ Login successful! Tokens stored in localStorage')
      console.log('👤 User:', data.user)
      
      return data
    } catch (error) {
      this.clearAuthData()
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 🆕 Register new user
   */
  async register(payload: RegisterData): Promise<AuthResponse> {
    try {
      const { data } = await axiosClient.post<AuthResponse>(AUTH_ENDPOINTS.REGISTER, payload)

      // Store tokens after registration
      this.storeAuthData({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        session_token: data.session_token,
        user: data.user
      })

      return data
    } catch (error) {
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 🚪 Logout user
   */
  async logout(): Promise<void> {
    try {
      await axiosClient.post(AUTH_ENDPOINTS.LOGOUT)
    } catch (error) {
      console.warn('Logout API call failed:', error)
    } finally {
      // Always clear stored tokens
      this.clearAuthData()
      console.log('🚪 User logged out')
    }
  }

  /**
   * 👤 Get current authenticated user
   */
  async getCurrentUser(): Promise<BaseUser> {
    try {
      const { data } = await axiosClient.get<{ user: BaseUser }>(AUTH_ENDPOINTS.ME)
      return data.user
    } catch (error: any) {
      // 401 — unauthorized
      if (error.response?.status === 401) {
        this.clearAuthData()
      }
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 🔁 Refresh access token
   */
  async refreshToken(): Promise<{ access_token: string }> {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token available')
      }

      const { data } = await axiosClient.post<{ access_token: string }>(
        AUTH_ENDPOINTS.REFRESH,
        {},
        {
          headers: { Authorization: `Bearer ${refreshToken}` }
        }
      )

      if (data.access_token) {
        localStorage.setItem('access_token', data.access_token)
        console.log('🔄 Token refreshed successfully')
      }

      return data
    } catch (error) {
      this.clearAuthData()
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 🧑‍💼 Direct Admin Login (no credentials)
   */
  async adminDirectLogin(): Promise<AuthResponse> {
    try {
      const { data } = await axiosClient.post<AuthResponse>(AUTH_ENDPOINTS.ADMIN_DIRECT_LOGIN)

      this.storeAuthData({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        session_token: data.session_token,
        user: data.user
      })

      return data
    } catch (error) {
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 🧠 Check active session
   */
  async checkSession(): Promise<BaseUser> {
    try {
      const { data } = await axiosClient.get<{ user: BaseUser }>(AUTH_ENDPOINTS.ME)
      return data.user
    } catch (error) {
      throw handleApiError(error as AxiosError)
    }
  }

  /**
   * 💾 Store authentication data in localStorage
   */
  private storeAuthData(authData: {
    access_token: string
    refresh_token: string
    session_token: string
    user: any
  }) {
    localStorage.setItem('access_token', authData.access_token)
    localStorage.setItem('refresh_token', authData.refresh_token)
    localStorage.setItem('session_token', authData.session_token)
    localStorage.setItem('user', JSON.stringify(authData.user))
    localStorage.setItem('tenant_id', authData.user.organization_id)
    
    console.log('💾 Auth data stored in localStorage')
  }

  /**
   * 🧹 Clear all authentication data
   */
  clearAuthData() {
    const items = [
      'access_token',
      'refresh_token',
      'session_token', 
      'user',
      'tenant_id'
    ]
    
    items.forEach(item => localStorage.removeItem(item))
    console.log('🧹 Auth data cleared from localStorage')
  }

  /**
   * 🔍 Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token')
    const user = localStorage.getItem('user')
    return !!(token && user)
  }

  /**
   * 👤 Get current user from storage
   */
  getStoredUser(): BaseUser | null {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * 🔑 Get access token from storage
   */
  getStoredAccessToken(): string | null {
    return localStorage.getItem('access_token')
  }

  /**
   * 🐛 Debug: Check what's in storage
   */
  debugStorage() {
    console.log('🔍 Auth Storage Debug:')
    const items = {
      'access_token': localStorage.getItem('access_token') ? '✅ Present' : '❌ Missing',
      'refresh_token': localStorage.getItem('refresh_token') ? '✅ Present' : '❌ Missing',
      'session_token': localStorage.getItem('session_token') ? '✅ Present' : '❌ Missing',
      'user': localStorage.getItem('user') ? '✅ Present' : '❌ Missing',
      'tenant_id': localStorage.getItem('tenant_id') ? '✅ Present' : '❌ Missing'
    }
    
    Object.entries(items).forEach(([key, value]) => {
      console.log(`${key}: ${value}`)
    })

    if (localStorage.getItem('user')) {
      console.log('👤 User data:', JSON.parse(localStorage.getItem('user')!))
    }
    
    return items
  }

  /**
   * 🧪 Test login function
   */
  async testLogin(): Promise<AuthResponse> {
    console.log('🧪 Testing authentication...')
    
    try {
      const result = await this.login({
        email: 'sojipariola@gmail.com',
        password: 'Soji1111'
      })
      
      console.log('✅ Login test successful!')
      this.debugStorage()
      
      return result
    } catch (error) {
      console.error('❌ Login test failed:', error)
      throw error
    }
  }
}

// Export singleton instance
export const authService = new AuthService()

// Make test function available globally for easy debugging
declare global {
  interface Window {
    testAuth: () => Promise<any>
    authService: AuthService
  }
}

if (typeof window !== 'undefined') {
  window.testAuth = () => authService.testLogin()
  window.authService = authService
}