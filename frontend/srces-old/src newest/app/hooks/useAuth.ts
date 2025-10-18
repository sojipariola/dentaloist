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

  // Check localStorage for existing user on mount
  useEffect(() => {
    const storedUser = localStorage.getItem(AUTH_STORAGE_KEY)
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const login = useCallback((userData: User) => {
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(userData))
    setUser(userData)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(AUTH_STORAGE_KEY)
    setUser(null)
  }, [])

  const isLoggedIn = Boolean(user)

  return { user, isLoggedIn, login, logout }
}
