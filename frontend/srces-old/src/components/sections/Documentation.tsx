const docs = [
  { title: "Getting Started", description: "Set up your account and configure your practice.", link: "#getting-started" },
  { title: "User Guide", description: "Learn how to use all of Dentaloist's features.", link: "#user-guide" },
  { title: "API Reference", description: "Technical documentation for our API.", link: "#api-docs" },
  { title: "Troubleshooting", description: "Solutions to common issues and problems.", link: "#troubleshooting" },
]

export default function Documentation() {
  return (
    <section id="docs" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">Documentation</h2>
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {docs.map((doc, i) => (
            <a key={i} href={doc.link} className="p-6 bg-white rounded-xl shadow hover:shadow-lg transition text-left">
              <h3 className="text-xl font-semibold mb-2">{doc.title}</h3>
              <p className="text-gray-600">{doc.description}</p>
            </a>
          ))}
        </div>
      </div>
    </section>
  )
}
