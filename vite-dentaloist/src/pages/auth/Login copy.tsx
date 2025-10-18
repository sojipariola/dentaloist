// src/pages/auth/Login.tsx - FIXED VERSION
import React, { useState, useEffect, useCallback } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { 
  Eye, EyeOff, LogIn, Stethoscope, Bug, 
  Github, Facebook, Mail 
} from 'lucide-react'
import { useAuthActions, useAdminDirectLogin } from '@/api/hooks'
import { useSocialAuth } from '@/api/hooks/useSocialAuth'
import { useAuthStore } from '@/app/store'
import { Button, Input, Card } from '@/components/ui'

const loginSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
  password: z.string().min(1, 'Password is required'),
  rememberMe: z.boolean().optional(),
})

type LoginFormData = z.infer<typeof loginSchema>

export default function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const [showPassword, setShowPassword] = useState(false)
  const [isAdminLogin, setIsAdminLogin] = useState(false)

  const from = (location.state as any)?.from?.pathname || '/dashboard'

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  // ✅ Use the hooks that exist
  const { login, loading: authLoading, error: authError } = useAuthActions()
  const adminDirectLogin = useAdminDirectLogin()
  const { socialLogin, loading: socialLoading } = useSocialAuth()

  const isLoading = authLoading || socialLoading

  // Define onSubmit with useCallback to avoid recreation
  const onSubmit = useCallback(async (data: LoginFormData) => {
    console.log('📝 [Login] Form submitted with data:', {
      email: data.email,
      passwordLength: data.password?.length,
      isAdminLogin
    })
    
    try {
      console.log('🔐 [Login] Starting login process...')
      
      if (isAdminLogin) {
        console.log('👨‍💼 [Login] Admin login path')
        await adminDirectLogin()
      } else {
        console.log('👤 [Login] Normal login path - calling login()')
        await login(data.email, data.password)
      }

      console.log('✅ [Login] Login successful, navigating to:', from)
      navigate(from, { replace: true })
    } catch (error: any) {
      console.error('❌ [Login] Login failed:', error)
      setError('root', {
        type: 'manual',
        message: error.message || 'Login failed. Please try again.',
      })
    }
  }, [isAdminLogin, adminDirectLogin, login, navigate, from, setError])

  // Simple social login handlers that work immediately
  const handleGoogleLogin = async () => {
    try {
      console.log('🔐 [Social] Starting Google login...')
      // For now, just show a message since we need to set up OAuth
      setError('root', {
        type: 'manual',
        message: 'Google login coming soon! Check console for details.',
      })
      console.log('ℹ️ [Social] Google OAuth setup required')
    } catch (error: any) {
      console.error('❌ [Social] Google login failed:', error)
      setError('root', {
        type: 'manual',
        message: error.message || 'Google login failed',
      })
    }
  }

  const handleFacebookLogin = async () => {
    try {
      console.log('🔐 [Social] Starting Facebook login...')
      // For now, just show a message since we need to set up OAuth
      setError('root', {
        type: 'manual',
        message: 'Facebook login coming soon! Check console for details.',
      })
      console.log('ℹ️ [Social] Facebook OAuth setup required')
    } catch (error: any) {
      console.error('❌ [Social] Facebook login failed:', error)
      setError('root', {
        type: 'manual',
        message: error.message || 'Facebook login failed',
      })
    }
  }

  const handleGithubLogin = async () => {
    try {
      console.log('🔐 [Social] Starting GitHub login...')
      
      // Simple GitHub OAuth redirect
      const clientId = process.env.REACT_APP_GITHUB_CLIENT_ID || 'your_github_client_id'
      const redirectUri = `${window.location.origin}/auth/github/callback`
      
      const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=user:email`
      
      window.location.href = githubAuthUrl
    } catch (error: any) {
      console.error('❌ [Social] GitHub login failed:', error)
      setError('root', {
        type: 'manual',
        message: error.message || 'GitHub login failed',
      })
    }
  }

  // Test social login with mock data
  const testSocialLogin = async (provider: 'google' | 'facebook' | 'github') => {
    try {
      console.log(`🧪 [Social Test] Testing ${provider} login...`)
      
      // Mock social login data for testing
      const mockData = {
        access_token: `mock_${provider}_token`,
        id_token: `mock_${provider}_id_token`,
      }
      
      const result = await socialLogin(provider, mockData)
      console.log(`✅ [Social Test] ${provider} login successful:`, result)
      
      navigate(from, { replace: true })
    } catch (error: any) {
      console.error(`❌ [Social Test] ${provider} login failed:`, error)
      setError('root', {
        type: 'manual',
        message: `Test ${provider} login failed: ${error.message}`,
      })
    }
  }

  // Manual test functions
  const testNormalLogin = async () => {
    console.log('🧪 [Manual Test] Normal login button clicked')
    try {
      await login('sojipariola@gmail.com', 'Soji1111')
      console.log('✅ [Manual Test] Normal login successful')
    } catch (error) {
      console.error('❌ [Manual Test] Normal login failed:', error)
    }
  }

  const testAdminLogin = async () => {
    console.log('🧪 [Manual Test] Admin login button clicked')
    try {
      await adminDirectLogin()
      console.log('✅ [Manual Test] Admin login successful')
    } catch (error) {
      console.error('❌ [Manual Test] Admin login failed:', error)
    }
  }

  // TEMPORARY DEBUG - REMOVE LATER
  useEffect(() => {
    // Expose test functions to global scope
    (window as any).debugLogin = {
      testNormalLogin: async () => {
        console.log('🧪 [Debug] Testing normal login...')
        try {
          const result = await login('sojipariola@gmail.com', 'Soji1111')
          console.log('✅ [Debug] Normal login successful:', result)
          return result
        } catch (error) {
          console.error('❌ [Debug] Normal login failed:', error)
          throw error
        }
      },
      
      testAdminLogin: async () => {
        console.log('🧪 [Debug] Testing admin login...')
        try {
          const result = await adminDirectLogin()
          console.log('✅ [Debug] Admin login successful:', result)
          return result
        } catch (error) {
          console.error('❌ [Debug] Admin login failed:', error)
          throw error
        }
      },
      
      testDirectFetch: async () => {
        console.log('🧪 [Debug] Testing direct fetch...')
        try {
          const response = await fetch('http://localhost:5000/api/auth/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
              email: 'sojipariola@gmail.com',
              password: 'Soji1111'
            })
          })
          console.log('📡 [Debug] Fetch status:', response.status)
          const data = await response.json()
          console.log('✅ [Debug] Direct fetch successful:', data)
          return data
        } catch (error) {
          console.error('❌ [Debug] Direct fetch failed:', error)
          throw error
        }
      },
      
      checkAuthState: () => {
        console.log('🔍 [Debug] Current auth state:')
        console.log('   - authLoading:', authLoading)
        console.log('   - authError:', authError)
        console.log('   - isAdminLogin:', isAdminLogin)
        console.log('   - adminDirectLogin type:', typeof adminDirectLogin)
        
        // Check localStorage
        console.log('💾 [Debug] localStorage:')
        console.log('   - access_token:', localStorage.getItem('access_token') ? '✅ Present' : '❌ Missing')
        console.log('   - user:', localStorage.getItem('user') ? '✅ Present' : '❌ Missing')
      },
      
      clearAuth: () => {
        console.log('🧹 [Debug] Clearing auth data...')
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('session_token')
        localStorage.removeItem('user')
        localStorage.removeItem('tenant_id')
        console.log('✅ [Debug] Auth data cleared')
      },
      
      testFormSubmission: () => {
        console.log('🧪 [Debug] Testing form submission...')
        handleSubmit(onSubmit)()
      }
    }
    
    console.log('🔧 [Debug] Login component mounted - debug functions available:')
    console.log('   - debugLogin.testNormalLogin()')
    console.log('   - debugLogin.testAdminLogin()') 
    console.log('   - debugLogin.testDirectFetch()')
    console.log('   - debugLogin.checkAuthState()')
    console.log('   - debugLogin.clearAuth()')
    console.log('   - debugLogin.testFormSubmission()')
    
    // Cleanup on unmount
    return () => {
      delete (window as any).debugLogin
    }
  }, [login, adminDirectLogin, authLoading, authError, isAdminLogin, handleSubmit, onSubmit])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="flex justify-center items-center space-x-2 mb-6">
            <Stethoscope className="h-8 w-8 text-primary-600" />
            <span className="text-2xl font-bold text-gray-900">Dentaloist</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Or{' '}
            <Link
              to="/register"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              create a new account
            </Link>
          </p>
        </div>

        <Card className="p-8">
          {/* Debug Panel - TEMPORARY */}
          <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
            <div className="flex items-center space-x-2 mb-2">
              <Bug className="h-4 w-4 text-yellow-600" />
              <span className="text-sm font-medium text-yellow-800">Debug Mode</span>
            </div>
            <p className="text-xs text-yellow-700 mb-3">
              Type commands in console or use buttons below
            </p>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={testNormalLogin}
                className="bg-green-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-green-600 transition-colors"
              >
                Test Normal
              </button>
              <button
                onClick={testAdminLogin}
                className="bg-purple-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-purple-600 transition-colors"
              >
                Test Admin
              </button>
              <button
                onClick={() => (window as any).debugLogin?.testDirectFetch()}
                className="bg-blue-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-blue-600 transition-colors"
              >
                Test Fetch
              </button>
              <button
                onClick={() => (window as any).debugLogin?.clearAuth()}
                className="bg-red-500 text-white py-2 px-3 rounded text-xs font-medium hover:bg-red-600 transition-colors"
              >
                Clear Auth
              </button>
            </div>
          </div>

          {/* Social Login Buttons */}
          <div className="mb-6 space-y-3">
            <Button
              type="button"
              variant="outline"
              size="lg"
              className="w-full flex items-center justify-center space-x-3 bg-white border-gray-300 hover:bg-gray-50"
              onClick={handleGoogleLogin}
              disabled={isLoading}
            >
              <Mail className="h-5 w-5 text-red-500" />
              <span>Continue with Google</span>
            </Button>

            <Button
              type="button"
              variant="outline"
              size="lg"
              className="w-full flex items-center justify-center space-x-3 bg-white border-gray-300 hover:bg-gray-50"
              onClick={handleFacebookLogin}
              disabled={isLoading}
            >
              <Facebook className="h-5 w-5 text-blue-600" />
              <span>Continue with Facebook</span>
            </Button>

            <Button
              type="button"
              variant="outline"
              size="lg"
              className="w-full flex items-center justify-center space-x-3 bg-white border-gray-300 hover:bg-gray-50"
              onClick={handleGithubLogin}
              disabled={isLoading}
            >
              <Github className="h-5 w-5 text-gray-800" />
              <span>Continue with GitHub</span>
            </Button>

            {/* Test Social Login Buttons - Remove in production */}
            <div className="border-t pt-3 mt-3">
              <p className="text-xs text-gray-500 text-center mb-2">Test Social Logins:</p>
              <div className="grid grid-cols-3 gap-2">
                <button
                  onClick={() => testSocialLogin('google')}
                  className="bg-red-500 text-white py-1 px-2 rounded text-xs hover:bg-red-600"
                >
                  Test Google
                </button>
                <button
                  onClick={() => testSocialLogin('facebook')}
                  className="bg-blue-500 text-white py-1 px-2 rounded text-xs hover:bg-blue-600"
                >
                  Test Facebook
                </button>
                <button
                  onClick={() => testSocialLogin('github')}
                  className="bg-gray-700 text-white py-1 px-2 rounded text-xs hover:bg-gray-800"
                >
                  Test GitHub
                </button>
              </div>
            </div>
          </div>

          {/* Divider */}
          <div className="relative mb-6">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-300" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-gray-500">Or continue with</span>
            </div>
          </div>

          {/* Admin Login Toggle */}
          <div className="mb-6">
            <button
              type="button"
              onClick={() => setIsAdminLogin(!isAdminLogin)}
              className="w-full flex items-center justify-center space-x-2 py-2 px-4 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <LogIn className="h-4 w-4" />
              <span className="text-sm font-medium">
                {isAdminLogin ? 'Switch to User Login' : 'Admin Direct Login'}
              </span>
            </button>
            {isAdminLogin && (
              <p className="mt-2 text-xs text-gray-500 text-center">
                Admin login bypasses credentials for development
              </p>
            )}
          </div>

          <form className="space-y-6" onSubmit={handleSubmit(onSubmit)}>
            {!isAdminLogin && (
              <>
                <Input
                  label="Email address"
                  type="email"
                  autoComplete="email"
                  error={errors.email?.message}
                  {...register('email')}
                />

                <div className="relative">
                  <Input
                    label="Password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    error={errors.password?.message}
                    {...register('password')}
                  />
                  <button
                    type="button"
                    className="absolute inset-y-0 right-0 pr-3 flex items-center mt-6"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4 text-gray-400" />
                    ) : (
                      <Eye className="h-4 w-4 text-gray-400" />
                    )}
                  </button>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <input
                      id="remember-me"
                      type="checkbox"
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                      {...register('rememberMe')}
                    />
                    <label
                      htmlFor="remember-me"
                      className="ml-2 block text-sm text-gray-900"
                    >
                      Remember me
                    </label>
                  </div>

                  <Link
                    to="/forgot-password"
                    className="text-sm font-medium text-primary-600 hover:text-primary-500"
                  >
                    Forgot password?
                  </Link>
                </div>
              </>
            )}

            {errors.root && (
              <div className="rounded-md bg-red-50 p-4">
                <div className="text-sm text-red-700">{errors.root.message}</div>
              </div>
            )}

            <Button
              type="submit"
              variant="primary"
              size="lg"
              loading={isLoading}
              className="w-full"
            >
              {isAdminLogin ? 'Admin Login' : 'Sign in'}
            </Button>
          </form>

          {/* Demo Credentials */}
          {!isAdminLogin && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-xs text-gray-600 text-center">
                <strong>Demo Credentials:</strong><br />
                Email: sojipariola@gmail.com<br />
                Password: Soji1111
              </p>
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}