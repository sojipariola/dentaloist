// src/app/router/guards/AuthGuard.tsx
import React from 'react'
import { useCurrentUser } from '@/api/hooks/useCurrentUser'

interface AuthGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  fallback?: React.ReactNode
}

export const AuthGuard: React.FC<AuthGuardProps> = ({ 
  children, 
  requireAuth = true,
  fallback 
}) => {
  const { loading, isAuthenticated } = useCurrentUser()

  // Show loading state
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Auth required but user not authenticated
  if (requireAuth && !isAuthenticated) {
    return <>{fallback}</> || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h1>
          <p className="text-gray-600 mb-6">Please log in to access this page.</p>
          <a
            href="/login"
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Go to Login
          </a>
        </div>
      </div>
    )
  }

  // Auth not required but user is authenticated (redirect to dashboard)
  if (!requireAuth && isAuthenticated) {
    return <>{fallback}</> || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Already Logged In</h1>
          <p className="text-gray-600 mb-6">You are already authenticated.</p>
          <a
            href="/dashboard"
            className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors"
          >
            Go to Dashboard
          </a>
        </div>
      </div>
    )
  }

  // User meets the auth requirements
  return <>{children}</>
}