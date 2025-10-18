import { Gender } from './user';

export interface Patient {
  id: number;
  organization_id: string;
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  date_of_birth?: string;
  gender?: Gender;
  address?: any;
  emergency_contact?: any;
  medical_history?: any;
  allergies?: any;
  medications?: any;
  insurance?: any;
  notes?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}
