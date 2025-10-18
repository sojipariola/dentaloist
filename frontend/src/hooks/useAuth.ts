'use client'
import { useState, useEffect, useCallback } from 'react'
import { User } from '@/types/auth'
import { AuthService } from '@/services/api'

export default function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    AuthService.currentUser()
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const loggedInUser = await AuthService.login(email, password)
    setUser(loggedInUser)
    return loggedInUser
  }, [])

  const logout = useCallback(async () => {
    await AuthService.logout()
    setUser(null)
  }, [])

  return { user, loading, login, logout, isLoggedIn: !!user }
}
