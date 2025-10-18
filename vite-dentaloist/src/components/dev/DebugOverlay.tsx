import React, { useEffect, useState } from 'react'
import { axiosClient } from '@/api/client/axiosClient'

interface AxiosLog {
  method: string
  url: string
  status?: number
  statusText?: string
  time: string
  error?: string
}

export const DebugOverlay: React.FC = () => {
  const [logs, setLogs] = useState<AxiosLog[]>([])
  const [visible, setVisible] = useState(true)
  const [baseUrl] = useState(import.meta.env?.VITE_API_URL || 'http://localhost:5000/api')

  useEffect(() => {
    const reqInterceptor = axiosClient.interceptors.request.use((config) => {
      setLogs((prev) => [
        {
          method: config.method?.toUpperCase() || '',
          url: `${config.baseURL}${config.url}`,
          time: new Date().toLocaleTimeString(),
        },
        ...prev,
      ])
      return config
    })

    const resInterceptor = axiosClient.interceptors.response.use(
      (res) => {
        setLogs((prev) =>
          prev.map((log, i) =>
            i === 0
              ? { ...log, status: res.status, statusText: res.statusText }
              : log
          )
        )
        return res
      },
      (err) => {
        setLogs((prev) =>
          prev.map((log, i) =>
            i === 0
              ? { ...log, error: err.message, status: err.response?.status }
              : log
          )
        )
        return Promise.reject(err)
      }
    )

    return () => {
      axiosClient.interceptors.request.eject(reqInterceptor)
      axiosClient.interceptors.response.eject(resInterceptor)
    }
  }, [])

  if (!visible) return null

  return (
    <div className="fixed bottom-2 right-2 bg-gray-900 text-white text-xs p-3 rounded-lg shadow-lg w-[340px] h-[260px] overflow-y-auto z-[9999]">
      <div className="flex justify-between mb-2">
        <span className="font-semibold">🧭 Axios Debug Panel</span>
        <button
          onClick={() => setVisible(false)}
          className="text-red-400 hover:text-red-300"
        >
          ✕
        </button>
      </div>

      <div className="text-gray-400 mb-2">
        <div>API: {baseUrl}</div>
        <div>Token: {localStorage.getItem('access_token') ? '✅ Yes' : '❌ No'}</div>
        <div>Tenant-ID: {localStorage.getItem('tenant_id') || '❌ None'}</div>
      </div>

      <div className="border-t border-gray-700 pt-2">
        {logs.slice(0, 6).map((log, idx) => (
          <div key={idx} className="mb-1">
            <div className="font-mono text-gray-300">
              [{log.time}] {log.method} {log.url}
            </div>
            <div>
              {log.status ? (
                <span
                  className={
                    log.status < 400
                      ? 'text-green-400'
                      : log.status < 500
                      ? 'text-yellow-400'
                      : 'text-red-400'
                  }
                >
                  {log.status} {log.statusText}
                </span>
              ) : (
                <span className="text-gray-500">Pending...</span>
              )}
              {log.error && <span className="text-red-400"> ⚠️ {log.error}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
