// src/types/notifications.ts
export interface Notification {
  id: number;
  userId: number;
  type: NotificationType;
  title: string;
  message: string;
  data?: NotificationData;
  priority: NotificationPriority;
  isRead: boolean;
  actionUrl?: string;
  expiresAt?: Date;
  createdAt: Date;
  
  // Relations
  user?: User;
}

export interface NotificationData {
  [key: string]: any;
}

export interface NotificationPreferences {
  email: boolean;
  sms: boolean;
  push: boolean;
  inApp: boolean;
  categories: NotificationCategoryPreferences;
}

export interface NotificationCategoryPreferences {
  appointments: boolean;
  billing: boolean;
  security: boolean;
  system: boolean;
  marketing: boolean;
}

export enum NotificationType {
  APPOINTMENT_REMINDER = 'appointment_reminder',
  APPOINTMENT_CONFIRMATION = 'appointment_confirmation',
  APPOINTMENT_CANCELLATION = 'appointment_cancellation',
  BILLING_INVOICE = 'billing_invoice',
  BILLING_PAYMENT = 'billing_payment',
  SECURITY_ALERT = 'security_alert',
  SYSTEM_UPDATE = 'system_update',
  NEW_MESSAGE = 'new_message',
  TASK_ASSIGNMENT = 'task_assignment'
}

export enum NotificationPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}