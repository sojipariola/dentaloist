// frontend/src/services/api/types.ts
// src/services/api/types.ts
export interface ApiResponse<T> {
  data: T;
  message: string;
  status: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface ApiError {
  message: string;
  status?: number;
  details?: any;
}
/*
// Re-exporting User and AuthResponse from auth types for convenience
export { 
  User, 
  AuthTokenResponse as AuthResponse, 
  RefreshTokenResponse 
} from '../types';

export { 
  Appointment, 
  CreateAppointmentData, 
  UpdateAppointmentData 
} from '../services/appointments/types';

export { 
  Patient, 
  CreatePatientData, 
  UpdatePatientData 
} from '../services/patients/types';

export { 
  Organization, 
  CreateOrganizationData, 
  UpdateOrganizationData 
} from '../services/organizations/types';

// You can add more types as needed for other services

*/