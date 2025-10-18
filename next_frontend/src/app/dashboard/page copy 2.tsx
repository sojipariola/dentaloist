// next_frontend/src/app/dashboard/page.tsx

'use client';

import { useState, useEffect } from 'react';
import { 
  Calendar, 
  Users, 
  DollarSign, 
  Activity,
  Plus,
  Building
} from 'lucide-react';
import { motion } from 'framer-motion';
import { useAuth } from '@/lib/hooks/useAuth';
import { DashboardStats } from '@/components/dashboard/DashboardStats';
import { RecentAppointments } from '@/components/dashboard/RecentAppointments';
import { QuickActions } from '@/components/dashboard/QuickActions';
import { dashboardApi, organizationsApi } from '@/lib/api';
import { Organization } from '@/types';

interface DashboardData {
  totalPatients: number;
  totalAppointments: number;
  revenue: number;
  pendingTasks: number;
  organization?: Organization;
}

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardData>({
    totalPatients: 0,
    totalAppointments: 0,
    revenue: 0,
    pendingTasks: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [organization, setOrganization] = useState<Organization | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!user?.organization_id) return;

      try {
        // Fetch organization details
        const orgResponse = await organizationsApi.getById(user.organization_id);
        const organizationData = orgResponse.data;
        setOrganization(organizationData);

        // Fetch dashboard stats
        const statsResponse = await dashboardApi.getStats(user.organization_id);
        setStats({
          ...statsResponse.data,
          organization: organizationData
        });

      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
        // Fallback to mock data if API fails
        setStats({
          totalPatients: 1247,
          totalAppointments: 48,
          revenue: 12540,
          pendingTasks: 12,
        });
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.first_name}!
          </h1>
          <p className="text-gray-600">
            {organization ? (
              <span className="flex items-center">
                <Building className="w-4 h-4 mr-2" />
                {organization.name} • {organization.type.replace('_', ' ')}
              </span>
            ) : (
              "Here's what's happening with your practice today."
            )}
          </p>
        </div>
        <div className="flex space-x-4">
          <button className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
            <Plus className="w-4 h-4" />
            <span>New Appointment</span>
          </button>
        </div>
      </div>

      {/* Organization Stats */}
      {organization && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-sm text-blue-600 font-medium">Plan</div>
              <div className="text-lg font-semibold text-blue-800 capitalize">
                {organization.subscription_plan}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-blue-600 font-medium">Staff Limit</div>
              <div className="text-lg font-semibold text-blue-800">
                {organization.max_staff}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-blue-600 font-medium">Patient Limit</div>
              <div className="text-lg font-semibold text-blue-800">
                {organization.max_patients}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-blue-600 font-medium">Status</div>
              <div className={`text-lg font-semibold ${
                organization.is_active ? 'text-green-600' : 'text-red-600'
              }`}>
                {organization.is_active ? 'Active' : 'Inactive'}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Stats Grid */}
      <DashboardStats stats={stats} />

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column */}
        <div className="lg:col-span-2 space-y-6">
          <RecentAppointments organizationId={user?.organization_id} />
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          <QuickActions organizationId={user?.organization_id} />
        </div>
      </div>
    </div>
  );
}