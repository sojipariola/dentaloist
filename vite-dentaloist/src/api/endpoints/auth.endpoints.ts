export const AUTH_ENDPOINTS = {
  LOGIN: '/auth/login',
  REGISTER: '/auth/register',
  LOGOUT: '/auth/logout',
  REFRESH: '/auth/refresh',
  FORGOT_PASSWORD: '/auth/forgot-password',
  RESET_PASSWORD: '/auth/reset-password',
  ME: '/auth/me',
  GOOGLE_LOGIN: '/auth/google/login',
  GOOGLE_CALLBACK: '/auth/google/callback',
  ADMIN_DIRECT_LOGIN: '/auth/admin-direct-login',
} as const