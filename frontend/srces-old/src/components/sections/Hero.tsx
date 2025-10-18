//  frontend/src/components/sections/Hero.tsx
'use client'

import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'

export default function Hero() {
  const router = useRouter()
  const { user, isAuthenticated, login, logout } = useAuth()

  // Mock credentials for demo login
  const mockCredentials = {
    email: 'demo@example.com',
    password: 'password123',
  }

  // Demo login for "Start Free Trial" 
  const handleDemoLogin = async () => {
    const result = await login(mockCredentials)
    // If login returns void, just redirect after calling login
    router.push('/dashboard')
  }

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="flex flex-col md:flex-row items-center justify-between">
        {/* Left Side: Text & Actions */}
        <div className="md:w-1/2 mb-12 md:mb-0">
          {isAuthenticated ? (
            <>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
                Welcome Back, {user?.first_name || user?.email}
                <span className="text-blue-600 block">{user?.role ? `Role: ${user.role}` : 'Demo2 Dental Practice'}</span>
              </h1>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Manage your appointments, patient records, billing, and analytics all in one place.
              </p>
              <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <Link
                  href="/dashboard"
                  className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg"
                >
                  Dashboard
                </Link>
                <Link
                  href="/appointments"
                  className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center font-semibold text-lg"
                >
                  Appointments
                </Link>
                <Link
                  href="/patients"
                  className="border border-green-600 text-green-600 px-8 py-4 rounded-lg hover:bg-green-50 transition text-center font-semibold text-lg"
                >
                  Patients
                </Link>
                <Link
                  href="/billing"
                  className="border border-purple-600 text-purple-600 px-8 py-4 rounded-lg hover:bg-purple-50 transition text-center font-semibold text-lg"
                >
                  Billing
                </Link>
                <Link
                  href="/reports"
                  className="border border-orange-600 text-orange-600 px-8 py-4 rounded-lg hover:bg-orange-50 transition text-center font-semibold text-lg"
                >
                  Reports
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
                Streamline your practice with appointments, patient records, billing, and analytics.
              </p>
              <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <button
                  onClick={handleDemoLogin}
                  className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg"
                >
                  Start Free Trial
                </button>
                <a
                  href="#demo"
                  className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center font-semibold text-lg"
                >
                  Watch Demo
                </a>
                <Link
                  href="/auth/login"
                  className="text-blue-600 px-8 py-4 rounded-lg hover:text-blue-800 transition text-center font-semibold text-lg"
                >
                  Login
                </Link>
                <Link
                  href="/auth/register"
                  className="text-green-600 px-8 py-4 rounded-lg hover:text-green-800 transition text-center font-semibold text-lg"
                >
                  Get Started
                </Link>
              </div>
            </>
          )}
        </div>

        {/* Right Side: Feature Cards */}
        <div className="md:w-1/2 relative">
          <div className="absolute -top-6 -left-6 w-64 h-64 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-6 -right-6 w-48 h-48 bg-indigo-300 rounded-full opacity-20 animate-pulse delay-1000"></div>
          <div className="relative bg-white rounded-2xl shadow-2xl p-8 transform hover:scale-105 transition duration-300">
            <div className="grid grid-cols-2 gap-6">
              {[
                { title: 'Appointments', icon: '📅', link: '/appointments', bg: 'blue' },
                { title: 'Patients', icon: '👥', link: '/patients', bg: 'green' },
                { title: 'Billing', icon: '💰', link: '/billing', bg: 'purple' },
                { title: 'Reports', icon: '📊', link: '/reports', bg: 'orange' },
              ].map((card) => (
                <Link
                  key={card.title}
                  href={isAuthenticated ? card.link : '/auth/login'}
                  className={`bg-${card.bg}-50 p-4 rounded-xl text-center hover:shadow-md transition`}
                >
                  <div className={`w-12 h-12 bg-${card.bg}-600 rounded-lg mb-3 flex items-center justify-center`}>
                    <span className="text-white text-2xl">{card.icon}</span>
                  </div>
                  <h3 className="font-semibold text-gray-800 mb-2">{card.title}</h3>
                  <p className="text-sm text-gray-600">
                    {card.title === 'Appointments' && 'Smart scheduling'}
                    {card.title === 'Patients' && 'Digital records'}
                    {card.title === 'Billing' && 'Easy payments'}
                    {card.title === 'Reports' && 'Live analytics'}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
