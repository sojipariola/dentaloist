const communitySections = [
  { title: "User Forum", icon: "👥", description: "Share tips, ask questions, and connect with other users.", link: "#forum" },
  { title: "Events & Webinars", icon: "📅", description: "Join our live events and training sessions.", link: "#events" },
  { title: "Feature Requests", icon: "💡", description: "Suggest and vote on new features for Dentaloist.", link: "#feature-requests" },
]

export default function Community() {
  return (
    <section id="community" className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">Join Our Community</h2>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {communitySections.map((c, i) => (
            <div key={i} className="bg-gray-50 p-6 rounded-xl shadow hover:shadow-lg transition">
              <div className="text-3xl mb-4">{c.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{c.title}</h3>
              <p className="text-gray-600 mb-4">{c.description}</p>
              <a href={c.link} className="text-blue-600 font-semibold hover:underline">Learn More →</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
