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
}

export enum Gender {
  MALE = "male",
  FEMALE = "female",
  OTHER = "other",
  PREFER_NOT_TO_SAY = "prefer_not_to_say",
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string | null;           // ✅ Allow null
  avatar_url?: string | null;      // ✅ Allow null
  bio?: string | null;             // ✅ Allow null
  date_of_birth?: string | null;   // ✅ Allow null
  gender?: Gender | null;          // ✅ Allow null
  address?: any | null;            // ✅ Allow null
  emergency_contact?: any | null;  // ✅ Allow null
  specialization?: string | null;  // ✅ Allow null
  license_number?: string | null;  // ✅ Allow null
  experience_years?: number | null; // ✅ Allow null
  role: UserRole;
  clinic_name?: string | null;     // ✅ Allow null
  organization_id: string;
  custom_role_id?: number | null;  // ✅ Allow null
  is_active: boolean;
  is_admin: boolean;
  last_login?: string | null;      // ✅ Allow null
  created_at: string;
  updated_at: string;
  tenant_id?: string | null;       // ✅ Allow null
  stripe_customer_id?: string | null; // ✅ Allow null
  permissions: string[];
  settings: UserSettings;
}

export interface UserSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  email_notifications: boolean;
  sms_notifications: boolean;
  push_notifications: boolean;
  appointment_reminders: boolean;
  billing_notifications: boolean;
  timezone: string;
  date_format: string;
  time_format: string;
  week_start: number;
  show_online_status: boolean;
  allow_profile_view: boolean;
  high_contrast_mode: boolean;
  reduced_motion: boolean;
}

