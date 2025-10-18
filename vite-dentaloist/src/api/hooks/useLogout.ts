// src/api/hooks/useLogout.ts (Enhanced version)
import { useCallback } from 'react'
import { useAuthStore } from '@/app/store'
import { authService } from '../services/auth.service'

interface UseLogoutOptions {
  redirectTo?: string
  onSuccess?: () => void
  onError?: (error: Error) => void
}

export const useLogout = (options: UseLogoutOptions = {}) => {
  const { redirectTo = '/login', onSuccess, onError } = options
  const logoutFromStore = useAuthStore((state) => state.logout)

  const logout = useCallback(async () => {
    try {
      await authService.logout()
      logoutFromStore()
      
      // Call success callback if provided
      onSuccess?.()
      
      // Redirect if specified
      if (redirectTo) {
        window.location.href = redirectTo
      }
    } catch (error) {
      console.error('Logout failed:', error)
      
      // Call error callback if provided
      onError?.(error as Error)
      
      // Even if API call fails, clear local state
      logoutFromStore()
      
      // Still redirect even on error
      if (redirectTo) {
        window.location.href = redirectTo
      }
    }
  }, [logoutFromStore, redirectTo, onSuccess, onError])

  return logout
}