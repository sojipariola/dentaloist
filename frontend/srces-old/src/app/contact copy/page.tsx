// app/contact/page.tsx
'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    company: '',
    subject: '',
    message: '',
    department: 'general'
  })

  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState<'idle' | 'success' | 'error'>('idle')

  const departments = [
    { value: 'general', label: 'General Inquiry' },
    { value: 'sales', label: 'Sales' },
    { value: 'support', label: 'Technical Support' },
    { value: 'billing', label: 'Billing' },
    { value: 'partnership', label: 'Partnership' },
    { value: 'careers', label: 'Careers' }
  ]

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus('idle')

    // Simulate form submission
    try {
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      // Randomly simulate success or error for demonstration
      const isSuccess = Math.random() > 0.3
      
      if (isSuccess) {
        setSubmitStatus('success')
        setFormData({
          firstName: '',
          lastName: '',
          email: '',
          phone: '',
          company: '',
          subject: '',
          message: '',
          department: 'general'
        })
      } else {
        throw new Error('Submission failed')
      }
    } catch (error) {
      setSubmitStatus('error')
    } finally {
      setIsSubmitting(false)
    }
  }

  const contactMethods = [
    {
      icon: '📧',
      title: 'Email',
      details: 'info@dentaloist.com',
      description: 'Send us an email anytime'
    },
    {
      icon: '📞',
      title: 'Phone',
      details: '+1 (555) 123-4567',
      description: 'Mon-Fri from 8am to 6pm PST'
    },
    {
      icon: '📍',
      title: 'Office',
      details: '123 Dental Street, Suite 100',
      description: 'San Francisco, CA 94102'
    },
    {
      icon: '💬',
      title: 'Live Chat',
      details: 'Available 24/7',
      description: 'Click the chat icon to start'
    }
  ]

  const faqs = [
    {
      question: 'How quickly do you respond to inquiries?',
      answer: 'We typically respond to all inquiries within 1 business day. For urgent matters, please call us directly.'
    },
    {
      question: 'Do you offer demos of your software?',
      answer: 'Yes! We offer personalized demos to show how Dentaloist can transform your practice. Schedule a demo through our contact form.'
    },
    {
      question: 'What support options are available?',
      answer: 'We offer email support, phone support, live chat, and comprehensive documentation for all our customers.'
    },
    {
      question: 'Are you HIPAA compliant?',
      answer: 'Absolutely. Dentaloist is fully HIPAA compliant and we take data security very seriously.'
    }
  ]

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
            <Link href="/#features" className="text-gray-600 hover:text-blue-600 transition">Features</Link>
            <Link href="/pricing" className="text-gray-600 hover:text-blue-600 transition">Pricing</Link>
            <Link href="/blog" className="text-gray-600 hover:text-blue-600 transition">Blog</Link>
            <Link href="/careers" className="text-gray-600 hover:text-blue-600 transition">Careers</Link>
            <Link href="/#about" className="text-gray-600 hover:text-blue-600 transition">About</Link>
          </div>
          <div className="flex space-x-4">
            <Link href="/login" className="text-blue-600 hover:text-blue-700 font-medium">
              Login
            </Link>
            <Link href="/register" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition shadow-md">
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Header */}
      <div className="container mx-auto px-6 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-6">
          Get in Touch
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Have questions? We'd love to hear from you. Send us a message and we'll respond as soon as possible.
        </p>
      </div>

      {/* Contact Methods */}
      <section className="bg-white py-16">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
            {contactMethods.map((method, index) => (
              <div key={index} className="text-center p-6 bg-blue-50 rounded-xl">
                <div className="text-3xl mb-4">{method.icon}</div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">{method.title}</h3>
                <p className="text-gray-700 font-medium mb-2">{method.details}</p>
                <p className="text-gray-600 text-sm">{method.description}</p>
              </div>
            ))}
          </div>

          <div className="grid lg:grid-cols-2 gap-12">
            {/* Contact Form */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Send us a Message</h2>
              
              {submitStatus === 'success' && (
                <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
                  <p>Thank you for your message! We'll get back to you soon.</p>
                </div>
              )}

              {submitStatus === 'error' && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                  <p>There was an error sending your message. Please try again or contact us directly.</p>
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      id="firstName"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    />
                  </div>
                  <div>
                    <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      id="lastName"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    />
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address *
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    />
                  </div>
                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                      Phone Number
                    </label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                    Company / Practice
                  </label>
                  <input
                    type="text"
                    id="company"
                    name="company"
                    value={formData.company}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                  />
                </div>

                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="department" className="block text-sm font-medium text-gray-700 mb-2">
                      Department *
                    </label>
                    <select
                      id="department"
                      name="department"
                      value={formData.department}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    >
                      {departments.map(dept => (
                        <option key={dept.value} value={dept.value}>
                          {dept.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">
                      Subject *
                    </label>
                    <input
                      type="text"
                      id="subject"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                    Message *
                  </label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={5}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none resize-none"
                  ></textarea>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg hover:bg-blue-700 transition font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <div className="flex items-center justify-center">
                      <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Sending...
                    </div>
                  ) : (
                    'Send Message'
                  )}
                </button>
              </form>
            </div>

            {/* Company Info & FAQ */}
            <div>
              <div className="bg-gray-50 rounded-2xl p-8 mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Office Hours</h2>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-gray-700">Monday - Friday</span>
                    <span className="text-gray-600">8:00 AM - 6:00 PM PST</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-700">Saturday</span>
                    <span className="text-gray-600">9:00 AM - 4:00 PM PST</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-700">Sunday</span>
                    <span className="text-gray-600">Emergency Support Only</span>
                  </div>
                </div>

                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-gray-800 mb-4">Emergency Support</h3>
                  <p className="text-gray-600 mb-2">For urgent technical issues outside business hours:</p>
                  <p className="text-blue-600 font-semibold">+1 (555) EMERGENCY</p>
                </div>
              </div>

              <div className="bg-white rounded-2xl shadow-xl p-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Frequently Asked Questions</h2>
                <div className="space-y-6">
                  {faqs.map((faq, index) => (
                    <div key={index}>
                      <h3 className="text-lg font-semibold text-gray-800 mb-2">{faq.question}</h3>
                      <p className="text-gray-600">{faq.answer}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Map Section */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">Visit Our Office</h2>
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="h-96 bg-gray-200 flex items-center justify-center">
              <div className="text-center">
                <div className="text-4xl mb-4">🗺️</div>
                <p className="text-gray-600">Interactive map would be displayed here</p>
                <p className="text-gray-500 text-sm mt-2">123 Dental Street, San Francisco, CA 94102</p>
              </div>
            </div>
            <div className="p-6 bg-gray-50">
              <div className="flex flex-col sm:flex-row justify-between items-center">
                <div>
                  <h3 className="font-semibold text-gray-800">Dentaloist Headquarters</h3>
                  <p className="text-gray-600">123 Dental Street, Suite 100</p>
                  <p className="text-gray-600">San Francisco, CA 94102</p>
                </div>
                <a
                  href="#directions"
                  className="mt-4 sm:mt-0 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
                >
                  Get Directions
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to Get Started?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of dental practices using Dentaloist to streamline their operations.
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link href="/register" className="bg-white text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg">
              Start Free Trial
            </Link>
            <Link href="/pricing" className="border border-white text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg">
              View Pricing
            </Link>
          </div>
        </div>
      </section>

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
      { href: "/#features", text: "Features" },
      { href: "/pricing", text: "Pricing" },
      { href: "/#demo", text: "Demo" }
    ]
  },
  {
    title: "Company",
    links: [
      { href: "/#about", text: "About" },
      { href: "/blog", text: "Blog" },
      { href: "/careers", text: "Careers" },
      { href: "/contact", text: "Contact" }
    ]
  },
  {
    title: "Support",
    links: [
      { href: "#", text: "Help Center" },
      { href: "#", text: "Documentation" },
      { href: "#", text: "Community" }
    ]
  }
]