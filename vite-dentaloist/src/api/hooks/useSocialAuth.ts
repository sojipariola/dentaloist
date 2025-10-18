// src/api/hooks/useSocialAuth.ts
import { useState, useCallback } from 'react'
import { useAuthStore } from '@/app/store'

interface SocialLoginResponse {
  access_token: string
  refresh_token: string
  user: any
  is_new_user: boolean
}

export const useSocialAuth = () => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { setTokens, setUser } = useAuthStore()

  const socialLogin = useCallback(async (
    provider: 'google' | 'facebook' | 'github',
    data: any
  ): Promise<SocialLoginResponse> => {
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`http://localhost:5000/api/auth/social/${provider}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      const result = await response.json()

      if (!response.ok) {
        throw new Error(result.error || `Social login failed`)
      }

      // Store tokens and user data
      setTokens({
        accessToken: result.access_token,
        refreshToken: result.refresh_token,
      })
      setUser(result.user)

      // Store in localStorage
      localStorage.setItem('access_token', result.access_token)
      localStorage.setItem('refresh_token', result.refresh_token)
      localStorage.setItem('user', JSON.stringify(result.user))

      return result
    } catch (err: any) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [setTokens, setUser])

  const clearError = useCallback(() => setError(null), [])

  return {
    socialLogin,
    loading,
    error,
    clearError,
  }
}