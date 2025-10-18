'use client'

import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12 mt-auto">
      <div className="container mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 className="text-xl font-bold text-white mb-4">Dentaloist</h3>
          <p>Modern dental practice management platform.</p>
        </div>
        <div>
          <h4 className="font-semibold text-white mb-3">Links</h4>
          <ul className="space-y-2">
            <li><Link href="#features">Features</Link></li>
            <li><Link href="#pricing">Pricing</Link></li>
            <li><Link href="#testimonials">Testimonials</Link></li>
          </ul>
        </div>
        <div>
          <h4 className="font-semibold text-white mb-3">Contact</h4>
          <p>Email: support@dentaloist.com</p>
          <p>Phone: +1 (800) 555-1234</p>
        </div>
      </div>
      <div className="text-center text-gray-500 mt-8">
        © {new Date().getFullYear()} Dentaloist. All rights reserved.
      </div>
    </footer>
  )
}
