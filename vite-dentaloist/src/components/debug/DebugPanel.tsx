import React, { useState } from 'react'
import { Bug, X, RefreshCw, Database, Shield, User } from 'lucide-react'
import { Button, Card } from '@/components/ui'
import { debug } from '@/utils/debug/debugHelpers'
import { useAuthStore } from '@/app/store'

export const DebugPanel: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [apiStatus, setApiStatus] = useState<any>(null)
  const { user } = useAuthStore()

  const checkApiStatus = async () => {
    const status = await debug.checkAPI()
    setApiStatus(status)
  }

  const clearStorage = () => {
    debug.clearStorage()
    window.location.reload()
  }

  const addMockPatient = () => {
    const mockPatient = debug.generateMockPatient()
    debug.log('Mock patient data:', mockPatient)
    // In a real app, this would dispatch an action to create the patient
    alert(`Mock patient created:\n${JSON.stringify(mockPatient, null, 2)}`)
  }

  if (!import.meta.env.DEV) return null

  return (
    <>
      {/* Debug Toggle Button */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-4 right-4 z-50 p-3 bg-red-500 text-white rounded-full shadow-lg hover:bg-red-600 transition-colors"
      >
        <Bug className="h-6 w-6" />
      </button>

      {/* Debug Panel */}
      {isOpen && (
        <div className="fixed inset-0 z-50 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Debug Panel</h2>
              <Button variant="ghost" onClick={() => setIsOpen(false)}>
                <X className="h-5 w-5" />
              </Button>
            </div>

            <div className="p-6 space-y-6">
              {/* Authentication Status */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <Shield className="h-5 w-5 mr-2" />
                  Authentication
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600">Local Storage</div>
                    <div className="text-sm font-mono">
                      {debug.checkAuth().hasToken ? '✅ Token found' : '❌ No token'}
                    </div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm text-gray-600">Store User</div>
                    <div className="text-sm font-mono">
                      {user ? `✅ ${user.first_name} ${user.last_name}` : '❌ No user'}
                    </div>
                  </div>
                </div>
              </div>

              {/* API Status */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <Database className="h-5 w-5 mr-2" />
                  API Status
                </h3>
                <div className="space-y-3">
                  <div className="flex space-x-3">
                    <Button onClick={checkApiStatus} variant="outline">
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Check API
                    </Button>
                  </div>
                  {apiStatus && (
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <pre className="text-sm">{JSON.stringify(apiStatus, null, 2)}</pre>
                    </div>
                  )}
                </div>
              </div>

              {/* Quick Actions */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center">
                  <User className="h-5 w-5 mr-2" />
                  Quick Actions
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <Button onClick={clearStorage} variant="outline" className="justify-start">
                    Clear Storage & Reload
                  </Button>
                  <Button onClick={addMockPatient} variant="outline" className="justify-start">
                    Generate Mock Patient
                  </Button>
                  <Button 
                    onClick={() => localStorage.setItem('access_token', 'debug-token')}
                    variant="outline" 
                    className="justify-start"
                  >
                    Set Debug Token
                  </Button>
                  <Button 
                    onClick={() => window.location.href = '/admin'}
                    variant="outline" 
                    className="justify-start"
                  >
                    Go to Admin
                  </Button>
                </div>
              </div>

              {/* Environment Info */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Environment</h3>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <div className="text-sm space-y-1">
                    <div>Mode: {import.meta.env.MODE}</div>
                    <div>Dev: {import.meta.env.DEV ? 'Yes' : 'No'}</div>
                    <div>Prod: {import.meta.env.PROD ? 'Yes' : 'No'}</div>
                    <div>API URL: {import.meta.env.VITE_API_URL}</div>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      )}
    </>
  )
}