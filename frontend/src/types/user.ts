// frontend/src/services/users/types.ts
// src/services/users/types.ts

// User Profile Types
export interface UserProfile {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  bio?: string;
  date_of_birth?: string;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  address?: UserAddress;
  emergency_contact?: EmergencyContact;
  specialization?: string;
  license_number?: string;
  experience_years?: number;
  is_active: boolean;
  is_admin: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
  // Role information from authentication
  role?: string;
  roles?: string[];
  permissions?: string[];
  organization_id?: number;
  clinic_name?: string;
}

export interface UserAddress {
  street?: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  formatted_address?: string;
}

export interface EmergencyContact {
  name?: string;
  relationship?: string;
  phone?: string;
  email?: string;
  primary?: boolean;
}

// User Settings Types
export interface UserSettings {
  id: number;
  user_id: number;
  // Appearance
  theme: 'light' | 'dark' | 'auto';
  language: string;
  // Notifications
  email_notifications: boolean;
  sms_notifications: boolean;
  push_notifications: boolean;
  appointment_reminders: boolean;
  billing_notifications: boolean;
  // Preferences
  timezone: string;
  date_format: 'MM/DD/YYYY' | 'DD/MM/YYYY' | 'YYYY-MM-DD';
  time_format: '12h' | '24h';
  week_start: 0 | 1; // 0 = Sunday, 1 = Monday
  // Privacy
  show_online_status: boolean;
  allow_profile_view: boolean;
  // Accessibility
  high_contrast_mode: boolean;
  reduced_motion: boolean;
  created_at: string;
  updated_at: string;
}

// Data Transfer Objects (DTOs)
export interface CreateUserDto {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: string;
  organization_id?: number;
  specialization?: string;
  license_number?: string;
  is_admin?: boolean;
}

export interface UpdateProfileDto {
  first_name?: string;
  last_name?: string;
  phone?: string;
  bio?: string;
  date_of_birth?: string;
  gender?: 'male' | 'female' | 'other' | 'prefer_not_to_say';
  address?: Partial<UserAddress>;
  emergency_contact?: Partial<EmergencyContact>;
  specialization?: string;
  license_number?: string;
  experience_years?: number;
}

export interface UpdateSettingsDto {
  theme?: 'light' | 'dark' | 'auto';
  language?: string;
  email_notifications?: boolean;
  sms_notifications?: boolean;
  push_notifications?: boolean;
  appointment_reminders?: boolean;
  billing_notifications?: boolean;
  timezone?: string;
  date_format?: 'MM/DD/YYYY' | 'DD/MM/YYYY' | 'YYYY-MM-DD';
  time_format?: '12h' | '24h';
  week_start?: 0 | 1;
  show_online_status?: boolean;
  allow_profile_view?: boolean;
  high_contrast_mode?: boolean;
  reduced_motion?: boolean;
}

export interface ChangePasswordDto {
  current_password: string;
  new_password: string;
  confirm_password: string;
}

export interface ResetPasswordRequestDto {
  email: string;
}

export interface ResetPasswordDto {
  token: string;
  password: string;
  confirm_password: string;
}

// API Response Types
export interface UserResponse {
  user: UserProfile;
  message?: string;
}

export interface UsersListResponse {
  users: UserProfile[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface SettingsResponse {
  settings: UserSettings;
}

export interface UploadAvatarResponse {
  avatar_url: string;
  message: string;
}

export interface PasswordChangeResponse {
  message: string;
  success: boolean;
}

// User Statistics Types
export interface UserStats {
  total_appointments: number;
  completed_appointments: number;
  upcoming_appointments: number;
  cancelled_appointments: number;
  total_patients?: number;
  average_rating?: number;
  years_experience?: number;
  monthly_revenue?: number;
  appointment_completion_rate: number;
  patient_satisfaction_score?: number;
  stats_period?: {
    start_date: string;
    end_date: string;
  };
}

export interface StatsResponse {
  stats: UserStats;
}

// User Activity Types
export interface UserActivity {
  id: number;
  user_id: number;
  action: string;
  description: string;
  entity_type?: string;
  entity_id?: number;
  ip_address?: string;
  user_agent?: string;
  location?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

export interface ActivityResponse {
  activities: UserActivity[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

// Search and Filter Types
export interface UsersQueryParams {
  page?: number;
  limit?: number;
  search?: string;
  role?: string;
  is_active?: boolean;
  is_admin?: boolean;
  organization_id?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface SearchUsersResponse {
  users: UserProfile[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

// Permission and Role Types
export interface UserPermission {
  id: number;
  name: string;
  description?: string;
  category: string;
}

export interface UserRole {
  id: number;
  name: string;
  description?: string;
  permissions: UserPermission[];
  is_system_role: boolean;
}

export interface RolesResponse {
  roles: UserRole[];
}

export interface PermissionsResponse {
  permissions: UserPermission[];
}

// File Upload Types
export interface FileUploadOptions {
  maxSize?: number; // in bytes
  allowedTypes?: string[];
  multiple?: boolean;
}

export interface UploadProgress {
  loaded: number;
  total: number;
  percentage: number;
}

// Validation Types
export interface ValidationError {
  field: string;
  message: string;
  code: string;
}

export interface ApiErrorResponse {
  message: string;
  errors?: ValidationError[];
  code?: string;
  statusCode: number;
}

// Pagination Types
export interface PaginationParams {
  page: number;
  limit: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    total_pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}

// Notification Preferences
export interface NotificationPreferences {
  email: {
    appointments: boolean;
    billing: boolean;
    security: boolean;
    promotions: boolean;
  };
  sms: {
    appointments: boolean;
    security: boolean;
  };
  push: {
    appointments: boolean;
    messages: boolean;
    updates: boolean;
  };
}

// User Status Types
export interface UserStatus {
  is_online: boolean;
  last_active?: string;
  current_status?: 'available' | 'busy' | 'away' | 'offline';
  status_message?: string;
}

// Export all types for easy importing
export type {
  UserProfile as DefaultUserProfile,
  UserSettings as DefaultUserSettings,
};

// Utility types for partial updates
export type PartialUserProfile = Partial<UserProfile>;
export type PartialUserSettings = Partial<UserSettings>;

// Type guards
export const isUserProfile = (obj: any): obj is UserProfile => {
  return obj && typeof obj.id === 'number' && typeof obj.email === 'string';
};

export const isUserSettings = (obj: any): obj is UserSettings => {
  return obj && typeof obj.user_id === 'number' && typeof obj.theme === 'string';
};

// Constants
export const USER_GENDERS = ['male', 'female', 'other', 'prefer_not_to_say'] as const;
export const USER_THEMES = ['light', 'dark', 'auto'] as const;
export const DATE_FORMATS = ['MM/DD/YYYY', 'DD/MM/YYYY', 'YYYY-MM-DD'] as const;
export const TIME_FORMATS = ['12h', '24h'] as const;

// Default values
export const DEFAULT_USER_SETTINGS: Omit<UserSettings, 'id' | 'user_id' | 'created_at' | 'updated_at'> = {
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

export const DEFAULT_AVATAR_OPTIONS = {
  maxSize: 5 * 1024 * 1024, // 5MB
  allowedTypes: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
};