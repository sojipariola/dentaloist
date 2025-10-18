export default function ApiSection() {
  return (
    <section id="api" className="bg-blue-50 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Developer API</h2>
        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
          Integrate our dental practice platform with your tools and workflow using our secure and RESTful API.
        </p>
        <a href="/docs" className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold">
          Explore Documentation
        </a>
      </div>
    </section>
  )
}
