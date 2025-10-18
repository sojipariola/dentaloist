// frontend/src/app/auth/page.tsx
'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function AuthPage() {
  const router = useRouter()
  const { login, register, googleLogin, isAuthenticated } = useAuth()

  const [tab, setTab] = useState<'login' | 'register'>('login')

  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [confirmPassword, setConfirmPassword] = useState('')
  const [clinicName, setClinicName] = useState('')
  const [role, setRole] = useState('VISITOR') // or ORG_ADMIN, etc.

  if (isAuthenticated) {
    router.push('/dashboard')
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      await login({ email, password })
      router.push('/dashboard')
    } catch (err: any) {
      setError(err?.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
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
      router.push('/dashboard')
    } catch (err: any) {
      setError(err?.message || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="bg-white shadow-xl rounded-xl p-10 w-full max-w-md">
        {/* Tabs */}
        <div className="flex mb-6 border-b border-gray-200">
          <button
            className={`flex-1 py-2 font-semibold ${tab === 'login' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            onClick={() => setTab('login')}
          >
            Login
          </button>
          <button
            className={`flex-1 py-2 font-semibold ${tab === 'register' ? 'border-b-2 border-blue-600 text-blue-600' : 'text-gray-500'}`}
            onClick={() => setTab('register')}
          >
            Register
          </button>
        </div>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        {tab === 'login' ? (
          <form onSubmit={handleLogin} className="space-y-4">
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
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
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
              {loading ? 'Registering...' : 'Register'}
            </button>
          </form>
        )}

        {/* Google Login */}
        <button
          type="button"
          onClick={googleLogin}
          className="w-full mt-4 py-3 border border-gray-300 rounded-lg flex justify-center items-center hover:bg-gray-100 transition"
        >
          <span className="mr-2">🔗</span> Continue with Google
        </button>
      </div>
    </div>
  )
}
