export default function CTA({ onAction }: { onAction: () => void }) {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Get Started?</h2>
        <p className="text-xl mb-12 max-w-2xl mx-auto">
          Join thousands of dental professionals who trust Dentaloist to manage their practice efficiently.
        </p>
        <div className="flex flex-col sm:flex-row justify-center gap-6">
          <button
            onClick={onAction}
            className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition font-semibold text-lg"
          >
            Get Started Free
          </button>
          <a href="#contact" className="border border-blue-600 text-blue-600 px-8 py-4 rounded-lg hover:bg-blue-50 transition font-semibold text-lg">
            Contact Sales
          </a>
        </div>
      </div>
    </section>
  )
}
