// src/components/dashboard/QuickActions.tsx
import { motion } from 'framer-motion';
import { Plus, Calendar, User, FileText, DollarSign } from 'lucide-react';

const actions = [
  {
    icon: Plus,
    label: 'New Appointment',
    description: 'Schedule a new patient appointment',
    color: 'bg-blue-500',
    href: '/appointments/new',
  },
  {
    icon: User,
    label: 'Add Patient',
    description: 'Register a new patient',
    color: 'bg-green-500',
    href: '/patients/new',
  },
  {
    icon: FileText,
    label: 'Create Report',
    description: 'Generate practice reports',
    color: 'bg-amber-500',
    href: '/reports',
  },
  {
    icon: DollarSign,
    label: 'Process Payment',
    description: 'Record patient payments',
    color: 'bg-purple-500',
    href: '/billing',
  },
];

export function QuickActions() {
  return (
    <motion.div
      className="bg-white rounded-xl p-6 shadow-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Quick Actions</h3>
      
      <div className="space-y-4">
        {actions.map((action, index) => {
          const Icon = action.icon;
          return (
            <motion.button
              key={index}
              className="flex items-center space-x-4 w-full p-4 border rounded-lg hover:shadow-md transition-shadow text-left"
              whileHover={{ x: 4 }}
              transition={{ duration: 0.2 }}
            >
              <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center`}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h4 className="font-medium text-gray-900">{action.label}</h4>
                <p className="text-sm text-gray-600">{action.description}</p>
              </div>
            </motion.button>
          );
        })}
      </div>
    </motion.div>
  );
}