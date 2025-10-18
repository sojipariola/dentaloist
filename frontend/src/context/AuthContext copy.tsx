'use client'

import { createContext, ReactNode, useContext, useEffect, useState } from 'react'
import * as authService from '@/services/authService'
import { User } from '@/types'

interface AuthContextType {
  user: User | null
  isLoggedIn: boolean
  login: (credentials: { email: string; password: string }) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const currentUser = authService.getCurrentUser()
    if (currentUser) setUser(currentUser)
  }, [])

  const login = async (credentials: { email: string; password: string }) => {
    const user = await authService.login(credentials)
    setUser(user)
  }

  const logout = () => {
    authService.logout()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, isLoggedIn: !!user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuthContext must be inside AuthProvider')
  return ctx
}
