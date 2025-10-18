// src/types/organizations.ts
export interface Organization {
  id: string;
  name: string;
  type: OrganizationType;
  subscriptionPlan: SubscriptionPlan;
  maxStaff: number;
  maxPatients: number;
  isActive: boolean;
  settings: OrganizationSettings;
  createdAt: Date;
  updatedAt: Date;
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
}

export interface BusinessHours {
  monday: TimeRange;
  tuesday: TimeRange;
  wednesday: TimeRange;
  thursday: TimeRange;
  friday: TimeRange;
  saturday: TimeRange;
  sunday: TimeRange;
}

export interface TimeRange {
  open: string;
  close: string;
  isClosed: boolean;
}

export enum OrganizationType {
  CLINIC = 'clinic',
  LABORATORY = 'laboratory',
  FAMILY = 'family'
}

export enum SubscriptionPlan {
  FREE = 'free',
  STARTER = 'starter',
  PROFESSIONAL = 'professional',
  ENTERPRISE = 'enterprise'
}