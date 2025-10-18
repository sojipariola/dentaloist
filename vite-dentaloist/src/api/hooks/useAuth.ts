// src/api/hooks/useAuth.ts
import { useState, useEffect, useCallback } from 'react'
import { authService, type BaseUser } from '@/api/services/auth.service'

// Define a proper error interface
interface AuthError {
  message: string
  status?: number
  code?: string
  timestamp?: Date
}

// Helper function to create AuthError from unknown error
const createAuthError = (err: unknown): AuthError => {
  if (err instanceof Error) {
    return {
      message: err.message,
      timestamp: new Date()
    }
  }
  
  return {
    message: 'An unexpected error occurred',
    timestamp: new Date()
  }
}

export const useAuth = () => {
  const [user, setUser] = useState<BaseUser | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<AuthError | null>(null)

  // Initialize auth state from storage
  useEffect(() => {
    const storedUser = authService.getStoredUser()
    if (storedUser) {
      setUser(storedUser)
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const authData = await authService.login({ email, password })
      setUser(authData.user)
      return authData
    } catch (err: unknown) {
      const authError = createAuthError(err)
      setError(authError)
      throw authError
    } finally {
      setLoading(false)
    }
  }, [])

  const logout = useCallback(async () => {
    setLoading(true)
    try {
      await authService.logout()
      setUser(null)
      setError(null) // Clear error on successful logout
    } catch (err: unknown) {
      const authError = createAuthError(err)
      setError(authError)
    } finally {
      setLoading(false)
    }
  }, [])

  const refreshUser = useCallback(async () => {
    try {
      const freshUser = await authService.getCurrentUser()
      setUser(freshUser)
      setError(null) // Clear error on success
      return freshUser
    } catch (err: unknown) {
      const authError = createAuthError(err)
      setError(authError)
      throw authError
    }
  }, [])

  const clearError = useCallback(() => {
    setError(null)
  }, [])

  return {
    user,
    loading,
    error,
    login,
    logout,
    refreshUser,
    isAuthenticated: authService.isAuthenticated(),
    clearError
  }
}