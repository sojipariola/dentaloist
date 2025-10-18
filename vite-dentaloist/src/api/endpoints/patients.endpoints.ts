export const PATIENTS_ENDPOINTS = {
  LIST: '/patients',
  CREATE: '/patients',
  DETAIL: (id: number) => `/patients/${id}`,
  UPDATE: (id: number) => `/patients/${id}`,
  DELETE: (id: number) => `/patients/${id}`,
  MEDICAL_HISTORY: (id: number) => `/patients/${id}/medical-history`,
  REACTIVATE: (id: number) => `/patients/${id}/reactivate`,
  IMPORT: '/patients/import',
  STATS: '/patients/stats',
} as const