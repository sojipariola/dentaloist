'use client'
import Link from 'next/link'
import useAuth from '@/hooks/useAuth'

export default function Hero() {
  const { user, isLoggedIn, login, logout } = useAuth()

  // Mock user data for demo login
  const mockUser = {
    id: '1',
    name: 'Soji',
    email: 'soji@example.com',
    role: 'Dentist',
  }

  return (
    <section className="container mx-auto px-6 py-20">
      <div className="flex flex-col md:flex-row items-center justify-between">
        <div className="md:w-1/2 mb-12 md:mb-0">
          {isLoggedIn ? (
            <>
              <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
                Welcome Back, {user?.name} 👋 as {user?.role}
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
                <Link
                  href="/appointments"
                  className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center font-semibold text-lg"
                >
                  View Appointments
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
                  onClick={() => login(mockUser)} // 🔑 updated to use login(user)
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
              <div className="bg-blue-50 p-4 rounded-xl text-center">
                <div className="w-12 h-12 bg-blue-600 rounded-lg mb-3 flex items-center justify-center">
                  <span className="text-white text-2xl">📅</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Appointments</h3>
                <p className="text-sm text-gray-600">Smart scheduling</p>
              </div>
              <div className="bg-green-50 p-4 rounded-xl text-center">
                <div className="w-12 h-12 bg-green-600 rounded-lg mb-3 flex items-center justify-center">
                  <span className="text-white text-2xl">👥</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Patients</h3>
                <p className="text-sm text-gray-600">Digital records</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-xl text-center">
                <div className="w-12 h-12 bg-purple-600 rounded-lg mb-3 flex items-center justify-center">
                  <span className="text-white text-2xl">💰</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Billing</h3>
                <p className="text-sm text-gray-600">Easy payments</p>
              </div>
              <div className="bg-orange-50 p-4 rounded-xl text-center">
                <div className="w-12 h-12 bg-orange-600 rounded-lg mb-3 flex items-center justify-center">
                  <span className="text-white text-2xl">📊</span>
                </div>
                <h3 className="font-semibold text-gray-800 mb-2">Reports</h3>
                <p className="text-sm text-gray-600">Live analytics</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
