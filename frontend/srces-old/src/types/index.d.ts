// frontend/src/types/index.d.ts

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  roles: string[];
  permissions: string[];
  clinic_name?: string;
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

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  message?: string;
}

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

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}

export interface ApiResponse<T = any> {
  data?: T;
  error?: string;
  status: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  user: any;
  message?: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  clinic_name: string;
  organization_id: string;
  role: string;
}

export interface CurrentUserResponse {
  user: User;
}

export interface Patient {
  id: number;
  organization_id?: number;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  address?: any;
  emergency_contact?: any;
  medical_history?: any;
  allergies?: any;
  medications?: any;
  insurance?: any;
  notes?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: number;
  organization_id: number;
  patient_id: number;
  dentist_id: number;
  cancelled_by?: number;
  created_by?: number;
  title: string;
  description?: string;
  type: string;
  status: string;
  priority: string;
  start_time: string;
  end_time: string;
  duration: number;
  room?: string;
  location?: string;
  treatment_notes?: string;
  prescribed_medications?: any;
  follow_up_required: boolean;
  follow_up_date?: string;
  cost?: number;
  insurance_covered?: number;
  patient_payment?: number;
  payment_status: string;
  reminder_sent: boolean;
  confirmation_sent: boolean;
  sms_reminder: boolean;
  email_reminder: boolean;
  cancellation_reason?: string;
  cancellation_date?: string;
  created_at: string;
  updated_at: string;
  patient?: Patient;
  dentist?: any;
}

export interface Organization {
  id: number;
  name: string;
  type: string;
  subscription_plan: string;
  max_staff: number;
  max_patients: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RefreshTokenResponse {
  access_token: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  user: User;
  message?: string;
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

