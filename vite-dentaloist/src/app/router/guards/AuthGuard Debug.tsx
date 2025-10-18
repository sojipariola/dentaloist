// src/app/router/guards/AuthGuard.tsx
import React, { useEffect } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuthStore } from '@/app/store'
import { useCurrentUser } from '@/api/hooks'
import { Loader2 } from 'lucide-react'
import { adaptUser } from '@/utils/userAdapter'

interface AuthGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  redirectTo?: string
}

export const AuthGuard: React.FC<AuthGuardProps> = ({
  children,
  requireAuth = true,
  redirectTo = '/login',
}) => {
  const location = useLocation()
  const { user, isAuthenticated, setUser } = useAuthStore()
  
  console.log('🔐 AuthGuard Debug:', {
    path: location.pathname,
    requireAuth,
    isAuthenticated,
    hasUser: !!user,
    fromPublicRoutes: location.pathname === '/' || location.pathname === '/login'
  })

  // Only fetch current user for protected routes OR if we have an auth token
  const shouldFetchUser = requireAuth || isAuthenticated
  
  const { data: currentUser, isLoading, error } = useCurrentUser(shouldFetchUser)

  console.log('🔐 AuthGuard User Fetch:', {
    shouldFetchUser,
    isLoading,
    hasCurrentUser: !!currentUser,
    error
  })

  // Update store when user data is fetched
  useEffect(() => {
    if (currentUser && !user) {
      console.log('🔐 Setting user in store')
      const adaptedUser = adaptUser(currentUser)
      setUser(adaptedUser)
    }
  }, [currentUser, user, setUser])

  // Show loading spinner only for protected routes that are checking auth
  if (requireAuth && isLoading) {
    console.log('🔐 Showing loading for protected route')
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // For public routes (requireAuth=false), allow access regardless of auth state
  if (!requireAuth) {
    console.log('🔐 Public route - allowing access')
    return <>{children}</>
  }

  // If authentication is required but user is not authenticated, redirect to login
  if (requireAuth && !isAuthenticated) {
    console.log('🔐 Protected route - redirecting to login')
    return <Navigate to={redirectTo} state={{ from: location }} replace />
  }

  console.log('🔐 Protected route - allowing access')
  return <>{children}</>
}