// src/app/store/auth.store.ts

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authService, type BaseUser } from '@/api/services/auth.service'

interface AuthState {
  user: BaseUser | null
  isAuthenticated: boolean
  isLoading: boolean
  setUser: (user: BaseUser | null) => void
  setAuthenticated: (authenticated: boolean) => void
  setLoading: (loading: boolean) => void
  logout: () => void
  initializeAuth: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: true,

      setUser: (user) => set({ user }),

      setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),

      setLoading: (isLoading) => set({ isLoading }),

      logout: () => {
        authService.logout()
        set({ user: null, isAuthenticated: false })
      },

      initializeAuth: async () => {
        const { setUser, setAuthenticated, setLoading } = get()
        
        try {
          setLoading(true)
          
          // Check if we have tokens in localStorage
          if (authService.isAuthenticated()) {
            try {
              // Try to get fresh user data
              const user = await authService.getCurrentUser()
              setUser(user)
              setAuthenticated(true)
            } catch (error) {
              console.error('Failed to get current user:', error)
              // Token might be invalid, clear auth
              authService.clearAuthData()
              setUser(null)
              setAuthenticated(false)
            }
          } else {
            setUser(null)
            setAuthenticated(false)
          }
        } catch (error) {
          console.error('Auth initialization error:', error)
          setUser(null)
          setAuthenticated(false)
        } finally {
          setLoading(false)
        }
      }
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        user: state.user,
        isAuthenticated: state.isAuthenticated 
      })
    }
  )
)