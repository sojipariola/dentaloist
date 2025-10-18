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
  phone?: string;
  avatar_url?: string;
  role: UserRole;
  permissions: string[];
  organization_id: string;
  settings: UserSettings;
}

export interface UserSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  // ... from your model
}