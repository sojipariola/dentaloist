// app/page.tsx
'use client';

import { motion } from 'framer-motion';
import { 
  Calendar, 
  Users, 
  DollarSign, 
  Activity,
  Tooth,
  Shield,
  Clock,
  Star
} from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const features = [
    {
      icon: Calendar,
      title: 'Appointment Management',
      description: 'Streamline scheduling with intelligent calendar system',
    },
    {
      icon: Users,
      title: 'Patient Records',
      description: 'Comprehensive patient history and treatment tracking',
    },
    {
      icon: DollarSign,
      title: 'Billing & Insurance',
      description: 'Automated billing and insurance claim processing',
    },
    {
      icon: Activity,
      title: 'Analytics Dashboard',
      description: 'Real-time insights into practice performance',
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="flex justify-between items-center p-6">
        <div className="flex items-center space-x-2">
          <Tooth className="h-8 w-8 text-blue-600" />
          <span className="text-2xl font-bold text-gray-900">Dentaloist</span>
        </div>
        <div className="flex space-x-4">
          <Link href="/login" className="px-4 py-2 text-gray-700 hover:text-blue-600">
            Login
          </Link>
          <Link 
            href="/register" 
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <motion.h1 
            className="text-5xl md:text-7xl font-bold text-gray-900 mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            Modern Dental Practice
            <span className="text-blue-600 block">Management</span>
          </motion.h1>
          
          <motion.p 
            className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Transform your dental practice with our all-in-one platform designed 
            to streamline operations, enhance patient care, and grow your business.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <Link 
              href="/dashboard" 
              className="px-8 py-4 bg-blue-600 text-white rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Explore Dashboard
            </Link>
            <button className="px-8 py-4 border border-gray-300 rounded-lg text-lg font-semibold hover:bg-gray-50 transition-colors">
              Watch Demo
            </button>
          </motion.div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Everything You Need in One Platform
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Designed by dental professionals for dental professionals. 
              Streamline your workflow and focus on what matters most - patient care.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                className="text-center p-6 rounded-xl hover:shadow-lg transition-shadow"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">500+</div>
              <div className="text-gray-600">Practices Served</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">1M+</div>
              <div className="text-gray-600">Patients Managed</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">99.9%</div>
              <div className="text-gray-600">Uptime</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">24/7</div>
              <div className="text-gray-600">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto text-center">
          <p>&copy; 2024 Dentaloist. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}