// src/app/dashboard/admin/page.tsx - Organization Admin Dashboard
'use client';

import { useState, useEffect } from 'react';
import { Users, Building, DollarSign, Calendar } from 'lucide-react';
import { dashboardApi, organizationsApi } from '@/lib/api';
import { useAuth } from '@/lib/hooks/useAuth';

export default function AdminDashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalStaff: 0,
    totalPatients: 0,
    monthlyRevenue: 0,
    upcomingAppointments: 0,
  });

  useEffect(() => {
    const fetchData = async () => {
      if (user?.organization_id) {
        try {
          const [statsResponse, orgResponse] = await Promise.all([
            dashboardApi.getStats(user.organization_id),
            organizationsApi.getById(user.organization_id)
          ]);
          
          setStats({
            totalStaff: orgResponse.data.users_count || 0,
            totalPatients: statsResponse.data.totalPatients,
            monthlyRevenue: statsResponse.data.revenue,
            upcomingAppointments: statsResponse.data.totalAppointments,
          });
        } catch (error) {
          console.error('Failed to fetch admin data:', error);
        }
      }
    };

    fetchData();
  }, [user]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <Users className="w-8 h-8 text-blue-600 mb-2" />
          <h3 className="text-lg font-semibold">Staff Members</h3>
          <p className="text-2xl font-bold">{stats.totalStaff}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <Users className="w-8 h-8 text-green-600 mb-2" />
          <h3 className="text-lg font-semibold">Total Patients</h3>
          <p className="text-2xl font-bold">{stats.totalPatients}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <DollarSign className="w-8 h-8 text-amber-600 mb-2" />
          <h3 className="text-lg font-semibold">Monthly Revenue</h3>
          <p className="text-2xl font-bold">${stats.monthlyRevenue}</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <Calendar className="w-8 h-8 text-purple-600 mb-2" />
          <h3 className="text-lg font-semibold">Upcoming Appointments</h3>
          <p className="text-2xl font-bold">{stats.upcomingAppointments}</p>
        </div>
      </div>
    </div>
  );
}