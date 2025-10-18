import React from 'react'

const API = () => {
  return (
    <section id="api" className="bg-white py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Developer API</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Extend Dentaloist's functionality with our powerful API for custom integrations.
        </p>
        <div className="bg-gray-800 text-white rounded-lg p-8 max-w-3xl mx-auto text-left">
          <div className="mb-6">
            <h3 className="text-xl font-semibold mb-2">RESTful API Endpoints</h3>
            <p className="text-gray-300">Access patient data, appointments, and more through our secure API.</p>
          </div>
          <div className="bg-gray-900 p-4 rounded mb-6 overflow-x-auto">
            <code className="text-sm text-green-400">
              {`// Example API request\nfetch('https://api.dentaloist.com/v1/patients', {\n  headers: {\n    'Authorization': 'Bearer YOUR_API_KEY'\n  }\n})`}
            </code>
          </div>
          <a href="#docs" className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
            View Documentation
          </a>
        </div>
      </div>
    </section>
  )
}

export default API
