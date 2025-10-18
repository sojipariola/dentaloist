// Admin-only route (uses user.is_admin)
<Route 
  path="/admin/users" 
  element={
    <RoleGuard isAdminOnly>
      <AdminUsers />
    </RoleGuard>
  } 
/>

// Role-based route (uses user.roles array)
<Route 
  path="/manage/patients" 
  element={
    <RoleGuard allowedRoles={['admin', 'manager', 'staff']}>
      <PatientManagement />
    </RoleGuard>
  } 
/>

// Permission-based route (uses user.permissions array)  
<Route 
  path="/reports" 
  element={
    <RoleGuard allowedPermissions={['reports:read', 'reports:write']}>
      <Reports />
    </RoleGuard>
  } 
/>

// Tenant/organization required route (uses user.organization_id)
<Route 
  path="/organization/settings" 
  element={
    <RoleGuard requireTenant>
      <OrganizationSettings />
    </RoleGuard>
  } 
/>