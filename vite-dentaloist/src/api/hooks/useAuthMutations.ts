// src/api/hooks/useAuthMutations.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuthStore } from '@/app/store'
import { authService, type LoginCredentials, type AuthResponse } from '../services/auth.service'

export const useLogin = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)
  const queryClient = useQueryClient()

  return useMutation<AuthResponse, Error, LoginCredentials>({
    mutationFn: (credentials) => authService.login(credentials),
    onSuccess: (data) => {
      // Store tokens in localStorage
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('session_token', data.session_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      localStorage.setItem('tenant_id', data.user.organization_id)

      // Update auth store
      setUser(data.user)
      setAuthenticated(true)

      // Invalidate any relevant queries
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
    onError: (error) => {
      console.error('Login mutation error:', error)
      // Clear any partial auth data on error
      authService.clearAuthData()
    }
  })
}

export const useAdminDirectLogin = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)
  const queryClient = useQueryClient()

  return useMutation<AuthResponse, Error>({
    mutationFn: () => authService.adminDirectLogin(),
    onSuccess: (data) => {
      // Store tokens in localStorage
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('session_token', data.session_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      localStorage.setItem('tenant_id', data.user.organization_id)

      // Update auth store
      setUser(data.user)
      setAuthenticated(true)

      // Invalidate any relevant queries
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
    onError: (error) => {
      console.error('Admin direct login mutation error:', error)
      // Clear any partial auth data on error
      authService.clearAuthData()
    }
  })
}

export const useLogoutMutation = () => {
  const logoutFromStore = useAuthStore((state) => state.logout)
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      // Clear all queries from cache
      queryClient.clear()
      
      // Redirect to login page
      window.location.href = '/login'
    },
    onError: (error) => {
      console.error('Logout mutation error:', error)
      // Still clear local state even if API call fails
      logoutFromStore()
      window.location.href = '/login'
    }
  })
}
// src/api/hooks/useAuthMutations.ts - Add this to your existing file
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useAuthStore } from '@/app/store'
import { authService, type RegisterData, type AuthResponse } from '../services/auth.service'

// Add this to your existing useAuthMutations.ts file
export const useRegister = () => {
  const setUser = useAuthStore((state) => state.setUser)
  const setAuthenticated = useAuthStore((state) => state.setAuthenticated)
  const queryClient = useQueryClient()

  return useMutation<AuthResponse, Error, RegisterData>({
    mutationFn: (registerData) => authService.register(registerData),
    onSuccess: (data) => {
      // Store tokens in localStorage
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('session_token', data.session_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      localStorage.setItem('tenant_id', data.user.organization_id)

      // Update auth store
      setUser(data.user)
      setAuthenticated(true)

      // Invalidate any relevant queries
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
    onError: (error) => {
      console.error('Registration mutation error:', error)
      // Clear any partial auth data on error
      authService.clearAuthData()
    }
  })
}