import { Patient } from './patient';

export enum AppointmentStatus {
  SCHEDULED = 'scheduled',
  CONFIRMED = 'confirmed',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
  NO_SHOW = 'no_show',
  RESCHEDULED = 'rescheduled',
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
  OTHER = 'other',
}

export enum PriorityLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent',
}

export interface Appointment {
  id: number;
  organization_id: string;
  patient_id: number;
  dentist_id: number;
  cancelled_by?: number;
  created_by?: number;
  title: string;
  description?: string;
  type: AppointmentType;
  status: AppointmentStatus;
  priority: PriorityLevel;
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
  patient?: {       //Patient;
    id: number;
    first_name: string;
    last_name: string;
  }
  dentist?: {
    id: number;
    first_name: string;
    last_name: string;
  };
}
