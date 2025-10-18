// src/services/patients/patientsService.ts
import { apiClient } from '../api';
import { API_ENDPOINTS } from '../api/config';
import { Patient, CreatePatientData, UpdatePatientData } from './types';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (typeof err === 'string') return new Error(err);
  if (err?.message) return new Error(err.message);
  return new Error(fallbackMessage);
};

export const patientsService = {
  // Get all patients
  async getPatients(params?: {
    page?: number;
    limit?: number;
    search?: string;
  }): Promise<{ patients: Patient[]; total: number }> {
    try {
      const queryString = params
        ? '?' +
          Object.entries(params)
            .filter(([_, v]) => v !== undefined && v !== null && v !== '')
            .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
            .join('&')
        : '';
      return await apiClient.get(API_ENDPOINTS.PATIENTS.LIST + queryString);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch patients');
    }
  },

  // Get single patient
  async getPatient(id: number): Promise<{ patient: Patient }> {
    try {
      const endpoint = API_ENDPOINTS.PATIENTS.DETAIL.replace(':id', id.toString());
      return await apiClient.get(endpoint);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch patient');
    }
  },

  // Create patient
  async createPatient(patientData: CreatePatientData): Promise<{ patient: Patient }> {
    try {
      return await apiClient.post(API_ENDPOINTS.PATIENTS.CREATE, patientData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to create patient');
    }
  },

  // Update patient
  async updatePatient(id: number, patientData: UpdatePatientData): Promise<{ patient: Patient }> {
    try {
      const endpoint = API_ENDPOINTS.PATIENTS.UPDATE.replace(':id', id.toString());
      return await apiClient.put(endpoint, patientData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to update patient');
    }
  },

  // Delete patient
  async deletePatient(id: number): Promise<{ message: string }> {
    try {
      const endpoint = API_ENDPOINTS.PATIENTS.DELETE.replace(':id', id.toString());
      return await apiClient.delete(endpoint);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to delete patient');
    }
  },
};