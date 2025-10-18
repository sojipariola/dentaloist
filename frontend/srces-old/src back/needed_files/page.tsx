'use client'
import Link from 'next/link'
import { useEffect, useState } from 'react'

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  
  // Simulate login status
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
    setMobileMenuOpen(false)
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
          // Update URL
          window.history.pushState(null, '', target.hash)
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
    <div className="min-h-screen bg-white font-sans">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">D</span>
              </div>
              <span className="text-xl font-medium text-gray-800">Dentaloist</span>
            </div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:flex space-x-8">
              <a href="#features" className="text-gray-600 hover:text-blue-600 transition py-2">Features</a>
              <a href="#pricing" className="text-gray-600 hover:text-blue-600 transition py-2">Pricing</a>
              <a href="#about" className="text-gray-600 hover:text-blue-600 transition py-2">About</a>
              <a href="#contact" className="text-gray-600 hover:text-blue-600 transition py-2">Contact</a>
            </div>
            
            <div className="hidden md:flex space-x-4 items-center">
              {isLoggedIn ? (
                <>
                  <Link href="/dashboard" className="text-gray-600 hover:text-blue-600 px-3 py-2">
                    Dashboard
                  </Link>
                  <button 
                    onClick={handleLogout}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition text-sm font-medium"
                  >
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <button 
                    onClick={handleLogin}
                    className="text-gray-600 hover:text-blue-600 px-3 py-2 font-medium"
                  >
                    Sign in
                  </button>
                  <button 
                    onClick={handleLogin}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition text-sm font-medium"
                  >
                    Get Started
                  </button>
                </>
              )}
            </div>
            
            {/* Mobile menu button */}
            <button 
              className="md:hidden p-2 rounded-md text-gray-600 hover:text-blue-600"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
          
          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden mt-4 py-4 border-t border-gray-200">
              <div className="flex flex-col space-y-4">
                <a href="#features" className="text-gray-600 hover:text-blue-600 py-2" onClick={() => setMobileMenuOpen(false)}>Features</a>
                <a href="#pricing" className="text-gray-600 hover:text-blue-600 py-2" onClick={() => setMobileMenuOpen(false)}>Pricing</a>
                <a href="#about" className="text-gray-600 hover:text-blue-600 py-2" onClick={() => setMobileMenuOpen(false)}>About</a>
                <a href="#contact" className="text-gray-600 hover:text-blue-600 py-2" onClick={() => setMobileMenuOpen(false)}>Contact</a>
                
                {isLoggedIn ? (
                  <>
                    <Link href="/dashboard" className="text-gray-600 hover:text-blue-600 py-2" onClick={() => setMobileMenuOpen(false)}>
                      Dashboard
                    </Link>
                    <button 
                      onClick={() => {
                        handleLogout();
                        setMobileMenuOpen(false);
                      }}
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition text-sm font-medium text-left"
                    >
                      Logout
                    </button>
                  </>
                ) : (
                  <>
                    <button 
                      onClick={() => {
                        handleLogin();
                        setMobileMenuOpen(false);
                      }}
                      className="text-gray-600 hover:text-blue-600 py-2 text-left font-medium"
                    >
                      Sign in
                    </button>
                    <button 
                      onClick={() => {
                        handleLogin();
                        setMobileMenuOpen(false);
                      }}
                      className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition text-sm font-medium text-left"
                    >
                      Get Started
                    </button>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-16 md:py-24 bg-gradient-to-b from-blue-50 to-white">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="md:w-1/2 mb-12 md:mb-0">
              {isLoggedIn ? (
                <>
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
                    Welcome Back to
                    <span className="text-blue-600 block">Demo Dental Practice</span>
                  </h1>
                  <p className="text-lg text-gray-600 mb-8 leading-relaxed max-w-lg">
                    Manage your appointments, patient records, and practice analytics all in one place.
                  </p>
                  <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                    <Link href="/dashboard" className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition shadow-sm text-center font-medium">
                      Go to Dashboard
                    </Link>
                    <Link href="/appointments" className="border border-gray-300 text-gray-700 px-6 py-3 rounded-md hover:bg-gray-50 transition text-center font-medium">
                      View Appointments
                    </Link>
                  </div>
                </>
              ) : (
                <>
                  <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
                    Modern Dental Practice
                    <span className="text-blue-600 block">Management Simplified</span>
                  </h1>
                  <p className="text-lg text-gray-600 mb-8 leading-relaxed max-w-lg">
                    Streamline your dental practice with our all-in-one solution for appointments, 
                    patient records, billing, and more. Focus on what matters most - your patients.
                  </p>
                  <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                    <button 
                      onClick={handleLogin}
                      className="bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition shadow-sm text-center font-medium"
                    >
                      Start Free Trial
                    </button>
                    <a href="#demo" className="border border-gray-300 text-gray-700 px-6 py-3 rounded-md hover:bg-gray-50 transition text-center font-medium">
                      Watch Demo
                    </a>
                  </div>
                </>
              )}
              <div className="mt-10 flex items-center">
                <div className="flex -space-x-2">
                  {[1, 2, 3, 4].map((i) => (
                    <div key={i} className="w-10 h-10 bg-blue-100 rounded-full border-2 border-white flex items-center justify-center">
                      <span className="text-blue-600 text-sm font-medium">D{i}</span>
                    </div>
                  ))}
                </div>
                <p className="ml-4 text-gray-600 text-sm">
                  <span className="font-semibold text-blue-600">500+</span> dental practices trusted
                </p>
              </div>
            </div>
            <div className="md:w-1/2">
              <div className="bg-white rounded-xl shadow-lg p-6 max-w-md mx-auto">
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-blue-50 p-4 rounded-lg">
                    <div className="w-10 h-10 bg-blue-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-xl">📅</span>
                    </div>
                    <h3 className="font-medium text-gray-800 mb-1 text-sm">Appointments</h3>
                    <p className="text-xs text-gray-600">Smart scheduling</p>
                  </div>
                  <div className="bg-green-50 p-4 rounded-lg">
                    <div className="w-10 h-10 bg-green-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-xl">👥</span>
                    </div>
                    <h3 className="font-medium text-gray-800 mb-1 text-sm">Patients</h3>
                    <p className="text-xs text-gray-600">Digital records</p>
                  </div>
                  <div className="bg-purple-50 p-4 rounded-lg">
                    <div className="w-10 h-10 bg-purple-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-xl">💰</span>
                    </div>
                    <h3 className="font-medium text-gray-800 mb-1 text-sm">Billing</h3>
                    <p className="text-xs text-gray-600">Easy payments</p>
                  </div>
                  <div className="bg-orange-50 p-4 rounded-lg">
                    <div className="w-10 h-10 bg-orange-600 rounded-lg mb-3 flex items-center justify-center">
                      <span className="text-white text-xl">📊</span>
                    </div>
                    <h3 className="font-medium text-gray-800 mb-1 text-sm">Reports</h3>
                    <p className="text-xs text-gray-600">Live analytics</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Everything You Need in One Place</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Designed by dental professionals for dental professionals. Streamline your practice with our comprehensive suite of tools.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="p-6 rounded-lg hover:shadow-md transition duration-300 border border-gray-100">
                <div className="w-14 h-14 bg-blue-100 rounded-lg mb-5 flex items-center justify-center">
                  <span className="text-2xl">{feature.icon}</span>
                </div>
                <h3 className="text-xl font-medium text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Choose the plan that works best for your practice with no hidden fees.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
              <h3 className="text-xl font-bold mb-4">Starter</h3>
              <div className="text-3xl font-bold text-gray-900 mb-6">$99<span className="text-base text-gray-500">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Up to 500 patients</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Basic scheduling</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Email support</li>
                <li className="flex items-center"><span className="text-gray-300 mr-2">✗</span> Advanced reporting</li>
                <li className="flex items-center"><span className="text-gray-300 mr-2">✗</span> Custom branding</li>
              </ul>
              <a href="#contact" className="block w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition text-center font-medium">
                Get Started
              </a>
            </div>
            <div className="bg-white rounded-lg shadow-md p-8 border-2 border-blue-600 relative">
              <div className="absolute top-0 right-0 bg-blue-600 text-white px-3 py-1 text-sm font-medium rounded-bl-lg">
                Most Popular
              </div>
              <h3 className="text-xl font-bold mb-4">Professional</h3>
              <div className="text-3xl font-bold text-gray-900 mb-6">$199<span className="text-base text-gray-500">/month</span></div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Unlimited patients</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Advanced scheduling</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Priority support</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Comprehensive reporting</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom branding</li>
              </ul>
              <a href="#contact" className="block w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition text-center font-medium">
                Get Started
              </a>
            </div>
            <div className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
              <h3 className="text-xl font-bold mb-4">Enterprise</h3>
              <div className="text-3xl font-bold text-gray-900 mb-6">Custom</div>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Multiple locations</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom integrations</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Dedicated account manager</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> White-label options</li>
                <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> API access</li>
              </ul>
              <a href="#contact" className="block w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition text-center font-medium">
                Contact Sales
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Additional sections would follow the same clean, minimal design pattern */}
      {/* For brevity, I'll include just one more section to demonstrate the pattern */}

      {/* Contact Section */}
      <section id="contact" className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Get In Touch</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Have questions? We'd love to hear from you. Contact our team today.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="text-center p-6">
              <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">📧</span>
              </div>
              <h3 className="font-medium text-gray-900 mb-2">Email</h3>
              <p className="text-gray-600">info@dentaloist.com</p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">📞</span>
              </div>
              <h3 className="font-medium text-gray-900 mb-2">Phone</h3>
              <p className="text-gray-600">+1 (555) 123-4567</p>
            </div>
            <div className="text-center p-6">
              <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-xl">📍</span>
              </div>
              <h3 className="font-medium text-gray-900 mb-2">Office</h3>
              <p className="text-gray-600">123 Dental Street<br />City, State 12345</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      {!isLoggedIn && (
        <section className="py-16 bg-blue-600">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl font-bold text-white mb-4">Ready to Get Started?</h2>
            <p className="text-lg text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of dental professionals who trust Dentaloist to manage their practice efficiently.
            </p>
            <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
              <button 
                onClick={handleLogin}
                className="bg-white text-blue-600 px-6 py-3 rounded-md hover:bg-blue-50 transition font-medium"
              >
                Get Started Free
              </button>
              <a href="#contact" className="bg-transparent border border-white text-white px-6 py-3 rounded-md hover:bg-white/10 transition font-medium">
                Contact Sales
              </a>
            </div>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="font-bold text-white">D</span>
                </div>
                <span className="text-lg font-medium">Dentaloist</span>
              </div>
              <p className="text-gray-400 text-sm">Modern dental practice management for the digital age.</p>
            </div>
            
            {footerSections.map((section, index) => (
              <div key={index}>
                <h4 className="font-medium mb-4 text-white">{section.title}</h4>
                <ul className="space-y-2">
                  {section.links.map((link, linkIndex) => (
                    <li key={linkIndex}>
                      <a href={link.href} className="text-gray-400 hover:text-white transition text-sm">
                        {link.text}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
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