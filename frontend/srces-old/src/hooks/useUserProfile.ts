// src/hooks/useUserProfile.ts


import { useState, useEffect, useCallback } from 'react';
import { UserProfile, UpdateProfileDto } from '@/types/user';
import { usersService } from '@/services/users';
import { useAuth } from '@/context/AuthContext';

interface UseUserProfileOptions {
  userId?: number;
  autoFetch?: boolean;
  onError?: (error: string) => void;
}

export const useUserProfile = (options: UseUserProfileOptions = {}) => {
  const { userId, autoFetch = true, onError } = options;
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user: authUser, isAuthenticated } = useAuth();

  const fetchProfile = useCallback(async (): Promise<UserProfile | null> => {
    if (!isAuthenticated) {
      setProfile(null);
      setIsLoading(false);
      return null;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const userProfile = await usersService.getProfile(userId);
      setProfile(userProfile);
      return userProfile;
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch user profile';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error fetching user profile:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [userId, isAuthenticated, onError]);

  const updateProfile = useCallback(async (profileData: UpdateProfileDto): Promise<UserProfile> => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Map gender to allowed values if necessary
      const allowedGenders = ['male', 'female', 'other', 'prefer_not_to_say'] as const;
      const mappedProfileData: UpdateProfileDto = {
        ...profileData,
        gender: profileData.gender && allowedGenders.includes(profileData.gender as typeof allowedGenders[number])
          ? profileData.gender as typeof allowedGenders[number]
          : undefined
      };
      const updatedProfile = await usersService.updateProfile(mappedProfileData);
      setProfile(updatedProfile);

      // If updating current user's profile, we might want to update auth context
      if (!userId || userId === authUser?.id) {
        // You could add logic here to update the auth context if needed
      }

      return updatedProfile;
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to update profile';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error updating profile:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [userId, authUser?.id, onError]);

  const uploadAvatar = useCallback(async (file: File): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      
      await usersService.uploadAvatar(file);
      
      // Refresh profile to get updated avatar URL
      await fetchProfile();
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to upload avatar';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error uploading avatar:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [fetchProfile, onError]);

  const deleteAvatar = useCallback(async (): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      
      await usersService.deleteAvatar();
      
      // Refresh profile to reflect avatar deletion
      await fetchProfile();
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to delete avatar';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error deleting avatar:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [fetchProfile, onError]);

  const refresh = useCallback(async (): Promise<UserProfile | null> => {
    return fetchProfile();
  }, [fetchProfile]);

  const resetError = useCallback((): void => {
    setError(null);
  }, []);

  // Auto-fetch profile on mount and when dependencies change
  useEffect(() => {
    if (autoFetch) {
      fetchProfile();
    }
  }, [autoFetch, fetchProfile]);

  return {
    // State
    profile,
    isLoading,
    error,
    
    // Actions
    fetchProfile,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
    refresh,
    resetError,
    
    // Utilities
    hasProfile: !!profile,
    isCurrentUser: !userId || userId === authUser?.id,
    canEdit: !userId || userId === authUser?.id || authUser?.is_admin,
    
    // Derived state
    displayName: profile ? `${profile.first_name} ${profile.last_name}`.trim() : '',
    initials: profile ? `${profile.first_name?.[0] || ''}${profile.last_name?.[0] || ''}`.toUpperCase() : '',
    hasAvatar: !!profile?.avatar_url
  };
};

// Convenience hook for current user's profile
export const useCurrentUserProfile = (options: Omit<UseUserProfileOptions, 'userId'> = {}) => {
  return useUserProfile(options);
};

// Convenience hook for another user's profile
export const useUserProfileById = (userId: number, options: Omit<UseUserProfileOptions, 'userId'> = {}) => {
  return useUserProfile({ ...options, userId });
};