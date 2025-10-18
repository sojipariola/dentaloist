// app/careers/page.tsx
'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function CareersPage() {
  const [activeDepartment, setActiveDepartment] = useState('all')
  const [activeLocation, setActiveLocation] = useState('all')
  const [activeJobType, setActiveJobType] = useState('all')

  const departments = [
    { id: 'all', name: 'All Departments' },
    { id: 'engineering', name: 'Engineering' },
    { id: 'product', name: 'Product' },
    { id: 'sales', name: 'Sales' },
    { id: 'marketing', name: 'Marketing' },
    { id: 'customer-success', name: 'Customer Success' },
    { id: 'dental-consulting', name: 'Dental Consulting' }
  ]

  const locations = [
    { id: 'all', name: 'All Locations' },
    { id: 'remote', name: 'Remote' },
    { id: 'new-york', name: 'New York, NY' },
    { id: 'san-francisco', name: 'San Francisco, CA' },
    { id: 'london', name: 'London, UK' },
    { id: 'toronto', name: 'Toronto, Canada' }
  ]

  const jobTypes = [
    { id: 'all', name: 'All Types' },
    { id: 'full-time', name: 'Full Time' },
    { id: 'part-time', name: 'Part Time' },
    { id: 'contract', name: 'Contract' },
    { id: 'internship', name: 'Internship' }
  ]

  const jobOpenings = [
    {
      id: 1,
      title: 'Senior Frontend Developer',
      department: 'engineering',
      location: 'remote',
      type: 'full-time',
      description: 'Build beautiful, responsive interfaces for our dental practice management platform using React and Next.js.',
      requirements: [
        '5+ years of frontend development experience',
        'Expert knowledge of React, TypeScript, and Next.js',
        'Experience with state management (Redux, Zustand)',
        'Strong UI/UX design sensibilities',
        'Experience with testing frameworks'
      ],
      postedDate: '2024-03-15',
      salary: '$120,000 - $150,000'
    },
    {
      id: 2,
      title: 'Product Manager',
      department: 'product',
      location: 'san-francisco',
      type: 'full-time',
      description: 'Lead product development for our dental practice management suite and help shape the future of dental technology.',
      requirements: [
        '3+ years of product management experience',
        'Background in healthcare or SaaS products',
        'Strong analytical and problem-solving skills',
        'Excellent communication and leadership abilities',
        'Experience with agile development methodologies'
      ],
      postedDate: '2024-03-12',
      salary: '$130,000 - $160,000'
    },
    {
      id: 3,
      title: 'Dental Practice Consultant',
      department: 'dental-consulting',
      location: 'remote',
      type: 'contract',
      description: 'Use your dental expertise to help shape our product and guide our development team.',
      requirements: [
        'DDS/DMD degree or equivalent experience',
        '5+ years of clinical practice experience',
        'Knowledge of practice management software',
        'Excellent communication and teaching skills',
        'Passion for technology and innovation'
      ],
      postedDate: '2024-03-10',
      salary: '$80 - $120/hour'
    },
    {
      id: 4,
      title: 'Sales Development Representative',
      department: 'sales',
      location: 'new-york',
      type: 'full-time',
      description: 'Generate new business opportunities and help dental practices discover our innovative solution.',
      requirements: [
        '2+ years of sales or business development experience',
        'Excellent communication and interpersonal skills',
        'Experience with CRM systems (Salesforce, HubSpot)',
        'Self-motivated and target-driven',
        'Knowledge of dental industry is a plus'
      ],
      postedDate: '2024-03-08',
      salary: '$65,000 - $85,000 + commission'
    },
    {
      id: 5,
      title: 'UX/UI Designer',
      department: 'engineering',
      location: 'london',
      type: 'full-time',
      description: 'Create intuitive and beautiful user experiences for our dental practice management platform.',
      requirements: [
        '4+ years of UX/UI design experience',
        'Strong portfolio showcasing SaaS or healthcare products',
        'Proficiency in Figma, Sketch, or Adobe XD',
        'Understanding of user research methodologies',
        'Experience with design systems'
      ],
      postedDate: '2024-03-05',
      salary: '£60,000 - £80,000'
    },
    {
      id: 6,
      title: 'Customer Success Manager',
      department: 'customer-success',
      location: 'remote',
      type: 'full-time',
      description: 'Ensure our dental practice customers achieve maximum value from our platform and have an exceptional experience.',
      requirements: [
        '3+ years in customer success or account management',
        'Experience with SaaS products',
        'Excellent problem-solving and communication skills',
        'Knowledge of dental industry preferred',
        'Experience with customer success platforms'
      ],
      postedDate: '2024-03-01',
      salary: '$70,000 - $90,000'
    },
    {
      id: 7,
      title: 'Marketing Intern',
      department: 'marketing',
      location: 'toronto',
      type: 'internship',
      description: 'Support our marketing team in creating content and campaigns for the dental industry.',
      requirements: [
        'Currently pursuing degree in Marketing or related field',
        'Strong writing and communication skills',
        'Familiarity with social media platforms',
        'Basic knowledge of marketing tools',
        'Interest in healthcare technology'
      ],
      postedDate: '2024-02-28',
      salary: '$20 - $25/hour'
    },
    {
      id: 8,
      title: 'Backend Engineer',
      department: 'engineering',
      location: 'san-francisco',
      type: 'full-time',
      description: 'Develop scalable backend systems for our dental practice management platform.',
      requirements: [
        '4+ years of backend development experience',
        'Expert knowledge of Node.js, Python, or Go',
        'Experience with databases (PostgreSQL, MongoDB)',
        'Knowledge of API design and microservices',
        'Experience with cloud platforms (AWS, GCP)'
      ],
      postedDate: '2024-02-25',
      salary: '$130,000 - $160,000'
    }
  ]

  const benefits = [
    {
      icon: '💻',
      title: 'Remote-First Culture',
      description: 'Work from anywhere with flexible hours and a supportive remote environment.'
    },
    {
      icon: '🏥',
      title: 'Health Insurance',
      description: 'Comprehensive medical, dental, and vision coverage for you and your family.'
    },
    {
      icon: '💰',
      title: 'Competitive Compensation',
      description: 'Industry-leading salaries, equity packages, and performance bonuses.'
    },
    {
      icon: '🏖️',
      title: 'Unlimited PTO',
      description: 'Take the time you need to recharge and maintain work-life balance.'
    },
    {
      icon: '📚',
      title: 'Learning Budget',
      description: 'Annual stipend for professional development, courses, and conferences.'
    },
    {
      icon: '👶',
      title: 'Parental Leave',
      description: 'Generous paid leave for new parents to bond with their children.'
    }
  ]

  const filteredJobs = jobOpenings.filter(job => {
    const matchesDepartment = activeDepartment === 'all' || job.department === activeDepartment
    const matchesLocation = activeLocation === 'all' || job.location === activeLocation
    const matchesJobType = activeJobType === 'all' || job.type === activeJobType
    return matchesDepartment && matchesLocation && matchesJobType
  })

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    })
  }

  const getDepartmentName = (id: string) => {
    return departments.find(dept => dept.id === id)?.name || id
  }

  const getLocationName = (id: string) => {
    return locations.find(loc => loc.id === id)?.name || id
  }

  const getJobTypeName = (id: string) => {
    return jobTypes.find(type => type.id === id)?.name || id
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
            <Link href="/blog" className="text-gray-600 hover:text-blue-600 transition">Blog</Link>
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
      <div className="container mx-auto px-6 py-16 text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-6">
          Join Our Mission
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Help us revolutionize dental practice management and create better experiences for dental professionals and their patients.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Link href="#open-positions" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold">
            View Open Positions
          </Link>
          <Link href="#why-join-us" className="border border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition font-semibold">
            Why Join Us
          </Link>
        </div>
      </div>

      {/* Why Join Us Section */}
      <section id="why-join-us" className="bg-white py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Why Join Dentaloist?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We're building the future of dental practice management, and we need talented people to help us get there.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
            {benefits.map((benefit, index) => (
              <div key={index} className="bg-blue-50 rounded-xl p-6 text-center">
                <div className="text-4xl mb-4">{benefit.icon}</div>
                <h3 className="text-xl font-semibold text-gray-800 mb-3">{benefit.title}</h3>
                <p className="text-gray-600">{benefit.description}</p>
              </div>
            ))}
          </div>

          <div className="bg-gray-50 rounded-2xl p-8 md:p-12">
            <div className="grid md:grid-cols-2 gap-8 items-center">
              <div>
                <h3 className="text-2xl font-bold text-gray-800 mb-4">Our Culture</h3>
                <p className="text-gray-600 mb-4">
                  At Dentaloist, we believe that great products are built by great teams. We foster a culture of collaboration, innovation, and continuous learning.
                </p>
                <p className="text-gray-600 mb-4">
                  We're passionate about making a real impact in the dental industry and helping practices provide better patient care through technology.
                </p>
                <ul className="space-y-2 text-gray-600">
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Collaborative and inclusive environment
                  </li>
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Focus on work-life balance
                  </li>
                  <li className="flex items-center">
                    <svg className="w-5 h-5 text-green-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    Opportunities for growth and development
                  </li>
                </ul>
              </div>
              <div className="bg-gray-200 rounded-lg h-64 flex items-center justify-center">
                <span className="text-gray-500">Team Culture Image</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Open Positions Section */}
      <section id="open-positions" className="py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Open Positions</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Join our team and help shape the future of dental practice management.
            </p>
          </div>

          {/* Filters */}
          <div className="bg-white rounded-xl p-6 shadow-md mb-8">
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Department</label>
                <select
                  value={activeDepartment}
                  onChange={(e) => setActiveDepartment(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {departments.map(dept => (
                    <option key={dept.id} value={dept.id}>{dept.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <select
                  value={activeLocation}
                  onChange={(e) => setActiveLocation(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {locations.map(loc => (
                    <option key={loc.id} value={loc.id}>{loc.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Job Type</label>
                <select
                  value={activeJobType}
                  onChange={(e) => setActiveJobType(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {jobTypes.map(type => (
                    <option key={type.id} value={type.id}>{type.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Job Listings */}
          <div className="space-y-6">
            {filteredJobs.length === 0 ? (
              <div className="text-center py-12 bg-white rounded-xl shadow-md">
                <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p className="text-gray-600 text-lg">No positions match your current filters.</p>
                <button
                  onClick={() => {
                    setActiveDepartment('all')
                    setActiveLocation('all')
                    setActiveJobType('all')
                  }}
                  className="text-blue-600 hover:text-blue-700 font-medium mt-4"
                >
                  Clear all filters
                </button>
              </div>
            ) : (
              filteredJobs.map(job => (
                <div key={job.id} className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-800 mb-2">{job.title}</h3>
                      <div className="flex flex-wrap gap-3 mb-4">
                        <span className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          {getDepartmentName(job.department)}
                        </span>
                        <span className="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                          {getLocationName(job.location)}
                        </span>
                        <span className="inline-flex items-center px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">
                          {getJobTypeName(job.type)}
                        </span>
                      </div>
                      <p className="text-gray-600 mb-4">{job.description}</p>
                      <div className="flex items-center text-sm text-gray-500">
                        <span>Posted {formatDate(job.postedDate)}</span>
                        <span className="mx-2">•</span>
                        <span className="font-semibold text-gray-700">{job.salary}</span>
                      </div>
                    </div>
                    <div className="mt-4 md:mt-0 md:ml-6">
                      <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold whitespace-nowrap">
                        Apply Now
                      </button>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Application Process */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Our Hiring Process</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We've designed our process to be transparent, respectful of your time, and focused on finding the right fit.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📝</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">1. Application</h3>
              <p className="text-gray-600">Submit your application and resume through our portal.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💬</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">2. Screening</h3>
              <p className="text-gray-600">Brief call with our recruiting team to discuss your background.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">👥</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">3. Interviews</h3>
              <p className="text-gray-600">Meet with the team and complete role-specific assessments.</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎉</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-2">4. Offer</h3>
              <p className="text-gray-600">Receive an offer and welcome to the Dentaloist team!</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to Join Our Team?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            If you don't see the perfect role but believe you'd be a great fit for Dentaloist, we'd still love to hear from you.
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link href="#open-positions" className="bg-white text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg">
              View All Positions
            </Link>
            <Link href="/#contact" className="border border-white text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg">
              General Application
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