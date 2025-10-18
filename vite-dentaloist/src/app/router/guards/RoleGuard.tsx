// src/app/router/guards/RoleGuard.tsx
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/app/store'

interface RoleGuardProps {
  children: React.ReactNode
  allowedRoles?: string[]
  allowedPermissions?: string[]
  isAdminOnly?: boolean
  requireTenant?: boolean
  fallback?: React.ReactNode
}

export const RoleGuard: React.FC<RoleGuardProps> = ({
  children,
  allowedRoles = [],
  allowedPermissions = [],
  isAdminOnly = false,
  requireTenant = false,
  fallback
}) => {
  const { user, isLoading } = useAuthStore()

  // Show loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // If no user, redirect to login
  if (!user) {
    return <Navigate to="/login" replace />
  }

  // Check admin access - use is_admin from your user object
  if (isAdminOnly && !user.is_admin) {
    return fallback ? <>{fallback}</> : <Navigate to="/dashboard" replace />
  }

  // Check tenant requirement - use organization_id from your user object
  if (requireTenant && !user.organization_id) {
    return fallback ? <>{fallback}</> : (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Organization Required
          </h2>
          <p className="text-gray-600">
            You need to be associated with an organization to access this page.
          </p>
        </div>
      </div>
    )
  }

  // Check role-based access using the actual user.roles array
  if (allowedRoles.length > 0) {
    const hasRequiredRole = allowedRoles.some(role => {
      // Check if user has the role in their roles array
      if (user.roles?.includes(role)) {
        return true
      }
      
      // Admin override - if user is admin, they have access to all roles
      if (user.is_admin) {
        return true
      }
      
      return false
    })
    
    if (!hasRequiredRole) {
      return fallback ? <>{fallback}</> : <Navigate to="/dashboard" replace />
    }
  }

  // Check permission-based access using user.permissions array
  if (allowedPermissions.length > 0) {
    const hasRequiredPermission = allowedPermissions.some(permission => {
      // Check if user has the specific permission
      if (user.permissions?.includes(permission)) {
        return true
      }
      
      // Check for wildcard permission
      if (user.permissions?.includes('*')) {
        return true
      }
      
      // Admin override
      if (user.is_admin) {
        return true
      }
      
      return false
    })
    
    if (!hasRequiredPermission) {
      return fallback ? <>{fallback}</> : <Navigate to="/dashboard" replace />
    }
  }

  return <>{children}</>
}