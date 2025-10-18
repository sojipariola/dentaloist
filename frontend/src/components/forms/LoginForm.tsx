'use client'
import { useState } from 'react'
import { useAuth } from '@/hooks/useAuth'

export default function LoginForm() {
  const { login } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await login({ email, password })
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto space-y-4">
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        className="w-full px-4 py-2 border rounded-lg"
      />
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
        className="w-full px-4 py-2 border rounded-lg"
      />
      <button type="submit" className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg">
        Login
      </button>
    </form>
  )
}
