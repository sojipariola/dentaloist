import { lazy } from 'react'

export const adminRoutes = [
  {
    path: '/admin',
    component: lazy(() => import('@/pages/admin/SystemStats')),
  },
  {
    path: '/admin/users',
    component: lazy(() => import('@/pages/admin/UserManagement')),
  },
  {
    path: '/admin/users/new',
    component: lazy(() => import('@/pages/admin/UserForm')),
  },
  {
    path: '/admin/users/:id/edit',
    component: lazy(() => import('@/pages/admin/UserForm')),
  },
  {
    path: '/admin/roles',
    component: lazy(() => import('@/pages/admin/RoleManagement')),
  },
  {
    path: '/admin/roles/new',
    component: lazy(() => import('@/pages/admin/RoleForm')),
  },
  {
    path: '/admin/roles/:id/edit',
    component: lazy(() => import('@/pages/admin/RoleForm')),
  },
  {
    path: '/admin/system',
    component: lazy(() => import('@/pages/admin/SystemSettings')),
  },
  {
    path: '/admin/audit-logs',
    component: lazy(() => import('@/pages/admin/AuditLogs')),
  },
  {
    path: '/admin/database',
    component: lazy(() => import('@/pages/admin/DatabaseManagement')),
  },
]