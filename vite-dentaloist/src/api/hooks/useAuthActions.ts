// src/api/hooks/useAuthActions.ts
import { useCallback, useState } from 'react'
import { useAuthStore } from '@/app/store'
import { authService, type LoginCredentials, type RegisterData, type AuthResponse } from '../services/auth.service'

export const useAuthActions = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)
  const logoutFromStore = useAuthStore((state) => state.logout)
  
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const login = useCallback(async (email: string, password: string) => {
    try {
      setLoading(true)
      setError(null)
      
      const authData = await authService.login({ email, password })
      
      // Store tokens in localStorage
      localStorage.setItem('access_token', authData.access_token)
      localStorage.setItem('refresh_token', authData.refresh_token)
      localStorage.setItem('session_token', authData.session_token)
      localStorage.setItem('user', JSON.stringify(authData.user))
      localStorage.setItem('tenant_id', authData.user.organization_id)

      // Update auth store
      setUser(authData.user)
      setAuthenticated(true)
      
      return authData
    } catch (err: any) {
      const errorMessage = err.message || 'Login failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setUser, setAuthenticated])

  const register = useCallback(async (registerData: RegisterData) => {
    try {
      setLoading(true)
      setError(null)
      
      const authData = await authService.register(registerData)
      
      // Store tokens in localStorage
      localStorage.setItem('access_token', authData.access_token)
      localStorage.setItem('refresh_token', authData.refresh_token)
      localStorage.setItem('session_token', authData.session_token)
      localStorage.setItem('user', JSON.stringify(authData.user))
      localStorage.setItem('tenant_id', authData.user.organization_id)

      // Update auth store
      setUser(authData.user)
      setAuthenticated(true)
      
      return authData
    } catch (err: any) {
      const errorMessage = err.message || 'Registration failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setUser, setAuthenticated])

  const logout = useCallback(async (redirectTo: string = '/login') => {
    try {
      setLoading(true)
      await authService.logout()
    } catch (err: any) {
      console.error('Logout API call failed:', err)
      // Continue with logout even if API call fails
    } finally {
      // Always clear local state
      logoutFromStore()
      setLoading(false)
      
      // Redirect if specified
      if (redirectTo) {
        window.location.href = redirectTo
      }
    }
  }, [logoutFromStore])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    login,
    register,
    logout,
    loading,
    error,
    clearError
  }
}