// frontend/src/types/auth.ts

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials{
  confirmPassword: string;
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
  clinic_name?: string;
  settings?: { /* ... full settings object ... */ },
  organization_id?: number;
  custom_role_id?: number;
  is_active: boolean;
  is_admin: boolean;
  last_login?: string;
  created_at: string;
  updated_at: string;
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

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => Promise<void>;
  googleLogin: () => void;
  facebookLogin: () => void;
  githubLogin: () => void;
  error: string | null;
  clearError: () => void;
  
  // User role methods
  hasRole: (role: UserRole | string) => boolean;
  hasAnyRole: (roles: (UserRole | string)[]) => boolean;
  hasAllRoles: (roles: (UserRole | string)[]) => boolean;
  isSuperAdmin: () => boolean;
  isOrgAdmin: () => boolean;
  isDentist: () => boolean;
  isLabTechnician: () => boolean;
  isAssistant: () => boolean;
  isNurse: () => boolean;
  isBillingStaff: () => boolean;
  isResearcher: () => boolean;
  isFamilyMember: () => boolean;
  isVisitor: () => boolean;
  isPatient: () => boolean;
  
  // Permission methods
  hasPermission: (permission: string) => boolean;
  hasAnyPermission: (permissions: string[]) => boolean;
  hasAllPermissions: (permissions: string[]) => boolean;
  checkPermissions: (check: PermissionCheck) => PermissionCheckResult;
  getUserPermissions: () => string[];
  getUserRoles: () => string[];
  
  // Organization methods
  isSameOrganization: (organizationId?: number) => boolean;
  canAccessOrganization: (organizationId?: number) => boolean;
}

// Aliases for backward compatibility if needed
export interface AuthResponse extends AuthTokenResponse {}
export interface LoginResponse extends AuthTokenResponse {}
export interface RegisterResponse extends AuthTokenResponse {}
