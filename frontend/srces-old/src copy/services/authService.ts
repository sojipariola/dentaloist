import { setTokens, clearTokens, getAccessToken } from './token'
import { User } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000'

export async function login(credentials: { email: string; password: string }): Promise<User> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  })

  if (!res.ok) throw new Error('Login failed')

  const data = await res.json()
  setTokens(data.access_token, data.refresh_token)
  return data.user
}

export function logout() {
  clearTokens()
}

export function getCurrentUser(): User | null {
  const token = getAccessToken()
  if (!token) return null
  // You may decode JWT here to extract user info
  return { id: '1', name: 'Demo User', email: 'demo@example.com' }
}
