// src/types/appointments.ts
export interface Appointment {
  id: number;
  organizationId: string;
  patientId: number;
  dentistId: number;
  title: string;
  description?: string;
  type: AppointmentType;
  status: AppointmentStatus;
  priority: PriorityLevel;
  startTime: Date;
  endTime: Date;
  duration: number;
  room?: string;
  location?: string;
  treatmentNotes?: string;
  prescribedMedications?: Medication[];
  followUpRequired: boolean;
  followUpDate?: Date;
  cost?: number;
  insuranceCovered?: number;
  patientPayment?: number;
  paymentStatus: PaymentStatus;
  reminderSent: boolean;
  confirmationSent: boolean;
  smsReminder: boolean;
  emailReminder: boolean;
  cancellationReason?: string;
  cancellationDate?: Date;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  dentist?: User;
  organization?: Organization;
}

export interface AppointmentCreate {
  patientId: number;
  dentistId: number;
  title: string;
  type: AppointmentType;
  startTime: Date;
  duration: number;
  description?: string;
  priority?: PriorityLevel;
}

export interface AppointmentUpdate {
  title?: string;
  description?: string;
  status?: AppointmentStatus;
  priority?: PriorityLevel;
  startTime?: Date;
  duration?: number;
  room?: string;
  treatmentNotes?: string;
}

export enum AppointmentType {
  CONSULTATION = 'consultation',
  CHECKUP = 'checkup',
  CLEANING = 'cleaning',
  FILLING = 'filling',
  EXTRACTION = 'extraction',
  ROOT_CANAL = 'root_canal',
  CROWN = 'crown',
  BRACES = 'braces',
  IMPLANT = 'implant',
  EMERGENCY = 'emergency',
  FOLLOW_UP = 'follow_up',
  OTHER = 'other'
}

export enum AppointmentStatus {
  SCHEDULED = 'scheduled',
  CONFIRMED = 'confirmed',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
  NO_SHOW = 'no_show',
  RESCHEDULED = 'rescheduled'
}

export enum PriorityLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export enum PaymentStatus {
  PENDING = 'pending',
  PARTIAL = 'partial',
  PAID = 'paid',
  INSURANCE_PENDING = 'insurance_pending',
  DENIED = 'denied'
}