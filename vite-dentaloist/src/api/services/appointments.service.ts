import { axiosClient } from '@/api/client/axiosClient'
import { handleApiError } from '@/api/client/interceptors'
import { APPOINTMENTS_ENDPOINTS } from '@/api/endpoints'

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

export interface AppointmentFilters {
  page?: number
  limit?: number
  search?: string
  status?: string
  date_from?: string
  date_to?: string
  dentist_id?: number
}

export interface AppointmentsResponse {
  appointments: Appointment[]
  total: number
  page: number
  limit: number
  totalPages: number
}

export const appointmentsService = {
  async getAppointments(filters: AppointmentFilters = {}): Promise<AppointmentsResponse> {
    try {
      const response = await axiosClient.get(APPOINTMENTS_ENDPOINTS.LIST, {
        params: filters,
      })
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async getAppointment(id: number): Promise<Appointment> {
    try {
      const response = await axiosClient.get(APPOINTMENTS_ENDPOINTS.DETAIL(id))
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async createAppointment(appointment: Omit<Appointment, 'id' | 'public_id' | 'created_at' | 'updated_at' | 'is_active'>): Promise<Appointment> {
    try {
      const response = await axiosClient.post(APPOINTMENTS_ENDPOINTS.CREATE, appointment)
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async updateAppointment(id: number, appointment: Partial<Appointment>): Promise<Appointment> {
    try {
      const response = await axiosClient.put(APPOINTMENTS_ENDPOINTS.UPDATE(id), appointment)
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async deleteAppointment(id: number): Promise<void> {
    try {
      await axiosClient.delete(APPOINTMENTS_ENDPOINTS.DELETE(id))
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async cancelAppointment(id: number, reason?: string): Promise<Appointment> {
    try {
      const response = await axiosClient.post(APPOINTMENTS_ENDPOINTS.CANCEL(id), {
        cancellation_reason: reason,
      })
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async completeAppointment(id: number): Promise<Appointment> {
    try {
      const response = await axiosClient.post(APPOINTMENTS_ENDPOINTS.COMPLETE(id))
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async checkAvailability(params: {
    start_time: string
    end_time: string
    dentist_id?: number
    treatment_room?: string
  }): Promise<{ available: boolean; conflicts?: any[] }> {
    try {
      const response = await axiosClient.get(APPOINTMENTS_ENDPOINTS.AVAILABILITY, {
        params,
      })
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },
}