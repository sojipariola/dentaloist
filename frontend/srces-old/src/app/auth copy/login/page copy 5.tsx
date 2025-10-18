// frontend/src/app/auth/login/page.tsx
'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

type FormType = 'login' | 'register'

export default function AuthPage() {
  const router = useRouter()
  const { login, register, googleLogin, isAuthenticated } = useAuth()
  const [formType, setFormType] = useState<FormType>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmPassword, setConfirmPassword] = useState('')
  const [clinicName, setClinicName] = useState('')
  const [role, setRole] = useState('VISITOR') // or ORG_ADMIN, etc.

  if (isAuthenticated) {
    router.push('/dashboard')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      if (formType === 'login') {
        await login({ email, password })
      } else {
        await register({
          email,
          password,
          confirmPassword: confirmPassword || password,
          first_name: firstName,
          last_name: lastName,
          organization_id: undefined,
          clinic_name: clinicName,
          role: role as any,
        })
      }
      router.push('/dashboard')
    } catch (err: any) {
      setError(err?.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleDemoLogin = async () => {
    setLoading(true)
    setError(null)
    try {
      await login({ email: 'demo@example.com', password: 'password123' })
      router.push('/dashboard')
    } catch (err: any) {
      setError(err?.message || 'Demo login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white shadow-xl rounded-xl p-10 w-full max-w-md">
        <h1 className="text-3xl font-bold text-center mb-6">
          {formType === 'login' ? 'Login' : 'Register'}
        </h1>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          {formType === 'register' && (
            <>
              <input
                type="text"
                placeholder="First Name"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
                required
              />
              <input
                type="text"
                placeholder="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
                required
              />
            </>
          )}
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-lg"
            required
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            {loading ? 'Please wait...' : formType === 'login' ? 'Login' : 'Register'}
          </button>
        </form>

        <button
          type="button"
          onClick={googleLogin}
          className="w-full mt-4 py-3 border border-gray-300 rounded-lg flex justify-center items-center hover:bg-gray-100 transition"
        >
          <span className="mr-2">🔗</span> Continue with Google
        </button>

        <button
          type="button"
          onClick={handleDemoLogin}
          className="w-full mt-4 py-3 bg-gray-200 rounded-lg hover:bg-gray-300 transition"
        >
          Demo Login
        </button>

        <p className="mt-6 text-center text-gray-600">
          {formType === 'login' ? "Don't have an account?" : 'Already have an account?'}
          <button
            type="button"
            onClick={() => setFormType(formType === 'login' ? 'register' : 'login')}
            className="ml-1 text-blue-600 font-semibold hover:underline"
          >
            {formType === 'login' ? 'Register' : 'Login'}
          </button>
        </p>
      </div>
    </div>
  )
}
