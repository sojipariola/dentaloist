// app/dashboard/page.tsx
'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { apiClient } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { ProtectedRoute } from '@/components/ProtectedRoute';

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalPatients: 0,
    totalAppointments: 0,
    todayAppointments: 0,
    revenue: 0
  });
  const [recentAppointments, setRecentAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

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
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <ProtectedRoute requiredPermission="view_dashboard">
      <div className="space-y-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Link href="/patients" className="stats-card">
            <h3>Total Patients</h3>
            <p className="text-3xl font-bold">{stats.totalPatients}</p>
          </Link>
          
          <Link href="/appointments" className="stats-card">
            <h3>Total Appointments</h3>
            <p className="text-3xl font-bold">{stats.totalAppointments}</p>
          </Link>
          
          <Link href="/appointments?filter=today" className="stats-card">
            <h3>Today's Appointments</h3>
            <p className="text-3xl font-bold">{stats.todayAppointments}</p>
          </Link>
          
          <Link href="/billing" className="stats-card">
            <h3>Revenue</h3>
            <p className="text-3xl font-bold">${stats.revenue.toLocaleString()}</p>
          </Link>
        </div>

        {/* Recent Appointments */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold">Recent Appointments</h2>
          </div>
          <div className="p-6">
            {recentAppointments.length > 0 ? (
              <div className="space-y-4">
                {recentAppointments.map((appt: any) => (
                  <Link 
                    key={appt.id} 
                    href={`/appointments/${appt.id}`}
                    className="block p-4 hover:bg-gray-50 rounded-lg border"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <h4 className="font-medium">{appt.title}</h4>
                        <p className="text-sm text-gray-600">
                          {new Date(appt.start_time).toLocaleDateString()} • 
                          {appt.patient?.first_name} {appt.patient?.last_name}
                        </p>
                      </div>
                      <span className={`status-badge status-${appt.status}`}>
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
              className="mt-4 inline-block text-blue-600 hover:text-blue-800"
            >
              View all appointments →
            </Link>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link 
            href="/patients/new" 
            className="action-card"
            style={{ display: hasPermission('create_patient') ? 'block' : 'none' }}
          >
            <h3>Add New Patient</h3>
            <p>Register a new patient</p>
          </Link>
          
          <Link 
            href="/appointments/new" 
            className="action-card"
            style={{ display: hasPermission('create_appointment') ? 'block' : 'none' }}
          >
            <h3>Schedule Appointment</h3>
            <p>Book a new appointment</p>
          </Link>
          
          <Link 
            href="/billing" 
            className="action-card"
            style={{ display: hasPermission('view_billing') ? 'block' : 'none' }}
          >
            <h3>Process Payments</h3>
            <p>Manage billing and payments</p>
          </Link>
        </div>
      </div>
    </ProtectedRoute>
  );
}