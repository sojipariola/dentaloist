// src/services/api/config.ts
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

export const API_CONFIG = {
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
};

export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: '/api/auth/login',
    REGISTER: '/api/auth/register',
    LOGOUT: '/api/auth/logout',
    ME: '/api/auth/me',
    REFRESH: '/api/auth/refresh',
    GOOGLE: '/api/auth/google/login',
    FACEBOOK: '/api/auth/facebook/login',
    GITHUB: '/api/auth/github/login',
  },
  DASHBOARD: {
    STATS: '/api/dashboard/stats',
  },
  PATIENTS: {
    LIST: '/api/patients',
    DETAIL: '/api/patients/:id',
    CREATE: '/api/patients',
    UPDATE: '/api/patients/:id',
    DELETE: '/api/patients/:id',
  },
  APPOINTMENTS: {
    LIST: '/api/appointments',
    DETAIL: '/api/appointments/:id',
    CREATE: '/api/appointments',
    UPDATE: '/api/appointments/:id',
    DELETE: '/api/appointments/:id',
    CANCEL: '/api/appointments/:id/cancel',
  },
  ORGANIZATIONS: {
    LIST: '/api/organizations',
    DETAIL: '/api/organizations/:id',
    CREATE: '/api/organizations',
    UPDATE: '/api/organizations/:id',
    CURRENT: '/api/organization/current',
    SWITCH: '/api/organization/switch/:id',
  },
  REPORTS: {
    LIST: '/api/reports',
    GENERATE: '/api/reports/generate',
  },
};
