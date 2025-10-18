// src/api/services/authService.ts
import { axiosClient } from '../client/axiosClient'

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

class AuthService {
  /**
   * Login user and store tokens in localStorage
   */
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      console.log('🔐 Attempting login...', { email: credentials.email })
      
      const response = await axiosClient.post<AuthResponse>('/auth/login', credentials)
      const { access_token, refresh_token, session_token, user } = response.data

      // 🎯 CRITICAL: Store tokens in localStorage
      this.storeAuthData({
        access_token,
        refresh_token,
        session_token,
        user
      })

      console.log('✅ Login successful! Tokens stored in localStorage')
      console.log('👤 User:', user)
      
      return response.data
      
    } catch (error: any) {
      console.error('❌ Login failed:', error)
      this.clearAuthData()
      throw new Error(
        error.response?.data?.message || 
        error.message || 
        'Login failed. Please try again.'
      )
    }
  }

  /**
   * Store authentication data in localStorage
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
  }

  /**
   * Clear all authentication data
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
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token')
    const user = localStorage.getItem('user')
    return !!(token && user)
  }

  /**
   * Get current user from storage
   */
  getCurrentUser() {
    const userStr = localStorage.getItem('user')
    return userStr ? JSON.parse(userStr) : null
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token')
  }

  /**
   * Logout user
   */
  async logout() {
    try {
      // Call logout endpoint if needed
      await axiosClient.post('/auth/logout')
    } catch (error) {
      console.warn('Logout API call failed:', error)
    } finally {
      this.clearAuthData()
      console.log('🚪 User logged out')
    }
  }

  /**
   * Debug: Check what's in storage
   */
  debugStorage() {
    console.log('🔍 Auth Storage Debug:')
    const items = {
      'access_token': localStorage.getItem('access_token'),
      'refresh_token': localStorage.getItem('refresh_token'),
      'session_token': localStorage.getItem('session_token'),
      'user': localStorage.getItem('user'),
      'tenant_id': localStorage.getItem('tenant_id')
    }
    
    Object.entries(items).forEach(([key, value]) => {
      console.log(`${key}:`, value ? '✅ Present' : '❌ Missing')
    })
    
    return items
  }
}

export const authService = new AuthService()