// app/dashboard/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { 
  Calendar, 
  Users, 
  DollarSign, 
  Activity,
  Plus,
  Search,
  Filter
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import { DashboardStats } from '@/components/dashboard/DashboardStats';
import { RecentAppointments } from '@/components/dashboard/RecentAppointments';
import { QuickActions } from '@/components/dashboard/QuickActions';
import { PatientOverview } from '@/components/dashboard/PatientOverview';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalPatients: 0,
    totalAppointments: 0,
    revenue: 0,
    pendingTasks: 0,
  });

  useEffect(() => {
    // Fetch dashboard stats
    const fetchStats = async () => {
      // Simulated data
      setStats({
        totalPatients: 1247,
        totalAppointments: 48,
        revenue: 12540,
        pendingTasks: 12,
      });
    };

    fetchStats();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-gray-600">Here's what's happening with your practice today.</p>
        </div>
        <div className="flex space-x-4">
          <button className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-4 h-4" />
            <span>New Appointment</span>
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <DashboardStats stats={stats} />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Recent Appointments */}
          <RecentAppointments />
          
          {/* Patient Overview */}
          <PatientOverview />
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Quick Actions */}
          <QuickActions />
          
          {/* Upcoming Schedule */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Upcoming Schedule
            </h3>
            {/* Schedule content */}
          </div>
        </div>
      </div>
    </div>
  );
}