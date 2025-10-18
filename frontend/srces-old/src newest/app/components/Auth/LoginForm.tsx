// frontend/src/app/components/Auth/LoginForm.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { UserRole } from '@/lib/api'

interface LoginFormProps {
  onLogin: (email: string, password: string) => Promise<boolean>
  onSuccess?: () => void
  onCancel?: () => void
  showRegisterLink?: boolean
}

interface RegisterFormData {
  email: string
  password: string
  confirmPassword: string
  first_name: string
  last_name: string
  clinic_name: string
  role: UserRole
}

export default function LoginForm({ 
  onLogin, 
  onSuccess, 
  onCancel, 
  showRegisterLink = true 
}: LoginFormProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [isRegistering, setIsRegistering] = useState(false)
  const [registerData, setRegisterData] = useState<RegisterFormData>({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    clinic_name: '',
    role: UserRole.DENTIST
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    const success = await onLogin(email, password)
    
    if (success) {
      onSuccess?.()
    } else {
      setError('Invalid email or password')
    }
    
    setIsLoading(false)
  }

  const handleRegisterChange = (field: keyof RegisterFormData, value: string) => {
    setRegisterData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')

    // Validation
    if (registerData.password !== registerData.confirmPassword) {
      setError('Passwords do not match')
      setIsLoading(false)
      return
    }

    if (registerData.password.length < 6) {
      setError('Password must be at least 6 characters long')
      setIsLoading(false)
      return
    }

    try {
      // In a real implementation, you would call your API client here
      // For now, we'll simulate registration by calling the login function
      const success = await onLogin(registerData.email, registerData.password)
      
      if (success) {
        onSuccess?.()
      } else {
        setError('Registration failed. Please try again.')
      }
    } catch (err) {
      setError('An error occurred during registration')
    }
    
    setIsLoading(false)
  }

  const demoLogin = async (role: UserRole) => {
    setIsLoading(true)
    setError('')
    
    let demoEmail = ''
    let demoPassword = 'password' // Same password for all demo accounts

    switch (role) {
      case UserRole.DENTIST:
        demoEmail = 'dentist@demo.com'
        break
      case UserRole.ASSISTANT:
        demoEmail = 'assistant@demo.com'
        break
      case UserRole.ORG_ADMIN:
        demoEmail = 'admin@demo.com'
        break
      case UserRole.BILLING_STAFF:
        demoEmail = 'billing@demo.com'
        break
      default:
        demoEmail = 'demo@dentaloist.com'
    }

    setEmail(demoEmail)
    setPassword(demoPassword)
    
    const success = await onLogin(demoEmail, demoPassword)
    
    if (success) {
      onSuccess?.()
    } else {
      setError('Demo login failed. Please try again.')
    }
    
    setIsLoading(false)
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full max-h-[90vh] overflow-y-auto">
        {isRegistering ? (
          // Registration Form
          <>
            <h2 className="text-2xl font-bold mb-6 text-center">Create Your Account</h2>
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}
            
            <form onSubmit={handleRegister}>
              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label htmlFor="first_name" className="block text-gray-700 mb-2">
                    First Name *
                  </label>
                  <input
                    id="first_name"
                    type="text"
                    value={registerData.first_name}
                    onChange={(e) => handleRegisterChange('first_name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="last_name" className="block text-gray-700 mb-2">
                    Last Name *
                  </label>
                  <input
                    id="last_name"
                    type="text"
                    value={registerData.last_name}
                    onChange={(e) => handleRegisterChange('last_name', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>

              <div className="mb-4">
                <label htmlFor="clinic_name" className="block text-gray-700 mb-2">
                  Clinic Name *
                </label>
                <input
                  id="clinic_name"
                  type="text"
                  value={registerData.clinic_name}
                  onChange={(e) => handleRegisterChange('clinic_name', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="register-email" className="block text-gray-700 mb-2">
                  Email *
                </label>
                <input
                  id="register-email"
                  type="email"
                  value={registerData.email}
                  onChange={(e) => handleRegisterChange('email', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="mb-4">
                <label htmlFor="role" className="block text-gray-700 mb-2">
                  Role *
                </label>
                <select
                  id="role"
                  value={registerData.role}
                  onChange={(e) => handleRegisterChange('role', e.target.value as UserRole)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  <option value={UserRole.DENTIST}>Dentist</option>
                  <option value={UserRole.ASSISTANT}>Dental Assistant</option>
                  <option value={UserRole.ORG_ADMIN}>Practice Administrator</option>
                  <option value={UserRole.BILLING_STAFF}>Billing Staff</option>
                </select>
              </div>

              <div className="mb-4">
                <label htmlFor="register-password" className="block text-gray-700 mb-2">
                  Password *
                </label>
                <input
                  id="register-password"
                  type="password"
                  value={registerData.password}
                  onChange={(e) => handleRegisterChange('password', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                  minLength={6}
                />
              </div>

              <div className="mb-6">
                <label htmlFor="confirm-password" className="block text-gray-700 mb-2">
                  Confirm Password *
                </label>
                <input
                  id="confirm-password"
                  type="password"
                  value={registerData.confirmPassword}
                  onChange={(e) => handleRegisterChange('confirmPassword', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>

              <div className="flex space-x-4">
                <button
                  type="button"
                  onClick={() => setIsRegistering(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition"
                  disabled={isLoading}
                >
                  Back to Login
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
                  disabled={isLoading}
                >
                  {isLoading ? 'Creating Account...' : 'Create Account'}
                </button>
              </div>
            </form>
          </>
        ) : (
          // Login Form
          <>
            <h2 className="text-2xl font-bold mb-6 text-center">Login to Dentaloist</h2>
            
            {error && (
              <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                {error}
              </div>
            )}
            
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="email" className="block text-gray-700 mb-2">
                  Email
                </label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div className="mb-6">
                <label htmlFor="password" className="block text-gray-700 mb-2">
                  Password
                </label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div className="flex space-x-4 mb-4">
                <button
                  type="button"
                  onClick={onCancel}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400 transition"
                  disabled={isLoading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition disabled:opacity-50"
                  disabled={isLoading}
                >
                  {isLoading ? 'Logging in...' : 'Login'}
                </button>
              </div>

              {showRegisterLink && (
                <div className="text-center mb-6">
                  <button
                    type="button"
                    onClick={() => setIsRegistering(true)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    Don't have an account? Register here
                  </button>
                </div>
              )}
            </form>

            {/* Demo Login Section */}
            <div className="border-t border-gray-200 pt-4">
              <h3 className="text-sm font-semibold text-gray-600 mb-3 text-center">Demo Accounts</h3>
              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={() => demoLogin(UserRole.DENTIST)}
                  disabled={isLoading}
                  className="bg-green-100 text-green-800 py-2 px-3 rounded text-sm hover:bg-green-200 transition disabled:opacity-50"
                >
                  Dentist Demo
                </button>
                <button
                  onClick={() => demoLogin(UserRole.ASSISTANT)}
                  disabled={isLoading}
                  className="bg-blue-100 text-blue-800 py-2 px-3 rounded text-sm hover:bg-blue-200 transition disabled:opacity-50"
                >
                  Assistant Demo
                </button>
                <button
                  onClick={() => demoLogin(UserRole.ORG_ADMIN)}
                  disabled={isLoading}
                  className="bg-purple-100 text-purple-800 py-2 px-3 rounded text-sm hover:bg-purple-200 transition disabled:opacity-50"
                >
                  Admin Demo
                </button>
                <button
                  onClick={() => demoLogin(UserRole.BILLING_STAFF)}
                  disabled={isLoading}
                  className="bg-orange-100 text-orange-800 py-2 px-3 rounded text-sm hover:bg-orange-200 transition disabled:opacity-50"
                >
                  Billing Demo
                </button>
              </div>
            </div>

            <p className="mt-6 text-center text-gray-600 text-sm">
              For demo purposes, use any of the demo accounts above with password: <strong>password</strong>
            </p>
          </>
        )}

        {/* Terms and Privacy */}
        {isRegistering && (
          <p className="mt-4 text-center text-gray-500 text-xs">
            By registering, you agree to our{' '}
            <Link href="/terms" className="text-blue-600 hover:underline">
              Terms of Service
            </Link>{' '}
            and{' '}
            <Link href="/privacy" className="text-blue-600 hover:underline">
              Privacy Policy
            </Link>
          </p>
        )}
      </div>
    </div>
  )
}