// src/api/hooks/useAdminDirectLogin.ts
import { useCallback } from 'react'
import { useAuthStore } from '@/app/store'
import { authService } from '../services/auth.service'

export const useAdminDirectLogin = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)
  const setLoading = useAuthStore((state) => state.setLoading)

  const adminDirectLogin = useCallback(async () => {
    try {
      setLoading(true)
      const authData = await authService.adminDirectLogin()
      
      setUser(authData.user)
      setAuthenticated(true)
      
      return authData
    } catch (error) {
      console.error('Admin direct login failed:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }, [setUser, setAuthenticated, setLoading])

  return adminDirectLogin
}