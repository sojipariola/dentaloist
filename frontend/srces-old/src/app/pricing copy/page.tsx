// app/pricing/page.tsx
'use client'

import Link from 'next/link'
import { useState } from 'react'

export default function PricingPage() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('annual')

  const plans = [
    {
      name: 'Starter',
      description: 'Perfect for small practices just getting started',
      monthlyPrice: 99,
      annualPrice: 89,
      annualSavings: 10,
      features: [
        'Up to 500 patients',
        'Basic scheduling',
        'Email support',
        'Standard reports',
        '1 user included',
        'Mobile app access'
      ],
      limitations: [
        'No advanced analytics',
        'No custom branding',
        'No API access'
      ],
      cta: 'Get Started',
      popular: false
    },
    {
      name: 'Professional',
      description: 'Everything growing practices need to succeed',
      monthlyPrice: 199,
      annualPrice: 179,
      annualSavings: 20,
      features: [
        'Unlimited patients',
        'Advanced scheduling',
        'Priority support',
        'Comprehensive reports',
        '5 users included',
        'Custom branding',
        'API access',
        'Advanced analytics'
      ],
      limitations: [],
      cta: 'Get Started',
      popular: true
    },
    {
      name: 'Enterprise',
      description: 'For large practices with complex needs',
      monthlyPrice: 399,
      annualPrice: 359,
      annualSavings: 40,
      features: [
        'Multiple locations',
        'Unlimited users',
        '24/7 dedicated support',
        'Custom integrations',
        'White-label options',
        'Advanced security',
        'Onboarding assistance',
        'Custom development'
      ],
      limitations: [],
      cta: 'Contact Sales',
      popular: false
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
          Simple, Transparent Pricing
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
          Choose the plan that works best for your practice. All plans include a 14-day free trial with no credit card required.
        </p>
        
        {/* Billing Toggle */}
        <div className="flex justify-center items-center mb-12">
          <span className={`mr-4 font-medium ${billingCycle === 'monthly' ? 'text-blue-600' : 'text-gray-500'}`}>
            Monthly
          </span>
          <button
            onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
            className="relative rounded-full w-14 h-7 transition duration-200 ease-linear"
          >
            <div className={`absolute rounded-full w-14 h-7 transition-colors duration-200 ${
              billingCycle === 'annual' ? 'bg-blue-600' : 'bg-gray-300'
            }`}></div>
            <div className={`absolute left-1 top-1 bg-white w-5 h-5 rounded-full transition-transform duration-200 ${
              billingCycle === 'annual' ? 'transform translate-x-7' : ''
            }`}></div>
          </button>
          <span className={`ml-4 font-medium ${billingCycle === 'annual' ? 'text-blue-600' : 'text-gray-500'}`}>
            Annual <span className="text-green-600 text-sm">(Save up to 20%)</span>
          </span>
        </div>
      </div>

      {/* Pricing Plans */}
      <div className="container mx-auto px-6 pb-20">
        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={index}
              className={`relative rounded-2xl p-8 ${
                plan.popular
                  ? 'border-2 border-blue-600 bg-white shadow-xl transform scale-105'
                  : 'bg-white border border-gray-200 shadow-lg'
              }`}
            >
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
              )}
              
              <h3 className="text-2xl font-bold text-gray-800 mb-2">{plan.name}</h3>
              <p className="text-gray-600 mb-6">{plan.description}</p>
              
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-800">
                  ${billingCycle === 'annual' ? plan.annualPrice : plan.monthlyPrice}
                </span>
                <span className="text-gray-600">/month</span>
                {billingCycle === 'annual' && (
                  <div className="text-sm text-green-600 mt-1">
                    Save ${plan.annualSavings}/month compared to monthly billing
                  </div>
                )}
              </div>
              
              <div className="mb-8">
                <h4 className="font-semibold text-gray-800 mb-4">What's included:</h4>
                <ul className="space-y-3">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-start">
                      <svg className="h-5 w-5 text-green-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-gray-600">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                {plan.limitations.length > 0 && (
                  <>
                    <h4 className="font-semibold text-gray-800 mt-6 mb-4">Limitations:</h4>
                    <ul className="space-y-3">
                      {plan.limitations.map((limitation, limitationIndex) => (
                        <li key={limitationIndex} className="flex items-start">
                          <svg className="h-5 w-5 text-red-500 mr-2 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                          </svg>
                          <span className="text-gray-600">{limitation}</span>
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
              
              <button
                className={`w-full py-3 px-6 rounded-lg font-semibold ${
                  plan.popular
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                } transition duration-200`}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* FAQ Section */}
      <div className="bg-gray-50 py-20">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center text-gray-800 mb-12">Frequently Asked Questions</h2>
          
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Can I change plans anytime?</h3>
              <p className="text-gray-600">
                Yes, you can upgrade, downgrade, or cancel your plan at any time. Changes to your plan will take effect at the start of your next billing cycle.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Is there a setup fee?</h3>
              <p className="text-gray-600">
                No, there are no setup fees for any of our plans. You only pay the monthly or annual subscription fee.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Do you offer discounts for nonprofits?</h3>
              <p className="text-gray-600">
                Yes, we offer a 20% discount for registered nonprofit organizations. Contact our sales team for more information.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">What payment methods do you accept?</h3>
              <p className="text-gray-600">
                We accept all major credit cards, PayPal, and bank transfers for annual plans. Monthly plans are credit card or PayPal only.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Is my data secure?</h3>
              <p className="text-gray-600">
                Absolutely. We use industry-standard encryption and are HIPAA compliant. Your patient data is always secure and private.
              </p>
            </div>
            
            <div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Can I get a refund?</h3>
              <p className="text-gray-600">
                We offer a 14-day free trial to test our platform. If you're not satisfied, you can cancel during the trial period with no charges. After that, we don't offer refunds but you can cancel at any time.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-blue-600 py-16">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">Ready to get started?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Join thousands of dental practices using Dentaloist to streamline their operations and provide better patient care.
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-6">
            <Link href="/register" className="bg-white text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg">
              Start Free Trial
            </Link>
            <Link href="/contact" className="border border-white text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg">
              Contact Sales
            </Link>
          </div>
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
      { href: "#", text: "Blog" },
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