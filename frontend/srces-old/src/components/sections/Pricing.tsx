export default function Pricing() {
  return (
    <section id="pricing" className="bg-gray-50 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Simple, Transparent Pricing</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Choose the plan that works best for your practice with no hidden fees.
        </p>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Starter */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold mb-4">Starter</h3>
            <div className="text-4xl font-bold text-blue-600 mb-6">$99<span className="text-lg text-gray-500">/month</span></div>
            <ul className="text-left space-y-3 mb-8">
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Up to 500 patients</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Basic scheduling</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Email support</li>
              <li className="flex items-center"><span className="text-gray-400 mr-2">✗</span> Advanced reporting</li>
              <li className="flex items-center"><span className="text-gray-400 mr-2">✗</span> Custom branding</li>
            </ul>
            <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
              Get Started
            </a>
          </div>
          {/* Professional */}
          <div className="bg-white rounded-lg shadow-xl p-8 border-2 border-blue-600 transform scale-105 relative">
            <div className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm absolute top-0 right-6 -translate-y-1/2">
              Most Popular
            </div>
            <h3 className="text-2xl font-bold mb-4">Professional</h3>
            <div className="text-4xl font-bold text-blue-600 mb-6">$199<span className="text-lg text-gray-500">/month</span></div>
            <ul className="text-left space-y-3 mb-8">
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Unlimited patients</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Advanced scheduling</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Priority support</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Comprehensive reporting</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom branding</li>
            </ul>
            <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
              Get Started
            </a>
          </div>
          {/* Enterprise */}
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h3 className="text-2xl font-bold mb-4">Enterprise</h3>
            <div className="text-4xl font-bold text-blue-600 mb-6">Custom</div>
            <ul className="text-left space-y-3 mb-8">
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Multiple locations</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Custom integrations</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Dedicated account manager</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> White-label options</li>
              <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> API access</li>
            </ul>
            <a href="#contact" className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold block text-center">
              Contact Sales
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}
