// src/services/appointments/appointmentsService.ts
import { apiClient } from '../api';
import { API_ENDPOINTS } from '../api/config';
import { Appointment, CreateAppointmentData, UpdateAppointmentData } from './types';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (typeof err === 'string') return new Error(err);
  if (err?.message) return new Error(err.message);
  return new Error(fallbackMessage);
};

export const appointmentsService = {
  // Get appointments with filters
  async getAppointments(params?: {
    page?: number;
    limit?: number;
    start_date?: string;
    end_date?: string;
    status?: string;
    patient_id?: number;
    dentist_id?: number;
    sort?: string;
  }): Promise<{ appointments: Appointment[]; total: number }> {
    try {
      const queryString = params
        ? '?' + new URLSearchParams(params as Record<string, string>).toString()
        : '';
      return await apiClient.get(API_ENDPOINTS.APPOINTMENTS.LIST + queryString);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch appointments');
    }
  },

  // Get single appointment
  async getAppointment(id: number): Promise<{ appointment: Appointment }> {
    try {
      const endpoint = API_ENDPOINTS.APPOINTMENTS.DETAIL.replace(':id', id.toString());
      return await apiClient.get(endpoint);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch appointment');
    }
  },

  // Create appointment
  async createAppointment(appointmentData: CreateAppointmentData): Promise<{ appointment: Appointment }> {
    try {
      return await apiClient.post(API_ENDPOINTS.APPOINTMENTS.CREATE, appointmentData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to create appointment');
    }
  },

  // Update appointment
  async updateAppointment(id: number, appointmentData: UpdateAppointmentData): Promise<{ appointment: Appointment }> {
    try {
      const endpoint = API_ENDPOINTS.APPOINTMENTS.UPDATE.replace(':id', id.toString());
      return await apiClient.put(endpoint, appointmentData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to update appointment');
    }
  },

  // Delete appointment
  async deleteAppointment(id: number): Promise<{ message: string }> {
    try {
      const endpoint = API_ENDPOINTS.APPOINTMENTS.DELETE.replace(':id', id.toString());
      return await apiClient.delete(endpoint);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to delete appointment');
    }
  },

  // Cancel appointment
  async cancelAppointment(id: number, reason: string): Promise<{ appointment: Appointment }> {
    try {
      const endpoint = API_ENDPOINTS.APPOINTMENTS.CANCEL.replace(':id', id.toString());
      return await apiClient.post(endpoint, { cancellation_reason: reason });
    } catch (err: any) {
      throw normalizeError(err, 'Failed to cancel appointment');
    }
  },
};