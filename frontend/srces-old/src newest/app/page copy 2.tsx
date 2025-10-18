'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import dynamic from 'next/dynamic'

// --- Define prop types for sections ---
type HeroProps = {
  isLoggedIn: boolean
  onLogin: () => void
}

type DemoProps = {
  isLoggedIn: boolean
}

type CTAProps = {
  onAction: () => void
}

// --- Dynamic imports with props typing ---
const Hero = dynamic<HeroProps>(() => import('./components/sections/Hero'), { ssr: false })
const Features = dynamic(() => import('./components/sections/Features'), { ssr: false })
const Pricing = dynamic(() => import('./components/sections/Pricing'), { ssr: false })
const Demo = dynamic<DemoProps>(() => import('./components/sections/Demo'), { ssr: false })
const About = dynamic(() => import('./components/sections/About'), { ssr: false })
const Blog = dynamic(() => import('./components/sections/Blog'), { ssr: false })
const Careers = dynamic(() => import('./components/sections/Careers'), { ssr: false })
const API = dynamic(() => import('./components/sections/API'), { ssr: false })
const Help = dynamic(() => import('./components/sections/Help'), { ssr: false })
const Documentation = dynamic(() => import('./components/sections/Documentation'), { ssr: false })
const Community = dynamic(() => import('./components/sections/Community'), { ssr: false })
const Status = dynamic(() => import('./components/sections/Status'), { ssr: false })
const Contact = dynamic(() => import('./components/sections/Contact'), { ssr: false })
const CTA = dynamic<CTAProps>(() => import('./components/sections/CTA'), { ssr: false })
const Footer = dynamic(() => import('./components/sections/Footer'), { ssr: false })

/**
// Sections
import Hero from '@/components/sections/Hero'
import Features from '@/components/sections/Features'
import Pricing from '@/components/sections/Pricing'
import Demo from '@/components/sections/Demo'
import About from '@/components/sections/About'
import Blog from '@/components/sections/Blog'
import Careers from '@/components/sections/Careers'
import API from '@/components/sections/API'
import Help from '@/components/sections/Help'
import Documentation from '@/components/sections/Documentation'
import Community from '@/components/sections/Community'
import Status from '@/components/sections/Status'
import Contact from '@/components/sections/Contact'
import CTA from '@/components/sections/CTA'
import Footer from '@/components/sections/Footer'
 */


export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  // Check login status on load
  useEffect(() => {
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true'
    setIsLoggedIn(loggedIn)
  }, [])

  const handleLogout = () => {
    localStorage.setItem('isLoggedIn', 'false')
    setIsLoggedIn(false)
  }

  const handleLogin = () => {
    localStorage.setItem('isLoggedIn', 'true')
    setIsLoggedIn(true)
  }

  // Smooth scrolling for anchor links
  useEffect(() => {
    const handleAnchorClick = (e: Event) => {
      const target = e.target as HTMLAnchorElement
      if (target.hash && target.pathname === window.location.pathname) {
        e.preventDefault()
        const element = document.querySelector(target.hash)
        if (element) element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const anchors = document.querySelectorAll('a[href^="#"]')
    anchors.forEach(a => a.addEventListener('click', handleAnchorClick as EventListener))

    return () => {
      anchors.forEach(a => a.removeEventListener('click', handleAnchorClick as EventListener))
    }
  }, [])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">

      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">D</span>
            </div>
            <span className="text-2xl font-bold text-gray-800">Dentaloist</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-600 hover:text-blue-600 transition">Features</a>
            <a href="#about" className="text-gray-600 hover:text-blue-600 transition">About</a>
            <a href="#contact" className="text-gray-600 hover:text-blue-600 transition">Contact</a>
          </div>
          <div className="flex space-x-4">
            {isLoggedIn ? (
              <>
                <Link href="/dashboard" className="text-blue-600 hover:text-blue-700 font-medium">Dashboard</Link>
                <Link href="/appointments" className="text-blue-600 hover:text-blue-700 font-medium">Appointments</Link>
                <Link href="/patients" className="text-blue-600 hover:text-blue-700 font-medium">Patients</Link>
                <button 
                  onClick={handleLogout}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition shadow-md"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button 
                  onClick={handleLogin}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Login
                </button>
                <button 
                  onClick={handleLogin}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition shadow-md"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Sections */}
      <Hero isLoggedIn={isLoggedIn} onLogin={handleLogin} />
      <Features />
      <Pricing />
      <Demo isLoggedIn={isLoggedIn} />
      <About />
      <Blog />
      <Careers />
      <API />
      <Help />
      <Documentation />
      <Community />
      <Status />
      <Contact />
      {!isLoggedIn && <CTA onAction={handleLogin} />}

      {/* Footer */}
      <Footer />
    </div>
  )
}
