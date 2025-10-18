// components/ProtectedRoute.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useEffect } from 'react';
import { debugAuth } from '@/services/authService'
import Link from 'next/link';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredPermission?: string;
  requiredRole?: string;
  fallback?: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredPermission, 
  requiredRole,
  fallback 
}) => {
  const { user, isLoading, isAuthenticated, hasPermission, hasRole } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  if (!isAuthenticated) {
    return null;
  }

  // Check permissions
  const hasRequiredPermission = !requiredPermission || hasPermission(requiredPermission);
  const hasRequiredRole = !requiredRole || hasRole(requiredRole);

  if (!hasRequiredPermission || !hasRequiredRole) {
    return fallback || (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Access Denied</h2>
          <p className="text-gray-600 mb-4">You don't have permission to access this page.</p>
          <Link 
            href="/dashboard" 
            className="text-blue-600 hover:text-blue-800"
          >
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }
  useEffect(() => {
    // Temporary debug
    debugAuth();
  }, []);
  
  return <>{children}</>;
};