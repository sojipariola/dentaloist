// src/hooks/useUserProfile.ts
import { useState, useEffect } from 'react';
import { UserProfile } from '@/types/user';
import { usersService } from '@/services/users/usersService';

export const useUserProfile = (userId?: number) => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await usersService.getProfile(userId);
      setProfile(response.profile);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const updateProfile = async (profileData: any) => {
    try {
      const response = await usersService.updateProfile(profileData);
      setProfile(response.profile);
      return response;
    } catch (err: any) {
      throw err;
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  return {
    profile,
    isLoading,
    error,
    refresh: fetchProfile,
    updateProfile
  };
};