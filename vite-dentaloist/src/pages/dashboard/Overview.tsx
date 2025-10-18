import React from 'react'
import { Link } from 'react-router-dom'
import { 
  Users, 
  Calendar, 
  DollarSign, 
  Package, 
  Plus,
  ArrowUp,
  ArrowDown
} from 'lucide-react'
import { useAuthStore } from '@/app/store'
import { usePatientStats } from '@/api/hooks'
import { Card, Button } from '@/components/ui'

export default function Overview() {
  const { user } = useAuthStore()
  const { data: stats, isLoading } = usePatientStats()

  const quickActions = [
    {
      title: 'Add Patient',
      description: 'Register new patient',
      icon: Users,
      href: '/patients/new',
      color: 'blue'
    },
    {
      title: 'Schedule Appointment',
      description: 'Book new appointment',
      icon: Calendar,
      href: '/appointments/new',
      color: 'green'
    },
    {
      title: 'Create Invoice',
      description: 'Generate new invoice',
      icon: DollarSign,
      href: '/billing/invoices/new',
      color: 'yellow'
    },
    {
      title: 'Manage Inventory',
      description: 'View stock levels',
      icon: Package,
      href: '/inventory',
      color: 'purple'
    }
  ]

  const getColorClasses = (color: string) => {
    const colors = {
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      yellow: 'bg-yellow-500',
      purple: 'bg-purple-500'
    }
    return colors[color as keyof typeof colors] || 'bg-gray-500'
  }

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-gray-600 mt-2">Loading dashboard data...</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i} className="p-6 animate-pulse">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gray-200 rounded-lg"></div>
                <div className="ml-4 flex-1">
                  <div className="h-4 bg-gray-200 rounded w-20 mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded w-12"></div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Welcome section */}
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-gray-600 mt-2">
            Here's what's happening with your practice today.
          </p>
        </div>
        <Button asChild>
          <Link to="/appointments/new">
            <Plus className="h-4 w-4 mr-2" />
            New Appointment
          </Link>
        </Button>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Patients</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.total_patients || 0}
              </p>
              <div className="flex items-center mt-1">
                <ArrowUp className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600">+12% this month</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses('blue')}`}>
              <Users className="h-6 w-6 text-white" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Today's Appointments</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.today_appointments || 0}
              </p>
              <div className="flex items-center mt-1">
                <Calendar className="h-3 w-3 text-blue-500 mr-1" />
                <span className="text-xs text-gray-600">Scheduled today</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses('green')}`}>
              <Calendar className="h-6 w-6 text-white" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Monthly Revenue</p>
              <p className="text-2xl font-bold text-gray-900">
                ${stats?.monthly_revenue ? (stats.monthly_revenue / 100).toFixed(2) : '0.00'}
              </p>
              <div className="flex items-center mt-1">
                <ArrowUp className="h-3 w-3 text-green-500 mr-1" />
                <span className="text-xs text-green-600">+8% from last month</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses('yellow')}`}>
              <DollarSign className="h-6 w-6 text-white" />
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending Tasks</p>
              <p className="text-2xl font-bold text-gray-900">
                {stats?.pending_tasks || 0}
              </p>
              <div className="flex items-center mt-1">
                <ArrowDown className="h-3 w-3 text-red-500 mr-1" />
                <span className="text-xs text-red-600">-3 from yesterday</span>
              </div>
            </div>
            <div className={`p-3 rounded-lg ${getColorClasses('purple')}`}>
              <Package className="h-6 w-6 text-white" />
            </div>
          </div>
        </Card>
      </div>

      {/* Quick actions */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => (
            <Link
              key={action.title}
              to={action.href}
              className="block p-4 border-2 border-dashed border-gray-300 rounded-lg text-gray-600 hover:border-gray-400 hover:text-gray-700 transition-colors text-center group"
            >
              <div className={`inline-flex p-3 rounded-lg ${getColorClasses(action.color)} mb-3 group-hover:scale-110 transition-transform`}>
                <action.icon className="h-6 w-6 text-white" />
              </div>
              <div className="text-sm font-medium">{action.title}</div>
              <div className="text-xs text-gray-500 mt-1">{action.description}</div>
            </Link>
          ))}
        </div>
      </Card>

      {/* Recent activity placeholder */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Appointments</h3>
          <div className="text-center text-gray-500 py-8">
            <Calendar className="h-12 w-12 mx-auto mb-2 text-gray-300" />
            <p>No recent appointments</p>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Patient Activity</h3>
          <div className="text-center text-gray-500 py-8">
            <Users className="h-12 w-12 mx-auto mb-2 text-gray-300" />
            <p>No recent patient activity</p>
          </div>
        </Card>
      </div>
    </div>
  )
}
