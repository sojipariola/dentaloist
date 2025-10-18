'use client'
import { useAuth } from '../lib/auth'
import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function Dashboard() {
  const { user, logout, loading } = useAuth()
  const router = useRouter()
  const [activeTab, setActiveTab] = useState('overview')
  const [stats, setStats] = useState({
    totalPatients: 0,
    appointmentsToday: 0,
    revenueThisMonth: 0,
    pendingTasks: 0
  })

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login')
    }
  }, [user, loading, router])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <Link href="/dashboard" className="flex items-center space-x-2">
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-xl">D</span>
                </div>
                <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{user?.first_name} {user?.last_name}</p>
                <p className="text-sm text-gray-600">{user?.clinic_name || user?.email}</p>
              </div>
              <button
                onClick={logout}
                className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Link href="/patients" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-lg">
                <span className="text-2xl">👥</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Patients</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalPatients}</p>
              </div>
            </div>
          </Link>

          <Link href="/appointments" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 rounded-lg">
                <span className="text-2xl">📅</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Today's Appointments</p>
                <p className="text-2xl font-bold text-gray-900">{stats.appointmentsToday}</p>
              </div>
            </div>
          </Link>

          <Link href="/billing" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <div className="flex items-center">
              <div className="p-3 bg-purple-100 rounded-lg">
                <span className="text-2xl">💰</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
                <p className="text-2xl font-bold text-gray-900">${stats.revenueThisMonth}</p>
              </div>
            </div>
          </Link>

          <Link href="/tasks" className="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <div className="flex items-center">
              <div className="p-3 bg-orange-100 rounded-lg">
                <span className="text-2xl">✅</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending Tasks</p>
                <p className="text-2xl font-bold text-gray-900">{stats.pendingTasks}</p>
              </div>
            </div>
          </Link>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow mb-8">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'patients', label: 'Patients', icon: '👥' },
              { id: 'appointments', label: 'Appointments', icon: '📅' },
              { id: 'billing', label: 'Billing', icon: '💰' },
              { id: 'reports', label: 'Reports', icon: '📈' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow p-6">
          {activeTab === 'overview' && <OverviewTab />}
          {activeTab === 'patients' && <PatientsTab />}
          {activeTab === 'appointments' && <AppointmentsTab />}
          {activeTab === 'billing' && <BillingTab />}
          {activeTab === 'reports' && <ReportsTab />}
        </div>
      </main>
    </div>
  )
}

// Tab Components
function OverviewTab() {
  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Practice Overview</h2>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-blue-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {[
              { action: 'New patient registration', time: '2 hours ago', link: '/patients/123' },
              { action: 'Appointment completed', time: '4 hours ago', link: '/appointments/456' },
              { action: 'Payment received', time: '6 hours ago', link: '/billing/789' }
            ].map((activity, i) => (
              <Link key={i} href={activity.link} className="flex items-center justify-between p-3 bg-white rounded hover:bg-gray-50 transition">
                <div>
                  <p className="font-medium">{activity.action}</p>
                  <p className="text-sm text-gray-600">{activity.time}</p>
                </div>
                <span className="text-green-600">✓</span>
              </Link>
            ))}
          </div>
        </div>

        <div className="bg-green-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 gap-4">
            <Link href="/patients/new" className="bg-white rounded-lg p-4 text-center hover:shadow-md transition">
              <span className="text-2xl block mb-2">➕</span>
              <span className="text-sm font-medium">New Patient</span>
            </Link>
            <Link href="/appointments/new" className="bg-white rounded-lg p-4 text-center hover:shadow-md transition">
              <span className="text-2xl block mb-2">📅</span>
              <span className="text-sm font-medium">New Appointment</span>
            </Link>
            <Link href="/billing" className="bg-white rounded-lg p-4 text-center hover:shadow-md transition">
              <span className="text-2xl block mb-2">💰</span>
              <span className="text-sm font-medium">Process Payment</span>
            </Link>
            <Link href="/reports" className="bg-white rounded-lg p-4 text-center hover:shadow-md transition">
              <span className="text-2xl block mb-2">📊</span>
              <span className="text-sm font-medium">Generate Report</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

function PatientsTab() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Patient Management</h2>
        <Link href="/patients/new" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
          Add New Patient
        </Link>
      </div>
      <div className="bg-gray-50 rounded-lg p-6">
        <p className="text-gray-600">Patient management features will be available soon.</p>
        <Link href="/patients" className="text-blue-600 hover:text-blue-700 mt-4 inline-block">
          View all patients →
        </Link>
      </div>
    </div>
  )
}

function AppointmentsTab() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Appointment Schedule</h2>
        <Link href="/appointments/new" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
          Schedule Appointment
        </Link>
      </div>
      <div className="bg-gray-50 rounded-lg p-6">
        <p className="text-gray-600">Appointment scheduling features will be available soon.</p>
        <Link href="/appointments" className="text-blue-600 hover:text-blue-700 mt-4 inline-block">
          View calendar →
        </Link>
      </div>
    </div>
  )
}

function BillingTab() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Billing & Payments</h2>
        <Link href="/billing/new" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
          Create Invoice
        </Link>
      </div>
      <div className="bg-gray-50 rounded-lg p-6">
        <p className="text-gray-600">Billing features will be available soon.</p>
        <Link href="/billing" className="text-blue-600 hover:text-blue-700 mt-4 inline-block">
          View billing dashboard →
        </Link>
      </div>
    </div>
  )
}

function ReportsTab() {
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Reports & Analytics</h2>
        <Link href="/reports/generate" className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
          Generate Report
        </Link>
      </div>
      <div className="bg-gray-50 rounded-lg p-6">
        <p className="text-gray-600">Reporting features will be available soon.</p>
        <Link href="/reports" className="text-blue-600 hover:text-blue-700 mt-4 inline-block">
          View all reports →
        </Link>
      </div>
    </div>
  )
}