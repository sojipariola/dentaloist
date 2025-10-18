'use client'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export default function Hero() {
  const { isLoggedIn, logout } = useAuth()

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="text-center">
        {isLoggedIn ? (
          <>
            <h1 className="text-5xl font-bold mb-6">Welcome Back!</h1>
            <p className="mb-6">Manage patients, appointments, and reports.</p>
            <Link href="/dashboard" className="px-6 py-3 bg-blue-600 text-white rounded-lg">
              Go to Dashboard
            </Link>
            <button
              onClick={logout}
              className="ml-4 px-6 py-3 border border-blue-600 text-blue-600 rounded-lg"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <h1 className="text-5xl font-bold mb-6">Dental Practice Management</h1>
            <p className="mb-6">All-in-one solution for appointments, billing, and patients.</p>
            <Link href="/login" className="px-6 py-3 bg-blue-600 text-white rounded-lg">
              Start Free Trial
            </Link>
          </>
        )}
      </div>
    </section>
  )
}
