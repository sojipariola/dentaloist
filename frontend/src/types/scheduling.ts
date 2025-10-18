// src/types/scheduling.ts
export interface Schedule {
  id: number;
  providerId: number;
  date: Date;
  slots: TimeSlot[];
  isAvailable: boolean;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  provider?: User;
}

export interface TimeSlot {
  start: string;
  end: string;
  isAvailable: boolean;
  appointmentId?: number;
  type?: AppointmentType;
  status?: SlotStatus;
}

export interface ScheduleTemplate {
  id: number;
  providerId: number;
  name: string;
  type: TemplateType;
  slots: TemplateSlot[];
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  provider?: User;
}

export interface TemplateSlot {
  dayOfWeek: number;
  start: string;
  end: string;
  type: AppointmentType;
  duration: number;
  maxPatients: number;
}

export interface Blockout {
  id: number;
  providerId: number;
  start: Date;
  end: Date;
  reason: BlockoutReason;
  description?: string;
  isRecurring: boolean;
  recurrencePattern?: RecurrencePattern;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  provider?: User;
}

export interface RecurrencePattern {
  frequency: RecurrenceFrequency;
  interval: number;
  daysOfWeek?: number[];
  endDate?: Date;
}

export enum SlotStatus {
  AVAILABLE = 'available',
  BOOKED = 'booked',
  BLOCKED = 'blocked',
  BREAK = 'break'
}

export enum TemplateType {
  WEEKLY = 'weekly',
  DAILY = 'daily',
  CUSTOM = 'custom'
}

export enum BlockoutReason {
  VACATION = 'vacation',
  MEETING = 'meeting',
  TRAINING = 'training',
  EMERGENCY = 'emergency',
  MAINTENANCE = 'maintenance'
}

export enum RecurrenceFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  YEARLY = 'yearly'
}