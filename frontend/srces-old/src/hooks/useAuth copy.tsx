// frontend/src/hooks/useAuth.ts
'use client'

import React, { createContext, useContext, ReactNode, useState, useEffect, useCallback } from 'react'
import { User, LoginCredentials, RegisterData, UserRole } from '@/types/auth'
import { apiClient } from '@/services/api'

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (credentials: LoginCredentials) => Promise<boolean>
  register: (userData: Omit<RegisterData, 'confirmPassword'>) => Promise<boolean>
  logout: () => void
  clearError: () => void
  checkAuth: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuthContext = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const login = useCallback(async (credentials: LoginCredentials) => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await apiClient.login(credentials)
      if (response.data?.access_token && response.data.user) {
        localStorage.setItem('authToken', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        setUser(response.data.user as User)
        setIsAuthenticated(true)
        return true
      }
      setError(response.error || 'Login failed')
      return false
    } catch (err) {
      setError('Login failed')
      return false
    } finally {
      setIsLoading(false)
    }
  }, [])

  const register = useCallback(async (userData: Omit<RegisterData, 'confirmPassword'>) => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await apiClient.register(userData)
      if (response.data?.access_token && response.data.user) {
        localStorage.setItem('authToken', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        setUser(response.data.user as User)
        setIsAuthenticated(true)
        return true
      }
      setError(response.error || 'Registration failed')
      return false
    } catch (err) {
      setError('Registration failed')
      return false
    } finally {
      setIsLoading(false)
    }
  }, [])

  const logout = useCallback(() => {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem('user')
    localStorage.removeItem('authToken')
  }, [])

  const clearError = useCallback(() => setError(null), [])

  const checkAuth = useCallback(() => {
    const storedUser = localStorage.getItem('user')
    const token = localStorage.getItem('authToken')
    if (storedUser && token) {
      setUser(JSON.parse(storedUser))
      setIsAuthenticated(true)
    } else {
      setUser(null)
      setIsAuthenticated(false)
    }
    setIsLoading(false)
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        error,
        login,
        register,
        logout,
        clearError,
        checkAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  /** ------------------------------
   * Login (real API)
   * ------------------------------ */
  const login = useCallback(async (credentials: LoginCredentials): Promise<boolean> => {
    try {
      setIsLoading(true)
      setError(null)

      const response = await apiClient.login(credentials)

      if (response.data?.access_token && response.data.user) {
        localStorage.setItem('authToken', response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))

        setUser(response.data.user as User)
        setIsAuthenticated(true)
        return true
      } else {
        setError(response.error || 'Login failed')
        return false
      }
    } catch (err) {
      setError('Login failed')
      return false
    } finally {
      setIsLoading(false)
    }
  }, [])

  /** ------------------------------
   * Register (real API)
   * ------------------------------ */
  const register = useCallback(
    async (userData: Omit<RegisterData, 'confirmPassword'>): Promise<boolean> => {
      try {
        setIsLoading(true)
        setError(null)

        const response = await apiClient.register(userData)

        if (response.data?.access_token && response.data.user) {
          localStorage.setItem('authToken', response.data.access_token)
          localStorage.setItem('user', JSON.stringify(response.data.user))

          setUser(response.data.user as User)
          setIsAuthenticated(true)
          return true
        } else {
          setError(response.error || 'Registration failed')
          return false
        }
      } catch (err) {
        setError('Registration failed')
        return false
      } finally {
        setIsLoading(false)
      }
    },
    []
  )

  /** ------------------------------
   * Logout
   * ------------------------------ */
  const logout = useCallback(() => {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem('user')
    localStorage.removeItem('authToken')
  }, [])

  /** ------------------------------
   * Clear error
   * ------------------------------ */
  const clearError = useCallback(() => {
    setError(null)
  }, [])

  /** ------------------------------
   * Check Authentication (on mount)
   * ------------------------------ */
  const checkAuth = useCallback(async () => {
    try {
      setIsLoading(true)
      const storedUser = localStorage.getItem('user')
      const token = localStorage.getItem('authToken')

      if (storedUser && token) {
        const parsedUser: User = JSON.parse(storedUser)
        setUser(parsedUser)
        setIsAuthenticated(true)
      } else {
        setUser(null)
        setIsAuthenticated(false)
      }
    } catch (err) {
      console.error('Failed to check auth:', err)
      setUser(null)
      setIsAuthenticated(false)
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    clearError,
    checkAuth,
  }
}
