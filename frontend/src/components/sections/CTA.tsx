'use client'

import Link from 'next/link'

export default function CTA() {
  return (
    <section id="cta" className="bg-blue-600 py-20 text-white text-center">
      <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Dental Practice?</h2>
      <p className="text-lg mb-8">Get started with a 14-day free trial. No credit card required.</p>
      <Link href="/signup" className="bg-white text-blue-600 px-8 py-4 rounded-lg shadow hover:bg-gray-100 transition font-semibold text-lg">
        Start Free Trial
      </Link>
    </section>
  )
}
