'use client'

export default function Features() {
  const features = [
    { icon: '📅', title: 'Appointments', desc: 'Smart scheduling and reminders.' },
    { icon: '👥', title: 'Patients', desc: 'Centralized patient records.' },
    { icon: '💳', title: 'Billing', desc: 'Automated invoicing & payments.' },
    { icon: '📊', title: 'Analytics', desc: 'Track growth in real time.' },
  ]

  return (
    <section id="features" className="container mx-auto px-6 py-20">
      <h2 className="text-4xl font-bold text-center mb-12">Key Features</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {features.map((f, idx) => (
          <div key={idx} className="bg-white shadow rounded-xl p-6 text-center hover:shadow-lg transition">
            <div className="text-5xl mb-4">{f.icon}</div>
            <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
            <p className="text-gray-600">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
