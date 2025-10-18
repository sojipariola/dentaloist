'use client'
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export default function Navbar() {
  const { isLoggedIn } = useAuth()

  return (
    <nav className="flex justify-between items-center px-6 py-4 bg-gray-100 shadow">
      <Link href="/" className="font-bold text-xl text-blue-600">Dentaloist</Link>
      <div className="space-x-6">
        {isLoggedIn ? (
          <Link href="/dashboard" className="text-gray-700 hover:text-blue-600">Dashboard</Link>
        ) : (
          <Link href="/login" className="text-gray-700 hover:text-blue-600">Login</Link>
        )}
      </div>
    </nav>
  )
}
