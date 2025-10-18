'use client'

export default function Testimonials() {
  const testimonials = [
    { name: 'Dr. Smith', text: 'Dentaloist has transformed how I manage my practice.' },
    { name: 'Dr. Lee', text: 'Appointments and billing are now effortless!' },
    { name: 'Dr. Patel', text: 'The analytics help me grow my practice strategically.' },
  ]

  return (
    <section id="testimonials" className="container mx-auto px-6 py-20">
      <h2 className="text-4xl font-bold text-center mb-12">What Dentists Say</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {testimonials.map((t, idx) => (
          <div key={idx} className="bg-white shadow rounded-xl p-6 text-center hover:shadow-lg transition">
            <p className="text-gray-700 italic mb-4">“{t.text}”</p>
            <h3 className="font-semibold text-gray-800">{t.name}</h3>
          </div>
        ))}
      </div>
    </section>
  )
}
