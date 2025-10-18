'use client'

import Link from 'next/link'
import { useAuthContext } from '@/context/AuthContext'
import dynamic from 'next/dynamic'

const Hero = dynamic(() => import('@/components/sections/Hero'))
const Features = dynamic(() => import('@/components/sections/Features'))
const Pricing = dynamic(() => import('@/components/sections/Pricing'))
const Testimonials = dynamic(() => import('@/components/sections/Testimonials'))
const CTA = dynamic(() => import('@/components/sections/CTA'))
const Footer = dynamic(() => import('@/components/sections/Footer'))

export default function HomePage() {
  const { isLoggedIn, user } = useAuthContext()

  return (
    <main className="flex flex-col min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="w-full bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-blue-600">Dentaloist</Link>
          <nav className="hidden md:flex space-x-6 text-gray-700 font-medium">
            <Link href="#features">Features</Link>
            <Link href="#pricing">Pricing</Link>
            <Link href="#testimonials">Testimonials</Link>
            <Link href="#contact">Contact</Link>
          </nav>
          <div>
            {isLoggedIn ? (
              <Link
                href="/dashboard"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
              >
                Hi, {user?.name || 'User'} 👋
              </Link>
            ) : (
              <Link
                href="/login"
                className="px-6 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700 transition"
              >
                Get Started
              </Link>
            )}
          </div>
        </div>
      </header>

      {/* Sections */}
      <Hero />
      <Features />
      <Pricing />
      <Testimonials />
      <CTA />

      <Footer />
    </main>
  )
}
