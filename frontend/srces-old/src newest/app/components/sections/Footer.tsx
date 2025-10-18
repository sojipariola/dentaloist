import React from 'react'

const footerSections = [
  {
    title: "Product",
    links: [
      { href: "#features", text: "Features" },
      { href: "#pricing", text: "Pricing" },
      { href: "#demo", text: "Demo" },
      { href: "#api", text: "API" }
    ]
  },
  {
    title: "Company",
    links: [
      { href: "#about", text: "About" },
      { href: "#blog", text: "Blog" },
      { href: "#careers", text: "Careers" },
      { href: "#contact", text: "Contact" }
    ]
  },
  {
    title: "Support",
    links: [
      { href: "#help", text: "Help Center" },
      { href: "#docs", text: "Documentation" },
      { href: "#community", text: "Community" },
      { href: "#status", text: "Status" }
    ]
  }
]

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-12">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <span className="font-bold">D</span>
              </div>
              <span className="text-xl font-bold">Dentaloist</span>
            </div>
            <p className="text-gray-400">Modern dental practice management for the digital age.</p>
          </div>
          
          {footerSections.map((section, index) => (
            <div key={index}>
              <h4 className="font-semibold mb-4">{section.title}</h4>
              <ul className="space-y-2">
                {section.links.map((link, linkIndex) => (
                  <li key={linkIndex}>
                    <a href={link.href} className="text-gray-400 hover:text-white transition">{link.text}</a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Dentaloist. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
