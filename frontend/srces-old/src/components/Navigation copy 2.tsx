// components/Navigation.tsx
'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';

const Navigation = () => {
  const pathname = usePathname();
  const { user, isAuthenticated, logout, hasPermission } = useAuth();

  const isActive = (path: string) => pathname === path;

  if (!isAuthenticated) {
    return null;
  }

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', permission: 'view_dashboard' },
    { path: '/patients', label: 'Patients', permission: 'view_patients' },
    { path: '/appointments', label: 'Appointments', permission: 'view_appointments' },
    { path: '/billing', label: 'Billing', permission: 'view_billing' },
    { path: '/reports', label: 'Reports', permission: 'view_reports' },
  ];

  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            {/* Logo */}
            <div className="flex-shrink-0 flex items-center">
              <Link href="/dashboard" className="text-xl font-bold text-blue-600">
                DentalApp
              </Link>
            </div>

            {/* Navigation Links */}
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navItems.map((item) => {
                if (!hasPermission(item.permission)) return null;

                return (
                  <Link
                    key={item.path}
                    href={item.path}
                    className={`inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium ${
                      isActive(item.path)
                        ? 'border-blue-500 text-gray-900'
                        : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                    }`}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </div>
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">
              {user?.first_name} {user?.last_name}
            </span>
            <Link
              href="/profile"
              className={`px-3 py-2 rounded-md text-sm font-medium ${
                isActive('/profile')
                  ? 'text-gray-900 bg-gray-100'
                  : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              Profile
            </Link>
            <button
              onClick={() => logout()}
              className="px-3 py-2 rounded-md text-sm font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-50"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;