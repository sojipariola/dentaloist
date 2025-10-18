export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
  role: 'admin' | 'dentist' | 'staff' | 'patient'
  phone?: string
  address?: string
  city?: string
  state?: string
  country?: string
  postal_code?: string
  timezone?: string
  avatar_url?: string
  bio?: string
  date_of_birth?: string
  gender_id?: number
  specialization?: string
  license_number?: string
  experience_years?: number
  clinic_name?: string
  user_role_id: number
  organization_id: string
  custom_role_id?: number
  tenant_id?: number
  is_admin: boolean
  email_verified: boolean
  last_login?: string
  last_activity?: string
  stripe_customer_id?: string
  settings?: any
  public_id: string
  created_at: string
  updated_at?: string
  is_active: boolean
}

// Base user type for authentication
export interface BaseUser {
  id: number
  email: string
  first_name: string
  last_name: string
  role: 'admin' | 'dentist' | 'staff' | 'patient'
  user_role_id: number
  organization_id: string
  is_admin: boolean
  email_verified: boolean
  public_id: string
  created_at: string
  is_active: boolean
}

// Full user type with all properties
export interface User extends BaseUser {
  phone?: string
  address?: string
  city?: string
  state?: string
  country?: string
  postal_code?: string
  timezone?: string
  avatar_url?: string
  bio?: string
  date_of_birth?: string
  gender_id?: number
  specialization?: string
  license_number?: string
  experience_years?: number
  clinic_name?: string
  custom_role_id?: number
  tenant_id?: number
  last_login?: string
  last_activity?: string
  stripe_customer_id?: string
  settings?: any
  updated_at?: string
}

export interface AuthResponse {
  user: BaseUser // Use BaseUser for auth responses
  token: string
  refresh_token: string
}


export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  first_name: string
  last_name: string
  email: string
  password: string
  role?: User['role']
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  expires_in?: number
}

export interface LoginResponse {
  user: User
  tokens: AuthTokens
}

export interface RegisterRequest {
  email: string
  password: string
  first_name: string
  last_name: string
  phone?: string
  organization_name?: string
}

export interface LoginRequest {
  email: string
  password: string
  remember_me?: boolean
}