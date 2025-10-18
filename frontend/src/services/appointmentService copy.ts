// src/services/appointmentService.ts
import { api } from './api';
import { Appointment } from '@/types';

export const appointmentService = {
  async getAppointments(filters = {}): Promise<Appointment[]> {
    const response = await api.get('/appointments', { params: filters });
    return response.data;
  },

  async getAppointment(id: number): Promise<Appointment> {
    const response = await api.get(`/appointments/${id}`);
    return response.data;
  },

  async createAppointment(appointmentData: Partial<Appointment>): Promise<Appointment> {
    const response = await api.post('/appointments', appointmentData);
    return response.data;
  },

  async updateAppointment(id: number, appointmentData: Partial<Appointment>): Promise<Appointment> {
    const response = await api.put(`/appointments/${id}`, appointmentData);
    return response.data;
  },

  async deleteAppointment(id: number): Promise<void> {
    await api.delete(`/appointments/${id}`);
  }
};