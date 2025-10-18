// src/components/layout/Sidebar.tsx
'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  LayoutDashboard, 
  Users, 
  Calendar, 
  FileText,
  DollarSign,
  Settings,
  LogOut,
  Menu,
  X,
  Clipboard,
  Package,
  Diamond,
  Shield,
  Bell,
  Activity,
  BarChart3,
  ClipboardList,
  Stethoscope,
  Heart,
  Microscope,
  Eye
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/lib/hooks/useAuth';

const getRoleSpecificMenu = (role: string) => {
  const baseMenu = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Patients', href: '/patients', icon: Users },
    { name: 'Appointments', href: '/appointments', icon: Calendar },
  ];

  const roleMenus: Record<string, any[]> = {
    super_admin: [
      ...baseMenu,
      { name: 'System Admin', href: '/admin/system', icon: Settings },
      { name: 'Organizations', href: '/admin/organizations', icon: Building },
      { name: 'Audit Logs', href: '/admin/audit-logs', icon: ClipboardList },
      { name: 'Reports', href: '/admin/reports', icon: BarChart3 },
    ],
    org_admin: [
      ...baseMenu,
      { name: 'Staff Management', href: '/admin/staff', icon: Users },
      { name: 'Billing', href: '/billing', icon: DollarSign },
      { name: 'Reports', href: '/reports', icon: BarChart3 },
      { name: 'Settings', href: '/settings', icon: Settings },
    ],
    dentist: [
      ...baseMenu,
      { name: 'Treatment Plans', href: '/dentist/treatment-plans', icon: Clipboard },
      { name: 'Medical Records', href: '/records', icon: FileText },
      { name: 'Prescriptions', href: '/dentist/prescriptions', icon: Stethoscope },
      { name: 'Lab Orders', href: '/dentist/lab-orders', icon: Package },
    ],
    lab_technician: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Lab Orders', href: '/lab/orders', icon: Package },
      { name: 'Restorations', href: '/lab/restorations', icon: Diamond },
      { name: 'Quality Control', href: '/lab/quality', icon: Activity },
      { name: 'Inventory', href: '/lab/inventory', icon: Package },
    ],
    billing_staff: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Invoices', href: '/billing/invoices', icon: FileText },
      { name: 'Payments', href: '/billing/payments', icon: DollarSign },
      { name: 'Insurance', href: '/billing/insurance', icon: Shield },
      { name: 'Reports', href: '/billing/reports', icon: BarChart3 },
    ],
    assistant: [
      ...baseMenu,
      { name: 'Room Management', href: '/assistant/rooms', icon: DoorOpen },
      { name: 'Inventory', href: '/assistant/inventory', icon: Package },
      { name: 'Patient Prep', href: '/assistant/prep', icon: Clipboard },
    ],
    nurse: [
      ...baseMenu,
      { name: 'Vitals', href: '/nurse/vitals', icon: Activity },
      { name: 'Medications', href: '/nurse/medications', icon: Pill },
      { name: 'Patient Care', href: '/nurse/care', icon: Heart },
    ],
    family_member: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Family Patients', href: '/family/patients', icon: Users },
      { name: 'Appointments', href: '/family/appointments', icon: Calendar },
      { name: 'Medical Records', href: '/family/records', icon: FileText },
    ],
    researcher: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Analytics', href: '/research/analytics', icon: BarChart3 },
      { name: 'Studies', href: '/research/studies', icon: Microscope },
      { name: 'Reports', href: '/research/reports', icon: FileText },
    ],
    visitor: [
      { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
      { name: 'Patient Portal', href: '/visitor/portal', icon: Eye },
      { name: 'Appointments', href: '/visitor/appointments', icon: Calendar },
    ],
  };

  return roleMenus[role] || baseMenu;
};

// Add missing icon components
const Building = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-4 0H9m4 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v12m4 0h-2" />
  </svg>
);

const DoorOpen = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const Pill = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-4 0H9m4 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v12m4 0h-2" />
  </svg>
);

export function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navigation = getRoleSpecificMenu(user?.role || '');

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-md shadow-md"
        onClick={() => setIsOpen(!isOpen)}
      >
        <Menu className="w-6 h-6" />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsOpen(false)}
          />
        )}
      </AnimatePresence>

      <motion.div
        className={`
          fixed lg:static inset-y-0 left-0 z-40 w-64 bg-white dark:bg-gray-800 shadow-lg
          transform lg:transform-none transition-transform duration-300
          ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        initial={false}
        animate={{ x: isOpen ? 0 : -256 }}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-6 border-b">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg" />
              <span className="text-xl font-semibold">Dentaloist</span>
            </div>
            <button
              className="lg:hidden p-1"
              onClick={() => setIsOpen(false)}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`
                    flex items-center space-x-3 p-3 rounded-lg transition-colors
                    ${isActive
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                      : 'text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700'
                    }
                  `}
                  onClick={() => setIsOpen(false)}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </nav>

          {/* User section */}
          <div className="p-4 border-t">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white">
                {user?.first_name?.[0]}{user?.last_name?.[0]}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.first_name} {user?.last_name}
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-400 truncate capitalize">
                  {user?.role?.replace('_', ' ')}
                </p>
              </div>
            </div>

            <button
              onClick={logout}
              className="flex items-center space-x-3 w-full p-3 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <LogOut className="w-5 h-5" />
              <span>Sign out</span>
            </button>
          </div>
        </div>
      </motion.div>
    </>
  );
}

// const navigation = user ? getRoleSpecificMenu(user.role) : [];