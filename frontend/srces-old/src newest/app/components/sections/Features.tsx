const features = [
  { icon: "📅", title: "Smart Scheduling", description: "Intuitive calendar system with automated reminders." },
  { icon: "📋", title: "Patient Management", description: "Comprehensive patient records, treatment history." },
  { icon: "💳", title: "Integrated Billing", description: "Seamless payment processing and financial reporting." },
  { icon: "📊", title: "Analytics Dashboard", description: "Real-time insights into practice performance." },
  { icon: "🔒", title: "Secure & Compliant", description: "HIPAA-compliant security with encrypted data storage." },
  { icon: "📱", title: "Mobile Ready", description: "Access your practice from anywhere on web & mobile." },
]

export default function Features() {
  return (
    <section id="features" className="bg-white py-20">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Everything You Need in One Place</h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Designed by dental professionals for dental professionals. Streamline your practice with our comprehensive suite of tools.
          </p>
        </div>
        <div className="grid md:grid-cols-3 gap-12">
          {features.map((f, i) => (
            <div key={i} className="text-center p-8 rounded-xl hover:shadow-xl transition duration-300">
              <div className="w-20 h-20 bg-blue-100 rounded-2xl mx-auto mb-6 flex items-center justify-center text-3xl">{f.icon}</div>
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">{f.title}</h3>
              <p className="text-gray-600 leading-relaxed">{f.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
