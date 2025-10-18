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

// Mock user data - in a real app, this would come from authentication
const mockUsers = {
  websiteAdmin: {
    id: 1,
    name: 'Sarah Johnson',
    email: 'sarah@dentaloist.com',
    role: 'website_admin',
    clinicId: null,
    status: 'Active',
    lastLogin: '2 hours ago'
  },
  clinicAdmin: {
    id: 2,
    name: 'Dr. Michael Chen',
    email: 'michael@dentalclinic.com',
    role: 'clinic_admin',
    clinicId: 'clinic-123',
    status: 'Active',
    lastLogin: '1 day ago'
  }
}

export default function AdminDashboard() {
  const [currentUser, setCurrentUser] = useState<User | null>(null)
  const [activeTab, setActiveTab] = useState('overview')
  const router = useRouter()

  useEffect(() => {
    // Simulate authentication check
    const userRole = localStorage.getItem('userRole') || 'website_admin'
    setCurrentUser(userRole === 'website_admin' ? mockUsers.websiteAdmin : mockUsers.clinicAdmin)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('userRole')
    localStorage.removeItem('isLoggedIn')
    router.push('/')
  }

  if (!currentUser) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  const isWebsiteAdmin = currentUser.role === 'website_admin'
  const isClinicAdmin = currentUser.role === 'clinic_admin'

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
                {isWebsiteAdmin && (
                  <>
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
                  </>
                )}
                {isClinicAdmin && (
                  <>
                    <button
                      onClick={() => setActiveTab('appointments')}
                      className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                        activeTab === 'appointments'
                          ? 'border-blue-500 text-gray-900'
                          : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }`}
                    >
                      Appointments
                    </button>
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
                  </>
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
            <div className="flex items-center">
              <div className="mr-4">
                <span className="text-sm text-gray-700">
                  {currentUser.name} ({isWebsiteAdmin ? 'Website Admin' : 'Clinic Admin'})
                </span>
              </div>
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
            {activeTab === 'appointments' && 'Appointment Management'}
            {activeTab === 'patients' && 'Patient Management'}
            {activeTab === 'settings' && 'Settings'}
          </h1>
          <p className="text-gray-600 mt-2">
            {activeTab === 'overview' && 'Welcome to your admin dashboard. Here you can manage your system.'}
            {activeTab === 'users' && 'Manage user accounts and permissions across the platform.'}
            {activeTab === 'clinics' && 'View and manage all dental clinics using the platform.'}
            {activeTab === 'appointments' && 'Manage appointments and scheduling for your clinic.'}
            {activeTab === 'patients' && 'View and manage patient records and information.'}
            {activeTab === 'settings' && 'Configure your account and system settings.'}
          </p>
        </div>

        {/* Dashboard Content */}
        <div className="grid grid-cols-1 gap-6">
          {activeTab === 'overview' && <OverviewTab isWebsiteAdmin={isWebsiteAdmin} isClinicAdmin={isClinicAdmin} />}
          {activeTab === 'users' && isWebsiteAdmin && <UsersTab />}
          {activeTab === 'clinics' && isWebsiteAdmin && <ClinicsTab />}
          {activeTab === 'appointments' && isClinicAdmin && <AppointmentsTab />}
          {activeTab === 'patients' && isClinicAdmin && <PatientsTab />}
          {activeTab === 'settings' && <SettingsTab user={currentUser} />}
        </div>
      </main>
    </div>
  )
}

// Tab Components
function OverviewTab({ isWebsiteAdmin, isClinicAdmin }: { isWebsiteAdmin: boolean; isClinicAdmin: boolean }) {
  const websiteStats: Stat[] = [
    { name: 'Total Users', value: '1,248', change: '+12%' },
    { name: 'Active Clinics', value: '89', change: '+5%' },
    { name: 'Monthly Revenue', value: '$45,231', change: '+8.2%' },
    { name: 'Avg. Session', value: '3.2min', change: '-1.2%' }
  ]

  const clinicStats: Stat[] = [
    { name: 'Today\'s Appointments', value: '24', change: '+3' },
    { name: 'Active Patients', value: '1,287', change: '+12' },
    { name: 'Monthly Revenue', value: '$12,456', change: '+5.2%' },
    { name: 'Available Staff', value: '8', change: '0' }
  ]

  const stats = isWebsiteAdmin ? websiteStats : clinicStats
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
          {isWebsiteAdmin ? (
            <>
              <button className="bg-blue-100 text-blue-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-blue-200">
                Add New User
              </button>
              <button className="bg-green-100 text-green-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-green-200">
                Create Clinic
              </button>
              <button className="bg-purple-100 text-purple-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-purple-200">
                View Reports
              </button>
              <button className="bg-orange-100 text-orange-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-orange-200">
                System Settings
              </button>
            </>
          ) : (
            <>
              <button className="bg-blue-100 text-blue-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-blue-200">
                New Appointment
              </button>
              <button className="bg-green-100 text-green-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-green-200">
                Add Patient
              </button>
              <button className="bg-purple-100 text-purple-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-purple-200">
                Schedule Staff
              </button>
              <button className="bg-orange-100 text-orange-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-orange-200">
                Generate Report
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

function UsersTab() {
  const users: User[] = [
    { id: 1, name: 'Sarah Johnson', email: 'sarah@dentaloist.com', role: 'Website Admin', clinicId: null, status: 'Active', lastLogin: '2 hours ago' },
    { id: 2, name: 'Dr. Michael Chen', email: 'michael@dentalclinic.com', role: 'Clinic Admin', clinicId: 'clinic-123', status: 'Active', lastLogin: '1 day ago' },
    { id: 3, name: 'Emily Rodriguez', email: 'emily@dentalclinic.com', role: 'Dentist', clinicId: 'clinic-123', status: 'Active', lastLogin: '3 days ago' },
    { id: 4, name: 'John Smith', email: 'john@dentalclinic.com', role: 'Receptionist', clinicId: 'clinic-123', status: 'Inactive', lastLogin: '2 weeks ago' }
  ]

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">User Management</h3>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
          Add New User
        </button>
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
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="flex-shrink-0 h-10 w-10">
                        <div className="h-10 w-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <span className="text-blue-600 font-medium">
                            {user.name.split(' ').map((n: string) => n[0]).join('')}
                          </span>
                        </div>
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{user.name}</div>
                        <div className="text-sm text-gray-500">{user.email}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                      {user.role}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                      user.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                    }`}>
                      {user.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {user.lastLogin}
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

function ClinicsTab() {
  const clinics: Clinic[] = [
    { id: 1, name: 'Bright Smile Dental', location: 'New York, NY', patients: 1248, status: 'Active', plan: 'Professional' },
    { id: 2, name: 'Healthy Teeth Clinic', location: 'San Francisco, CA', patients: 876, status: 'Active', plan: 'Enterprise' },
    { id: 3, name: 'Family Dental Care', location: 'Chicago, IL', patients: 543, status: 'Active', plan: 'Starter' },
    { id: 4, name: 'Modern Dentistry', location: 'Austin, TX', patients: 321, status: 'Trial', plan: 'Trial' }
  ]

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
        <h3 className="text-lg font-medium text-gray-900">Clinic Management</h3>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
          Add New Clinic
        </button>
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

function AppointmentsTab() {
  const appointments: Appointment[] = [
    { id: 1, patient: 'John Doe', dentist: 'Dr. Smith', time: '10:00 AM', date: '2024-03-20', type: 'Checkup', status: 'Scheduled' },
    { id: 2, patient: 'Jane Smith', dentist: 'Dr. Johnson', time: '11:30 AM', date: '2024-03-20', type: 'Cleaning', status: 'Scheduled' },
    { id: 3, patient: 'Bob Wilson', dentist: 'Dr. Chen', time: '2:00 PM', date: '2024-03-20', type: 'Filling', status: 'Completed' },
    { id: 4, patient: 'Alice Brown', dentist: 'Dr. Rodriguez', time: '3:30 PM', date: '2024-03-20', type: 'Consultation', status: 'Cancelled' }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900">Today's Appointments</h3>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
            New Appointment
          </button>
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
                    Dentist
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Time
                  </th>
                  <th className="px-6 py-3 bg-gray-50 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Type
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
                {appointments.map((appt) => (
                  <tr key={appt.id}>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{appt.patient}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {appt.dentist}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {appt.time}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {appt.type}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                        appt.status === 'Scheduled' ? 'bg-blue-100 text-blue-800' :
                        appt.status === 'Completed' ? 'bg-green-100 text-green-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {appt.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                      <button className="text-red-600 hover:text-red-900">Cancel</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Appointment Statistics</h3>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Scheduled Today</span>
              <span className="font-medium">12</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Completed Today</span>
              <span className="font-medium">8</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Cancelled Today</span>
              <span className="font-medium">2</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">No-shows</span>
              <span className="font-medium">1</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Schedule</h3>
          <div className="space-y-4">
            <button className="w-full bg-blue-100 text-blue-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-blue-200">
              Schedule New Appointment
            </button>
            <button className="w-full bg-green-100 text-green-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-green-200">
              View Calendar
            </button>
            <button className="w-full bg-purple-100 text-purple-700 px-4 py-3 rounded-lg text-sm font-medium hover:bg-purple-200">
              Generate Schedule Report
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

function PatientsTab() {
  const patients: Patient[] = [
    { id: 1, name: 'John Doe', email: 'john@example.com', phone: '(555) 123-4567', lastVisit: '2024-03-15', status: 'Active' },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '(555) 234-5678', lastVisit: '2024-03-10', status: 'Active' },
    { id: 3, name: 'Bob Wilson', email: 'bob@example.com', phone: '(555) 345-6789', lastVisit: '2024-02-28', status: 'Inactive' },
    { id: 4, name: 'Alice Brown', email: 'alice@example.com', phone: '(555) 456-7890', lastVisit: '2024-03-18', status: 'Active' }
  ]

  const activities: Activity[] = [
    { action: 'New patient registration', user: 'John Doe', time: '2 hours ago' },
    { action: 'Medical records updated', user: 'Jane Smith', time: '4 hours ago' },
    { action: 'Appointment scheduled', user: 'Bob Wilson', time: '1 day ago' },
    { action: 'Treatment plan created', user: 'Alice Brown', time: '2 days ago' }
  ]

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-5 border-b border-gray-200 flex justify-between items-center">
          <h3 className="text-lg font-medium text-gray-900">Patient Records</h3>
          <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
            Add New Patient
          </button>
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
                      <button className="text-blue-600 hover:text-blue-900 mr-3">View</button>
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

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Patient Statistics</h3>
          <div className="space-y-4">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Patients</span>
              <span className="font-medium">1,287</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">New This Month</span>
              <span className="font-medium">42</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Active Patients</span>
              <span className="font-medium">1,024</span>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6 md:col-span-2">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Patient Activity</h3>
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
              <p className="text-sm text-gray-500">
                {user.role === 'website_admin' ? 'Website Administrator' : 'Clinic Administrator'}
              </p>
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