import { axiosClient } from '@/api/client/axiosClient'
import { handleApiError } from '@/api/client/interceptors'
import { PATIENTS_ENDPOINTS } from '@/api/endpoints'

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
  address?: any
  emergency_contact?: any
  medical_history?: any
  allergies?: any
  medications?: any
  insurance_info?: any
  status?: string
  created_at: string
  updated_at?: string
  is_active: boolean
}

export interface PatientFilters {
  page?: number
  limit?: number
  search?: string
  status?: string
  gender?: string
}

export interface PatientsResponse {
  patients: Patient[]
  total: number
  page: number
  limit: number
  totalPages: number
}

export const patientsService = {
  async getPatients(filters: PatientFilters = {}): Promise<PatientsResponse> {
    try {
      const response = await axiosClient.get(PATIENTS_ENDPOINTS.LIST, {
        params: filters,
      })
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async getPatient(id: number): Promise<Patient> {
    try {
      const response = await axiosClient.get(PATIENTS_ENDPOINTS.DETAIL(id))
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async createPatient(patient: Omit<Patient, 'id' | 'public_id' | 'created_at' | 'updated_at' | 'is_active'>): Promise<Patient> {
    try {
      const response = await axiosClient.post(PATIENTS_ENDPOINTS.CREATE, patient)
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async updatePatient(id: number, patient: Partial<Patient>): Promise<Patient> {
    try {
      const response = await axiosClient.put(PATIENTS_ENDPOINTS.UPDATE(id), patient)
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async deletePatient(id: number): Promise<void> {
    try {
      await axiosClient.delete(PATIENTS_ENDPOINTS.DELETE(id))
    } catch (error) {
      throw handleApiError(error)
    }
  },

  async getPatientStats(): Promise<any> {
    try {
      const response = await axiosClient.get(PATIENTS_ENDPOINTS.STATS)
      return response.data
    } catch (error) {
      throw handleApiError(error)
    }
  },
}