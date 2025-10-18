'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import dynamic from 'next/dynamic'
import { io, Socket } from 'socket.io-client'

// --- Define prop types for sections ---
type HeroProps = {
  isLoggedIn: boolean
  onLogin: () => void
}

type DemoProps = {
  isLoggedIn: boolean
}

type CTAProps = {
  onAction: () => void
}

// --- Dynamic imports with props typing ---
const Hero = dynamic<HeroProps>(() => import('../components/sections/Hero'), { ssr: false })
const Features = dynamic(() => import('../components/sections/Features'), { ssr: false })
const Pricing = dynamic(() => import('../components/sections/Pricing'), { ssr: false })
const Demo = dynamic<DemoProps>(() => import('../components/sections/Demo'), { ssr: false })
const About = dynamic(() => import('../components/sections/About'), { ssr: false })
const Blog = dynamic(() => import('../components/sections/Blog'), { ssr: false })
const Careers = dynamic(() => import('../components/sections/Careers'), { ssr: false })
const API = dynamic(() => import('../components/sections/API'), { ssr: false })
const Help = dynamic(() => import('../components/sections/Help'), { ssr: false })
const Documentation = dynamic(() => import('../components/sections/Documentation'), { ssr: false })
const Community = dynamic(() => import('../components/sections/Community'), { ssr: false })
const Status = dynamic(() => import('../components/sections/Status'), { ssr: false })
const Contact = dynamic(() => import('../components/sections/Contact'), { ssr: false })
const CTA = dynamic<CTAProps>(() => import('../components/sections/CTA'), { ssr: false })
const Footer = dynamic(() => import('../components/sections/Footer'), { ssr: false })

// Widget types
interface WidgetData {
  id: number
  name: string
  value: number
  unit: string
  type: string
}

export default function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [isWidgetOpen, setIsWidgetOpen] = useState(false)
  const [widgets, setWidgets] = useState<WidgetData[]>([])
  const [isConnected, setIsConnected] = useState(false)
  const [loading, setLoading] = useState(true)
  const [socket, setSocket] = useState<Socket | null>(null)

  // Check login status on load
  useEffect(() => {
    const loggedIn = localStorage.getItem('isLoggedIn') === 'true'
    setIsLoggedIn(loggedIn)
  }, [])

  // Initialize Socket.IO connection and fetch widget data
  useEffect(() => {
    // Initialize Socket.IO connection
    const socketInstance = io('http://localhost:5000', {
      transports: ['websocket', 'polling']
    })

    socketInstance.on('connect', () => {
      console.log('Connected to Flask server')
      setIsConnected(true)
    })

    socketInstance.on('disconnect', () => {
      console.log('Disconnected from Flask server')
      setIsConnected(false)
    })

    socketInstance.on('widget_update', (data) => {
      console.log('Widget update received:', data)
      setWidgets(prev => prev.map(widget => 
        widget.id === data.widgetId 
          ? { ...widget, ...data.updates }
          : widget
      ))
    })

    socketInstance.on('connection_response', (data) => {
      console.log('Connection response:', data)
    })

    setSocket(socketInstance)

    const initializeWidgets = async () => {
      try {
        // Fetch initial widget data - CORRECTED ENDPOINT
        const response = await fetch('http://localhost:5000/api/widgets/data')
        if (response.ok) {
          const data = await response.json()
          setWidgets(data.widgets)
        } else {
          console.error('Failed to fetch widgets:', response.status)
        }
      } catch (error) {
        console.error('Error fetching widget data:', error)
      } finally {
        setLoading(false)
      }
    }

    initializeWidgets()

    // Smooth scrolling for anchor links
    const handleAnchorClick = (e: Event) => {
      const target = e.target as HTMLAnchorElement
      if (target.hash && target.pathname === window.location.pathname) {
        e.preventDefault()
        const element = document.querySelector(target.hash)
        if (element) element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const anchors = document.querySelectorAll('a[href^="#"]')
    anchors.forEach(a => a.addEventListener('click', handleAnchorClick as EventListener))

    return () => {
      socketInstance.disconnect()
      anchors.forEach(a => a.removeEventListener('click', handleAnchorClick as EventListener))
    }
  }, [])

  const handleLogout = () => {
    localStorage.setItem('isLoggedIn', 'false')
    setIsLoggedIn(false)
  }

  const handleLogin = () => {
    localStorage.setItem('isLoggedIn', 'true')
    setIsLoggedIn(true)
  }

  const toggleWidget = () => {
    setIsWidgetOpen(!isWidgetOpen)
  }

  const handleWidgetUpdate = async (widgetId: number, newValue: number) => {
    try {
      // CORRECTED ENDPOINT
      const response = await fetch('http://localhost:5000/api/widgets/update', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: widgetId,
          value: newValue,
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to update widget')
      }

      const data = await response.json()
      console.log('Update successful:', data)

    } catch (error) {
      console.error('Error updating widget:', error)
    }
  }

  const sendTestEvent = () => {
    if (socket) {
      socket.emit('widget_event', {
        message: 'Test event from homepage widget',
        timestamp: new Date().toISOString()
      })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 relative">

      {/* Floating Widget Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleWidget}
          className="bg-blue-600 text-white p-4 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 flex items-center justify-center w-14 h-14"
          aria-label="Toggle widget"
        >
          <svg 
            className={`w-6 h-6 transition-transform duration-300 ${isWidgetOpen ? 'rotate-180' : ''}`}
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      {/* Collapsible Widget Panel */}
      {isWidgetOpen && (
        <div className="fixed bottom-20 right-6 z-50 w-80 bg-white rounded-lg shadow-xl border border-gray-200 p-4">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Real-time Dashboard</h3>
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-xs text-gray-500">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>
          </div>
          
          {loading ? (
            <div className="text-center py-4">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="text-sm text-gray-600 mt-2">Loading widgets...</p>
            </div>
          ) : (
            <>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {widgets.map((widget) => (
                  <div key={widget.id} className="bg-gray-50 rounded-lg p-3 border border-gray-200">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">{widget.name}</span>
                      <span className="text-xs px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                        {widget.type}
                      </span>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-bold text-blue-600">
                        {widget.value}
                        <span className="text-sm text-gray-500 ml-1">{widget.unit}</span>
                      </span>
                      
                      {widget.type === 'control' && (
                        <div className="flex space-x-2">
                          <input
                            type="number"
                            value={widget.value}
                            onChange={(e) => {
                              const newValue = Number(e.target.value);
                              setWidgets(prev => prev.map(w => 
                                w.id === widget.id ? { ...w, value: newValue } : w
                              ));
                            }}
                            className="w-16 px-2 py-1 text-sm border border-gray-300 rounded"
                          />
                          <button
                            onClick={() => handleWidgetUpdate(widget.id, widget.value)}
                            className="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                          >
                            Update
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="mt-4 pt-4 border-t border-gray-200">
                <div className="flex justify-between items-center">
                  <button
                    onClick={sendTestEvent}
                    className="px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700"
                    disabled={!isConnected}
                  >
                    Test Connection
                  </button>
                  <span className="text-xs text-gray-500">
                    {widgets.length} widget{widgets.length !== 1 ? 's' : ''}
                  </span>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* Navigation */}
      <nav className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">D</span>
            </div>
            <span className="text-2xl font-bold text-gray-800">Dentaloist</span>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="#features" className="text-gray-600 hover:text-blue-600 transition">Features</a>
            <a href="#about" className="text-gray-600 hover:text-blue-600 transition">About</a>
            <a href="#contact" className="text-gray-600 hover:text-blue-600 transition">Contact</a>
          </div>
          <div className="flex space-x-4">
            {isLoggedIn ? (
              <>
                <Link href="/dashboard" className="text-blue-600 hover:text-blue-700 font-medium">Dashboard</Link>
                <Link href="/appointments" className="text-blue-600 hover:text-blue-700 font-medium">Appointments</Link>
                <Link href="/patients" className="text-blue-600 hover:text-blue-700 font-medium">Patients</Link>
                <button 
                  onClick={handleLogout}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition shadow-md"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button 
                  onClick={handleLogin}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Login
                </button>
                <button 
                  onClick={handleLogin}
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition shadow-md"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Sections */}
      <Hero isLoggedIn={isLoggedIn} onLogin={handleLogin} />
      <Features />
      <Pricing />
      <Demo isLoggedIn={isLoggedIn} />
      <About />
      <Blog />
      <Careers />
      <API />
      <Help />
      <Documentation />
      <Community />
      <Status />
      <Contact />
      {!isLoggedIn && <CTA onAction={handleLogin} />}

      {/* Footer */}
      <Footer />
    </div>
  )
}