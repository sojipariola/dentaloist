const blogPosts = [
  { title: "5 Tips for Efficient Dental Scheduling", link: "#" },
  { title: "How Digital Records Improve Patient Care", link: "#" },
  { title: "Billing Automation for Modern Practices", link: "#" },
]

export default function Blog() {
  return (
    <section id="blog" className="bg-gray-50 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">From Our Blog</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {blogPosts.map((post, i) => (
            <div key={i} className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
              <h3 className="text-2xl font-semibold text-gray-800 mb-4">{post.title}</h3>
              <a href={post.link} className="text-blue-600 font-semibold hover:underline">Read More →</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
