import React from 'react'

const Help = () => {
  return (
    <section id="help" className="bg-gray-50 py-20">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-4xl font-bold text-gray-800 mb-6">Help Center</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Find answers to common questions and get the support you need.
        </p>
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl">📚</span>
            </div>
            <h3 className="text-lg font-semibold mb-3">Guides & Tutorials</h3>
            <p className="text-gray-600 mb-4">Step-by-step instructions for getting the most out of Dentaloist.</p>
            <a href="#guides" className="text-blue-600 font-semibold hover:underline">Browse guides</a>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl">❓</span>
            </div>
            <h3 className="text-lg font-semibold mb-3">FAQs</h3>
            <p className="text-gray-600 mb-4">Answers to frequently asked questions about Dentaloist.</p>
            <a href="#faqs" className="text-blue-600 font-semibold hover:underline">View FAQs</a>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <span className="text-xl">💬</span>
            </div>
            <h3 className="text-lg font-semibold mb-3">Community Forum</h3>
            <p className="text-gray-600 mb-4">Connect with other Dentaloist users and share tips.</p>
            <a href="#community" className="text-blue-600 font-semibold hover:underline">Join discussion</a>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Help
