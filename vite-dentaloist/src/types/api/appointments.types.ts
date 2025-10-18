export interface Appointment {
  id: number
  public_id: string
  organization_id: string
  patient_id: number
  dentist_id?: number
  treatment_id?: number
  staff_id?: number
  availability_slot_id?: number
  appointment_type_id: number
  status_id: number
  priority_id?: number
  title: string
  description?: string
  start_time: string
  end_time: string
  duration: number
  actual_start_time?: string
  actual_end_time?: string
  actual_duration?: number
  treatment_room?: string
  location?: string
  equipment_needed?: any[]
  chief_complaint?: string
  treatment_notes?: string
  prescribed_medications?: any[]
  follow_up_required?: boolean
  follow_up_date?: string
  estimated_cost?: number
  insurance_covered?: number
  patient_payment?: number
  payment_status?: string
  reminder_sent?: boolean
  confirmation_sent?: boolean
  sms_reminder?: boolean
  email_reminder?: boolean
  reminder_sent_at?: string
  cancellation_reason?: string
  cancelled_by_id?: number
  cancellation_date?: string
  created_at: string
  updated_at?: string
  is_active: boolean
}

export interface AppointmentCreateRequest {
  patient_id: number
  dentist_id?: number
  appointment_type_id: number
  start_time: string
  end_time: string
  title: string
  description?: string
  treatment_room?: string
  location?: string
  equipment_needed?: any[]
  chief_complaint?: string
}

export interface AppointmentUpdateRequest extends Partial<AppointmentCreateRequest> {
  status_id?: number
  actual_start_time?: string
  actual_end_time?: string
  treatment_notes?: string
  prescribed_medications?: any[]
  follow_up_required?: boolean
  follow_up_date?: string
}