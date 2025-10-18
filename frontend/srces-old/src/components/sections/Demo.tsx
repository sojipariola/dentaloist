export default function Demo() {
  return (
    <section id="demo" className="bg-blue-50 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">See Demo in Action</h2>
        <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
          Explore the features of our dental management system with a live interactive demo.
        </p>
        <div className="relative aspect-video rounded-xl overflow-hidden shadow-lg">
          <iframe
            src="https://www.youtube.com/embed/dQw4w9WgXcQ"
            title="Demo Video"
            className="w-full h-full"
            allowFullScreen
          ></iframe>
        </div>
      </div>
    </section>
  )
}
