// src/types/index.ts

export interface Organization {
  id: string;
  name: string;
  type: string;
  subscription_plan: string;
  max_staff: number;
  max_patients: number;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface DashboardStats {
  totalPatients: number;
  totalAppointments: number;
  revenue: number;
  pendingTasks: number;
  organization?: Organization;
}