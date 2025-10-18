// src/features/dashboard/DashboardContent


'use client'

import React from 'react'
import { useAuth } from '@/hooks/useAuth'

export const DashboardContent: React.FC = () => {
  const { user, logout } = useAuth()

  return (
    <div className="container mx-auto px-6 py-10">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-800">
          Welcome, {user?.first_name} {user?.last_name} 👋
        </h1>
        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition"
        >
          Logout
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-blue-50 p-6 rounded-xl shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Appointments</h2>
          <p className="text-gray-600">View and manage patient appointments.</p>
        </div>

        <div className="bg-green-50 p-6 rounded-xl shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Patients</h2>
          <p className="text-gray-600">Access patient records and history.</p>
        </div>

        <div className="bg-purple-50 p-6 rounded-xl shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Billing</h2>
          <p className="text-gray-600">Manage invoices and payments.</p>
        </div>

        <div className="bg-orange-50 p-6 rounded-xl shadow hover:shadow-lg transition">
          <h2 className="text-xl font-semibold mb-2">Reports</h2>
          <p className="text-gray-600">Generate practice analytics and insights.</p>
        </div>
      </div>
    </div>
  )
}
