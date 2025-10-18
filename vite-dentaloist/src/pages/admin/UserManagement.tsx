import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { 
  Users, 
  Plus, 
  Search,
  Filter,
  MoreHorizontal,
  Edit,
  Shield,
  Mail,
  Phone,
  Calendar,
  CheckCircle,
  XCircle
} from 'lucide-react'
import { Button, Input, Card } from '@/components/ui'

// Mock data
const mockUsers = [
  {
    id: 1,
    first_name: 'Sarah',
    last_name: 'Johnson',
    email: 'sarah.johnson@dentalclinic.com',
    phone: '+1 (555) 123-4567',
    role: 'Dentist',
    specialization: 'General Dentistry',
    status: 'active',
    last_login: '2024-01-15T14:30:00Z',
    created_at: '2023-06-10T00:00:00Z',
    is_admin: false
  },
  {
    id: 2,
    first_name: 'Michael',
    last_name: 'Chen',
    email: 'michael.chen@dentalclinic.com',
    phone: '+1 (555) 123-4568',
    role: 'Dentist',
    specialization: 'Orthodontics',
    status: 'active',
    last_login: '2024-01-14T16:45:00Z',
    created_at: '2023-08-15T00:00:00Z',
    is_admin: false
  },
  {
    id: 3,
    first_name: 'Jennifer',
    last_name: 'Martinez',
    email: 'jennifer.martinez@dentalclinic.com',
    phone: '+1 (555) 123-4569',
    role: 'Dental Assistant',
    specialization: '',
    status: 'active',
    last_login: '2024-01-16T09:15:00Z',
    created_at: '2023-11-20T00:00:00Z',
    is_admin: false
  },
  {
    id: 4,
    first_name: 'Robert',
    last_name: 'Wilson',
    email: 'robert.wilson@dentalclinic.com',
    phone: '+1 (555) 123-4570',
    role: 'Receptionist',
    specialization: '',
    status: 'inactive',
    last_login: '2024-01-05T11:20:00Z',
    created_at: '2023-12-01T00:00:00Z',
    is_admin: false
  },
  {
    id: 5,
    first_name: 'Admin',
    last_name: 'User',
    email: 'admin@dentalclinic.com',
    phone: '+1 (555) 123-4571',
    role: 'System Administrator',
    specialization: '',
    status: 'active',
    last_login: '2024-01-16T08:00:00Z',
    created_at: '2023-01-01T00:00:00Z',
    is_admin: true
  }
]

export default function UserManagement() {
  const [searchTerm, setSearchTerm] = useState('')
  const [roleFilter, setRoleFilter] = useState('all')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredUsers = mockUsers.filter(user =>
    `${user.first_name} ${user.last_name}`.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase())
  ).filter(user => 
    (roleFilter === 'all' || user.role === roleFilter) &&
    (statusFilter === 'all' || user.status === statusFilter)
  )

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getStatusColor = (status: string) => {
    const colors = {
      active: 'bg-green-100 text-green-800',
      inactive: 'bg-gray-100 text-gray-800',
      suspended: 'bg-red-100 text-red-800',
    }
    return colors[status as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  const getRoleColor = (role: string) => {
    const colors = {
      'Dentist': 'bg-blue-100 text-blue-800',
      'Dental Assistant': 'bg-purple-100 text-purple-800',
      'Receptionist': 'bg-orange-100 text-orange-800',
      'System Administrator': 'bg-red-100 text-red-800',
      'Hygienist': 'bg-green-100 text-green-800',
    }
    return colors[role as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">User Management</h1>
          <p className="text-gray-600 mt-2">Manage staff accounts and permissions</p>
        </div>
        <Button asChild>
          <Link to="/admin/users/new">
            <Plus className="h-4 w-4 mr-2" />
            Add User
          </Link>
        </Button>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Users</p>
              <p className="text-2xl font-bold text-gray-900">{mockUsers.length}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-lg">
              <Users className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Users</p>
              <p className="text-2xl font-bold text-gray-900">
                {mockUsers.filter(u => u.status === 'active').length}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Dentists</p>
              <p className="text-2xl font-bold text-gray-900">
                {mockUsers.filter(u => u.role === 'Dentist').length}
              </p>
            </div>
            <div className="p-3 bg-purple-100 rounded-lg">
              <Shield className="h-6 w-6 text-purple-600" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Admins</p>
              <p className="text-2xl font-bold text-gray-900">
                {mockUsers.filter(u => u.is_admin).length}
              </p>
            </div>
            <div className="p-3 bg-red-100 rounded-lg">
              <Shield className="h-6 w-6 text-red-600" />
            </div>
          </div>
        </Card>
      </div>

      {/* Search and Filters */}
      <Card className="p-6">
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <Input
              placeholder="Search users by name or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              icon={Search}
            />
          </div>
          <div className="flex flex-wrap gap-2">
            <select
              value={roleFilter}
              onChange={(e) => setRoleFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Roles</option>
              <option value="Dentist">Dentists</option>
              <option value="Dental Assistant">Dental Assistants</option>
              <option value="Receptionist">Receptionists</option>
              <option value="Hygienist">Hygienists</option>
              <option value="System Administrator">Administrators</option>
            </select>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="suspended">Suspended</option>
            </select>
            <Button variant="outline">
              <Filter className="h-4 w-4 mr-2" />
              More Filters
            </Button>
          </div>
        </div>
      </Card>

      {/* Users Table */}
      <Card className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">User</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Contact</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Role</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Status</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Last Login</th>
                <th className="text-left py-4 px-6 text-sm font-medium text-gray-900">Admin</th>
                <th className="text-right py-4 px-6 text-sm font-medium text-gray-900">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {filteredUsers.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50">
                  <td className="py-4 px-6">
                    <div>
                      <div className="font-medium text-gray-900">
                        {user.first_name} {user.last_name}
                      </div>
                      <div className="text-sm text-gray-500">
                        {user.specialization}
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <div className="space-y-1">
                      <div className="flex items-center space-x-2 text-sm text-gray-900">
                        <Mail className="h-4 w-4 text-gray-400" />
                        <span>{user.email}</span>
                      </div>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <Phone className="h-4 w-4 text-gray-400" />
                        <span>{user.phone}</span>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getRoleColor(user.role)}`}>
                      {user.role}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(user.status)}`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-sm text-gray-900">
                    {formatDate(user.last_login)}
                  </td>
                  <td className="py-4 px-6">
                    {user.is_admin ? (
                      <CheckCircle className="h-5 w-5 text-green-500" />
                    ) : (
                      <XCircle className="h-5 w-5 text-gray-300" />
                    )}
                  </td>
                  <td className="py-4 px-6 text-right">
                    <div className="flex justify-end space-x-2">
                      <Button variant="ghost" size="sm" asChild>
                        <Link to={`/admin/users/${user.id}/edit`}>
                          <Edit className="h-4 w-4" />
                        </Link>
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Shield className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredUsers.length === 0 && (
          <div className="p-8 text-center">
            <Users className="h-12 w-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No users found</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm || roleFilter !== 'all' || statusFilter !== 'all'
                ? 'Try adjusting your search or filters'
                : 'Get started by adding your first user'
              }
            </p>
            {!(searchTerm || roleFilter !== 'all' || statusFilter !== 'all') && (
              <Button asChild>
                <Link to="/admin/users/new">
                  <Plus className="h-4 w-4 mr-2" />
                  Add User
                </Link>
              </Button>
            )}
          </div>
        )}
      </Card>
    </div>
  )
}