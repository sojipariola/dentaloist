// frontend/src/app/dashboard/page.tsx
'use client'

import { ProtectedRoute } from '@/components/ProtectedRoute';
import { DashboardContent } from '@/features/dashboard/DashboardContent';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}

