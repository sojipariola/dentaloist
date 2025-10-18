// src/components/AuthGuard.tsx
import React from 'react'
import { useCurrentUser } from '@/api/hooks/useCurrentUser'

interface AuthGuardProps {
  children: React.ReactNode
  fallback?: React.ReactNode
  requireAuth?: boolean
}

/**
 * 🔐 AuthGuard component
 * 
 * Protects routes that require authentication
 * - If requireAuth=true: Only shows children when user is authenticated
 * - If requireAuth=false: Only shows children when user is NOT authenticated (login pages)
 */
export const AuthGuard: React.FC<AuthGuardProps> = ({ 
  children, 
  fallback = null,
  requireAuth = true 
}) => {
  const { user, loading, isAuthenticated } = useCurrentUser()

  // Show loading state
  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '200px' 
      }}>
        <div>Loading...</div>
      </div>
    )
  }

  // Auth required but user not authenticated
  if (requireAuth && !isAuthenticated) {
    return <>{fallback}</> || (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '200px',
        flexDirection: 'column',
        gap: '10px'
      }}>
        <h3>Authentication Required</h3>
        <p>Please log in to access this page.</p>
        <button 
          onClick={() => window.location.href = '/login'}
          style={{ padding: '10px 20px' }}
        >
          Go to Login
        </button>
      </div>
    )
  }

  // Auth not required but user is authenticated (for login pages)
  if (!requireAuth && isAuthenticated) {
    return <>{fallback}</> || (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '200px',
        flexDirection: 'column',
        gap: '10px'
      }}>
        <h3>Already Logged In</h3>
        <p>You are already authenticated.</p>
        <button 
          onClick={() => window.location.href = '/dashboard'}
          style={{ padding: '10px 20px' }}
        >
          Go to Dashboard
        </button>
      </div>
    )
  }

  // User meets the auth requirements
  return <>{children}</>
}

/**
 * 🎯 Higher-Order Component version of AuthGuard
 */
export const withAuthGuard = <P extends object>(
  Component: React.ComponentType<P>,
  requireAuth: boolean = true,
  fallback?: React.ReactNode
) => {
  return (props: P) => (
    <AuthGuard requireAuth={requireAuth} fallback={fallback}>
      <Component {...props} />
    </AuthGuard>
  )
}