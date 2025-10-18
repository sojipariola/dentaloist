// src/utils/userAdapter.ts
import { BaseUser, User } from '@/types/api/auth.types'

// Adapter to convert BaseUser (from API) to full User type
export function adaptUser(baseUser: BaseUser): User {
  return {
    ...baseUser,
    // Add default values for optional properties that might be missing
    phone: baseUser.phone || undefined,
    address: baseUser.address || undefined,
    city: baseUser.city || undefined,
    state: baseUser.state || undefined,
    country: baseUser.country || undefined,
    postal_code: baseUser.postal_code || undefined,
    timezone: baseUser.timezone || undefined,
    avatar_url: baseUser.avatar_url || undefined,
    bio: baseUser.bio || undefined,
    date_of_birth: baseUser.date_of_birth || undefined,
    gender_id: baseUser.gender_id || undefined,
    specialization: baseUser.specialization || undefined,
    license_number: baseUser.license_number || undefined,
    experience_years: baseUser.experience_years || undefined,
    clinic_name: baseUser.clinic_name || undefined,
    custom_role_id: baseUser.custom_role_id || undefined,
    tenant_id: baseUser.tenant_id || undefined,
    last_login: baseUser.last_login || undefined,
    last_activity: baseUser.last_activity || undefined,
    stripe_customer_id: baseUser.stripe_customer_id || undefined,
    settings: baseUser.settings || undefined,
    updated_at: baseUser.updated_at || undefined,
  }
}