'use client'

import React, { createContext, useContext, ReactNode } from 'react'
import useAuth from '@/hooks/useAuth'

interface AuthContextType {
  user: any
  isLoggedIn: boolean
  login: (userData: any) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const { user, isLoggedIn, login, logout } = useAuth()

  return (
    <AuthContext.Provider value={{ user, isLoggedIn, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}
