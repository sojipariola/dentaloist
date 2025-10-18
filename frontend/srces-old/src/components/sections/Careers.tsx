const jobOpenings = [
  { title: "Dental Software Developer", location: "Remote", link: "#" },
  { title: "Product Manager", location: "London, UK", link: "#" },
  { title: "Customer Support Specialist", location: "Remote", link: "#" },
]

export default function Careers() {
  return (
    <section id="careers" className="py-20 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">Join Our Team</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {jobOpenings.map((job, i) => (
            <div key={i} className="p-6 bg-gray-50 rounded-xl shadow hover:shadow-lg transition">
              <h3 className="text-2xl font-semibold text-gray-800 mb-2">{job.title}</h3>
              <p className="text-gray-600 mb-4">{job.location}</p>
              <a href={job.link} className="text-blue-600 font-semibold hover:underline">Apply Now →</a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
