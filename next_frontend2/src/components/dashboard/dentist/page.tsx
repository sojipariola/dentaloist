'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { WidgetGrid } from '@/components/dashboard/WidgetGrid';
import { AppointmentCalendar } from '@/components/dashboard/AppointmentCalendar';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';

export default function DentistDashboard() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Not authenticated</div>;

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-6">Welcome, Dr. {user.first_name}</h1>
          
          <div className="grid gap-6 md:grid-cols-2">
            <div className="md:col-span-2">
              <h2 className="text-xl font-semibold mb-4">Today's Appointments</h2>
              <AppointmentCalendar />
            </div>
            
            <div className="md:col-span-2">
              <h2 className="text-xl font-semibold mb-4">Dashboard Widgets</h2>
              <WidgetGrid />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}