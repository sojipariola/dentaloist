// frontend/src/services/appointments/types.ts
// src/services/appointments/types.ts
export interface Appointment {
  id: number;
  patient_id: number;
  dentist_id: number;
  date: string; // ISO date string
  time: string; // e.g., "14:30"
  status: 'scheduled' | 'completed' | 'canceled';
  notes?: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface CreateAppointmentData {
  patient_id: number;
  dentist_id: number;
  date: string; // ISO date string
  time: string; // e.g., "14:30"
  notes?: string;
}

export interface UpdateAppointmentData {
  date?: string; // ISO date string
  time?: string; // e.g., "14:30"
  status?: 'scheduled' | 'completed' | 'canceled';
  notes?: string;
}

// You can add more types as needed for appointment-related data