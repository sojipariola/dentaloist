// src/contexts/UserContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { UserProfile, UserSettings } from '@/types/user';
import { usersService } from '@/services/users/usersService';
import { useAuth } from './AuthContext';

interface UserContextType {
  profile: UserProfile | null;
  settings: UserSettings | null;
  isLoading: boolean;
  error: string | null;
  refreshProfile: () => Promise<void>;
  refreshSettings: () => Promise<void>;
  updateProfile: (data: any) => Promise<void>;
  updateSettings: (data: any) => Promise<void>;
  uploadAvatar: (file: File) => Promise<void>;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user: authUser, isAuthenticated } = useAuth();

  const loadUserData = async () => {
    if (!isAuthenticated) {
      setProfile(null);
      setSettings(null);
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const [profileResponse, settingsResponse] = await Promise.all([
        usersService.getProfile(),
        usersService.getSettings()
      ]);

      setProfile(profileResponse.profile);
      setSettings(settingsResponse.settings);
    } catch (err: any) {
      setError(err.message);
      console.error('Failed to load user data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const refreshProfile = async () => {
    try {
      const response = await usersService.getProfile();
      setProfile(response.profile);
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const refreshSettings = async () => {
    try {
      const response = await usersService.getSettings();
      setSettings(response.settings);
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const updateProfile = async (profileData: any) => {
    try {
      const response = await usersService.updateProfile(profileData);
      setProfile(response.profile);
      return response;
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const updateSettings = async (settingsData: any) => {
    try {
      const response = await usersService.updateSettings(settingsData);
      setSettings(response.settings);
      return response;
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const uploadAvatar = async (file: File) => {
    try {
      const response = await usersService.uploadAvatar(file);
      // Refresh profile to get updated avatar URL
      await refreshProfile();
      return response;
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  useEffect(() => {
    loadUserData();
  }, [isAuthenticated, authUser?.id]);

  const value: UserContextType = {
    profile,
    settings,
    isLoading,
    error,
    refreshProfile,
    refreshSettings,
    updateProfile,
    updateSettings,
    uploadAvatar
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};