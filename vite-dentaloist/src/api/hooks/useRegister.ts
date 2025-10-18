// src/api/hooks/useRegister.ts (Simple version)
import { useCallback } from 'react'
import { useAuthStore } from '@/app/store'
import { authService, type RegisterData } from '../services/auth.service'

export const useRegister = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)

  const register = useCallback(async (registerData: RegisterData) => {
    try {
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
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }, [setUser, setAuthenticated])

  return {
    mutateAsync: register,
    isPending: false // You can manage loading state differently if needed
  }
}