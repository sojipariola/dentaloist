// src/api/hooks/useCurrentUser.ts
import { useState, useEffect } from 'react'
import { authService, type BaseUser } from '../services/auth.service'

export const useCurrentUser = () => {
  const [user, setUser] = useState<BaseUser | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadCurrentUser = async () => {
      try {
        setLoading(true)
        
        // First check if we have a stored user
        const storedUser = authService.getStoredUser()
        if (storedUser) {
          setUser(storedUser)
        }

        // Then try to fetch fresh user data from API
        if (authService.isAuthenticated()) {
          const freshUser = await authService.getCurrentUser()
          setUser(freshUser)
        }
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Failed to load user'
        setError(errorMessage)
        console.error('Error loading current user:', err)
      } finally {
        setLoading(false)
      }
    }

    loadCurrentUser()
  }, [])

  const refreshUser = async () => {
    try {
      if (authService.isAuthenticated()) {
        const freshUser = await authService.getCurrentUser()
        setUser(freshUser)
        return freshUser
      }
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to refresh user'
      setError(errorMessage)
      throw err
    }
  }

  return {
    user,
    loading,
    error,
    refreshUser,
    isAuthenticated: authService.isAuthenticated()
  }
}