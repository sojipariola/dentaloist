export interface PatientAddress {
  street?: string
  city?: string
  state?: string
  postal_code?: string
  country?: string
}

export interface EmergencyContact {
  name?: string
  relationship?: string
  phone?: string
  email?: string
}

export interface MedicalHistory {
  conditions?: string[]
  medications?: string[]
  allergies?: string[]
  surgeries?: string[]
  family_history?: string[]
  notes?: string
}

export interface InsuranceInfo {
  provider?: string
  policy_number?: string
  group_number?: string
  effective_date?: string
  expiration_date?: string
  is_primary?: boolean
}

export interface Patient {
  id: number
  public_id: string
  organization_id: string
  first_name: string
  last_name: string
  email?: string
  phone?: string
  date_of_birth?: string
  gender?: string
  address?: PatientAddress
  emergency_contact?: EmergencyContact
  medical_history?: MedicalHistory
  allergies?: any[]
  medications?: any[]
  insurance_info?: InsuranceInfo
  dental_history?: any
  oral_hygiene?: string
  last_dental_visit?: string
  next_recall_date?: string
  status?: string
  preferred_language?: string
  communication_preferences?: any
  created_at: string
  updated_at?: string
  is_active: boolean
}

export interface PatientCreateRequest {
  first_name: string
  last_name: string
  email?: string
  phone?: string
  date_of_birth?: string
  gender?: string
  address?: PatientAddress
  emergency_contact?: EmergencyContact
  medical_history?: MedicalHistory
}

export interface PatientUpdateRequest extends Partial<PatientCreateRequest> {
  status?: string
  next_recall_date?: string
}