'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth} from '@/hooks/useAuth'
import { LoginCredentials } from '@/types/auth'

export default function LoginPage() {
  const { login, isLoading, error } = useAuth()
  const router = useRouter()

  const [form, setForm] = useState<LoginCredentials>({
    email: '',
    password: '',
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const result = await login(form)
    // If login returns void, just redirect after login completes
    router.push('/dashboard')
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-6">
      <form className="bg-white p-10 rounded-xl shadow-lg w-full max-w-md" onSubmit={handleSubmit}>
        <h1 className="text-3xl font-bold mb-6 text-center">Login</h1>
        {error && <p className="text-red-500 mb-4">{error.message}</p>}

        <input
          name="email"
          type="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-full p-3 mb-3 border rounded"
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full p-3 mb-6 border rounded"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700 transition"
          disabled={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>

        <div className="mt-4 text-center text-gray-600">
          <p>
            Don't have an account? <a href="/register" className="text-blue-600">Get Started</a>
          </p>
          <p className="mt-2">
            Login as <a href="/login?role=dentist" className="text-blue-600">Dentist</a> |{' '}
            <a href="/login?role=receptionist" className="text-blue-600">Receptionist</a> |{' '}
            <a href="/login?role=admin" className="text-blue-600">Admin</a>
          </p>
        </div>
      </form>
    </div>
  )
}
