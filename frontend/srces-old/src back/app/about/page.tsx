'use client'
import Image from 'next/image'
import Link from 'next/link'

export default function About() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-200 rounded-full opacity-20"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-300 rounded-full opacity-20"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            About <span className="text-blue-600">Dentaloist</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Transforming dental care through innovative technology and compassionate service
          </p>
          <div className="w-24 h-2 bg-blue-600 mx-auto mb-12"></div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <div className="relative">
                <div className="absolute -top-6 -left-6 w-64 h-64 bg-blue-200 rounded-lg opacity-20"></div>
                <div className="relative bg-white rounded-2xl shadow-xl p-8">
                  <div className="text-6xl mb-6">🎯</div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Mission</h2>
                  <p className="text-lg text-gray-600 mb-6">
                    To empower dental professionals with cutting-edge technology that simplifies practice management, 
                    enhances patient care, and drives practice growth.
                  </p>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                      <span className="text-white text-2xl">💡</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Innovation Driven</p>
                      <p className="text-sm text-gray-600">Continuous improvement</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div className="relative">
                <div className="absolute -top-6 -right-6 w-64 h-64 bg-green-200 rounded-lg opacity-20"></div>
                <div className="relative bg-white rounded-2xl shadow-xl p-8">
                  <div className="text-6xl mb-6">🌟</div>
                  <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Vision</h2>
                  <p className="text-lg text-gray-600 mb-6">
                    To become the leading platform that revolutionizes dental practice management worldwide, 
                    making exceptional dental care accessible to everyone.
                  </p>
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center">
                      <span className="text-white text-2xl">🌍</span>
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900">Global Impact</p>
                      <p className="text-sm text-gray-600">Worldwide accessibility</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Story Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Story</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From a simple idea to a comprehensive dental practice management solution
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-100 rounded-2xl mx-auto mb-6 flex items-center justify-center">
                <span className="text-4xl">💡</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">The Beginning</h3>
              <p className="text-gray-600">
                Founded in 2018 by dental professionals who saw the need for better practice management tools
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-green-100 rounded-2xl mx-auto mb-6 flex items-center justify-center">
                <span className="text-4xl">🚀</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Rapid Growth</h3>
              <p className="text-gray-600">
                Quickly expanded to serve over 500 dental practices across the country
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-purple-100 rounded-2xl mx-auto mb-6 flex items-center justify-center">
                <span className="text-4xl">🏆</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Today</h3>
              <p className="text-gray-600">
                Leading provider of dental practice management solutions with continuous innovation
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dedicated professionals committed to transforming dental practice management
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <div key={index} className="text-center group">
                <div className="relative mb-6">
                  <div className="w-32 h-32 mx-auto bg-gradient-to-br from-blue-200 to-indigo-300 rounded-full flex items-center justify-center group-hover:scale-105 transition-transform duration-300">
                    <span className="text-4xl">{member.emoji}</span>
                  </div>
                  <div className="absolute -bottom-2 -right-2 w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center">
                    <span className="text-2xl">⭐</span>
                  </div>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                <p className="text-blue-600 font-medium mb-2">{member.role}</p>
                <p className="text-gray-600 text-sm">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Our Values</h2>
            <p className="text-xl opacity-90 max-w-3xl mx-auto">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <div key={index} className="text-center group">
                <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl mx-auto mb-6 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                  <span className="text-3xl">{value.emoji}</span>
                </div>
                <h3 className="text-xl font-semibold mb-4">{value.title}</h3>
                <p className="opacity-90">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">500+</div>
              <p className="text-gray-600">Dental Practices</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">50K+</div>
              <p className="text-gray-600">Patients Served</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">99.9%</div>
              <p className="text-gray-600">Uptime</p>
            </div>
            <div>
              <div className="text-4xl font-bold text-orange-600 mb-2">24/7</div>
              <p className="text-gray-600">Support</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">Join the Dentaloist Family</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Ready to transform your dental practice with our comprehensive management solution?
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link
              href="/register"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg"
            >
              Get Started Free
            </Link>
            <Link
              href="/contact"
              className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg"
            >
              Schedule Demo
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}

const teamMembers = [
  {
    emoji: "👨‍⚕️",
    name: "Dr. Michael Chen",
    role: "Chief Dental Officer",
    bio: "20+ years in dental practice with expertise in digital dentistry"
  },
  {
    emoji: "👩‍💼",
    name: "Sarah Johnson",
    role: "CEO & Founder",
    bio: "Former practice manager with passion for healthcare technology"
  },
  {
    emoji: "👨‍💻",
    name: "David Kim",
    role: "CTO",
    bio: "Software engineer with background in healthcare systems"
  },
  {
    emoji: "👩‍⚕️",
    name: "Dr. Emily Rodriguez",
    role: "Clinical Advisor",
    bio: "Periodontist and digital transformation advocate"
  }
]

const values = [
  {
    emoji: "❤️",
    title: "Patient First",
    description: "Everything we do is focused on improving patient care and experience"
  },
  {
    emoji: "⚡",
    title: "Innovation",
    description: "Constantly pushing boundaries to deliver cutting-edge solutions"
  },
  {
    emoji: "🤝",
    title: "Collaboration",
    description: "Working together with dental professionals to create the best tools"
  },
  {
    emoji: "🎯",
    title: "Excellence",
    description: "Committed to delivering the highest quality in everything we do"
  }
]