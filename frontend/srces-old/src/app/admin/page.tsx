// app/admin/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

// Define types
interface User {
  id: number
  name: string
  email: string
  role: string
  clinicId: string | null
  permissions: string[]
  status?: string
  lastLogin?: string
}

interface Stat {
  name: string
  value: string
  change: string
}

interface Activity {
  action: string
  user: string
  time: string
  patient?: string
}

interface Appointment {
  id: number
  patient: string
  dentist: string
  time: string
  date: string
  type: string
  status: string
}

interface Patient {
  id: number
  name: string
  email: string
  phone: string
  lastVisit: string
  status: string
}

interface Clinic {
  id: number
  name: string
  location: string
  patients: number
  status: string
  plan: string
}

// Define roles and permissions
export const ROLES = {
  SUPER_ADMIN: 'SuperAdmin',
  ORG_ADMIN: 'OrgAdmin',
  DENTIST: 'Dentist',
  LAB_TECH: 'LabTechnician',
  ASSISTANT: 'Assistant',
  BILLING_STAFF: 'BillingStaff',
  RESEARCHER: 'Researcher',
  MODERATOR: 'Moderator'
} as const

export const PERMISSIONS = {
  // Patient permissions
  CREATE_PATIENT: 'create_patient',
  READ_PATIENT: 'read_patient',
  UPDATE_PATIENT: 'update_patient',
  DELETE_PATIENT: 'delete_patient',
  
  // Data permissions
  VIEW_DATA: 'view_data',
  UPLOAD_DATA: 'upload_data',
  EXPORT_DATA: 'export_data',
  
  // Clinical permissions
  DIAGNOSE: 'diagnose',
  TREAT: 'treat',
  DESIGN_RESTORATION: 'design_restoration',
  MANAGE_TREATMENT_PLAN: 'manage_treatment_plan',
  
  // User management
  CREATE_USER: 'create_user',
  READ_USER: 'read_user',
  UPDATE_USER: 'update_user',
  DELETE_USER: 'delete_user',
  
  // Billing permissions
  MANAGE_BILLING: 'manage_billing',
  PROCESS_PAYMENTS: 'process_payments',
  VIEW_FINANCIAL_REPORTS: 'view_financial_reports',
  
  // System permissions
  MANAGE_SETTINGS: 'manage_settings',
  ACCESS_ADMIN_PANEL: 'access_admin_panel',
  MANAGE_CLINICS: 'manage_clinics'
} as const

// Role permissions mapping
export const ROLE_PERMISSIONS: Record<string, string[]> = {
  [ROLES.SUPER_ADMIN]: [
    PERMISSIONS.CREATE_PATIENT,
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.UPDATE_PATIENT,
    PERMISSIONS.DELETE_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.UPLOAD_DATA,
    PERMISSIONS.EXPORT_DATA,
    PERMISSIONS.DIAGNOSE,
    PERMISSIONS.TREAT,
    PERMISSIONS.DESIGN_RESTORATION,
    PERMISSIONS.MANAGE_TREATMENT_PLAN,
    PERMISSIONS.CREATE_USER,
    PERMISSIONS.READ_USER,
    PERMISSIONS.UPDATE_USER,
    PERMISSIONS.DELETE_USER,
    PERMISSIONS.MANAGE_BILLING,
    PERMISSIONS.PROCESS_PAYMENTS,
    PERMISSIONS.VIEW_FINANCIAL_REPORTS,
    PERMISSIONS.MANAGE_SETTINGS,
    PERMISSIONS.ACCESS_ADMIN_PANEL,
    PERMISSIONS.MANAGE_CLINICS
  ],
  [ROLES.ORG_ADMIN]: [
    PERMISSIONS.CREATE_PATIENT,
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.UPDATE_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.UPLOAD_DATA,
    PERMISSIONS.EXPORT_DATA,
    PERMISSIONS.CREATE_USER,
    PERMISSIONS.READ_USER,
    PERMISSIONS.UPDATE_USER,
    PERMISSIONS.MANAGE_BILLING,
    PERMISSIONS.PROCESS_PAYMENTS,
    PERMISSIONS.VIEW_FINANCIAL_REPORTS,
    PERMISSIONS.ACCESS_ADMIN_PANEL,
    PERMISSIONS.MANAGE_CLINICS
  ],
  [ROLES.DENTIST]: [
    PERMISSIONS.CREATE_PATIENT,
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.UPDATE_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.UPLOAD_DATA,
    PERMISSIONS.DIAGNOSE,
    PERMISSIONS.TREAT,
    PERMISSIONS.DESIGN_RESTORATION,
    PERMISSIONS.MANAGE_TREATMENT_PLAN
  ],
  [ROLES.LAB_TECH]: [
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.UPLOAD_DATA,
    PERMISSIONS.DESIGN_RESTORATION
  ],
  [ROLES.ASSISTANT]: [
    PERMISSIONS.CREATE_PATIENT,
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.UPDATE_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.UPLOAD_DATA
  ],
  [ROLES.BILLING_STAFF]: [
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.MANAGE_BILLING,
    PERMISSIONS.PROCESS_PAYMENTS,
    PERMISSIONS.VIEW_FINANCIAL_REPORTS
  ],
  [ROLES.RESEARCHER]: [
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.VIEW_DATA,
    PERMISSIONS.EXPORT_DATA
  ],
  [ROLES.MODERATOR]: [
    PERMISSIONS.READ_PATIENT,
    PERMISSIONS.READ_USER,
    PERMISSIONS.UPDATE_USER,
    PERMISSIONS.VIEW_DATA
  ]
}

// Helper function to check permissions
const hasPermission = (user: User | null, permission: string): boolean => {
  return user?.permissions?.includes(permission) || false
}

// Mock user data - in a real app, this would come from authentication
const mockUsers = {
  superAdmin: {
    id: 1,
    name: 'Sarah Johnson',
    email: 'sarah@dentaloist.com',
    role: ROLES.SUPER_ADMIN,
    clinicId: null,
    permissions: ROLE_PERMISSIONS[ROLES.SUPER_ADMIN],
    status: 'Active',
    lastLogin: '2 hours ago'
  },
  orgAdmin: {
    id: 2,
    name: 'Dr. Michael Chen',
    email: 'michael@dentalclinic.com',
    role: ROLES.ORG_ADMIN,
    clinicId: 'clinic-123',
    permissions: ROLE_PERMISSIONS[ROLES.ORG_ADMIN],
    status: 'Active',
    lastLogin: '1 day ago'
  },
  dentist: {
    id: 3,
    name: 'Dr. Emily Rodriguez',
    email: 'emily@dentalclinic.com',
    role: ROLES.DENTIST,
    clinicId: 'clinic-123',
    permissions: ROLE_PERMISSIONS[ROLES.DENTIST],
    status: 'Active',
    lastLogin: '3 days ago'
  },
  labTech: {
    id: 4,
    name: 'John Smith',
    email: 'john@dentalclinic.com',
    role: ROLES.LAB_TECH,
    clinicId: 'clinic-123',
    permissions: ROLE_PERMISSIONS[ROLES.LAB_TECH],
    status: 'Active',
    lastLogin: '2 weeks ago'
  }
}

export default function AdminDashboard() {
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [activeTab, setActiveTab] = useState('overview')
  const router = useRouter()

  useEffect(() => {
    // Simulate authentication check
    const userRole = localStorage.getItem('userRole') || ROLES.SUPER_ADMIN
    setCurrentUser(
      userRole === ROLES.SUPER_ADMIN ? mockUsers.superAdmin :
      userRole === ROLES.ORG_ADMIN ? mockUsers.orgAdmin :
      userRole === ROLES.DENTIST ? mockUsers.dentist :
      mockUsers.labTech
    )
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('userRole')
    localStorage.removeItem('isLoggedIn')
    router.push('/')
  }

  const handleRoleChange = (role: string) => {
    localStorage.setItem('userRole', role)
    setCurrentUser(
      role === ROLES.SUPER_ADMIN ? mockUsers.superAdmin :
      role === ROLES.ORG_ADMIN ? mockUsers.orgAdmin :
      role === ROLES.DENTIST ? mockUsers.dentist :
      mockUsers.labTech
    )
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center mr-2">
                  <span className="text-white font-bold">D</span>
                </div>
                <span className="text-xl font-bold text-gray-800">Dentaloist Admin</span>
              </div>
              <div className="hidden md:ml-6 md:flex md:space-x-8">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    activeTab === 'overview'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Overview
                </button>
                
                {/* Conditionally show tabs based on permissions */}
                {hasPermission(currentUser, PERMISSIONS.READ_USER) && (
                  <button
                    onClick={() => setActiveTab('users')}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      activeTab === 'users'
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Users
                  </button>
                )}
                
                {hasPermission(currentUser, PERMISSIONS.MANAGE_CLINICS) && (
                  <button
                    onClick={() => setActiveTab('clinics')}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      activeTab === 'clinics'
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Clinics
                  </button>
                )}
                
                {hasPermission(currentUser, PERMISSIONS.READ_PATIENT) && (
                  <button
                    onClick={() => setActiveTab('patients')}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      activeTab === 'patients'
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Patients
                  </button>
                )}
                
                {hasPermission(currentUser, PERMISSIONS.VIEW_FINANCIAL_REPORTS) && (
                  <button
                    onClick={() => setActiveTab('billing')}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      activeTab === 'billing'
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Billing
                  </button>
                )}
                
                <button
                  onClick={() => setActiveTab('settings')}
                  className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                    activeTab === 'settings'
                      ? 'border-blue-500 text-gray-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Settings
                </button>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="mr-4">
                <span className="text-sm text-gray-700">
                  {currentUser.name} ({currentUser.role})
                </span>
              </div>
              
              {/* Role switcher for demo purposes */}
              <select
                value={currentUser.role}
                onChange={(e) => handleRoleChange(e.target.value)}
                className="bg-gray-100 border border-gray-300 rounded-md px-3 py-1 text-sm"
              >
                <option value={ROLES.SUPER_ADMIN}>Super Admin</option>
                <option value={ROLES.ORG_ADMIN}>Org Admin</option>
                <option value={ROLES.DENTIST}>Dentist</option>
                <option value={ROLES.LAB_TECH}>Lab Tech</option>
                <option value={ROLES.ASSISTANT}>Assistant</option>
                <option value={ROLES.BILLING_STAFF}>Billing Staff</option>
                <option value={ROLES.RESEARCHER}>Researcher</option>
                <option value={ROLES.MODERATOR}>Moderator</option>
              </select>
              
              <button
                onClick={handleLogout}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-200"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">
            {activeTab === 'overview' && 'Dashboard Overview'}
            {activeTab === 'users' && 'User Management'}
            {activeTab === 'clinics' && 'Clinic Management'}
            {activeTab === 'patients' && 'Patient Management'}
            {activeTab === 'billing' && 'Billing & Financials'}
            {activeTab === 'settings' && 'Settings'}
          </h1>
          <p className="text-gray-600 mt-2">
            {activeTab === 'overview' && `Welcome to your admin dashboard. You have ${currentUser.permissions.length} permissions as a ${currentUser.role}.`}
            {activeTab === 'users' && 'Manage user accounts and permissions across the platform.'}
            {activeTab === 'clinics' && 'View and manage all dental clinics using the platform.'}
            {activeTab === 'patients' && 'View and manage patient records and information.'}
            {activeTab === 'billing' && 'Manage billing, payments, and financial reports.'}
            {activeTab === 'settings' && 'Configure your account and system settings.'}
          </p>
        </div>

        {/* Dashboard Content */}
        <div className="grid grid-cols-1 gap-6">
          {activeTab === 'overview' && <OverviewTab user={currentUser} />}
          {activeTab === 'users' && hasPermission(currentUser, PERMISSIONS.READ_USER) && <UsersTab user={currentUser} />}
          {activeTab === 'clinics' && hasPermission(currentUser, PERMISSIONS.MANAGE_CLINICS) && <ClinicsTab user={currentUser} />}
          {activeTab === 'patients' && hasPermission(currentUser, PERMISSIONS.READ_PATIENT) && <PatientsTab user={currentUser} />}
          {activeTab === 'billing' && hasPermission(currentUser, PERMISSIONS.VIEW_FINANCIAL_REPORTS) && <BillingTab user={currentUser} />}
          {activeTab === 'settings' && <SettingsTab user={currentUser} />}
        </div>
      </main>
    </div>
  )
}

// Tab Components
function OverviewTab({ user }: { user: User }) {
  const stats: Stat[] = [
    { name: 'Total Patients', value: '1,287', change: '+12%' },
    { name: 'Appointments Today', value: '24', change: '+3' },
    { name: 'Monthly Revenue', value: '$12,456', change: '+5.2%' },
    { name: 'Active Staff', value: '8', change: '0' }
  ]

  const activities: Activity[] = [
    { action: 'New appointment scheduled', user: 'John Doe', time: '2 minutes ago' },
    { action: 'Patient record updated', user: 'Dr. Smith', time: '15 minutes ago' },
    { action: 'New user registered', user: 'Sarah Wilson', time: '1 hour ago' },
    { action: 'Payment processed', user: 'System', time: '2 hours ago' }
  ]

  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                stat.change.includes('+') ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {stat.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* User Permissions */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Your Permissions</h3>
        </div>
        <div className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {user.permissions.map((permission, index) => (
              <div key={index} className="bg-blue-50 text-blue-800 px-3 py-2 rounded-md text-sm">
                {permission.replace(/_/g, ' ')}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {activities.map((activity, index) => (
              <div key={index} className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 text-sm">!</span>
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                  <p className="text-sm text-gray-500">by {activity.user} • {activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {hasPermission(user, PERMISSIONS.CREATE_PATIENT) && (
            <button className="bg-blue-100 text-blue-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-blue-200">
              Add New Patient
            </button>
          )}
          
          {hasPermission(user, PERMISSIONS.CREATE_USER) && (
            <button className="bg-green-100 text-green-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-green-200">
              Create User
            </button>
          )}
          
          {hasPermission(user, PERMISSIONS.VIEW_FINANCIAL_REPORTS) && (
            <button className="bg-purple-100 text-purple-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-purple-200">
              View Reports
            </button>
          )}
          
          {hasPermission(user, PERMISSIONS.MANAGE_SETTINGS) && (
            <button className="bg-orange-100 text-orange-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-orange-200">
              System Settings
            </button>
          )}
          
          {hasPermission(user, PERMISSIONS.DIAGNOSE) && (
            <button className="bg-teal-100 text-teal-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-teal-200">
              New Diagnosis
            </button>
          )}
          
          {hasPermission(user, PERMISSIONS.DESIGN_RESTORATION) && (
            <button className="bg-pink-100 text-pink-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-pink-200">
              Design Restoration
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

function UsersTab({ user }: { user: User }) {
  const users: User[] = [
    { id: 1, name: 'Sarah Johnson', email: 'sarah@dentaloist.com', role: ROLES.SUPER_ADMIN, clinicId: null, permissions: ROLE_PERMISSIONS[ROLES.SUPER_ADMIN], status: 'Active', lastLogin: '2 hours ago' },
    { id: 2, name: 'Dr. Michael Chen', email: 'michael@dentalclinic.com', role: ROLES.ORG_ADMIN, clinicId: 'clinic-123', permissions: ROLE_PERMISSIONS[ROLES.ORG_ADMIN], status: 'Active', lastLogin: '1 day ago' },
    { id: 3, name: 'Dr. Emily Rodriguez', email: 'emily@dentalclinic.com', role: ROLES.DENTIST, clinicId: 'clinic-123', permissions: ROLE_PERMISSIONS[ROLES.DENTIST], status: 'Active', lastLogin: '3 days ago' },
    { id: 4, name: 'John Smith', email: 'john@dentalclinic.com', role: ROLES.LAB_TECH, clinicId: 'clinic-123', permissions: ROLE_PERMISSIONS[ROLES.LAB_TECH], status: 'Inactive', lastLogin: '2 weeks ago' }
  ]

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">User Management</h3>
        {hasPermission(user, PERMISSIONS.CREATE_USER) && (
          <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
            Add New User
          </button>
        )}
      </div>
      <div className="p-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  User
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Role
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Last Login
                </th>
                <th className="px-6 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {users.map((userItem) => (
                <tr key={userItem.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-medium">
                            {userItem.name.split(' ').map((n: string) => n[0]).join('')}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{userItem.name}</div>
                        <div className="text-sm text-gray-500">{userItem.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                      {userItem.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      userItem.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {userItem.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {userItem.lastLogin}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    {hasPermission(user, PERMISSIONS.UPDATE_USER) && (
                      <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                    )}
                    {hasPermission(user, PERMISSIONS.DELETE_USER) && (
                      <button className="text-red-600 hover:text-red-900">Delete</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function ClinicsTab({ user }: { user: User }) {
  const clinics: Clinic[] = [
    { id: 1, name: 'Bright Smile Dental', location: 'New York, NY', patients: 1248, status: 'Active', plan: 'Professional' },
    { id: 2, name: 'Healthy Teeth Clinic', location: 'San Francisco, CA', patients: 876, status: 'Active', plan: 'Enterprise' },
    { id: 3, name: 'Family Dental Care', location: 'Chicago, IL', patients: 543, status: 'Active', plan: 'Starter' },
    { id: 4, name: 'Modern Dentistry', location: 'Austin, TX', patients: 321, status: 'Trial', plan: 'Trial' }
  ]

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-5 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Clinic Management</h3>
      </div>
      <div className="p-6">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Clinic
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Location
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Patients
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Plan
                </th>
                <th className="px-6 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {clinics.map((clinic) => (
                <tr key={clinic.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{clinic.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {clinic.location}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {clinic.patients}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      clinic.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {clinic.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {clinic.plan}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                    <button className="text-red-600 hover:text-red-900">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

function PatientsTab({ user }: { user: User }) {
  const patients: Patient[] = [
    { id: 1, name: 'John Doe', email: 'john@example.com', phone: '(555) 123-4567', lastVisit: '2024-03-15', status: 'Active' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '(555) 234-5678', lastVisit: '2024-03-10', status: 'Active' },
    { id: 3, name: 'Bob Wilson', email: 'bob@example.com', phone: '(555) 345-6789', lastVisit: '2024-02-28', status: 'Inactive' },
    { id: 4, name: 'Alice Brown', email: 'alice@example.com', phone: '(555) 456-7890', lastVisit: '2024-03-18', status: 'Active' }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900">Patient Records</h3>
          {hasPermission(user, PERMISSIONS.CREATE_PATIENT) && (
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
              Add New Patient
            </button>
          )}
        </div>
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Patient
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Contact
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Last Visit
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {patients.map((patient) => (
                  <tr key={patient.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-shrink-0 h-10 w-10">
                          <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-medium">
                              {patient.name.split(' ').map((n: string) => n[0]).join('')}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          <div className="text-sm font-medium text-gray-900">{patient.name}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-500">{patient.email}</div>
                      <div className="text-sm text-gray-500">{patient.phone}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {patient.lastVisit}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        patient.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {patient.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {hasPermission(user, PERMISSIONS.READ_PATIENT) && (
                        <button className="text-blue-600 hover:text-blue-900 mr-3">View</button>
                      )}
                      {hasPermission(user, PERMISSIONS.UPDATE_PATIENT) && (
                        <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                      )}
                      {hasPermission(user, PERMISSIONS.DELETE_PATIENT) && (
                        <button className="text-red-600 hover:text-red-900">Delete</button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

function BillingTab({ user }: { user: User }) {
  const billingData = [
    { id: 1, patient: 'John Doe', service: 'Dental Checkup', amount: '$150', status: 'Paid', date: '2024-03-15' },
    { id: 2, patient: 'Jane Smith', service: 'Teeth Cleaning', amount: '$120', status: 'Pending', date: '2024-03-14' },
    { id: 3, patient: 'Bob Wilson', service: 'Filling', amount: '$250', status: 'Paid', date: '2024-03-13' },
    { id: 4, patient: 'Alice Brown', service: 'Root Canal', amount: '$850', status: 'Insurance', date: '2024-03-12' }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Billing Records</h3>
        </div>
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead>
                <tr>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Patient
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Service
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Amount
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {billingData.map((item) => (
                  <tr key={item.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{item.patient}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {item.service}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {item.amount}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        item.status === 'Paid' ? 'bg-green-100 text-green-800' :
                        item.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {item.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      {hasPermission(user, PERMISSIONS.PROCESS_PAYMENTS) && (
                        <button className="text-blue-600 hover:text-blue-900 mr-3">Process</button>
                      )}
                      <button className="text-blue-600 hover:text-blue-900">View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {hasPermission(user, PERMISSIONS.VIEW_FINANCIAL_REPORTS) && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Revenue This Month</h3>
            <div className="text-3xl font-bold text-gray-800">$12,456</div>
            <p className="text-green-600 text-sm mt-2">+5.2% from last month</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Outstanding Payments</h3>
            <div className="text-3xl font-bold text-gray-800">$3,245</div>
            <p className="text-red-600 text-sm mt-2">23 unpaid invoices</p>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Insurance Claims</h3>
            <div className="text-3xl font-bold text-gray-800">$8,750</div>
            <p className="text-blue-600 text-sm mt-2">15 pending claims</p>
          </div>
        </div>
      )}
    </div>
  )
}

function SettingsTab({ user }: { user: User }) {
  const [notifications, setNotifications] = useState({
    email: true,
    sms: false,
    push: true,
    newsletter: true
  })

  const handleNotificationChange = (key: keyof typeof notifications) => {
    setNotifications(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Profile Information</h3>
        </div>
        <div className="p-6">
          <div className="flex items-center mb-6">
            <div className="flex-shrink-0">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                <span className="text-blue-600 text-xl font-medium">
                  {user.name.split(' ').map((n: string) => n[0]).join('')}
                </span>
              </div>
            </div>
            <div className="ml-4">
              <h4 className="text-lg font-medium text-gray-900">{user.name}</h4>
              <p className="text-gray-500">{user.email}</p>
              <p className="text-sm text-gray-500">{user.role}</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">First Name</label>
              <input
                type="text"
                defaultValue={user.name.split(' ')[0]}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Last Name</label>
              <input
                type="text"
                defaultValue={user.name.split(' ')[1]}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
              <input
                type="email"
                defaultValue={user.email}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
              <input
                type="tel"
                placeholder="(555) 123-4567"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="mt-6">
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition font-semibold">
              Save Changes
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Notification Preferences</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[
              { key: 'email', label: 'Email Notifications', description: 'Receive important updates via email' },
              { key: 'sms', label: 'SMS Notifications', description: 'Receive text message alerts' },
              { key: 'push', label: 'Push Notifications', description: 'Receive browser push notifications' },
              { key: 'newsletter', label: 'Newsletter', description: 'Receive our monthly newsletter' }
            ].map((item) => (
              <div key={item.key} className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{item.label}</p>
                  <p className="text-sm text-gray-500">{item.description}</p>
                </div>
                <button
                  onClick={() => handleNotificationChange(item.key as keyof typeof notifications)}
                  className={`relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 ${
                    notifications[item.key as keyof typeof notifications] ? 'bg-blue-600' : 'bg-gray-200'
                  }`}
                >
                  <span
                    className={`pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200 ${
                      notifications[item.key as keyof typeof notifications] ? 'translate-x-5' : 'translate-x-0'
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Security</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            <button className="w-full text-left py-4 px-6 border border-gray-200 rounded-lg hover:bg-gray-50">
              <p className="font-medium text-gray-900">Change Password</p>
              <p className="text-sm text-gray-500">Update your password regularly to keep your account secure</p>
            </button>
            <button className="w-full text-left py-4 px-6 border border-gray-200 rounded-lg hover:bg-gray-50">
              <p className="font-medium text-gray-900">Two-Factor Authentication</p>
              <p className="text-sm text-gray-500">Add an extra layer of security to your account</p>
            </button>
            <button className="w-full text-left py-4 px-6 border border-gray-200 rounded-lg hover:bg-gray-50">
              <p className="font-medium text-gray-900">Active Sessions</p>
              <p className="text-sm text-gray-500">View and manage your active login sessions</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}