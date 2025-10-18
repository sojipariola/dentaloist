'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function DashboardPage() {
  const { user, isLoggedIn } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoggedIn) router.push('/login')
  }, [isLoggedIn, router])

  if (!isLoggedIn) return <p>Redirecting to login...</p>

  return (
    <section className="container mx-auto px-6 py-20">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <p>Welcome, {user?.name || 'User'}!</p>
    </section>
  )
}
