'use client'

export default function Pricing() {
  const plans = [
    { name: 'Basic', price: '$29/mo', features: ['Appointments', 'Patient Records'] },
    { name: 'Pro', price: '$59/mo', features: ['Everything in Basic', 'Billing', 'Analytics'] },
    { name: 'Enterprise', price: 'Custom', features: ['Dedicated Support', 'Custom Integrations'] },
  ]

  return (
    <section id="pricing" className="bg-gray-100 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold mb-12">Affordable Pricing</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan, idx) => (
            <div key={idx} className="bg-white rounded-xl shadow p-8 hover:shadow-lg transition">
              <h3 className="text-2xl font-semibold mb-4">{plan.name}</h3>
              <p className="text-3xl font-bold text-blue-600 mb-6">{plan.price}</p>
              <ul className="mb-6 space-y-2">
                {plan.features.map((f, i) => (
                  <li key={i} className="text-gray-700">✅ {f}</li>
                ))}
              </ul>
              <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                Choose Plan
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
