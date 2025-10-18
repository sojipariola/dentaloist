import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { 
  Calendar, 
  Users, 
  DollarSign, 
  Stethoscope, 
  Package, 
  Shield,
  ArrowRight,
  CheckCircle2,
  Play
} from 'lucide-react'

export default function Home() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
  }, [])

  const features = [
    {
      icon: Calendar,
      title: 'Appointment Management',
      description: 'Streamline scheduling, reminders, and patient communications'
    },
    {
      icon: Users,
      title: 'Patient Management',
      description: 'Comprehensive patient records and medical history tracking'
    },
    {
      icon: DollarSign,
      title: 'Billing & Insurance',
      description: 'Automated invoicing, payment processing, and insurance claims'
    },
    {
      icon: Stethoscope,
      title: 'Clinical Tools',
      description: 'Treatment planning, clinical notes, and prescription management'
    },
    {
      icon: Package,
      title: 'Inventory Management',
      description: 'Track supplies, manage orders, and optimize stock levels'
    },
    {
      icon: Shield,
      title: 'Security & Compliance',
      description: 'HIPAA-compliant security with audit trails and role-based access'
    }
  ]

  const testimonials = [
    {
      name: 'Dr. Sarah Johnson',
      role: 'Dental Practice Owner',
      content: 'Dentaloist transformed our practice. We\'ve reduced administrative work by 60% and improved patient satisfaction significantly.',
      practice: 'Bright Smile Dental'
    },
    {
      name: 'Dr. Michael Chen',
      role: 'Orthodontist',
      content: 'The inventory management alone saved us thousands in optimized supply ordering. The clinical tools are exceptional.',
      practice: 'Perfect Teeth Orthodontics'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Stethoscope className="h-8 w-8 text-primary-600" />
              <span className="text-2xl font-bold text-gray-900">Dentaloist</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#features" className="text-gray-600 hover:text-gray-900 transition-colors">Features</a>
              <a href="#testimonials" className="text-gray-600 hover:text-gray-900 transition-colors">Testimonials</a>
              <a href="#pricing" className="text-gray-600 hover:text-gray-900 transition-colors">Pricing</a>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login" className="text-gray-600 hover:text-gray-900 transition-colors">
                Sign In
              </Link>
              <Link 
                to="/register" 
                className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors font-medium"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className={`text-center space-y-8 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
            <h1 className="text-5xl md:text-7xl font-bold text-gray-900 leading-tight">
              Modern Dental Practice
              <span className="block text-primary-600">Management</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Streamline your dental practice with all-in-one software for appointments, 
              patient records, billing, and inventory management.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
              <Link 
                to="/register" 
                className="bg-primary-600 text-white px-8 py-4 rounded-xl hover:bg-primary-700 transition-all duration-200 font-semibold text-lg flex items-center space-x-2 shadow-lg hover:shadow-xl"
              >
                <span>Start Free Trial</span>
                <ArrowRight className="h-5 w-5" />
              </Link>
              <button className="border-2 border-gray-300 text-gray-700 px-8 py-4 rounded-xl hover:border-gray-400 transition-all duration-200 font-semibold text-lg flex items-center space-x-2">
                <Play className="h-5 w-5" />
                <span>Watch Demo</span>
              </button>
            </div>
            <div className="pt-8">
              <p className="text-gray-500 text-sm">Trusted by 500+ dental practices worldwide</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Everything Your Practice Needs
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Comprehensive tools designed specifically for dental professionals to save time and grow your practice.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div 
                key={feature.title}
                className="card p-8 hover:shadow-lg transition-all duration-300 group"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-6 group-hover:bg-primary-200 transition-colors">
                  <feature.icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Loved by Dental Professionals
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              See how Dentaloist is transforming dental practices around the world.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {testimonials.map((testimonial, index) => (
              <div 
                key={testimonial.name}
                className="card p-8 relative"
                style={{ animationDelay: `${index * 200}ms` }}
              >
                <div className="absolute -top-4 -left-4 w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <CheckCircle2 className="h-5 w-5 text-white" />
                </div>
                <p className="text-gray-700 text-lg italic mb-6">
                  "{testimonial.content}"
                </p>
                <div>
                  <p className="font-semibold text-gray-900">{testimonial.name}</p>
                  <p className="text-gray-600">{testimonial.role}</p>
                  <p className="text-primary-600 font-medium">{testimonial.practice}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
            Ready to Transform Your Practice?
          </h2>
          <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
            Join thousands of dental professionals who trust Dentaloist to run their practice efficiently.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              to="/register" 
              className="bg-white text-primary-600 px-8 py-4 rounded-xl hover:bg-gray-100 transition-all duration-200 font-semibold text-lg shadow-lg hover:shadow-xl"
            >
              Start Free Trial
            </Link>
            <button className="border-2 border-white text-white px-8 py-4 rounded-xl hover:bg-white hover:text-primary-600 transition-all duration-200 font-semibold text-lg">
              Schedule a Demo
            </button>
          </div>
          <p className="text-primary-200 mt-6 text-sm">
            No credit card required • 14-day free trial • Setup in minutes
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Stethoscope className="h-6 w-6 text-primary-400" />
              <span className="text-xl font-bold">Dentaloist</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2024 Dentaloist. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}