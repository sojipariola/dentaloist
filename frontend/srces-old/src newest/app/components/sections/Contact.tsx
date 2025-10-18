const contactMethods = [
  { title: "Email", icon: "📧", detail: "info@dentaloist.com" },
  { title: "Phone", icon: "📞", detail: "+1 (555) 123-4567" },
  { title: "Office", icon: "📍", detail: "123 Dental Street, City, State 12345" },
]

export default function Contact() {
  return (
    <section id="contact" className="py-20 bg-blue-600 text-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold mb-6">Get In Touch</h2>
        <p className="text-xl mb-12 max-w-2xl mx-auto">
          Have questions? We'd love to hear from you.
        </p>
        <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          {contactMethods.map((c, i) => (
            <div key={i} className="p-6 rounded-xl bg-white bg-opacity-10">
              <div className="text-3xl mb-4">{c.icon}</div>
              <h3 className="font-semibold mb-2">{c.title}</h3>
              <p>{c.detail}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
