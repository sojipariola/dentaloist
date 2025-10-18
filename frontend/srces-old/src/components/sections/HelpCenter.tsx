export default function HelpCenter() {
  return (
    <section id="help" className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Help Center</h2>
        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
          Need help? Find guides, tutorials, and support resources to get the most out of our platform.
        </p>
        <a href="/support" className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold">
          Visit Help Center
        </a>
      </div>
    </section>
  )
}
