// src/components/debug/AuthDebug.tsx
import { useAuthStore } from '@/app/store'

export function AuthDebug() {
  const { user, isAuthenticated } = useAuthStore()
  const token = localStorage.getItem('access_token')
  const refreshToken = localStorage.getItem('refresh_token')

  return (
    <div className="fixed bottom-4 right-4 p-4 bg-gray-900 text-white rounded-lg text-xs max-w-sm">
      <h3 className="font-bold mb-2">Auth Debug</h3>
      <div className="space-y-1">
        <div>Token: {token ? '✅ Present' : '❌ Missing'}</div>
        <div>Refresh Token: {refreshToken ? '✅ Present' : '❌ Missing'}</div>
        <div>Store User: {user ? '✅ Present' : '❌ Missing'}</div>
        <div>Authenticated: {isAuthenticated ? '✅ Yes' : '❌ No'}</div>
        {user && (
          <div>User: {user.email} ({user.role})</div>
        )}
      </div>
    </div>
  )
}