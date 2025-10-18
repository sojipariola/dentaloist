// src/api/hooks/session.ts
import { useQuery } from '@tanstack/react-query'
import { authService } from '../services'

export const useSessionCheck = () => {
  return useQuery({
    queryKey: ['session'],
    queryFn: () => authService.checkSession(),
    retry: false,
    staleTime: 5 * 60 * 1000,
  })
}