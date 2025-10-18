const aboutPoints = [
  { title: "Trusted by Dentists Worldwide", description: "Over 10,000 dental practices rely on us for seamless management." },
  { title: "Built for Efficiency", description: "Streamline workflows and reduce administrative overhead." },
  { title: "Secure & Compliant", description: "HIPAA-compliant data security and encrypted storage." },
]

export default function About() {
  return (
    <section id="about" className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">About Our Practice Management</h2>
        <div className="grid md:grid-cols-3 gap-12">
          {aboutPoints.map((point, i) => (
            <div key={i} className="p-6 rounded-xl shadow hover:shadow-xl transition">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">{point.title}</h3>
              <p className="text-gray-600 leading-relaxed">{point.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
