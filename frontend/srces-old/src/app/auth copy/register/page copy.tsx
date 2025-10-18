// frontend/src/app/auth/register/page.tsx
'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function RegisterPage() {
  const router = useRouter()
  const { register, googleLogin, isAuthenticated } = useAuth()

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

  const handleSubmit = async (e: React.FormEvent) => {
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
        <h1 className="text-3xl font-bold text-center mb-6">Register</h1>

        {error && <p className="text-red-500 text-center mb-4">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
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

        <button
          type="button"
          onClick={googleLogin}
          className="w-full mt-4 py-3 border border-gray-300 rounded-lg flex justify-center items-center hover:bg-gray-100 transition"
        >
          <span className="mr-2">🔗</span> Continue with Google
        </button>

        <p className="mt-6 text-center text-gray-600">
          Already have an account?
          <a href="/auth/login" className="ml-1 text-blue-600 font-semibold hover:underline">
            Login
          </a>
        </p>
      </div>
    </div>
  )
}
