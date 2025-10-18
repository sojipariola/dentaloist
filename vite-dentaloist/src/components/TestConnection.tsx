import { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { axiosClient } from '@/api/client/axiosClient';

export const TestConnection = () => {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const testConnection = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Test without auth token first
      const response = await axiosClient.get('/test-cors');
      setResult(response.data);
    } catch (err: any) {
      setError(err.message);
      setResult(err.response?.data || null);
    } finally {
      setLoading(false);
    }
  };

  const testWithAuth = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Set a mock token for testing
      localStorage.setItem('access_token', 'test-mock-token-for-cors');
      
      const response = await axiosClient.get('/test-cors');
      setResult(response.data);
    } catch (err: any) {
      setError(err.message);
      setResult(err.response?.data || null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto mt-8">
      <CardHeader>
        <CardTitle>Test Backend Connection</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex space-x-2">
          <Button 
            onClick={testConnection} 
            disabled={loading}
            variant="outline"
          >
            Test Without Auth
          </Button>
          <Button 
            onClick={testWithAuth} 
            disabled={loading}
          >
            Test With Auth
          </Button>
        </div>
        
        {loading && <div className="text-blue-600">Testing connection...</div>}
        
        {error && (
          <div className="text-red-600 p-3 bg-red-50 rounded">
            <strong>Error:</strong> {error}
          </div>
        )}
        
        {result && (
          <div className="p-3 bg-green-50 rounded">
            <strong>Success!</strong>
            <pre className="mt-2 text-sm overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </CardContent>
    </Card>
  );
};