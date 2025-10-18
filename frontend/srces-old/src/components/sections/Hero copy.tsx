'use client'
import Link from 'next/link'
import { useAuth } from '@/./hooks/useAuth'

export default function Hero() {
  const { user, isAuthenticated, login, logout } = useAuth()

  // Prepare mock credentials if needed
  const mockCredentials = {
    email: 'soji@example.com',
    password: 'password123',
  }

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="flex flex-col md:flex-row items-center justify-between">
        <div className="md:w-1/2 mb-12 md:mb-0">
          {isAuthenticated ? (
            <>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
                Welcome Back, {user?.email} {/* Use email or whatever property exists */}
                <span className="text-blue-600 block">Demo2 Dental Practice</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Manage your appointments, patient records, and practice analytics all in one place.
              </p>
              <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <Link
                  href="/dashboard"
                  className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg"
                >
                  Go to Dashboard
                </Link>
                <button
                  onClick={logout}
                  className="bg-red-500 text-white px-8 py-4 rounded-lg hover:bg-red-600 transition shadow-lg text-center font-semibold text-lg"
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
                Modern Dental Practice
                <span className="text-blue-600 block">Management Simplified</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Streamline your dental practice with our all-in-one solution for appointments, 
                patient records, billing, and more.
              </p>
              <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <button 
                  onClick={() => login(mockCredentials)} // Send proper credentials
                  className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg"
                >
                  Start Free Trial
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </section>
  )
}
