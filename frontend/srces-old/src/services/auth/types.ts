// frontend/src/types/auth.ts

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials{
  confirmPassword?: string;
  first_name: string;
  last_name: string;
  organization_id?: string;
  clinic_name: string;
  role: UserRole;
}

export interface AuthTokenResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  message?: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  roles: string[];
  permissions: string[];
  is_active: boolean;
  is_admin: boolean;  
  created_at: string;
  updated_at: string; 
  clinic_name?: string;
  settings?: { /* ... full settings object ... */ },
  organization_id?: number;
  custom_role_id?: number;
  last_login?: string;
}


export enum UserRole {
  SUPER_ADMIN = 'super_admin',
  ORG_ADMIN = 'org_admin',
  DENTIST = 'dentist',
  LAB_TECHNICIAN = 'lab_technician',
  ASSISTANT = 'assistant',
  NURSE = 'nurse',
  BILLING_STAFF = 'billing_staff',
  RESEARCHER = 'researcher',
  FAMILY_MEMBER = 'family_member',
  VISITOR = 'visitor',
  PATIENT = 'patient',
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

export interface RefreshTokenResponse {
  access_token: string;
}

export interface CurrentUserResponse {
  user: User;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

// Permission types
export interface PermissionCheck {
  requiredPermission?: string;
  requiredPermissions?: string[]; // For multiple permissions
  requireAll?: boolean; // If true, user must have ALL required permissions
}

export type PermissionCheckResult = {
  hasPermission: boolean;
  missingPermissions?: string[];
};

// Aliases for backward compatibility if needed
export interface AuthResponse extends AuthTokenResponse {}
export interface LoginResponse extends AuthTokenResponse {}
export interface RegisterResponse extends AuthTokenResponse {}
