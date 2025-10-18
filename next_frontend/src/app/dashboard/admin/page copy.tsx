'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { Header } from '@/components/layout/Header';
import { Sidebar } from '@/components/layout/Sidebar';
import { PatientTable } from '@/components/dashboard/PatientTable';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function AdminDashboard() {
  const { user, isLoading } = useAuth();

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Not authenticated</div>;

  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-6">Admin Dashboard - {user.organization_id}</h1>
          
          <div className="grid gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Manage Patients</CardTitle>
              </CardHeader>
              <CardContent>
                <PatientTable />
              </CardContent>
            </Card>
            
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>User Management</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Manage staff and user roles</p>
                  <button className="mt-4 bg-primary text-primary-foreground px-4 py-2 rounded">
                    Manage Users
                  </button>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader>
                  <CardTitle>Billing & Invoices</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>View and manage financial records</p>
                  <button className="mt-4 bg-primary text-primary-foreground px-4 py-2 rounded">
                    View Billing
                  </button>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
