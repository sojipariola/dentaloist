// src/types/settings.ts
export interface UserSettings {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  emailNotifications: boolean;
  smsNotifications: boolean;
  pushNotifications: boolean;
  appointmentReminders: boolean;
  billingNotifications: boolean;
  timezone: string;
  dateFormat: string;
  timeFormat: '12h' | '24h';
  weekStart: number;
  showOnlineStatus: boolean;
  allowProfileView: boolean;
  highContrastMode: boolean;
  reducedMotion: boolean;
}

export interface OrganizationSettings {
  timezone: string;
  locale: string;
  dateFormat: string;
  timeFormat: '12h' | '24h';
  currency: string;
  businessHours: BusinessHours;
  appointmentReminders: boolean;
  smsNotifications: boolean;
  emailNotifications: boolean;
  autoConfirmAppointments: boolean;
  cancellationPolicy: CancellationPolicy;
  privacySettings: PrivacySettings;
}

export interface CancellationPolicy {
  noticeHours: number;
  feePercentage: number;
  maxCancellations: number;
}

export interface PrivacySettings {
  dataRetention: DataRetention;
  accessControls: AccessControls;
  auditLogging: boolean;
}

export interface DataRetention {
  patientRecords: number; // months
  financialRecords: number; // months
  auditLogs: number; // months
}

export interface AccessControls {
  ipRestrictions: string[];
  twoFactorRequired: boolean;
  sessionTimeout: number; // minutes
}