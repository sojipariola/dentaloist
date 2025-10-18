// frontend/src/services/patients/types.ts
// src/services/patients/types.ts

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

export interface CreatePatientData {
    first_name: string;
    last_name: string;
    date_of_birth: string; // ISO date string
    phone?: string;
    email?: string;
    address?: string;
}

export interface UpdatePatientData {
    first_name?: string;
    last_name?: string;
    date_of_birth?: string; // ISO date string
    phone?: string;
    email?: string;
    address?: string;
}

/* You can add more fields as needed based on your backend API response 
export interface CreatePatientData {
  first_name: string;
  last_name: string;
  date_of_birth: string; // ISO date string
  phone?: string;
  email?: string;
  address?: string;
}

export interface UpdatePatientData {
  first_name?: string;
  last_name?: string;
  date_of_birth?: string; // ISO date string
  phone?: string;
  email?: string;
  address?: string;
}

// You can add more types as needed for patient-related data
*/