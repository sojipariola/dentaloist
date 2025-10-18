import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Bell, 
  Search, 
  Menu, 
  LogOut, 
  User, 
  Settings,
  Shield
} from 'lucide-react'
import { useUIStore, useAuthStore } from '@/app/store'
import { useLogout } from '@/api/hooks'
import { Button } from '@/components/ui'

export default function Navbar() {
  const { sidebarOpen, setSidebarOpen } = useUIStore()
  const { user, logout: storeLogout } = useAuthStore()
  const logoutMutation = useLogout()
  const [showUserMenu, setShowUserMenu] = useState(false)

  const handleLogout = async () => {
    try {
      await logoutMutation.mutateAsync()
      storeLogout()
    } catch (error) {
      console.error('Logout failed:', error)
      // Force logout even if API call fails
      storeLogout()
    }
  }

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Left side */}
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors lg:hidden"
            >
              <Menu className="h-5 w-5 text-gray-600" />
            </button>
            
            {/* Search */}
            <div className="relative max-w-md w-full hidden md:block">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-4 w-4 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Right side */}
          <div className="flex items-center space-x-4">
            {/* Notifications */}
            <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors relative">
              <Bell className="h-5 w-5 text-gray-600" />
              <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full border-2 border-white"></span>
            </button>

            {/* User menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {user?.first_name[0]}{user?.last_name[0]}
                </div>
                <div className="hidden md:block text-left">
                  <p className="text-sm font-medium text-gray-900">
                    {user?.first_name} {user?.last_name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {user?.is_admin ? 'Administrator' : 'User'}
                  </p>
                </div>
              </button>

              {/* User dropdown */}
              {showUserMenu && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
                  <Link
                    to="/profile"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setShowUserMenu(false)}
                  >
                    <User className="h-4 w-4 mr-3" />
                    Your Profile
                  </Link>
                  
                  <Link
                    to="/settings"
                    className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    onClick={() => setShowUserMenu(false)}
                  >
                    <Settings className="h-4 w-4 mr-3" />
                    Settings
                  </Link>

                  {user?.is_admin && (
                    <Link
                      to="/admin"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <Shield className="h-4 w-4 mr-3" />
                      Admin Panel
                    </Link>
                  )}
                  // Add admin links to the user dropdown
                  {user?.is_admin && (
                    <Link
                      to="/admin"
                      className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      onClick={() => setShowUserMenu(false)}
                    >
                      <Shield className="h-4 w-4 mr-3" />
                      Admin Panel
                    </Link>
                  )}

                  <div className="border-t border-gray-200 my-1"></div>

                  <button
                    onClick={handleLogout}
                    className="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    <LogOut className="h-4 w-4 mr-3" />
                    Sign out
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Overlay for mobile menu */}
      {showUserMenu && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowUserMenu(false)}
        />
      )}
    </header>
  )
}