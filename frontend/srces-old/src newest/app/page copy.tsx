// frontend/src/app/page.tsx (updated)

'use client'
import Link from 'next/link'
import { useEffect, useState } from 'react'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  
  // Simulate login status (in a real app, this would come from authentication context)
  useEffect(() => {
    // Check if user is logged in (this is just a simulation)
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

  useEffect(() => {
    // Smooth scrolling for anchor links
    const handleAnchorClick = (e: Event) => {
      const target = e.target as HTMLAnchorElement
      if (target.hash && target.pathname === window.location.pathname) {
        e.preventDefault()
        const element = document.querySelector(target.hash)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' })
        }
      }
    }

    const anchors = document.querySelectorAll('a[href^="#"]')
    anchors.forEach(anchor => {
      anchor.addEventListener('click', handleAnchorClick as EventListener)
    })

    return () => {
      anchors.forEach(anchor => {
        anchor.removeEventListener('click', handleAnchorClick as EventListener)
      })
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
                <Link href="/dashboard" className="text-blue-600 hover:text-blue-700 font-medium">
                  Dashboard
                </Link>
                <Link href="/appointments" className="text-blue-600 hover:text-blue-700 font-medium">
                  Appointments
                </Link>
                <Link href="/patients" className="text-blue-600 hover:text-blue-700 font-medium">
                  Patients
                </Link>
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

      {/* Hero Section - Different message for logged in users */}
      <section className="container mx-auto px-6 py-20">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="md:w-1/2 mb-12 md:mb-0">
            {isLoggedIn ? (
              <>
                <h1 className="text-5xl md:text-6xl font-bold text-gray-800 leading-tight mb-6">
                  Welcome Back to
                  <span className="text-blue-600 block">Demo Dental Practice</span>
                </h1>
                <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                  Manage your appointments, patient records, and practice analytics all in one place.
                </p>
                <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                  <Link href="/dashboard" className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg">
                    Go to Dashboard
                  </Link>
                  <Link href="/appointments" className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center font-semibold text-lg">
                    View Appointments
                  </Link>
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
                  patient records, billing, and more. Focus on what matters most - your patients.
                </p>
                <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                  <button 
                    onClick={handleLogin}
                    className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition shadow-lg text-center font-semibold text-lg"
                  >
                    Start Free Trial
                  </button>
                  <a href="#demo" className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition text-center font-semibold text-lg">
                    Watch Demo
                  </a>
                </div>
              </>
            )}
            <div className="mt-8 flex items-center space-x-4">
              <div className="flex -space-x-3">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="w-10 h-10 bg-blue-200 rounded-full border-2 border-white flex items-center justify-center">
                    <span className="text-blue-600 font-semibold">D{i}</span>
                  </div>
                ))}
              </div>
              <p className="text-gray-600">
                <span className="font-semibold text-blue-600">500+</span> dental practices trusted
              </p>
            </div>
          </div>
          <div className="md:w-1/2">
            <div className="relative">
              <div className="absolute -top-6 -left-6 w-64 h-64 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
              <div className="absolute -bottom-6 -right-6 w-48 h-48 bg-indigo-300 rounded-full opacity-20 animate-pulse delay-1000"></div>
              <div className="relative bg-white rounded-2xl shadow-2xl p-8 transform hover:scale-105 transition duration-300">
                <div className="grid grid-cols-2 gap-6">
                  <div className="bg-blue-50 p-4 rounded-xl">
                    <div className="w-12 h-12 bg-blue-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-2xl">📅</span>
                    </div>
                    <h3 className="font-semibold text-gray-800 mb-2">Appointments</h3>
                    <p className="text-sm text-gray-600">Smart scheduling</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-xl">
                    <div className="w-12 h-12 bg-green-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-2xl">👥</span>
                    </div>
                    <h3 className="font-semibold text-gray-800 mb-2">Patients</h3>
                    <p className="text-sm text-gray-600">Digital records</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-xl">
                    <div className="w-12 h-12 bg-purple-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-2xl">💰</span>
                    </div>
                    <h3 className="font-semibold text-gray-800 mb-2">Billing</h3>
                    <p className="text-sm text-gray-600">Easy payments</p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-xl">
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
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="bg-white py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">Everything You Need in One Place</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Designed by dental professionals for dental professionals. Streamline your practice with our comprehensive suite of tools.
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-12">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-8 rounded-xl hover:shadow-xl transition duration-300">
                <div className="w-20 h-20 bg-blue-100 rounded-2xl mx-auto mb-6 flex items-center justify-center">
                  <span className="text-3xl">{feature.icon}</span>
                </div>
                <h3 className="text-2xl font-semibold text-gray-800 mb-4">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="bg-gray-50 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Simple, Transparent Pricing</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Choose the plan that works best for your practice with no hidden fees.
          </p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold mb-4">Starter</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">$99<span className="text-lg text-gray-500">/month</span></div>
              <ul className="text-left space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Up to 500 patients</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Basic scheduling</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Email support</li>
                <li className="flex items-center"><span className="text-gray-400 mr-2">✗</span> Advanced reporting</li>
                <li className="flex items-center"><span className="text-gray-400 mr-2">✗</span> Custom branding</li>
              </ul>
              <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
                Get Started
              </a>
            </div>
            <div className="bg-white rounded-lg shadow-xl p-8 border-2 border-blue-600 transform scale-105">
              <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold absolute top-0 right-6 -translate-y-1/2">
                Most Popular
              </div>
              <h3 className="text-2xl font-bold mb-4">Professional</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">$199<span className="text-lg text-gray-500">/month</span></div>
              <ul className="text-left space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Unlimited patients</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Advanced scheduling</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Priority support</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Comprehensive reporting</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom branding</li>
              </ul>
              <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
                Get Started
              </a>
            </div>
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
              <div className="text-4xl font-bold text-blue-600 mb-6">Custom</div>
              <ul className="text-left space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Multiple locations</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom integrations</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Dedicated account manager</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> White-label options</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> API access</li>
              </ul>
              <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
                Contact Sales
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section id="demo" className="bg-gray-50 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">See Dentaloist in Action</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            {isLoggedIn 
              ? "Explore advanced features and tools available in your dashboard." 
              : "Schedule a personalized demo to see how Dentaloist can transform your dental practice."
            }
          </p>
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
            <div className="aspect-video bg-gray-200 rounded mb-6 flex items-center justify-center">
              <span className="text-gray-500 text-lg">Demo video placeholder</span>
            </div>
            {isLoggedIn ? (
              <>
                <p className="text-gray-600 mb-6">Your account gives you access to all our premium features.</p>
                <Link href="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
                  Explore Features
                </Link>
              </>
            ) : (
              <>
                <p className="text-gray-600 mb-6">Contact us to schedule a demo and see all features in action.</p>
                <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
                  Contact Us for Demo
                </a>
              </>
            )}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="bg-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">About Dentaloist</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Founded by dental professionals, Dentaloist is dedicated to simplifying practice management 
            so you can focus on providing exceptional patient care.
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Our Mission</h3>
              <p className="text-gray-600">To empower dental professionals with intuitive technology.</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🌟</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Our Vision</h3>
              <p className="text-gray-600">Revolutionizing dental practice management worldwide.</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">❤️</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Our Values</h3>
              <p className="text-gray-600">Innovation, reliability, and patient-centered care.</p>
            </div>
          </div>
        </div>
      </section>


      {/* Blog Section */}
      <section id="blog" className="bg-white py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-800 mb-4">From Our Blog</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Stay updated with the latest trends, tips, and news in dental practice management.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">Blog Image</span>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">5 Ways to Streamline Your Dental Practice</h3>
                <p className="text-gray-600 mb-4">Learn how to optimize your workflow and improve patient experience.</p>
                <a href="#blog-post" className="text-blue-600 font-semibold hover:underline">Read more</a>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">Blog Image</span>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">The Future of Digital Dentistry</h3>
                <p className="text-gray-600 mb-4">Exploring emerging technologies that are transforming dental care.</p>
                <a href="#blog-post" className="text-blue-600 font-semibold hover:underline">Read more</a>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">Blog Image</span>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-semibold mb-2">Managing Patient Records Securely</h3>
                <p className="text-gray-600 mb-4">Best practices for maintaining HIPAA compliance in the digital age.</p>
                <a href="#blog-post" className="text-blue-600 font-semibold hover:underline">Read more</a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Careers Section */}
      <section id="careers" className="bg-gray-50 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Join Our Team</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            We're always looking for talented individuals to help us revolutionize dental practice management.
          </p>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-4">Frontend Developer</h3>
              <p className="text-gray-600 mb-6">Help us build beautiful, responsive interfaces for our dental practice management platform.</p>
              <a href="#apply" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
                Apply Now
              </a>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold mb-4">Dental Consultant</h3>
              <p className="text-gray-600 mb-6">Use your dental expertise to help shape our product and guide our development.</p>
              <a href="#apply" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
                Apply Now
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* API Section */}
      <section id="api" className="bg-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Developer API</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Extend Dentaloist's functionality with our powerful API for custom integrations.
          </p>
          <div className="bg-gray-800 text-white rounded-lg p-8 max-w-3xl mx-auto text-left">
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">RESTful API Endpoints</h3>
              <p className="text-gray-300">Access patient data, appointments, and more through our secure API.</p>
            </div>
            <div className="bg-gray-900 p-4 rounded mb-6 overflow-x-auto">
              <code className="text-sm text-green-400">
                {`// Example API request\nfetch('https://api.dentaloist.com/v1/patients', {\n  headers: {\n    'Authorization': 'Bearer YOUR_API_KEY'\n  }\n})`}
              </code>
            </div>
            <a href="#docs" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
              View Documentation
            </a>
          </div>
        </div>
      </section>

      {/* Help Center Section */}
      <section id="help" className="bg-gray-50 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Help Center</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Find answers to common questions and get the support you need.
          </p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">📚</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">Guides & Tutorials</h3>
              <p className="text-gray-600 mb-4">Step-by-step instructions for getting the most out of Dentaloist.</p>
              <a href="#guides" className="text-blue-600 font-semibold hover:underline">Browse guides</a>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">❓</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">FAQs</h3>
              <p className="text-gray-600 mb-4">Answers to frequently asked questions about Dentaloist.</p>
              <a href="#faqs" className="text-blue-600 font-semibold hover:underline">View FAQs</a>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">💬</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">Community Forum</h3>
              <p className="text-gray-600 mb-4">Connect with other Dentaloist users and share tips.</p>
              <a href="#community" className="text-blue-600 font-semibold hover:underline">Join discussion</a>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation Section */}
      <section id="docs" className="bg-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Documentation</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Comprehensive documentation to help you implement and use Dentaloist effectively.
          </p>
          <div className="bg-gray-50 rounded-lg p-8 max-w-3xl mx-auto">
            <div className="grid md:grid-cols-2 gap-6">
              <a href="#getting-started" className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                <h3 className="text-lg font-semibold mb-2">Getting Started</h3>
                <p className="text-gray-600">Set up your account and configure your practice.</p>
              </a>
              <a href="#user-guide" className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                <h3 className="text-lg font-semibold mb-2">User Guide</h3>
                <p className="text-gray-600">Learn how to use all of Dentaloist's features.</p>
              </a>
              <a href="#api-docs" className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                <h3 className="text-lg font-semibold mb-2">API Reference</h3>
                <p className="text-gray-600">Technical documentation for our API.</p>
              </a>
              <a href="#troubleshooting" className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition">
                <h3 className="text-lg font-semibold mb-2">Troubleshooting</h3>
                <p className="text-gray-600">Solutions to common issues and problems.</p>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Community Section */}
      <section id="community" className="bg-gray-50 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">Join Our Community</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Connect with other dental professionals using Dentaloist.
          </p>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">👥</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">User Forum</h3>
              <p className="text-gray-600 mb-4">Share tips, ask questions, and connect with other users.</p>
              <a href="#forum" className="text-blue-600 font-semibold hover:underline">Visit forum</a>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">📅</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">Events & Webinars</h3>
              <p className="text-gray-600 mb-4">Join our live events and training sessions.</p>
              <a href="#events" className="text-blue-600 font-semibold hover:underline">View events</a>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">💡</span>
              </div>
              <h3 className="text-lg font-semibold mb-3">Feature Requests</h3>
              <p className="text-gray-600 mb-4">Suggest and vote on new features for Dentaloist.</p>
              <a href="#feature-requests" className="text-blue-600 font-semibold hover:underline">Make a suggestion</a>
            </div>
          </div>
        </div>
      </section>

      {/* Status Section */}
      <section id="status" className="bg-white py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-gray-800 mb-6">System Status</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Check the current status of Dentaloist services and scheduled maintenance.
          </p>
          <div className="bg-gray-50 rounded-lg p-8 max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-6">
              <span className="text-lg font-semibold">All Systems Operational</span>
              <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Online</span>
            </div>
            <div className="space-y-4 text-left">
              <div className="flex items-center justify-between">
                <span>Web Application</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>API Services</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Database</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Operational</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Payment Processing</span>
                <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Operational</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="bg-blue-600 py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Get In Touch</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Have questions? We'd love to hear from you. Contact our team today.
          </p>
          <div className="grid md:grid-cols-3 gap-8 text-white">
            <div>
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span>📧</span>
              </div>
              <h3 className="font-semibold mb-2">Email</h3>
              <p>info@dentaloist.com</p>
            </div>
            <div>
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span>📞</span>
              </div>
              <h3 className="font-semibold mb-2">Phone</h3>
              <p>+1 (555) 123-4567</p>
            </div>
            <div>
              <div className="w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <span>📍</span>
              </div>
              <h3 className="font-semibold mb-2">Office</h3>
              <p>123 Dental Street<br />City, State 12345</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isLoggedIn && (
        <section className="bg-white py-20">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold text-gray-800 mb-6">Ready to Get Started?</h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join thousands of dental professionals who trust Dentaloist to manage their practice efficiently.
            </p>
            <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
              <button 
                onClick={handleLogin}
                className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg"
              >
                Get Started Free
              </button>
              <a href="#contact" className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg">
                Contact Sales
              </a>
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="font-bold">D</span>
                </div>
                <span className="text-xl font-bold">Dentaloist</span>
              </div>
              <p className="text-gray-400">Modern dental practice management for the digital age.</p>
            </div>
            
            {footerSections.map((section, index) => (
              <div key={index}>
                <h4 className="font-semibold mb-4">{section.title}</h4>
                <ul className="space-y-2">
                  {section.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <a href={link.href} className="text-gray-400 hover:text-white transition">
                        {link.text}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Dentaloist. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

const features = [
  {
    icon: "📅",
    title: "Smart Scheduling",
    description: "Intuitive calendar system with automated reminders and easy rescheduling for patients and staff."
  },
  {
    icon: "📋",
    title: "Patient Management",
    description: "Comprehensive patient records, treatment history, and digital documentation all in one place."
  },
  {
    icon: "💳",
    title: "Integrated Billing",
    description: "Seamless payment processing, insurance claims, and financial reporting made simple."
  },
  {
    icon: "📊",
    title: "Analytics Dashboard",
    description: "Real-time insights into practice performance, patient trends, and financial metrics."
  },
  {
    icon: "🔒",
    title: "Secure & Compliant",
    description: "HIPAA-compliant security with encrypted data storage and regular backups."
  },
  {
    icon: "📱",
    title: "Mobile Ready",
    description: "Access your practice from anywhere with our responsive web and mobile applications."
  }
]

const footerSections = [
  {
    title: "Product",
    links: [
      { href: "#features", text: "Features" },
      { href: "#pricing", text: "Pricing" },
      { href: "#demo", text: "Demo" },
      { href: "#api", text: "API" }
    ]
  },
  {
    title: "Company",
    links: [
      { href: "#about", text: "About" },
      { href: "#blog", text: "Blog" },
      { href: "#careers", text: "Careers" },
      { href: "#contact", text: "Contact" }
    ]
  },
  {
    title: "Support",
    links: [
      { href: "#help", text: "Help Center" },
      { href: "#docs", text: "Documentation" },
      { href: "#community", text: "Community" },
      { href: "#status", text: "Status" }
    ]
  }
]