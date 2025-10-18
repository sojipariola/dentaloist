// src/components/DebugTools.tsx
'use client';

import { useState } from 'react';
import { checkApiHealth, testAllEndpoints } from '@/utils/apiHealthCheck';

export const DebugTools: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<any>(null);
  const [isTesting, setIsTesting] = useState(false);

  const testConnectivity = async () => {
    setIsTesting(true);
    try {
      const health = await checkApiHealth();
      setHealthStatus(health);
      
      if (!health.healthy) {
        await testAllEndpoints();
      }
    } catch (error) {
      console.error('Debug test failed:', error);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="fixed bottom-4 right-4 bg-white p-4 rounded-lg shadow-lg border">
      <h3 className="text-sm font-semibold mb-2">API Debug</h3>
      <button
        onClick={testConnectivity}
        disabled={isTesting}
        className="bg-blue-500 text-white px-3 py-1 rounded text-sm disabled:opacity-50"
      >
        {isTesting ? 'Testing...' : 'Test API'}
      </button>
      
      {healthStatus && (
        <div className="mt-2 text-xs">
          <p className={healthStatus.healthy ? 'text-green-600' : 'text-red-600'}>
            Status: {healthStatus.healthy ? 'Healthy' : 'Unhealthy'}
          </p>
          <p>Message: {healthStatus.message}</p>
          {healthStatus.error && (
            <p>Error: {healthStatus.error}</p>
          )}
        </div>
      )}
    </div>
  );
};