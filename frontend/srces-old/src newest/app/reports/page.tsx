'use client'
import { useState } from 'react'
import Link from 'next/link'

interface ReportData {
  revenue: {
    monthly: number[]
    yearly: number
    growth: number
  }
  appointments: {
    total: number
    completed: number
    cancelled: number
    noShow: number
  }
  patients: {
    total: number
    newThisMonth: number
    active: number
    inactive: number
  }
  services: {
    name: string
    count: number
    revenue: number
  }[]
  financial: {
    revenue: number
    expenses: number
    profit: number
    outstanding: number
  }
  trends: {
    month: string
    revenue: number
    appointments: number
    newPatients: number
  }[]
}

export default function Reports() {
  const [dateRange, setDateRange] = useState<'7days' | '30days' | '90days' | 'year'>('30days')
  const [activeTab, setActiveTab] = useState<'overview' | 'financial' | 'appointments' | 'patients' | 'services'>('overview')

  // Mock data - replace with actual API calls
  const reportData: ReportData = {
    revenue: {
      monthly: [12500, 13200, 14500, 15800, 16200, 17500, 18300, 19200, 20100, 21500, 22300, 23800],
      yearly: 238500,
      growth: 12.5
    },
    appointments: {
      total: 347,
      completed: 312,
      cancelled: 22,
      noShow: 13
    },
    patients: {
      total: 1248,
      newThisMonth: 42,
      active: 893,
      inactive: 355
    },
    services: [
      { name: 'Checkups', count: 156, revenue: 15600 },
      { name: 'Cleanings', count: 134, revenue: 20100 },
      { name: 'Fillings', count: 87, revenue: 13050 },
      { name: 'Crowns', count: 23, revenue: 27600 },
      { name: 'Root Canals', count: 15, revenue: 13500 },
      { name: 'Extractions', count: 32, revenue: 6400 },
      { name: 'Whitening', count: 28, revenue: 8400 },
      { name: 'Implants', count: 12, revenue: 36000 }
    ],
    financial: {
      revenue: 238500,
      expenses: 156200,
      profit: 82300,
      outstanding: 42300
    },
    trends: [
      { month: 'Jan', revenue: 12500, appointments: 245, newPatients: 28 },
      { month: 'Feb', revenue: 13200, appointments: 263, newPatients: 31 },
      { month: 'Mar', revenue: 14500, appointments: 278, newPatients: 35 },
      { month: 'Apr', revenue: 15800, appointments: 292, newPatients: 38 },
      { month: 'May', revenue: 16200, appointments: 301, newPatients: 42 },
      { month: 'Jun', revenue: 17500, appointments: 315, newPatients: 45 },
      { month: 'Jul', revenue: 18300, appointments: 327, newPatients: 48 },
      { month: 'Aug', revenue: 19200, appointments: 335, newPatients: 51 },
      { month: 'Sep', revenue: 20100, appointments: 342, newPatients: 53 },
      { month: 'Oct', revenue: 21500, appointments: 355, newPatients: 56 },
      { month: 'Nov', revenue: 22300, appointments: 362, newPatients: 58 },
      { month: 'Dec', revenue: 23800, appointments: 378, newPatients: 62 }
    ]
  }

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount)
  }

  const formatNumber = (num: number) => {
    return new Intl.NumberFormat('en-US').format(num)
  }

  const calculatePercentage = (value: number, total: number) => {
    return ((value / total) * 100).toFixed(1)
  }

  const getGrowthColor = (growth: number) => {
    return growth >= 0 ? 'text-green-600' : 'text-red-600'
  }

  const getGrowthIcon = (growth: number) => {
    return growth >= 0 ? '↗' : '↘'
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
            <p className="text-gray-600 mt-2">Practice performance insights and metrics</p>
          </div>
          <div className="flex items-center space-x-4">
            <select
              value={dateRange}
              onChange={(e) => setDateRange(e.target.value as any)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="7days">Last 7 days</option>
              <option value="30days">Last 30 days</option>
              <option value="90days">Last 90 days</option>
              <option value="year">This Year</option>
            </select>
            <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
              Export Report
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow mb-8">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Overview', icon: '📊' },
              { id: 'financial', label: 'Financial', icon: '💰' },
              { id: 'appointments', label: 'Appointments', icon: '📅' },
              { id: 'patients', label: 'Patients', icon: '👥' },
              { id: 'services', label: 'Services', icon: '🦷' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
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
        <div className="space-y-8">
          {activeTab === 'overview' && (
            <>
              {/* Key Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Total Revenue</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatCurrency(reportData.revenue.yearly)}
                      </p>
                    </div>
                    <div className="text-2xl">💰</div>
                  </div>
                  <div className={`mt-2 text-sm ${getGrowthColor(reportData.revenue.growth)}`}>
                    {getGrowthIcon(reportData.revenue.growth)} {Math.abs(reportData.revenue.growth)}% from last year
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Appointments</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatNumber(reportData.appointments.total)}
                      </p>
                    </div>
                    <div className="text-2xl">📅</div>
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    {reportData.appointments.completed} completed
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Patients</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatNumber(reportData.patients.total)}
                      </p>
                    </div>
                    <div className="text-2xl">👥</div>
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    {reportData.patients.newThisMonth} new this month
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600">Net Profit</p>
                      <p className="text-2xl font-bold text-gray-900">
                        {formatCurrency(reportData.financial.profit)}
                      </p>
                    </div>
                    <div className="text-2xl">📈</div>
                  </div>
                  <div className="mt-2 text-sm text-gray-600">
                    {calculatePercentage(reportData.financial.profit, reportData.financial.revenue)}% margin
                  </div>
                </div>
              </div>

              {/* Revenue Trend Chart */}
              <div className="bg-white rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Revenue Trend</h3>
                <div className="grid grid-cols-12 gap-4 items-end h-64">
                  {reportData.trends.map((month, index) => (
                    <div key={month.month} className="flex flex-col items-center">
                      <div
                        className="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                        style={{
                          height: `${(month.revenue / 25000) * 100}%`,
                          minHeight: '2px'
                        }}
                        title={`${month.month}: ${formatCurrency(month.revenue)}`}
                      />
                      <span className="text-xs text-gray-500 mt-2">{month.month}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Appointment Stats</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Completed</span>
                      <span className="font-medium">
                        {reportData.appointments.completed} ({calculatePercentage(reportData.appointments.completed, reportData.appointments.total)}%)
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Cancelled</span>
                      <span className="font-medium text-yellow-600">
                        {reportData.appointments.cancelled} ({calculatePercentage(reportData.appointments.cancelled, reportData.appointments.total)}%)
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">No-Shows</span>
                      <span className="font-medium text-red-600">
                        {reportData.appointments.noShow} ({calculatePercentage(reportData.appointments.noShow, reportData.appointments.total)}%)
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Patient Overview</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Active Patients</span>
                      <span className="font-medium">
                        {reportData.patients.active} ({calculatePercentage(reportData.patients.active, reportData.patients.total)}%)
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Inactive Patients</span>
                      <span className="font-medium text-gray-600">
                        {reportData.patients.inactive} ({calculatePercentage(reportData.patients.inactive, reportData.patients.total)}%)
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">New This Month</span>
                      <span className="font-medium text-green-600">
                        +{reportData.patients.newThisMonth}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {activeTab === 'financial' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Financial Reports</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Financial Summary */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Financial Summary</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                      <span className="text-gray-700">Total Revenue</span>
                      <span className="font-bold text-green-600">{formatCurrency(reportData.financial.revenue)}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                      <span className="text-gray-700">Total Expenses</span>
                      <span className="font-bold text-red-600">{formatCurrency(reportData.financial.expenses)}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                      <span className="text-gray-700">Net Profit</span>
                      <span className="font-bold text-blue-600">{formatCurrency(reportData.financial.profit)}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-yellow-50 rounded-lg">
                      <span className="text-gray-700">Outstanding Payments</span>
                      <span className="font-bold text-yellow-600">{formatCurrency(reportData.financial.outstanding)}</span>
                    </div>
                  </div>
                </div>

                {/* Profit Margin */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Profit Margin</h3>
                  <div className="flex items-center justify-center">
                    <div className="relative w-48 h-48">
                      <svg className="w-full h-full" viewBox="0 0 100 100">
                        {/* Background circle */}
                        <circle
                          className="text-gray-200"
                          strokeWidth="10"
                          stroke="currentColor"
                          fill="transparent"
                          r="40"
                          cx="50"
                          cy="50"
                        />
                        {/* Progress circle */}
                        <circle
                          className="text-blue-500"
                          strokeWidth="10"
                          strokeLinecap="round"
                          stroke="currentColor"
                          fill="transparent"
                          r="40"
                          cx="50"
                          cy="50"
                          strokeDasharray={2 * Math.PI * 40}
                          strokeDashoffset={2 * Math.PI * 40 * (1 - reportData.financial.profit / reportData.financial.revenue)}
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-2xl font-bold text-gray-900">
                          {calculatePercentage(reportData.financial.profit, reportData.financial.revenue)}%
                        </span>
                      </div>
                    </div>
                  </div>
                  <p className="text-center text-gray-600 mt-4">Net Profit Margin</p>
                </div>
              </div>

              {/* Monthly Revenue */}
              <div className="mt-8">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Revenue</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Month</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Revenue</th>
                        <th className="px-4 py-2 text-left text-sm font-medium text-gray-700">Growth</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {reportData.trends.map((month, index) => {
                        const prevMonth = index > 0 ? reportData.trends[index - 1].revenue : month.revenue
                        const growth = ((month.revenue - prevMonth) / prevMonth) * 100
                        return (
                          <tr key={month.month}>
                            <td className="px-4 py-3 text-sm text-gray-900">{month.month}</td>
                            <td className="px-4 py-3 text-sm text-gray-900">{formatCurrency(month.revenue)}</td>
                            <td className="px-4 py-3 text-sm">
                              <span className={growth >= 0 ? 'text-green-600' : 'text-red-600'}>
                                {growth >= 0 ? '+' : ''}{growth.toFixed(1)}%
                              </span>
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'appointments' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Appointment Analytics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                {/* Appointment Stats */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Appointment Overview</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                      <span>Total Appointments</span>
                      <span className="font-bold">{reportData.appointments.total}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-green-50 rounded-lg">
                      <span>Completed</span>
                      <span className="font-bold text-green-600">{reportData.appointments.completed}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-yellow-50 rounded-lg">
                      <span>Cancelled</span>
                      <span className="font-bold text-yellow-600">{reportData.appointments.cancelled}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-red-50 rounded-lg">
                      <span>No-Shows</span>
                      <span className="font-bold text-red-600">{reportData.appointments.noShow}</span>
                    </div>
                  </div>
                </div>

                {/* Appointment Trends */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Trends</h3>
                  <div className="space-y-4">
                    {reportData.trends.slice(-6).map(month => (
                      <div key={month.month} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{month.month}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${(month.appointments / 400) * 100}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium w-12">{month.appointments}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Cancellation Rate */}
              <div className="bg-yellow-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-yellow-900 mb-2">Cancellation Rate</h3>
                <p className="text-yellow-700 mb-4">
                  {calculatePercentage(reportData.appointments.cancelled + reportData.appointments.noShow, reportData.appointments.total)}% 
                  of appointments were cancelled or resulted in no-shows
                </p>
                <div className="w-full bg-yellow-200 rounded-full h-3">
                  <div
                    className="bg-yellow-500 h-3 rounded-full"
                    style={{ 
                      width: `${calculatePercentage(reportData.appointments.cancelled + reportData.appointments.noShow, reportData.appointments.total)}%` 
                    }}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'patients' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Patient Analytics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                {/* Patient Demographics */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Patient Overview</h3>
                  <div className="space-y-3">
                    <div className="flex justify-between p-3 bg-gray-50 rounded-lg">
                      <span>Total Patients</span>
                      <span className="font-bold">{formatNumber(reportData.patients.total)}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-blue-50 rounded-lg">
                      <span>Active Patients</span>
                      <span className="font-bold text-blue-600">{formatNumber(reportData.patients.active)}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-gray-100 rounded-lg">
                      <span>Inactive Patients</span>
                      <span className="font-bold text-gray-600">{formatNumber(reportData.patients.inactive)}</span>
                    </div>
                    <div className="flex justify-between p-3 bg-green-50 rounded-lg">
                      <span>New This Month</span>
                      <span className="font-bold text-green-600">+{reportData.patients.newThisMonth}</span>
                    </div>
                  </div>
                </div>

                {/* New Patient Acquisition */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">New Patient Trend</h3>
                  <div className="space-y-4">
                    {reportData.trends.slice(-6).map(month => (
                      <div key={month.month} className="flex items-center justify-between">
                        <span className="text-sm text-gray-600">{month.month}</span>
                        <div className="flex items-center space-x-2">
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-green-500 h-2 rounded-full"
                              style={{ width: `${(month.newPatients / 70) * 100}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium w-8">{month.newPatients}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Patient Retention */}
              <div className="bg-blue-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-blue-900 mb-2">Patient Retention Rate</h3>
                <p className="text-blue-700 mb-4">
                  {calculatePercentage(reportData.patients.active, reportData.patients.total)}% 
                  of patients are active and returning
                </p>
                <div className="w-full bg-blue-200 rounded-full h-3">
                  <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{ 
                      width: `${calculatePercentage(reportData.patients.active, reportData.patients.total)}%` 
                    }}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'services' && (
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Service Analytics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                {/* Top Services by Revenue */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Services by Revenue</h3>
                  <div className="space-y-3">
                    {reportData.services
                      .sort((a, b) => b.revenue - a.revenue)
                      .slice(0, 5)
                      .map(service => (
                        <div key={service.name} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <span className="text-sm">{service.name}</span>
                          <span className="font-bold text-green-600">{formatCurrency(service.revenue)}</span>
                        </div>
                      ))}
                  </div>
                </div>

                {/* Top Services by Volume */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Services by Volume</h3>
                  <div className="space-y-3">
                    {reportData.services
                      .sort((a, b) => b.count - a.count)
                      .slice(0, 5)
                      .map(service => (
                        <div key={service.name} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                          <span className="text-sm">{service.name}</span>
                          <span className="font-bold text-blue-600">{service.count} procedures</span>
                        </div>
                      ))}
                  </div>
                </div>
              </div>

              {/* Service Distribution */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Service Distribution</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {reportData.services.map(service => (
                    <div key={service.name} className="bg-gray-50 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{service.name}</span>
                        <span className="text-sm text-gray-600">
                          {calculatePercentage(service.count, reportData.services.reduce((sum, s) => sum + s.count, 0))}%
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{
                            width: `${calculatePercentage(service.count, reportData.services.reduce((sum, s) => sum + s.count, 0))}%`
                          }}
                        />
                      </div>
                      <div className="flex justify-between text-xs text-gray-600 mt-1">
                        <span>{service.count} procedures</span>
                        <span>{formatCurrency(service.revenue)}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}