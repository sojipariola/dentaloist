'use client';

import { useEffect } from 'react';
import { useAuth } from '@/lib/hooks/useAuth';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && user) {
      // Redirect based on role
      const roleRoutes: Record<string, string> = {
        dentist: '/dashboard/dentist',
        org_admin: '/dashboard/admin',
        lab_technician: '/dashboard/lab',
        billing_staff: '/dashboard/billing',
        family_member: '/dashboard/family',
        assistant: '/dashboard/assistant',
        nurse: '/dashboard/nurse',
        researcher: '/dashboard/researcher',
        visitor: '/dashboard/visitor',
      };
      
      const route = roleRoutes[user.role] || '/dashboard/dentist';
      router.push(route);
    } else if (!isLoading && !user) {
      router.push('/login');
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  return null;
}
