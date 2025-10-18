// src/utils/apiHealthCheck.ts
export const checkApiHealth = async (): Promise<{
  healthy: boolean;
  message: string;
  error?: any;
}> => {
  try {
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';
    
    console.log('Testing API connectivity to:', API_BASE_URL);
    
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (response.ok) {
      const data = await response.json();
      return {
        healthy: true,
        message: 'API is reachable and healthy',
      };
    } else {
      return {
        healthy: false,
        message: `API returned error status: ${response.status}`,
      };
    }
  } catch (error) {
    return {
      healthy: false,
      message: 'Failed to connect to API',
      error: error instanceof Error ? error.message : 'Unknown error',
    };
  }
};

export const testAllEndpoints = async (): Promise<void> => {
  const endpoints = [
    '/health',
    '/api/auth/me',
    '/api/dashboard/stats',
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'}${endpoint}`);
      console.log(`${endpoint}: ${response.status} ${response.statusText}`);
    } catch (error) {
      console.error(`${endpoint}: ERROR -`, error);
    }
  }
};