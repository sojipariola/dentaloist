// components/ProtectedRoute.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { PermissionCheck, UserRole } from '@/types';

interface ProtectedRouteProps {
  children: React.ReactNode;
  // Permission checks
  requiredPermission?: string;
  requiredPermissions?: string[];
  requireAllPermissions?: boolean;
  
  // Role checks
  requiredRole?: UserRole | string;
  requiredRoles?: (UserRole | string)[];
  requireAllRoles?: boolean;
  
  // Organization checks
  requiredOrganizationId?: number;
  
  // Access control
  allowSuperAdmin?: boolean;
  allowOrgAdmin?: boolean;
  
  // UI
  fallback?: React.ReactNode;
  redirectTo?: string;
  showLoading?: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  // Permission checks
  requiredPermission, 
  requiredPermissions,
  requireAllPermissions = true,
  
  // Role checks
  requiredRole,
  requiredRoles,
  requireAllRoles = true,
  
  // Organization checks
  requiredOrganizationId,
  
  // Access control
  allowSuperAdmin = true,
  allowOrgAdmin = true,
  
  // UI
  fallback,
  redirectTo = '/unauthorized',
  showLoading = true
}) => {
  const { 
    user, 
    isLoading, 
    isAuthenticated, 
    checkPermissions, 
    hasAnyRole, 
    hasAllRoles,
    isSuperAdmin,
    isOrgAdmin,
    canAccessOrganization 
  } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading && showLoading) {
    return <div className="loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  // Check organization access
  if (requiredOrganizationId && !canAccessOrganization(requiredOrganizationId)) {
    if (fallback) return fallback;
    router.push(redirectTo);
    return null;
  }

  // Check role-based access
  let hasRequiredRole = true;
  
  if (requiredRole || requiredRoles) {
    const rolesToCheck = requiredRole ? [requiredRole] : requiredRoles || [];
    
    if (requireAllRoles) {
      hasRequiredRole = hasAllRoles(rolesToCheck);
    } else {
      hasRequiredRole = hasAnyRole(rolesToCheck);
    }
  }

  // Check permission-based access
  let hasRequiredPermission = true;
  
  if (requiredPermission || requiredPermissions) {
    const permissionCheck: PermissionCheck = {
      requiredPermission,
      requiredPermissions,
      requireAll: requireAllPermissions,
    };

    const result = checkPermissions(permissionCheck);
    hasRequiredPermission = result.hasPermission;
  }

  // Allow super admin to bypass most restrictions
  const isBypassAllowed = (allowSuperAdmin && isSuperAdmin()) || 
                         (allowOrgAdmin && isOrgAdmin());

  const hasAccess = isBypassAllowed || (hasRequiredRole && hasRequiredPermission);

  if (!hasAccess) {
    if (fallback) return fallback;
    router.push(redirectTo);
    return null;
  }

  return <>{children}</>;
};


/**
 * 
Usage Examples
1. Role-based Protection
typescript
// Only dentists and assistants can access
<ProtectedRoute requiredRoles={[UserRole.DENTIST, UserRole.ASSISTANT]} requireAllRoles={false}>
  <DentalToolsPage />
</ProtectedRoute>

// Only org admins (super admin can bypass)
<ProtectedRoute requiredRole={UserRole.ORG_ADMIN} allowSuperAdmin={true}>
  <OrganizationSettings />
</ProtectedRoute>
2. Permission-based Protection
typescript
// User needs both permissions
<ProtectedRoute 
  requiredPermissions={['view_patient_records', 'edit_patient_records']} 
  requireAllPermissions={true}
>
  <PatientRecords />
</ProtectedRoute>

// User needs at least one permission
<ProtectedRoute 
  requiredPermissions={['create_appointment', 'manage_schedule']} 
  requireAllPermissions={false}
>
  <SchedulingPage />
</ProtectedRoute>
3. Organization-based Protection
typescript
// Only users from specific organization
<ProtectedRoute requiredOrganizationId={123}>
  <ClinicDashboard />
</ProtectedRoute>
4. Complex Access Control
typescript
// Multiple conditions
<ProtectedRoute
  requiredRole={UserRole.DENTIST}
  requiredPermissions={['perform_procedures', 'prescribe_medications']}
  requiredOrganizationId={currentClinicId}
  allowSuperAdmin={true}
  fallback={<CustomAccessDenied message="Dentist access required" />}
>
  <TreatmentRoom />
</ProtectedRoute>
5. In-component Checks
typescript
const { hasPermission, isDentist, canAccessOrganization } = useAuth();

const canEditPatient = hasPermission('edit_patient_records') && 
                     (isDentist() || isOrgAdmin()) &&
                     canAccessOrganization(patient.organization_id);

{canEditPatient && <EditPatientButton />}
This implementation provides comprehensive access control that works with your specific user 
type structure, including role-based, permission-based, and organization-based access controls.
 */