// src/api/hooks/auth.ts
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { authService } from '../services'
import { LoginCredentials } from '@/types/api/auth.types'

export const useLogin = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => authService.login(credentials),
    onSuccess: (data) => {
      // Tokens are now stored in the component, but we can also store them here as backup
      localStorage.setItem('access_token', data.token)
      localStorage.setItem('refresh_token', data.refresh_token)
      
      // Invalidate any existing user queries
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
  })
}

export const useAdminDirectLogin = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: () => authService.adminDirectLogin(),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.token)
      localStorage.setItem('refresh_token', data.refresh_token)
      queryClient.invalidateQueries({ queryKey: ['currentUser'] })
    },
  })
}