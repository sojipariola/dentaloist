// src/hooks/useUserSettings.ts
import { useState, useEffect } from 'react';
import { UserSettings, UpdateSettingsDto } from '@/types/user';
import { usersService } from '@/services/users/usersService';

export const useUserSettings = () => {
  const [settings, setSettings] = useState<UserSettings | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSettings = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await usersService.getSettings();
      setSettings(response.settings);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const updateSettings = async (settingsData: UpdateSettingsDto) => {
    try {
      const response = await usersService.updateSettings(settingsData);
      setSettings(response.settings);
      return response;
    } catch (err: any) {
      throw err;
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  return {
    settings,
    isLoading,
    error,
    refresh: fetchSettings,
    updateSettings
  };
};