export const APPOINTMENTS_ENDPOINTS = {
  LIST: '/appointments',
  CREATE: '/appointments',
  DETAIL: (id: number) => `/appointments/${id}`,
  UPDATE: (id: number) => `/appointments/${id}`,
  DELETE: (id: number) => `/appointments/${id}`,
  CANCEL: (id: number) => `/appointments/${id}/cancel`,
  COMPLETE: (id: number) => `/appointments/${id}/complete`,
  AVAILABILITY: '/appointments/availability',
  TODAY: '/appointments/today',
  UPCOMING: '/appointments/upcoming',
} as const