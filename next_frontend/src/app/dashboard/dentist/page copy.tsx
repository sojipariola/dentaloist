'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { WidgetGrid } from '@/components/dashboard/WidgetGrid';
import { AppointmentCalendar } from '@/components/dashboard/AppointmentCalendar';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

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
              <Card>
                <CardHeader>
                  <CardTitle>Today's Appointments</CardTitle>
                </CardHeader>
                <CardContent>
                  <AppointmentCalendar />
                </CardContent>
              </Card>
            </div>
            
            <div className="md:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Dashboard Widgets</CardTitle>
                </CardHeader>
                <CardContent>
                  <WidgetGrid />
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
