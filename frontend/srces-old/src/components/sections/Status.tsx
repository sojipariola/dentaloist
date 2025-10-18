const statusItems = [
  { label: "Web Application", status: "Operational", color: "green" },
  { label: "API Services", status: "Operational", color: "green" },
  { label: "Database", status: "Operational", color: "green" },
  { label: "Payment Processing", status: "Operational", color: "green" },
]

export default function Status() {
  return (
    <section id="status" className="py-20 bg-gray-50">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-12">System Status</h2>
        <div className="bg-white rounded-xl p-8 shadow max-w-2xl mx-auto text-left">
          <div className="flex justify-between mb-6">
            <span className="font-semibold text-lg">All Systems Operational</span>
            <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Online</span>
          </div>
          <div className="space-y-4">
            {statusItems.map((item, i) => (
              <div key={i} className="flex justify-between">
                <span>{item.label}</span>
                <span className={`px-3 py-1 rounded-full text-sm ${item.color === "green" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"}`}>
                  {item.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
