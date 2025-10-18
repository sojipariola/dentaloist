// frontend/src/services/organizations/types.ts
// src/services/organizations/types.ts
export interface Organization {
  id: number;
  name: string;
  address?: string;
  phone?: string;
  email?: string;
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

export interface CreateOrganizationData {
  name: string;
  address?: string;
  phone?: string;
  email?: string;
}

export interface UpdateOrganizationData {
  name?: string;
  address?: string;
  phone?: string;
  email?: string;
}

// You can add more types as needed for organization-related data