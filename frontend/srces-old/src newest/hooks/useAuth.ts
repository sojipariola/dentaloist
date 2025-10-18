'use client'

import { useState, useEffect, useCallback } from 'react'

interface User {
  id: string
  name: string
  email: string
  role?: string
}

interface UseAuthReturn {
  user: User | null
  isLoggedIn: boolean
  login: (userData: User) => void
  logout: () => void
}

const AUTH_STORAGE_KEY = 'dentaloist_user'

export default function useAuth(): UseAuthReturn {
  const [user, setUser] = useState<User | null>(null)

  // 🔄 Restore user from localStorage on mount
  useEffect(() => {
    const storedUser = localStorage.getItem(AUTH_STORAGE_KEY)
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (err) {
        console.error('Failed to parse stored user:', err)
        localStorage.removeItem(AUTH_STORAGE_KEY)
      }
    }
  }, [])

  // ✅ Login and persist to localStorage
  const login = useCallback((userData: User) => {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(userData))
    setUser(userData)
  }, [])

  // ✅ Logout and clear localStorage
  const logout = useCallback(() => {
    localStorage.removeItem(AUTH_STORAGE_KEY)
    setUser(null)
  }, [])

  return {
    user,
    isLoggedIn: Boolean(user),
    login,
    logout,
  }
}
