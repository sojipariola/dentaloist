// src/pages/auth/GithubCallback.tsx
import React, { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useSocialAuth } from '@/api/hooks'

export default function GithubCallback() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { socialLogin } = useSocialAuth()

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code')
      const error = searchParams.get('error')

      if (error) {
        console.error('GitHub OAuth error:', error)
        navigate('/login?error=github_auth_failed')
        return
      }

      if (code) {
        try {
          await socialLogin('github', { code })
          navigate('/dashboard', { replace: true })
        } catch (err) {
          console.error('GitHub login failed:', err)
          navigate('/login?error=github_login_failed')
        }
      } else {
        navigate('/login')
      }
    }

    handleCallback()
  }, [searchParams, socialLogin, navigate])

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Completing GitHub login...</p>
      </div>
    </div>
  )
}