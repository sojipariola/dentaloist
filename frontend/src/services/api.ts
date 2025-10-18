import { fetcher } from '@/utils/fetcher'
import { User } from '@/types/auth'

const BASE_URL = 'http://127.0.0.1:5000/api'

export const AuthService = {
  login: (email: string, password: string) =>
    fetcher<User>(`${BASE_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  logout: () =>
    fetcher<{ message: string }>(`${BASE_URL}/auth/logout`, {
      method: 'POST',
    }),

  currentUser: () =>
    fetcher<User>(`${BASE_URL}/auth/me`),
}

