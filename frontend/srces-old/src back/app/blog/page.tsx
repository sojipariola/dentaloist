// app/blog/page.tsx
'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function BlogPage() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')

  const categories = [
    { id: 'all', name: 'All Articles' },
    { id: 'practice-management', name: 'Practice Management' },
    { id: 'dental-technology', name: 'Dental Technology' },
    { id: 'patient-care', name: 'Patient Care' },
    { id: 'industry-news', name: 'Industry News' },
    { id: 'tips-tricks', name: 'Tips & Tricks' }
  ]

  const articles = [
    {
      id: 1,
      title: '5 Ways to Streamline Your Dental Practice Workflow',
      excerpt: 'Learn how to optimize your daily operations and improve efficiency in your dental practice with these proven strategies.',
      category: 'practice-management',
      date: '2024-03-15',
      readTime: '8 min read',
      author: {
        name: 'Dr. Sarah Johnson',
        role: 'Dental Practice Consultant'
      },
      image: '/api/placeholder/400/250?text=Dental+Workflow'
    },
    {
      id: 2,
      title: 'The Future of Digital Dentistry: Trends to Watch in 2024',
      excerpt: 'Explore the latest technological advancements that are transforming dental care and how to implement them in your practice.',
      category: 'dental-technology',
      date: '2024-03-10',
      readTime: '12 min read',
      author: {
        name: 'Michael Chen',
        role: 'Dental Technology Expert'
      },
      image: '/api/placeholder/400/250?text=Digital+Dentistry'
    },
    {
      id: 3,
      title: 'Improving Patient Experience: From Scheduling to Follow-up',
      excerpt: 'Discover practical tips to enhance patient satisfaction at every touchpoint of their journey through your practice.',
      category: 'patient-care',
      date: '2024-03-05',
      readTime: '6 min read',
      author: {
        name: 'Dr. Emily Rodriguez',
        role: 'Patient Experience Specialist'
      },
      image: '/api/placeholder/400/250?text=Patient+Experience'
    },
    {
      id: 4,
      title: 'HIPAA Compliance in the Digital Age: What You Need to Know',
      excerpt: 'Stay up-to-date with the latest HIPAA requirements and best practices for protecting patient data in your practice.',
      category: 'practice-management',
      date: '2024-02-28',
      readTime: '10 min read',
      author: {
        name: 'Jennifer Williams',
        role: 'Healthcare Compliance Officer'
      },
      image: '/api/placeholder/400/250?text=HIPAA+Compliance'
    },
    {
      id: 5,
      title: 'Implementing Teledentistry: A Practical Guide for Practices',
      excerpt: 'Learn how to successfully integrate teledentistry services into your practice to expand your reach and improve access to care.',
      category: 'dental-technology',
      date: '2024-02-20',
      readTime: '9 min read',
      author: {
        name: 'Dr. Robert Kim',
        role: 'Telehealth Advocate'
      },
      image: '/api/placeholder/400/250?text=Teledentistry'
    },
    {
      id: 6,
      title: 'Building a Strong Team Culture in Your Dental Practice',
      excerpt: 'Discover strategies for fostering collaboration, communication, and job satisfaction among your dental team members.',
      category: 'practice-management',
      date: '2024-02-15',
      readTime: '7 min read',
      author: {
        name: 'Lisa Thompson',
        role: 'Dental Practice Manager'
      },
      image: '/api/placeholder/400/250?text=Team+Culture'
    },
    {
      id: 7,
      title: 'The Art of Case Presentation: Converting Consultations to Treatment',
      excerpt: 'Master the skills needed to effectively present treatment plans and help patients make informed decisions about their care.',
      category: 'patient-care',
      date: '2024-02-10',
      readTime: '11 min read',
      author: {
        name: 'Dr. James Wilson',
        role: 'Practice Growth Consultant'
      },
      image: '/api/placeholder/400/250?text=Case+Presentation'
    },
    {
      id: 8,
      title: 'Latest CDC Guidelines for Infection Control in Dentistry',
      excerpt: 'Stay current with the most recent infection prevention recommendations and protocols for dental settings.',
      category: 'industry-news',
      date: '2024-02-05',
      readTime: '5 min read',
      author: {
        name: 'Dr. Amanda Park',
        role: 'Infection Control Specialist'
      },
      image: '/api/placeholder/400/250?text=Infection+Control'
    }
  ]

  const featuredArticle = articles[0]

  const filteredArticles = articles.filter(article => {
    const matchesCategory = activeCategory === 'all' || article.category === activeCategory
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          article.excerpt.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesCategory && matchesSearch
  })

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    })
  }

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
            <Link href="/#about" className="text-gray-600 hover:text-blue-600 transition">About</Link>
            <Link href="/#contact" className="text-gray-600 hover:text-blue-600 transition">Contact</Link>
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
      <div className="container mx-auto px-6 py-16">
        <div className="text-center max-w-3xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-6">
            Dentaloist Blog
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Insights, tips, and news for modern dental practices. Stay updated with the latest in practice management, patient care, and dental technology.
          </p>
          
          {/* Search Bar */}
          <div className="relative max-w-2xl mx-auto mb-12">
            <input
              type="text"
              placeholder="Search articles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-6 py-4 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none shadow-sm"
            />
            <svg className="absolute right-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" 
                 fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap justify-center gap-4 mb-12">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setActiveCategory(category.id)}
              className={`px-6 py-2 rounded-full transition-colors ${
                activeCategory === category.id
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Featured Article */}
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden mb-16">
          <div className="md:flex">
            <div className="md:flex-1">
              <div className="h-64 md:h-full bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">Featured Article Image</span>
              </div>
            </div>
            <div className="md:flex-1 p-8 md:p-12">
              <span className="inline-block px-4 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold mb-4">
                {categories.find(cat => cat.id === featuredArticle.category)?.name}
              </span>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                {featuredArticle.title}
              </h2>
              <p className="text-gray-600 mb-6 text-lg">
                {featuredArticle.excerpt}
              </p>
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-gray-300 rounded-full mr-3 flex items-center justify-center">
                    <span className="text-gray-600 text-sm">AV</span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">{featuredArticle.author.name}</p>
                    <p className="text-sm text-gray-500">{featuredArticle.author.role}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-500">{formatDate(featuredArticle.date)}</p>
                  <p className="text-sm text-gray-500">{featuredArticle.readTime}</p>
                </div>
              </div>
              <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
                Read Article
              </button>
            </div>
          </div>
        </div>

        {/* Articles Grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">
            {activeCategory === 'all' ? 'Latest Articles' : `${categories.find(cat => cat.id === activeCategory)?.name} Articles`}
          </h2>
          
          {filteredArticles.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-600 text-lg">No articles found matching your criteria.</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredArticles.filter(article => article.id !== featuredArticle.id).map(article => (
                <article key={article.id} className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="h-48 bg-gray-200 flex items-center justify-center">
                    <span className="text-gray-500">Article Image</span>
                  </div>
                  <div className="p-6">
                    <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold mb-3">
                      {categories.find(cat => cat.id === article.category)?.name}
                    </span>
                    <h3 className="text-xl font-semibold text-gray-800 mb-3 line-clamp-2">
                      {article.title}
                    </h3>
                    <p className="text-gray-600 mb-4 line-clamp-3">
                      {article.excerpt}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className="w-8 h-8 bg-gray-300 rounded-full mr-2 flex items-center justify-center">
                          <span className="text-gray-600 text-xs">AV</span>
                        </div>
                        <span className="text-sm text-gray-700">{article.author.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{formatDate(article.date)}</span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>

        {/* Newsletter Subscription */}
        <div className="bg-blue-600 rounded-2xl p-8 md:p-12 text-center text-white mb-16">
          <h2 className="text-3xl font-bold mb-4">Stay Updated</h2>
          <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
            Subscribe to our newsletter and never miss new articles, product updates, and industry insights.
          </p>
          <div className="flex flex-col sm:flex-row max-w-2xl mx-auto gap-4">
            <input
              type="email"
              placeholder="Enter your email address"
              className="flex-1 px-6 py-3 rounded-lg border border-blue-300 focus:ring-2 focus:ring-white focus:border-transparent outline-none text-gray-800"
            />
            <button className="bg-white text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition font-semibold">
              Subscribe
            </button>
          </div>
          <p className="text-blue-200 text-sm mt-4">
            No spam. Unsubscribe at any time.
          </p>
        </div>
      </div>

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
      { href: "#", text: "Careers" },
      { href: "/#contact", text: "Contact" }
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