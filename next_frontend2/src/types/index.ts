// types/index.ts
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  avatar_url?: string;
  role: string;
  organization_id: string;
  is_active: boolean;
  is_admin: boolean;
  permissions: string[];
  settings: Record<string, any>;
}

export interface Organization {
  id: string;
  name: string;
  type: string;
  subscription_plan: string;
  max_staff: number;
  max_patients: number;
  is_active: boolean;
}

export interface Patient {
  id: number;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: string;
  organization_id: string;
}

export interface Appointment {
  id: number;
  title: string;
  description?: string;
  type: string;
  status: string;
  priority: string;
  start_time: string;
  end_time: string;
  duration: number;
  patient: {
    id: number;
    first_name: string;
    last_name: string;
  };
  dentist: {
    id: number;
    first_name: string;
    last_name: string;
  };
  cost?: number;
  payment_status: string;
}

export interface DashboardStats {
  total_patients: number;
  total_appointments: number;
  revenue: number;
  pending_tasks: number;
}