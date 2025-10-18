import React, { useState, useEffect } from 'react'
import { CheckCircle, XCircle, RefreshCw, Server, Database, Shield } from 'lucide-react'
import { Button, Card } from '@/components/ui'

interface HealthCheck {
  service: string
  status: 'healthy' | 'unhealthy' | 'checking'
  responseTime?: number
  error?: string
}

export default function ApiStatus() {
  const [healthChecks, setHealthChecks] = useState<HealthCheck[]>([
    { service: 'API Server', status: 'checking' },
    { service: 'Database', status: 'checking' },
    { service: 'Authentication', status: 'checking' }
  ])
  const [isChecking, setIsChecking] = useState(false)

  const checkHealth = async () => {
    setIsChecking(true)
    const checks: HealthCheck[] = []

    // Check API Server
    try {
      const startTime = Date.now()
      const response = await fetch('http://localhost:5000/api/health')
      const endTime = Date.now()
      
      checks.push({
        service: 'API Server',
        status: response.ok ? 'healthy' : 'unhealthy',
        responseTime: endTime - startTime,
        error: response.ok ? undefined : `HTTP ${response.status}`
      })
    } catch (error) {
      checks.push({
        service: 'API Server',
        status: 'unhealthy',
        error: error instanceof Error ? error.message : 'Connection failed'
      })
    }

    // Check Database (via API)
    try {
      const response = await fetch('http://localhost:5000/admin/api/stats')
      checks.push({
        service: 'Database',
        status: response.ok ? 'healthy' : 'unhealthy',
        error: response.ok ? undefined : 'Database connection failed'
      })
    } catch (error) {
      checks.push({
        service: 'Database',
        status: 'unhealthy',
        error: 'Database connection failed'
      })
    }

    // Check Authentication
    try {
      const token = localStorage.getItem('access_token')
      if (token) {
        const response = await fetch('http://localhost:5000/api/auth/me', {
          headers: { 'Authorization': `Bearer ${token}` }
        })
        checks.push({
          service: 'Authentication',
          status: response.ok ? 'healthy' : 'unhealthy',
          error: response.ok ? undefined : 'Auth check failed'
        })
      } else {
        checks.push({
          service: 'Authentication',
          status: 'healthy',
          error: 'No token (not logged in)'
        })
      }
    } catch (error) {
      checks.push({
        service: 'Authentication',
        status: 'unhealthy',
        error: 'Auth service unavailable'
      })
    }

    setHealthChecks(checks)
    setIsChecking(false)
  }

  useEffect(() => {
    checkHealth()
  }, [])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'unhealthy':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <RefreshCw className="h-5 w-5 text-yellow-500 animate-spin" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-100 text-green-800'
      case 'unhealthy':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-yellow-100 text-yellow-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto space-y-6">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900">System Status</h1>
          <p className="text-gray-600 mt-2">Check the health of all system components</p>
        </div>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">Health Checks</h2>
              <p className="text-gray-600">Real-time status of system services</p>
            </div>
            <Button onClick={checkHealth} loading={isChecking}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh
            </Button>
          </div>

          <div className="space-y-4">
            {healthChecks.map((check, index) => (
              <div key={index} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getStatusIcon(check.status)}
                  <div>
                    <div className="font-medium text-gray-900">{check.service}</div>
                    {check.error && (
                      <div className="text-sm text-gray-500">{check.error}</div>
                    )}
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {check.responseTime && (
                    <div className="text-sm text-gray-500">
                      {check.responseTime}ms
                    </div>
                  )}
                  <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(check.status)}`}>
                    {check.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Troubleshooting Tips */}
        <Card className="p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Troubleshooting Tips</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Server className="h-4 w-4 text-blue-500" />
                <span className="font-medium">Backend Server</span>
              </div>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Ensure backend is running on port 5000</li>
                <li>Check <code className="bg-gray-100 px-1 rounded">python3 wsgi.py</code></li>
                <li>Verify no port conflicts</li>
              </ul>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Database className="h-4 w-4 text-green-500" />
                <span className="font-medium">Database</span>
              </div>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Check database connection</li>
                <li>Verify migrations are applied</li>
                <li>Ensure tables exist</li>
              </ul>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Shield className="h-4 w-4 text-purple-500" />
                <span className="font-medium">Authentication</span>
              </div>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Clear browser storage if stuck</li>
                <li>Check token validity</li>
                <li>Verify CORS settings</li>
              </ul>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <RefreshCw className="h-4 w-4 text-orange-500" />
                <span className="font-medium">Development</span>
              </div>
              <ul className="text-gray-600 space-y-1 list-disc list-inside">
                <li>Use Debug Panel (red bug icon)</li>
                <li>Check browser console for errors</li>
                <li>Verify environment variables</li>
              </ul>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}