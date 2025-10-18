// src/utils/typeGuards.ts
import { BaseUser } from '@/types/api/auth.types'

export function isBaseUser(user: any): user is BaseUser {
  return (
    user &&
    typeof user.id === 'number' &&
    typeof user.email === 'string' &&
    typeof user.first_name === 'string' &&
    typeof user.last_name === 'string' &&
    typeof user.role === 'string' &&
    typeof user.user_role_id === 'number' &&
    typeof user.organization_id === 'string' &&
    typeof user.is_admin === 'boolean' &&
    typeof user.email_verified === 'boolean' &&
    typeof user.public_id === 'string' &&
    typeof user.created_at === 'string' &&
    typeof user.is_active === 'boolean'
  )
}