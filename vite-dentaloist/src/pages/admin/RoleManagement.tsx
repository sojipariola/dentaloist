import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Shield, 
  Plus, 
  Search,
  Users,
  CheckCircle,
  XCircle,
  Edit,
  MoreHorizontal
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockRoles = [
  {
    id: 1,
    name: 'System Administrator',
    description: 'Full system access with all permissions',
    user_count: 1,
    permissions: ['all'],
    is_system_role: true,
    is_default: false
  },
  {
    id: 2,
    name: 'Dentist',
    description: 'Clinical staff with patient management and treatment permissions',
    user_count: 2,
    permissions: ['patients:read', 'patients:write', 'appointments:read', 'appointments:write', 'clinical:read', 'clinical:write'],
    is_system_role: false,
    is_default: true
  },
  {
    id: 3,
    name: 'Dental Assistant',
    description: 'Clinical support staff with limited patient access',
    user_count: 1,
    permissions: ['patients:read', 'appointments:read', 'clinical:read'],
    is_system_role: false,
    is_default: false
  },
  {
    id: 4,
    name: 'Receptionist',
    description: 'Front desk staff with appointment and billing access',
    user_count: 1,
    permissions: ['patients:read', 'patients:write', 'appointments:read', 'appointments:write', 'billing:read', 'billing:write'],
    is_system_role: false,
    is_default: false
  },
  {
    id: 5,
    name: 'Hygienist',
    description: 'Dental hygiene specialist with clinical permissions',
    user_count: 0,
    permissions: ['patients:read', 'appointments:read', 'appointments:write', 'clinical:read', 'clinical:write'],
    is_system_role: false,
    is_default: false
  }
]

// Permission categories
const permissionCategories = [
  {
    name: 'Patients',
    permissions: ['patients:read', 'patients:write', 'patients:delete']
  },
  {
    name: 'Appointments',
    permissions: ['appointments:read', 'appointments:write', 'appointments:delete']
  },
  {
    name: 'Clinical',
    permissions: ['clinical:read', 'clinical:write', 'clinical:delete']
  },
  {
    name: 'Billing',
    permissions: ['billing:read', 'billing:write', 'billing:delete']
  },
  {
    name: 'Inventory',
    permissions: ['inventory:read', 'inventory:write', 'inventory:delete']
  },
  {
    name: 'Administration',
    permissions: ['users:read', 'users:write', 'system:read', 'system:write']
  }
]

export default function RoleManagement() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedRole, setSelectedRole] = useState<typeof mockRoles[0] | null>(null)

  const filteredRoles = mockRoles.filter(role =>
    role.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    role.description.toLowerCase().includes(searchTerm.toLowerCase())
  )

  const hasPermission = (role: typeof mockRoles[0], permission: string) => {
    return role.permissions.includes('all') || role.permissions.includes(permission)
  }

  const getPermissionLabel = (permission: string) => {
    const labels: { [key: string]: string } = {
      'patients:read': 'View Patients',
      'patients:write': 'Edit Patients',
      'patients:delete': 'Delete Patients',
      'appointments:read': 'View Appointments',
      'appointments:write': 'Edit Appointments',
      'appointments:delete': 'Delete Appointments',
      'clinical:read': 'View Clinical Records',
      'clinical:write': 'Edit Clinical Records',
      'clinical:delete': 'Delete Clinical Records',
      'billing:read': 'View Billing',
      'billing:write': 'Edit Billing',
      'billing:delete': 'Delete Billing',
      'inventory:read': 'View Inventory',
      'inventory:write': 'Edit Inventory',
      'inventory:delete': 'Delete Inventory',
      'users:read': 'View Users',
      'users:write': 'Edit Users',
      'system:read': 'View System Settings',
      'system:write': 'Edit System Settings',
    }
    return labels[permission] || permission
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Role Management</h1>
          <p className="text-gray-600 mt-2">Manage user roles and permissions</p>
        </div>
        <Button asChild>
          <Link to="/admin/roles/new">
            <Plus className="h-4 w-4 mr-2" />
            New Role
          </Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Roles List */}
        <div className="lg:col-span-1 space-y-4">
          <Card className="p-6">
            <Input
              placeholder="Search roles..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </Card>

          <div className="space-y-3">
            {filteredRoles.map((role) => (
              <Card 
                key={role.id}
                className={`p-4 cursor-pointer transition-colors ${
                  selectedRole?.id === role.id ? 'ring-2 ring-primary-500' : 'hover:bg-gray-50'
                }`}
                onClick={() => setSelectedRole(role)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <h3 className="font-semibold text-gray-900">{role.name}</h3>
                      {role.is_system_role && (
                        <Shield className="h-4 w-4 text-red-500" />
                      )}
                      {role.is_default && (
                        <span className="inline-flex px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                          Default
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{role.description}</p>
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <div className="flex items-center space-x-1">
                        <Users className="h-4 w-4" />
                        <span>{role.user_count} users</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Shield className="h-4 w-4" />
                        <span>{role.permissions.length} permissions</span>
                      </div>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Edit className="h-4 w-4" />
                  </Button>
                </div>
              </Card>
            ))}
          </div>

          {filteredRoles.length === 0 && (
            <Card className="p-8 text-center">
              <Shield className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No roles found</h3>
              <p className="text-gray-600">Try adjusting your search</p>
            </Card>
          )}
        </div>

        {/* Role Details */}
        <div className="lg:col-span-2">
          {selectedRole ? (
            <Card className="p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900">{selectedRole.name}</h2>
                  <p className="text-gray-600 mt-1">{selectedRole.description}</p>
                </div>
                <div className="flex space-x-2">
                  <Button variant="outline" asChild>
                    <Link to={`/admin/roles/${selectedRole.id}/edit`}>
                      <Edit className="h-4 w-4 mr-2" />
                      Edit Role
                    </Link>
                  </Button>
                  {!selectedRole.is_system_role && (
                    <Button variant="outline">
                      Duplicate
                    </Button>
                  )}
                </div>
              </div>

              {/* Role Information */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div>
                  <label className="text-sm font-medium text-gray-500">User Count</label>
                  <p className="text-lg font-semibold text-gray-900">{selectedRole.user_count}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">System Role</label>
                  <p className="text-lg font-semibold text-gray-900">
                    {selectedRole.is_system_role ? 'Yes' : 'No'}
                  </p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Default Role</label>
                  <p className="text-lg font-semibold text-gray-900">
                    {selectedRole.is_default ? 'Yes' : 'No'}
                  </p>
                </div>
              </div>

              {/* Permissions */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Permissions</h3>
                <div className="space-y-6">
                  {permissionCategories.map((category) => (
                    <div key={category.name}>
                      <h4 className="font-medium text-gray-900 mb-3">{category.name}</h4>
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {category.permissions.map((permission) => (
                          <div
                            key={permission}
                            className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg"
                          >
                            {hasPermission(selectedRole, permission) ? (
                              <CheckCircle className="h-5 w-5 text-green-500" />
                            ) : (
                              <XCircle className="h-5 w-5 text-gray-300" />
                            )}
                            <span className="text-sm text-gray-700">
                              {getPermissionLabel(permission)}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center">
              <Shield className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Select a Role</h3>
              <p className="text-gray-600">Choose a role from the list to view details</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}