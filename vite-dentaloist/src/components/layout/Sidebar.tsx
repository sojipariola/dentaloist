import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Calendar, 
  FileText, 
  DollarSign, 
  Package,
  Settings,
  Stethoscope,
  ChevronLeft,
  ChevronRight
} from 'lucide-react'
import { useUIStore, useAuthStore } from '@/app/store'
import { clsx } from 'clsx'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Patients', href: '/patients', icon: Users },
  { name: 'Appointments', href: '/appointments', icon: Calendar },
  { name: 'Clinical', href: '/clinical', icon: Stethoscope },
  { name: 'Billing', href: '/billing', icon: DollarSign },
  { name: 'Inventory', href: '/inventory', icon: Package },
  { name: 'Reports', href: '/reports', icon: FileText },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export default function Sidebar() {
  const location = useLocation()
  const { sidebarOpen, toggleSidebar } = useUIStore()
  const { user } = useAuthStore()

  return (
    <div
      className={clsx(
        'fixed inset-y-0 left-0 z-50 bg-white border-r border-gray-200 transition-all duration-300 ease-in-out',
        sidebarOpen ? 'w-64' : 'w-20'
      )}
    >
      {/* Logo */}
      <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200">
        {sidebarOpen ? (
          <div className="flex items-center space-x-2">
            <Stethoscope className="h-6 w-6 text-primary-600" />
            <span className="text-lg font-semibold text-gray-900">Dentaloist</span>
          </div>
        ) : (
          <Stethoscope className="h-6 w-6 text-primary-600 mx-auto" />
        )}
        
        <button
          onClick={toggleSidebar}
          className="p-1 rounded-lg hover:bg-gray-100 transition-colors"
        >
          {sidebarOpen ? (
            <ChevronLeft className="h-4 w-4 text-gray-600" />
          ) : (
            <ChevronRight className="h-4 w-4 text-gray-600" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="mt-4 px-2 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={clsx(
                'group flex items-center rounded-lg px-2 py-2 text-sm font-medium transition-colors',
                isActive
                  ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              )}
            >
              <item.icon
                className={clsx(
                  'flex-shrink-0 h-5 w-5 transition-colors',
                  isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'
                )}
              />
              {sidebarOpen && (
                <span className="ml-3">{item.name}</span>
              )}
            </Link>
          )
        })}
      </nav>

      {/* User info (collapsed) */}
      {!sidebarOpen && user && (
        <div className="absolute bottom-4 left-0 right-0 px-2">
          <div className="flex justify-center">
            <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
              {user.first_name[0]}{user.last_name[0]}
            </div>
          </div>
        </div>
      )}

      {/* User info (expanded) */}
      {sidebarOpen && user && (
        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-gray-50 rounded-lg p-3">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                {user.first_name[0]}{user.last_name[0]}
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {user.first_name} {user.last_name}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user.email}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}