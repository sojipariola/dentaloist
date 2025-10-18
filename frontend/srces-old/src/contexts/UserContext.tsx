// src/contexts/UserContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { UserProfile, UserSettings, UpdateProfileDto, UpdateSettingsDto } from '@/types/user';
import { usersService } from '@/services/users';
import { useAuth } from './AuthContext';

interface UserContextType {
  // Profile State
  profile: UserProfile | null;
  profileLoading: boolean;
  profileError: string | null;
  
  // Settings State
  settings: UserSettings | null;
  settingsLoading: boolean;
  settingsError: string | null;
  
  // Combined Loading State
  isLoading: boolean;
  
  // Profile Actions
  fetchProfile: (userId?: number) => Promise<UserProfile | null>;
  updateProfile: (data: UpdateProfileDto) => Promise<UserProfile>;
  uploadAvatar: (file: File) => Promise<void>;
  deleteAvatar: () => Promise<void>;
  refreshProfile: () => Promise<UserProfile | null>;
  
  // Settings Actions
  fetchSettings: () => Promise<UserSettings | null>;
  updateSettings: (data: UpdateSettingsDto) => Promise<UserSettings>;
  refreshSettings: () => Promise<UserSettings | null>;
  resetSettings: () => Promise<UserSettings>;
  
  // Error Handling
  clearProfileError: () => void;
  clearSettingsError: () => void;
  clearAllErrors: () => void;
  
  // Derived State
  displayName: string;
  initials: string;
  hasAvatar: boolean;
  isCurrentUser: (userId?: number) => boolean;
  canEditProfile: (userId?: number) => boolean;
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
  autoFetch?: boolean;
  onError?: (error: string, context: string) => void;
}

export const UserProvider: React.FC<UserProviderProps> = ({ 
  children, 
  autoFetch = true,
  onError 
}) => {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [profileLoading, setProfileLoading] = useState(true);
  const [profileError, setProfileError] = useState<string | null>(null);
  
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [settingsLoading, setSettingsLoading] = useState(true);
  const [settingsError, setSettingsError] = useState<string | null>(null);

  const { user: authUser, isAuthenticated, updateAuthUser } = useAuth();

  // Combined loading state
  const isLoading = profileLoading || settingsLoading;

  // Error handling utility
  const handleError = useCallback((error: any, context: string, setError: React.Dispatch<React.SetStateAction<string | null>>) => {
    const errorMessage = error.message || `Failed to ${context}`;
    setError(errorMessage);
    onError?.(errorMessage, context);
    console.error(`UserContext Error (${context}):`, error);
    return errorMessage;
  }, [onError]);

  // Profile Management
  const fetchProfile = useCallback(async (userId?: number): Promise<UserProfile | null> => {
    if (!isAuthenticated) {
      setProfile(null);
      setProfileLoading(false);
      return null;
    }

    try {
      setProfileLoading(true);
      setProfileError(null);
      
      const userProfile = await usersService.getProfile(userId);
      setProfile(userProfile);
      return userProfile;
    } catch (error: any) {
      const errorMessage = handleError(error, 'fetch profile', setProfileError);
      throw new Error(errorMessage);
    } finally {
      setProfileLoading(false);
    }
  }, [isAuthenticated, handleError]);

  const updateProfile = useCallback(async (data: UpdateProfileDto): Promise<UserProfile> => {
    try {
      setProfileLoading(true);
      setProfileError(null);
      
      const updatedProfile = await usersService.updateProfile(data);
      setProfile(updatedProfile);
      
      // Update auth user if updating current user's profile
      if (!data.id || data.id === authUser?.id) {
        updateAuthUser?.({
          ...authUser,
          first_name: updatedProfile.first_name,
          last_name: updatedProfile.last_name,
          // Add other fields that might be relevant for auth context
        });
      }
      
      return updatedProfile;
    } catch (error: any) {
      const errorMessage = handleError(error, 'update profile', setProfileError);
      throw new Error(errorMessage);
    } finally {
      setProfileLoading(false);
    }
  }, [authUser, updateAuthUser, handleError]);

  const uploadAvatar = useCallback(async (file: File): Promise<void> => {
    try {
      setProfileLoading(true);
      setProfileError(null);
      
      await usersService.uploadAvatar(file);
      
      // Refresh profile to get updated avatar URL
      await fetchProfile();
    } catch (error: any) {
      const errorMessage = handleError(error, 'upload avatar', setProfileError);
      throw new Error(errorMessage);
    } finally {
      setProfileLoading(false);
    }
  }, [fetchProfile, handleError]);

  const deleteAvatar = useCallback(async (): Promise<void> => {
    try {
      setProfileLoading(true);
      setProfileError(null);
      
      await usersService.deleteAvatar();
      
      // Refresh profile to reflect avatar deletion
      await fetchProfile();
    } catch (error: any) {
      const errorMessage = handleError(error, 'delete avatar', setProfileError);
      throw new Error(errorMessage);
    } finally {
      setProfileLoading(false);
    }
  }, [fetchProfile, handleError]);

  const refreshProfile = useCallback(async (): Promise<UserProfile | null> => {
    return fetchProfile();
  }, [fetchProfile]);

  // Settings Management
  const fetchSettings = useCallback(async (): Promise<UserSettings | null> => {
    if (!isAuthenticated) {
      setSettings(null);
      setSettingsLoading(false);
      return null;
    }

    try {
      setSettingsLoading(true);
      setSettingsError(null);
      
      const userSettings = await usersService.getSettings();
      setSettings(userSettings);
      return userSettings;
    } catch (error: any) {
      const errorMessage = handleError(error, 'fetch settings', setSettingsError);
      throw new Error(errorMessage);
    } finally {
      setSettingsLoading(false);
    }
  }, [isAuthenticated, handleError]);

  const updateSettings = useCallback(async (data: UpdateSettingsDto): Promise<UserSettings> => {
    try {
      setSettingsLoading(true);
      setSettingsError(null);
      
      const updatedSettings = await usersService.updateSettings(data);
      setSettings(updatedSettings);
      return updatedSettings;
    } catch (error: any) {
      const errorMessage = handleError(error, 'update settings', setSettingsError);
      throw new Error(errorMessage);
    } finally {
      setSettingsLoading(false);
    }
  }, [handleError]);

  const refreshSettings = useCallback(async (): Promise<UserSettings | null> => {
    return fetchSettings();
  }, [fetchSettings]);

  const resetSettings = useCallback(async (): Promise<UserSettings> => {
    try {
      setSettingsLoading(true);
      setSettingsError(null);
      
      const defaultSettings: UpdateSettingsDto = {
        theme: 'auto',
        language: 'en',
        email_notifications: true,
        sms_notifications: false,
        push_notifications: true,
        appointment_reminders: true,
        billing_notifications: true,
        timezone: 'UTC',
        date_format: 'MM/DD/YYYY',
        time_format: '12h',
        week_start: 0,
        show_online_status: true,
        allow_profile_view: true,
        high_contrast_mode: false,
        reduced_motion: false,
      };
      
      const updatedSettings = await updateSettings(defaultSettings);
      return updatedSettings;
    } catch (error: any) {
      const errorMessage = handleError(error, 'reset settings', setSettingsError);
      throw new Error(errorMessage);
    } finally {
      setSettingsLoading(false);
    }
  }, [updateSettings, handleError]);

  // Error Handling
  const clearProfileError = useCallback(() => {
    setProfileError(null);
  }, []);

  const clearSettingsError = useCallback(() => {
    setSettingsError(null);
  }, []);

  const clearAllErrors = useCallback(() => {
    setProfileError(null);
    setSettingsError(null);
  }, []);

  // Derived State
  const displayName = profile 
    ? `${profile.first_name} ${profile.last_name}`.trim() 
    : authUser?.email 
    ? authUser.email 
    : 'User';

  const initials = profile
    ? `${profile.first_name?.[0] || ''}${profile.last_name?.[0] || ''}`.toUpperCase()
    : authUser?.email?.[0]?.toUpperCase() || 'U';

  const hasAvatar = !!profile?.avatar_url;

  const isCurrentUser = useCallback((userId?: number): boolean => {
    if (!userId) return true;
    return userId === authUser?.id;
  }, [authUser?.id]);

  const canEditProfile = useCallback((userId?: number): boolean => {
    if (!userId) return true;
    return userId === authUser?.id || authUser?.is_admin === true;
  }, [authUser?.id, authUser?.is_admin]);

  // Auto-fetch data on mount and auth changes
  useEffect(() => {
    if (autoFetch && isAuthenticated) {
      fetchProfile();
      fetchSettings();
    }
  }, [autoFetch, isAuthenticated, fetchProfile, fetchSettings]);

  // Reset state when user logs out
  useEffect(() => {
    if (!isAuthenticated) {
      setProfile(null);
      setSettings(null);
      setProfileError(null);
      setSettingsError(null);
      setProfileLoading(false);
      setSettingsLoading(false);
    }
  }, [isAuthenticated]);

  const value: UserContextType = {
    // State
    profile,
    profileLoading,
    profileError,
    settings,
    settingsLoading,
    settingsError,
    isLoading,
    
    // Profile Actions
    fetchProfile,
    updateProfile,
    uploadAvatar,
    deleteAvatar,
    refreshProfile,
    
    // Settings Actions
    fetchSettings,
    updateSettings,
    refreshSettings,
    resetSettings,
    
    // Error Handling
    clearProfileError,
    clearSettingsError,
    clearAllErrors,
    
    // Derived State
    displayName,
    initials,
    hasAvatar,
    isCurrentUser,
    canEditProfile,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};

// Convenience hook for current user's profile only
export const useCurrentUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useCurrentUser must be used within a UserProvider');
  }
  return context;
};

// Convenience hook for user settings only
export const useUserSettings = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUserSettings must be used within a UserProvider');
  }
  
  return {
    settings: context.settings,
    isLoading: context.settingsLoading,
    error: context.settingsError,
    updateSettings: context.updateSettings,
    refreshSettings: context.refreshSettings,
    resetSettings: context.resetSettings,
    clearError: context.clearSettingsError,
  };
};

// Convenience hook for user profile only
export const useUserProfile = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUserProfile must be used within a UserProvider');
  }
  
  return {
    profile: context.profile,
    isLoading: context.profileLoading,
    error: context.profileError,
    updateProfile: context.updateProfile,
    uploadAvatar: context.uploadAvatar,
    deleteAvatar: context.deleteAvatar,
    refreshProfile: context.refreshProfile,
    clearError: context.clearProfileError,
    displayName: context.displayName,
    initials: context.initials,
    hasAvatar: context.hasAvatar,
  };
};