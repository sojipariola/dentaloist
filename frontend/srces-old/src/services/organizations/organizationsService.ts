// frontend/src/services/organizations/organizationsService.ts
// src/services/organizations/organizationsService.ts
import { apiClient } from '../api';
import { Organization, CreateOrganizationData, UpdateOrganizationData } from './types';

export const getOrganizations = async (): Promise<Organization[]> => {
  return apiClient.get('/api/organizations');
};

export const getOrganizationById = async (id: number): Promise<Organization> => {
  return apiClient.get(`/api/organizations/${id}`);
};

export const createOrganization = async (data: CreateOrganizationData): Promise<Organization> => {
  return apiClient.post('/api/organizations', data);
};

export const updateOrganization = async (id: number, data: UpdateOrganizationData): Promise<Organization> => {
  return apiClient.put(`/api/organizations/${id}`, data);
};

export const deleteOrganization = async (id: number): Promise<void> => {
  return apiClient.request(`/api/organizations/${id}`, { method: 'DELETE' });
};
