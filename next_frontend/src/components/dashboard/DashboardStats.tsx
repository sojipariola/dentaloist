// src/components/dashboard/DashboardStats.tsx
import { motion } from 'framer-motion';
import { Users, Calendar, DollarSign, Activity } from 'lucide-react';

interface Stats {
  totalPatients: number;
  totalAppointments: number;
  revenue: number;
  pendingTasks: number;
}

interface StatCardProps {
  icon: React.ComponentType<any>;
  label: string;
  value: number | string;
  trend?: number;
  color: string;
}

function StatCard({ icon: Icon, label, value, trend, color }: StatCardProps) {
  return (
    <motion.div
      className="bg-white p-6 rounded-xl shadow-sm border"
      whileHover={{ y: -2 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p className={`text-sm ${trend >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              {trend >= 0 ? '+' : ''}{trend}% from last week
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </motion.div>
  );
}

export function DashboardStats({ stats }: { stats: Stats }) {
  const statCards = [
    {
      icon: Users,
      label: 'Total Patients',
      value: stats.totalPatients.toLocaleString(),
      trend: 12,
      color: 'bg-blue-500',
    },
    {
      icon: Calendar,
      label: 'Appointments Today',
      value: stats.totalAppointments,
      trend: 8,
      color: 'bg-green-500',
    },
    {
      icon: DollarSign,
      label: 'Revenue',
      value: `$${stats.revenue.toLocaleString()}`,
      trend: 23,
      color: 'bg-amber-500',
    },
    {
      icon: Activity,
      label: 'Pending Tasks',
      value: stats.pendingTasks,
      trend: -4,
      color: 'bg-red-500',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {statCards.map((card, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
        >
          <StatCard {...card} />
        </motion.div>
      ))}
    </div>
  );
}