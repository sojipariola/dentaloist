import pytest
import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class TestAPIPerformance:
    """Test API performance and response times"""
    
    def test_api_response_times(self, backend_url, test_credentials):
        """Test critical API endpoints response times"""
        
        # Login to get token
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['super_admin']
        )
        access_token = auth_response.json()['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        endpoints = [
            '/api/patients',
            '/api/appointments', 
            '/api/staff',
            '/api/treatments',
            '/api/tenants'
        ]
        
        performance_results = {}
        
        for endpoint in endpoints:
            response_times = []
            
            # Test 10 requests to get average
            for _ in range(10):
                start_time = time.time()
                response = requests.get(f"{backend_url}{endpoint}", headers=headers)
                end_time = time.time()
                
                assert response.status_code == 200
                response_times.append((end_time - start_time) * 1000)  # Convert to ms
            
            avg_time = statistics.mean(response_times)
            max_time = max(response_times)
            min_time = min(response_times)
            
            performance_results[endpoint] = {
                'avg_ms': avg_time,
                'max_ms': max_time, 
                'min_ms': min_time,
                'samples': len(response_times)
            }
            
            # Assert performance requirements
            assert avg_time < 500, f"{endpoint} too slow: {avg_time:.2f}ms"
            assert max_time < 1000, f"{endpoint} has high latency: {max_time:.2f}ms"
        
        print("📊 API Performance Results:")
        for endpoint, metrics in performance_results.items():
            print(f"  {endpoint}: {metrics['avg_ms']:.2f}ms avg, {metrics['max_ms']:.2f}ms max")
        
        print("✅ API performance test passed")
    
    def test_concurrent_tenant_switching(self, backend_url, test_credentials, test_tenants):
        """Test concurrent tenant switching performance"""
        
        auth_response = requests.post(
            f"{backend_url}/api/auth/login",
            json=test_credentials['super_admin'] 
        )
        access_token = auth_response.json()['access_token']
        
        def switch_tenant(tenant_id):
            headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(
                f"{backend_url}/api/switch-tenant",
                headers=headers,
                json={'tenant_id': tenant_id}
            )
            return response.status_code
        
        # Test concurrent switches
        with ThreadPoolExecutor(max_workers=5) as executor:
            tenant_ids = list(test_tenants.values()) * 2  # 6 switch requests
            start_time = time.time()
            
            results = list(executor.map(switch_tenant, tenant_ids))
            end_time = time.time()
            
            total_time = end_time - start_time
            requests_per_second = len(tenant_ids) / total_time
        
        # Verify all requests succeeded
        assert all(status == 200 for status in results)
        
        # Performance requirements
        assert total_time < 5, f"Concurrent switching too slow: {total_time:.2f}s"
        assert requests_per_second > 1, f"Low throughput: {requests_per_second:.2f} req/s"
        
        print(f"✅ Concurrent tenant switching: {requests_per_second:.2f} req/s")