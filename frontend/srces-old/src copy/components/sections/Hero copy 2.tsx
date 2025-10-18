'use client'
import Link from 'next/link'
import { useAuthContext } from '@/context/AuthContext'

export default function Hero() {
  const { isLoggedIn, login } = useAuthContext()

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="text-center">
        {isLoggedIn ? (
          <>
            <h1 className="text-5xl font-bold text-gray-800">
              Welcome back 👋
            </h1>
            <Link href="/dashboard" className="mt-6 inline-block bg-blue-600 text-white px-6 py-3 rounded-lg">
              Go to Dashboard
            </Link>
          </>
        ) : (
          <>
            <h1 className="text-5xl font-bold text-gray-800">
              Modern Dental Practice <span className="text-blue-600">Simplified</span>
            </h1>
            <button
              onClick={() => login('demo@demo.com', 'password')}
              className="mt-6 bg-blue-600 text-white px-6 py-3 rounded-lg"
            >
              Start Free Trial
            </button>
          </>
        )}
      </div>
    </section>
  )
}
