// src/services/users/usersService.ts

import { apiClient } from '../api';
import {
  UserProfile,
  UserSettings,
  CreateUserDto,
  UpdateProfileDto,
  UpdateSettingsDto,
  ChangePasswordDto,
  UploadAvatarResponse,
  UserStats,
  UserActivity,
  UsersQueryParams,
  SearchUsersResponse,
  UserResponse,
  UsersListResponse,
  SettingsResponse,
  PasswordChangeResponse,
  StatsResponse,
  ActivityResponse,
  ResetPasswordRequestDto,
  ResetPasswordDto,
  ApiErrorResponse,
  DEFAULT_AVATAR_OPTIONS
} from './types';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (typeof err === 'string') return new Error(err);
  if (err?.message) return new Error(err.message);
  if (err?.response?.data?.message) return new Error(err.response.data.message);
  return new Error(fallbackMessage);
};

const handleApiError = (error: any, context: string): never => {
  console.error(`Users Service Error (${context}):`, error);
  
  if (error.response?.data) {
    const apiError = error.response.data as ApiErrorResponse;
    throw new Error(apiError.message || `Failed to ${context}`);
  }
  
  throw normalizeError(error, `Failed to ${context}`);
};

export const usersService = {
  // ===== PROFILE MANAGEMENT =====
  async getProfile(userId?: number): Promise<UserProfile> {
    try {
      const endpoint = userId ? `/api/users/${userId}/profile` : '/api/users/me/profile';
      const response: UserResponse = await apiClient.get(endpoint);
      return response.user;
    } catch (error) {
      throw handleApiError(error, 'fetch user profile');
    }
  },

  async updateProfile(profileData: UpdateProfileDto): Promise<UserProfile> {
    try {
      const response: UserResponse = await apiClient.put('/api/users/me/profile', profileData);
      return response.user;
    } catch (error) {
      throw handleApiError(error, 'update profile');
    }
  },

  // ===== SETTINGS MANAGEMENT =====
  async getSettings(): Promise<UserSettings> {
    try {
      const response: SettingsResponse = await apiClient.get('/api/users/me/settings');
      return response.settings;
    } catch (error) {
      throw handleApiError(error, 'fetch user settings');
    }
  },

  async updateSettings(settingsData: UpdateSettingsDto): Promise<UserSettings> {
    try {
      const response: SettingsResponse = await apiClient.put('/api/users/me/settings', settingsData);
      return response.settings;
    } catch (error) {
      throw handleApiError(error, 'update settings');
    }
  },

  // ===== AVATAR MANAGEMENT =====
  async uploadAvatar(file: File): Promise<UploadAvatarResponse> {
    try {
      // Validate file
      if (file.size > DEFAULT_AVATAR_OPTIONS.maxSize) {
        throw new Error(`File size must be less than ${DEFAULT_AVATAR_OPTIONS.maxSize / 1024 / 1024}MB`);
      }

      if (!DEFAULT_AVATAR_OPTIONS.allowedTypes.includes(file.type)) {
        throw new Error('File type not allowed. Please use JPEG, PNG, GIF, or WebP');
      }

      const formData = new FormData();
      formData.append('avatar', file);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/me/avatar`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Upload failed: ${response.status}`);
      }

      return response.json();
    } catch (error) {
      throw handleApiError(error, 'upload avatar');
    }
  },

  async deleteAvatar(): Promise<{ message: string }> {
    try {
      return await apiClient.delete('/api/users/me/avatar');
    } catch (error) {
      throw handleApiError(error, 'delete avatar');
    }
  },

  // ===== PASSWORD MANAGEMENT =====
  async changePassword(passwordData: ChangePasswordDto): Promise<PasswordChangeResponse> {
    try {
      return await apiClient.post('/api/users/me/change-password', passwordData);
    } catch (error) {
      throw handleApiError(error, 'change password');
    }
  },

  async requestPasswordReset(emailData: ResetPasswordRequestDto): Promise<{ message: string }> {
    try {
      return await apiClient.post('/api/auth/forgot-password', emailData);
    } catch (error) {
      throw handleApiError(error, 'request password reset');
    }
  },

  async resetPassword(resetData: ResetPasswordDto): Promise<{ message: string }> {
    try {
      return await apiClient.post('/api/auth/reset-password', resetData);
    } catch (error) {
      throw handleApiError(error, 'reset password');
    }
  },

  // ===== USER STATISTICS =====
  async getUserStats(userId?: number): Promise<UserStats> {
    try {
      const endpoint = userId ? `/api/users/${userId}/stats` : '/api/users/me/stats';
      const response: StatsResponse = await apiClient.get(endpoint);
      return response.stats;
    } catch (error) {
      throw handleApiError(error, 'fetch user stats');
    }
  },

  // ===== ACTIVITY LOG =====
  async getActivityLog(params?: {
    page?: number;
    limit?: number;
    action?: string;
  }): Promise<{ activities: UserActivity[]; total: number }> {
    try {
      const queryString = params ? `?${new URLSearchParams(params as any).toString()}` : '';
      const response: ActivityResponse = await apiClient.get(`/api/users/me/activity${queryString}`);
      return {
        activities: response.activities,
        total: response.total
      };
    } catch (error) {
      throw handleApiError(error, 'fetch activity log');
    }
  },

  // ===== USER SEARCH & MANAGEMENT (Admin) =====
  async searchUsers(params: {
    query: string;
    role?: string;
    is_active?: boolean;
    page?: number;
    limit?: number;
  }): Promise<SearchUsersResponse> {
    try {
      const queryString = new URLSearchParams(params as any).toString();
      return await apiClient.get(`/api/users/search?${queryString}`);
    } catch (error) {
      throw handleApiError(error, 'search users');
    }
  },

  async getUsers(params?: UsersQueryParams): Promise<UsersListResponse> {
    try {
      const queryString = params ? `?${new URLSearchParams(params as any).toString()}` : '';
      return await apiClient.get(`/api/users${queryString}`);
    } catch (error) {
      throw handleApiError(error, 'fetch users');
    }
  },

  async getUserById(userId: number): Promise<UserProfile> {
    try {
      const response: UserResponse = await apiClient.get(`/api/users/${userId}`);
      return response.user;
    } catch (error) {
      throw handleApiError(error, 'fetch user by ID');
    }
  },

  async createUser(userData: CreateUserDto): Promise<UserProfile> {
    try {
      const response: UserResponse = await apiClient.post('/api/users', userData);
      return response.user;
    } catch (error) {
      throw handleApiError(error, 'create user');
    }
  },

  async updateUser(userId: number, userData: Partial<UserProfile>): Promise<UserProfile> {
    try {
      const response: UserResponse = await apiClient.put(`/api/users/${userId}`, userData);
      return response.user;
    } catch (error) {
      throw handleApiError(error, 'update user');
    }
  },

  async deactivateUser(userId: number): Promise<{ message: string }> {
    try {
      return await apiClient.post(`/api/users/${userId}/deactivate`, {});
    } catch (error) {
      throw handleApiError(error, 'deactivate user');
    }
  },

  async reactivateUser(userId: number): Promise<{ message: string }> {
    try {
      return await apiClient.post(`/api/users/${userId}/reactivate`, {});
    } catch (error) {
      throw handleApiError(error, 'reactivate user');
    }
  },

  async deleteUser(userId: number): Promise<{ message: string }> {
    try {
      return await apiClient.delete(`/api/users/${userId}`);
    } catch (error) {
      throw handleApiError(error, 'delete user');
    }
  },

  // ===== UTILITY METHODS =====
  async validateEmail(email: string): Promise<{ valid: boolean; message?: string }> {
    try {
      const response = await apiClient.post('/api/users/validate-email', { email });
      return response;
    } catch (error) {
      // If validation fails, it's still useful information
      if (
        typeof error === 'object' &&
        error !== null &&
        'response' in error &&
        typeof (error as any).response === 'object' &&
        (error as any).response !== null &&
        'data' in (error as any).response &&
        typeof (error as any).response.data === 'object' &&
        (error as any).response.data !== null &&
        'message' in (error as any).response.data
      ) {
        return { valid: false, message: (error as any).response.data.message };
      }
      throw handleApiError(error, 'validate email');
    }
  },

  async checkUsernameAvailability(username: string): Promise<{ available: boolean }> {
    try {
      return await apiClient.post('/api/users/check-username', { username });
    } catch (error) {
      throw handleApiError(error, 'check username availability');
    }
  },

  // ===== BATCH OPERATIONS =====
  async bulkUpdateUsers(userIds: number[], updates: Partial<UserProfile>): Promise<{ updated: number; failed: number }> {
    try {
      return await apiClient.post('/api/users/bulk-update', { userIds, updates });
    } catch (error) {
      throw handleApiError(error, 'bulk update users');
    }
  },

  async exportUsers(params?: UsersQueryParams): Promise<Blob> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users/export?${new URLSearchParams(params as any)}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Export failed: ${response.status}`);
      }

      return response.blob();
    } catch (error) {
      throw handleApiError(error, 'export users');
    }
  },

  // ===== SESSION MANAGEMENT =====
  async getActiveSessions(): Promise<any[]> {
    try {
      const response = await apiClient.get('/api/users/me/sessions');
      return response.sessions;
    } catch (error) {
      throw handleApiError(error, 'fetch active sessions');
    }
  },

  async revokeSession(sessionId: string): Promise<{ message: string }> {
    try {
      return await apiClient.delete(`/api/users/me/sessions/${sessionId}`);
    } catch (error) {
      throw handleApiError(error, 'revoke session');
    }
  },

  async revokeAllSessions(): Promise<{ message: string }> {
    try {
      return await apiClient.delete('/api/users/me/sessions');
    } catch (error) {
      throw handleApiError(error, 'revoke all sessions');
    }
  }
};

// Export for individual imports if needed
export const {
  getProfile,
  updateProfile,
  getSettings,
  updateSettings,
  uploadAvatar,
  deleteAvatar,
  changePassword,
  requestPasswordReset,
  resetPassword,
  getUserStats,
  getActivityLog,
  searchUsers,
  getUsers,
  getUserById,
  createUser,
  updateUser,
  deactivateUser,
  reactivateUser,
  deleteUser,
  validateEmail,
  checkUsernameAvailability,
  bulkUpdateUsers,
  exportUsers,
  getActiveSessions,
  revokeSession,
  revokeAllSessions
} = usersService;