// src/api/client/interceptors.ts

// import { AxiosResponse, AxiosError } from 'axios'
import { AxiosError } from 'axios'

export const setupResponseInterceptors = () => {
  // Global response handler can be added here
}

export interface ApiError {
  message: string
  status: number
  code?: string
  details?: any
}

export const handleApiError = (error: AxiosError): ApiError => {
  if (error.response) {
    // Server responded with error status
    const data = error.response.data as any
    return {
      message: data.message || 'An error occurred',
      status: error.response.status,
      code: data.code,
      details: data.details,
    }
  } else if (error.request) {
    // Request was made but no response received
    return {
      message: 'Network error. Please check your connection.',
      status: 0,
    }
  } else {
    // Something else happened
    return {
      message: error.message || 'An unexpected error occurred',
      status: -1,
    }
  }
}