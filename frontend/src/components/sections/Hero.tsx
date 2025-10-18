'use client'

import Link from 'next/link'
import { useAuthContext } from '@/context/AuthContext'

export default function Hero() {
  const { isLoggedIn } = useAuthContext()

  return (
    <section className="container mx-auto px-6 py-20 flex flex-col md:flex-row items-center">
      <div className="md:w-1/2">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
          Modern Dental Practice
          <span className="text-blue-600 block">Management Simplified</span>
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Streamline your appointments, patient records, billing, and analytics —
          all in one secure platform.
        </p>
        <div className="flex space-x-4">
          {isLoggedIn ? (
            <Link href="/dashboard" className="bg-blue-600 text-white px-8 py-4 rounded-lg shadow hover:bg-blue-700 transition">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link href="/signup" className="bg-blue-600 text-white px-8 py-4 rounded-lg shadow hover:bg-blue-700 transition">
                Start Free Trial
              </Link>
              <Link href="#demo" className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition">
                Watch Demo
              </Link>
            </>
          )}
        </div>
      </div>
      <div className="md:w-1/2 mt-12 md:mt-0 flex justify-center">
        <img src="/dental-dashboard.png" alt="Dentaloist Demo" className="rounded-xl shadow-xl" />
      </div>
    </section>
  )
}
