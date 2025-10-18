// src/hooks/useUserSettings.ts
import { useState, useEffect, useCallback } from 'react';
import { UserSettings, UpdateSettingsDto } from '@/types/user';
import { usersService } from '@/services/users';
import { useAuth } from '@/context/AuthContext';

interface UseUserSettingsOptions {
  autoFetch?: boolean;
  onError?: (error: string) => void;
}

export const useUserSettings = (options: UseUserSettingsOptions = {}) => {
  const { autoFetch = true, onError } = options;
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  const fetchSettings = useCallback(async (): Promise<UserSettings | null> => {
    if (!isAuthenticated) {
      setSettings(null);
      setIsLoading(false);
      return null;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      const userSettings = await usersService.getSettings();
      setSettings(userSettings);
      return userSettings;
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to fetch user settings';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error fetching user settings:', err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [isAuthenticated, onError]);

  const updateSettings = useCallback(async (settingsData: UpdateSettingsDto): Promise<UserSettings> => {
    try {
      setIsLoading(true);
      setError(null);
      
      const updatedSettings = await usersService.updateSettings(settingsData);
      setSettings(updatedSettings);
      return updatedSettings;
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to update settings';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error updating settings:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [onError]);

  const updateSetting = useCallback(async <K extends keyof UpdateSettingsDto>(
    key: K,
    value: UpdateSettingsDto[K]
  ): Promise<UserSettings> => {
    return updateSettings({ [key]: value } as UpdateSettingsDto);
  }, [updateSettings]);

  const refresh = useCallback(async (): Promise<UserSettings | null> => {
    return fetchSettings();
  }, [fetchSettings]);

  const resetError = useCallback((): void => {
    setError(null);
  }, []);

  const resetToDefaults = useCallback(async (): Promise<UserSettings> => {
    try {
      setIsLoading(true);
      setError(null);
      
      // Create default settings object (you might want to define this differently)
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
    } catch (err: any) {
      const errorMessage = err.message || 'Failed to reset settings to defaults';
      setError(errorMessage);
      onError?.(errorMessage);
      console.error('Error resetting settings:', err);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [updateSettings, onError]);

  // Auto-fetch settings on mount
  useEffect(() => {
    if (autoFetch) {
      fetchSettings();
    }
  }, [autoFetch, fetchSettings]);

  return {
    // State
    settings,
    isLoading,
    error,
    
    // Actions
    fetchSettings,
    updateSettings,
    updateSetting,
    refresh,
    resetError,
    resetToDefaults,
    
    // Utilities
    hasSettings: !!settings,
    
    // Derived state - convenience getters
    theme: settings?.theme || 'auto',
    language: settings?.language || 'en',
    timezone: settings?.timezone || 'UTC',
    dateFormat: settings?.date_format || 'MM/DD/YYYY',
    timeFormat: settings?.time_format || '12h',
    
    // Notification settings
    emailNotifications: settings?.email_notifications ?? true,
    smsNotifications: settings?.sms_notifications ?? false,
    pushNotifications: settings?.push_notifications ?? true,
    appointmentReminders: settings?.appointment_reminders ?? true,
    billingNotifications: settings?.billing_notifications ?? true,
    
    // Privacy settings
    showOnlineStatus: settings?.show_online_status ?? true,
    allowProfileView: settings?.allow_profile_view ?? true,
    
    // Accessibility settings
    highContrastMode: settings?.high_contrast_mode ?? false,
    reducedMotion: settings?.reduced_motion ?? false
  };
};

// Convenience hook for specific setting categories
export const useNotificationSettings = () => {
  const { settings, updateSetting, ...rest } = useUserSettings();
  
  const updateNotificationSetting = useCallback(async (
    key: keyof Pick<UserSettings, 
      | 'email_notifications'
      | 'sms_notifications' 
      | 'push_notifications'
      | 'appointment_reminders'
      | 'billing_notifications'
    >, 
    value: boolean
  ) => {
    return updateSetting(key, value);
  }, [updateSetting]);

  return {
    ...rest,
    settings: settings ? {
      email: settings.email_notifications,
      sms: settings.sms_notifications,
      push: settings.push_notifications,
      appointments: settings.appointment_reminders,
      billing: settings.billing_notifications
    } : null,
    updateSetting: updateNotificationSetting
  };
};

export const useAppearanceSettings = () => {
  const { settings, updateSetting, ...rest } = useUserSettings();
  
  const updateAppearanceSetting = useCallback(async (
    key: keyof Pick<UserSettings, 
      | 'theme'
      | 'language'
      | 'timezone'
      | 'date_format'
      | 'time_format'
    >,
    value: any
  ) => {
    return updateSetting(key, value);
  }, [updateSetting]);

  return {
    ...rest,
    settings: settings ? {
      theme: settings.theme,
      language: settings.language,
      timezone: settings.timezone,
      dateFormat: settings.date_format,
      timeFormat: settings.time_format
    } : null,
    updateSetting: updateAppearanceSetting
  };
};