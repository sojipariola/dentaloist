// src/app/profile/page.tsx
'use client';

import { useUser } from '@/contexts/UserContext';
import { useAuth } from '@/context/AuthContext';
import { ProtectedRoute } from '@/components/ProtectedRoute';

export default function ProfilePage() {
  const { profile, settings, isLoading, updateProfile, uploadAvatar } = useUser();
  const { user: authUser } = useAuth();

  if (isLoading) {
    return <div>Loading profile...</div>;
  }

  return (
    <ProtectedRoute>
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">Profile</h1>
        
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center space-x-6 mb-6">
            <div className="w-24 h-24 bg-gray-300 rounded-full flex items-center justify-center">
              {profile?.avatar_url ? (
                <img
                  src={profile.avatar_url}
                  alt="Profile"
                  className="w-24 h-24 rounded-full object-cover"
                />
              ) : (
                <span className="text-2xl font-bold text-gray-600">
                  {getUserInitials(profile)}
                </span>
              )}
            </div>
            
            <div>
              <h2 className="text-xl font-semibold">
                {getUserDisplayName(profile)}
              </h2>
              <p className="text-gray-600">{authUser?.email}</p>
              <p className="text-sm text-gray-500">
                {formatUserRole(authUser?.role || 'user')}
              </p>
            </div>
          </div>

          {/* Profile form would go here */}
        </div>
      </div>
    </ProtectedRoute>
  );
}