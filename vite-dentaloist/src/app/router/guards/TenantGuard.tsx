import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/app/store'

interface TenantGuardProps {
  children: React.ReactNode
  requireTenant?: boolean
}

export const TenantGuard: React.FC<TenantGuardProps> = ({
  children,
  requireTenant = true,
}) => {
  const { user } = useAuthStore()

  if (!user) {
    return <Navigate to="/login" replace />
  }

  // Check if user has a tenant (for multi-tenant features)
  if (requireTenant && !user.tenant_id) {
    return (
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

  return <>{children}</>
}