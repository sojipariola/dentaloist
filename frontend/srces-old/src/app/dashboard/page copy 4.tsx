// app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { useWidgets } from '@/contexts/WidgetContext';
import { WidgetRenderer } from '@/components/widgets/WidgetRenderer';
import { ProtectedRoute } from '@/components/ProtectedRoute';

interface DashboardStats {
  totalPatients: number;
  totalAppointments: number;
  todayAppointments: number;
  revenue: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    totalPatients: 0,
    totalAppointments: 0,
    todayAppointments: 0,
    revenue: 0
  });
  const [recentAppointments, setRecentAppointments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, hasPermission } = useAuth();
  const { widgets, isLoading, error } = useWidgets();

    if (isLoading) {
    return <div>Loading widgets...</div>;
  }

  if (error) {
    return <div>Error loading widgets: {error}</div>;
  }

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [statsRes, appointmentsRes] = await Promise.all([
        apiClient.get('/dashboard/stats'),
        apiClient.get('/appointments?limit=5&sort=start_time:desc')
      ]);

      if (statsRes.data) setStats(statsRes.data);
      if (appointmentsRes.data) setRecentAppointments(appointmentsRes.data.appointments || []);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <ProtectedRoute requiredPermission="view_dashboard">
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <div className="text-sm text-gray-600">
            Welcome back, {user?.first_name} {user?.last_name}
          </div>
        </div>

        {/* Widgets Section */}
        <h2 className="text-2xl font-semibold">Your Widgets</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 p-6">
          {widgets
            .filter(widget => widget.isVisible)
            .map(widget => (
              <div key={widget.id} className={`widget-${widget.size}`}>
                <WidgetRenderer widget={widget} />
              </div>
            ))}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link href="/patients" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Patients</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.totalPatients}</p>
          </Link>
          
          <Link href="/appointments" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Total Appointments</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.totalAppointments}</p>
          </Link>
          
          <Link href="/appointments?filter=today" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Today's Appointments</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.todayAppointments}</p>
          </Link>
          
          <Link href="/billing" className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
            <h3 className="text-sm font-medium text-gray-600 mb-2">Revenue</h3>
            <p className="text-3xl font-bold text-gray-900">${stats.revenue.toLocaleString()}</p>
          </Link>
        </div>

        {/* Recent Appointments */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Recent Appointments</h2>
          </div>
          <div className="p-6">
            {recentAppointments.length > 0 ? (
              <div className="space-y-4">
                {recentAppointments.map((appt) => (
                  <Link 
                    key={appt.id} 
                    href={`/appointments/${appt.id}`}
                    className="block p-4 hover:bg-gray-50 rounded-lg border transition-colors"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <h4 className="font-medium text-gray-900">{appt.title}</h4>
                        <p className="text-sm text-gray-600">
                          {new Date(appt.start_time).toLocaleDateString()} • 
                          {appt.patient?.first_name} {appt.patient?.last_name}
                        </p>
                      </div>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        appt.status === 'scheduled' ? 'bg-blue-100 text-blue-800' :
                        appt.status === 'completed' ? 'bg-green-100 text-green-800' :
                        appt.status === 'cancelled' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {appt.status}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No recent appointments</p>
            )}
            <Link 
              href="/appointments" 
              className="mt-4 inline-block text-blue-600 hover:text-blue-800 text-sm font-medium"
            >
              View all appointments →
            </Link>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {hasPermission('create_patient') && (
            <Link 
              href="/patients/new" 
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-blue-500"
            >
              <h3 className="font-semibold text-gray-900 mb-2">Add New Patient</h3>
              <p className="text-sm text-gray-600">Register a new patient</p>
            </Link>
          )}
          
          {hasPermission('create_appointment') && (
            <Link 
              href="/appointments/new" 
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-green-500"
            >
              <h3 className="font-semibold text-gray-900 mb-2">Schedule Appointment</h3>
              <p className="text-sm text-gray-600">Book a new appointment</p>
            </Link>
          )}
          
          {hasPermission('view_billing') && (
            <Link 
              href="/billing" 
              className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow border-l-4 border-purple-500"
            >
              <h3 className="font-semibold text-gray-900 mb-2">Process Payments</h3>
              <p className="text-sm text-gray-600">Manage billing and payments</p>
            </Link>
          )}
        </div>
      </div>
    </ProtectedRoute>
  );
}