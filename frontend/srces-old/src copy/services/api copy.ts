import axios from 'axios'
import { getAccessToken, getRefreshToken, setTokens, clearTokens } from './token'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:5000'

const api = axios.create({
  baseURL: API_URL,
})

api.interceptors.request.use(config => {
  const token = getAccessToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  res => res,
  async error => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refreshToken = getRefreshToken()
      if (refreshToken) {
        try {
          const res = await axios.post(`${API_URL}/auth/refresh`, { refresh_token: refreshToken })
          setTokens(res.data.access_token, res.data.refresh_token)
          originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`
          return api(originalRequest)
        } catch (err) {
          clearTokens()
          window.location.href = '/login'
        }
      }
    }
    return Promise.reject(error)
  }
)

export default api
