// src/components/layout/Header.tsx
'use client';

import { Search, Bell, User, Settings } from 'lucide-react';
import { useAuth } from '@/lib/hooks/useAuth';

export function Header() {
  const { user } = useAuth();

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b px-6 py-4">
      <div className="flex items-center justify-between">
        {/* Search */}
        <div className="flex-1 max-w-2xl">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Search patients, appointments, records..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center space-x-4">
          {/* Notifications */}
          <button className="relative p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white">
            <Bell className="w-6 h-6" />
            <span className="absolute top-0 right-0 w-3 h-3 bg-red-500 rounded-full" />
          </button>

          {/* User menu */}
          <div className="flex items-center space-x-3">
            <div className="text-right hidden md:block">
              <p className="text-sm font-medium text-gray-900 dark:text-white">
                {user?.first_name} {user?.last_name}
              </p>
              <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">
                {user?.role?.replace('_', ' ')}
              </p>
            </div>
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}