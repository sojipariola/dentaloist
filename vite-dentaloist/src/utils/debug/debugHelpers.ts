// Debug utilities for development
export const debug = {
  log: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.log(`🔍 [DEBUG] ${message}`, data || '')
    }
  },
  
  error: (message: string, error?: any) => {
    if (import.meta.env.DEV) {
      console.error(`❌ [DEBUG] ${message}`, error || '')
    }
  },
  
  warn: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.warn(`⚠️ [DEBUG] ${message}`, data || '')
    }
  },
  
  // Check if user is authenticated
  checkAuth: () => {
    const token = localStorage.getItem('access_token')
    return {
      hasToken: !!token,
      token: token ? `${token.substring(0, 20)}...` : 'No token',
      isAuthenticated: !!token
    }
  },
  
  // Check API connectivity
  checkAPI: async () => {
    try {
      const response = await fetch('http://localhost:5000/api/health')
      return {
        status: response.status,
        ok: response.ok,
        url: response.url
      }
    } catch (error) {
      return {
        error: error instanceof Error ? error.message : 'Unknown error',
        status: 'offline'
      }
    }
  },
  
  // Clear all local storage
  clearStorage: () => {
    localStorage.clear()
    sessionStorage.clear()
    console.log('🧹 Storage cleared')
  },
  
  // Mock data generator for testing
  generateMockPatient: () => ({
    first_name: 'Test',
    last_name: 'Patient',
    email: `test.patient${Date.now()}@example.com`,
    phone: '+1 (555) 123-4567',
    date_of_birth: '1985-01-15',
    gender: 'other'
  })
}