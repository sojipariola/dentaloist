'use client'
import Link from 'next/link'
import { useState } from 'react'

export default function FeaturesPage() {
  const [activeCategory, setActiveCategory] = useState('all')

  const categories = [
    { id: 'all', name: 'All Features' },
    { id: 'practice', name: 'Practice Management' },
    { id: 'patient', name: 'Patient Care' },
    { id: 'billing', name: 'Billing & Payments' },
    { id: 'reporting', name: 'Reporting & Analytics' }
  ]

  const features = [
    {
      id: 1,
      title: 'Smart Appointment Scheduling',
      description: 'Intuitive calendar system with automated reminders and easy rescheduling for patients and staff.',
      category: 'practice',
      icon: '📅',
      status: 'live',
      link: '/features/scheduling'
    },
    {
      id: 2,
      title: 'Patient Records Management',
      description: 'Comprehensive digital patient records with treatment history, notes, and documentation.',
      category: 'patient',
      icon: '📋',
      status: 'live',
      link: '/features/patient-records'
    },
    {
      id: 3,
      title: 'Integrated Billing System',
      description: 'Seamless payment processing, insurance claims, and financial reporting made simple.',
      category: 'billing',
      icon: '💳',
      status: 'live',
      link: '/features/billing'
    },
    {
      id: 4,
      title: 'Analytics Dashboard',
      description: 'Real-time insights into practice performance, patient trends, and financial metrics.',
      category: 'reporting',
      icon: '📊',
      status: 'live',
      link: '/features/analytics'
    },
    {
      id: 5,
      title: 'HIPAA Compliant Security',
      description: 'Enterprise-grade security with encrypted data storage and regular backups.',
      category: 'practice',
      icon: '🔒',
      status: 'live',
      link: '/features/security'
    },
    {
      id: 6,
      title: 'Mobile Application',
      description: 'Access your practice from anywhere with our responsive web and mobile applications.',
      category: 'practice',
      icon: '📱',
      status: 'live',
      link: '/features/mobile'
    },
    {
      id: 7,
      title: 'Treatment Planning',
      description: 'Create detailed treatment plans with cost estimates and track progress through completion.',
      category: 'patient',
      icon: '🦷',
      status: 'live',
      link: '/features/treatment-planning'
    },
    {
      id: 8,
      title: 'Automated Reminders',
      description: 'Reduce no-shows with automated appointment reminders via SMS and email.',
      category: 'practice',
      icon: '⏰',
      status: 'live',
      link: '/features/reminders'
    },
    {
      id: 9,
      title: 'Insurance Claims Processing',
      description: 'Streamline insurance claims with automated verification and submission.',
      category: 'billing',
      icon: '🏥',
      status: 'live',
      link: '/features/insurance'
    },
    {
      id: 10,
      title: 'Custom Reporting',
      description: 'Generate custom reports tailored to your practice\'s specific needs and metrics.',
      category: 'reporting',
      icon: '📈',
      status: 'live',
      link: '/features/reporting'
    },
    {
      id: 11,
      title: 'Telehealth Integration',
      description: 'Conduct virtual consultations with integrated telehealth capabilities.',
      category: 'patient',
      icon: '👨‍⚕️',
      status: 'beta',
      link: '/features/telehealth'
    },
    {
      id: 12,
      title: 'Inventory Management',
      description: 'Track dental supplies and equipment with automated reordering alerts.',
      category: 'practice',
      icon: '📦',
      status: 'coming-soon',
      link: '/features/inventory'
    }
  ]

  const filteredFeatures = activeCategory === 'all' 
    ? features 
    : features.filter(feature => feature.category === activeCategory)

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-xl">D</span>
              </div>
              <span className="text-2xl font-bold text-gray-800">Dentaloist</span>
            </Link>
            <nav className="hidden md:flex space-x-8">
              <Link href="/features" className="text-blue-600 font-medium">Features</Link>
              <Link href="/pricing" className="text-gray-600 hover:text-blue-600 transition">Pricing</Link>
              <Link href="/about" className="text-gray-600 hover:text-blue-600 transition">About</Link>
              <Link href="/contact" className="text-gray-600 hover:text-blue-600 transition">Contact</Link>
            </nav>
            <div className="flex items-center space-x-4">
              <Link href="/login" className="text-gray-600 hover:text-blue-600 font-medium">Login</Link>
              <Link href="/signup" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition shadow-md">
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Powerful Features for Modern Dental Practices</h1>
          <p className="text-xl max-w-3xl mx-auto mb-8">
            Everything you need to streamline operations, improve patient care, and grow your practice.
          </p>
          <div className="flex justify-center space-x-4">
            <Link href="/demo" className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50 transition">
              Request a Demo
            </Link>
            <Link href="/pricing" className="bg-transparent border border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10 transition">
              View Pricing
            </Link>
          </div>
        </div>
      </section>

      {/* Category Filters */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-4">
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`px-6 py-2 rounded-full transition ${activeCategory === category.id 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                {category.name}
              </button>
            ))}
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredFeatures.map(feature => (
              <div key={feature.id} className="bg-white rounded-xl shadow-md overflow-hidden border border-gray-100 hover:shadow-lg transition">
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">
                      {feature.icon}
                    </div>
                    <span className={`text-xs font-semibold px-2 py-1 rounded-full ${feature.status === 'live' ? 'bg-green-100 text-green-800' : feature.status === 'beta' ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'}`}>
                      {feature.status === 'coming-soon' ? 'Coming Soon' : feature.status}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-gray-800 mb-2">{feature.title}</h3>
                  <p className="text-gray-600 mb-6">{feature.description}</p>
                  <Link href={feature.link} className="text-blue-600 font-semibold hover:text-blue-700 flex items-center">
                    Learn more
                    <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-100">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">500+</div>
              <div className="text-gray-600">Dental Practices</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">1.2M+</div>
              <div className="text-gray-600">Patients Managed</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">98%</div>
              <div className="text-gray-600">Customer Satisfaction</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">24/7</div>
              <div className="text-gray-600">Support Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">What Our Customers Say</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold mr-4">
                  JD
                </div>
                <div>
                  <div className="font-semibold">Dr. John Doe</div>
                  <div className="text-gray-600 text-sm">Owner, Bright Smile Dental</div>
                </div>
              </div>
              <p className="text-gray-600">"Dentaloist has transformed how we manage our practice. The scheduling system alone has reduced no-shows by 30%."</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-green-600 font-bold mr-4">
                  SJ
                </div>
                <div>
                  <div className="font-semibold">Sarah Johnson</div>
                  <div className="text-gray-600 text-sm">Office Manager, Family Dental Care</div>
                </div>
              </div>
              <p className="text-gray-600">"The billing and insurance features have streamlined our processes so much that we're processing claims twice as fast."</p>
            </div>
            <div className="bg-gray-50 p-6 rounded-xl">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold mr-4">
                  MR
                </div>
                <div>
                  <div className="font-semibold">Dr. Maria Rodriguez</div>
                  <div className="text-gray-600 text-sm">Orthodontist, Perfect Smile Ortho</div>
                </div>
              </div>
              <p className="text-gray-600">"The treatment planning tools are exceptional. I can easily show patients their options and track progress throughout treatment."</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-blue-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Transform Your Practice?</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join thousands of dental professionals who trust Dentaloist to manage their practice efficiently.
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link href="/signup" className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition">
              Start Free Trial
            </Link>
            <Link href="/demo" className="bg-transparent border border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition">
              Schedule a Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="container mx-auto px-4">
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
                      <Link href={link.href} className="text-gray-400 hover:text-white transition">
                        {link.text}
                      </Link>
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

const footerSections = [
  {
    title: "Product",
    links: [
      { href: "/features", text: "Features" },
      { href: "/pricing", text: "Pricing" },
      { href: "/demo", text: "Demo" },
      { href: "/api", text: "API" }
    ]
  },
  {
    title: "Company",
    links: [
      { href: "/about", text: "About" },
      { href: "/blog", text: "Blog" },
      { href: "/careers", text: "Careers" },
      { href: "/contact", text: "Contact" }
    ]
  },
  {
    title: "Support",
    links: [
      { href: "/help", text: "Help Center" },
      { href: "/docs", text: "Documentation" },
      { href: "/community", text: "Community" },
      { href: "/status", text: "Status" }
    ]
  }
]