#!/usr/bin/env python3
"""
COMPREHENSIVE ROUTE TESTING
Tests all application routes for basic functionality
"""

import sys
import pathlib

# Add backend to path
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import pytest
from flask import url_for
from app import create_app, db
from app.models.core import User, Organization, Tenant
import json

print("🔍 COMPREHENSIVE ROUTE TESTING")
print("=" * 80)

class TestRoutes:
    """Test all application routes"""
    
    @pytest.fixture
    def app(self):
        """Create test app"""
        app = create_app('testing')
        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()
    
    @pytest.fixture
    def client(self, app):
        """Create test client"""
        return app.test_client()
    
    @pytest.fixture
    def init_database(self, app):
        """Initialize test database"""
        with app.app_context():
            # Create test tenant
            tenant = Tenant(
                name='Test Tenant',
                domain='test.localhost',
                subdomain='test'
            )
            db.session.add(tenant)
            db.session.commit()
            
            # Create test organization
            org = Organization(
                name='Test Organization',
                tenant_id=tenant.id
            )
            db.session.add(org)
            db.session.commit()
            
            # Create test user
            user = User(
                email='test@example.com',
                password_hash='test_password_hash',
                first_name='Test',
                last_name='User',
                organization_id=org.id,
                tenant_id=tenant.id
            )
            db.session.add(user)
            db.session.commit()
            
            yield db
            
            db.session.remove()
            db.drop_all()

    def test_health_check(self, client):
        """Test health check endpoint"""
        print("🧪 Testing health check route...")
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        print("✅ Health check passed")

    def test_api_docs(self, client):
        """Test API documentation endpoint"""
        print("🧪 Testing API docs route...")
        response = client.get('/api/docs')
        assert response.status_code in [200, 302]  # 302 if redirect to Swagger UI
        print("✅ API docs check passed")

    def test_authentication_routes(self, client, init_database):
        """Test authentication-related routes"""
        print("🧪 Testing authentication routes...")
        
        # Test login route exists
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'password'
        })
        # Should get 401 (unauthorized) rather than 404 (not found)
        assert response.status_code != 404
        print("✅ Login route exists")
        
        # Test register route
        response = client.post('/api/auth/register', json={
            'email': 'newuser@example.com',
            'password': 'password',
            'first_name': 'New',
            'last_name': 'User'
        })
        assert response.status_code != 404
        print("✅ Register route exists")
        
        # Test logout route
        response = client.post('/api/auth/logout')
        assert response.status_code != 404
        print("✅ Logout route exists")

    def test_user_routes(self, client, init_database):
        """Test user management routes"""
        print("🧪 Testing user routes...")
        
        # Test get current user
        response = client.get('/api/users/me')
        assert response.status_code != 404
        print("✅ Current user route exists")
        
        # Test get users list
        response = client.get('/api/users')
        assert response.status_code != 404
        print("✅ Users list route exists")

    def test_organization_routes(self, client, init_database):
        """Test organization routes"""
        print("🧪 Testing organization routes...")
        
        response = client.get('/api/organizations')
        assert response.status_code != 404
        print("✅ Organizations route exists")

    def test_patient_routes(self, client, init_database):
        """Test patient routes"""
        print("🧪 Testing patient routes...")
        
        response = client.get('/api/patients')
        assert response.status_code != 404
        print("✅ Patients route exists")

    def test_appointment_routes(self, client, init_database):
        """Test appointment routes"""
        print("🧪 Testing appointment routes...")
        
        response = client.get('/api/appointments')
        assert response.status_code != 404
        print("✅ Appointments route exists")

    def test_treatment_routes(self, client, init_database):
        """Test treatment routes"""
        print("🧪 Testing treatment routes...")
        
        response = client.get('/api/treatments')
        assert response.status_code != 404
        print("✅ Treatments route exists")

    def test_analytics_routes(self, client, init_database):
        """Test analytics routes"""
        print("🧪 Testing analytics routes...")
        
        response = client.get('/api/analytics/dashboards')
        assert response.status_code != 404
        print("✅ Analytics dashboards route exists")

    def test_inventory_routes(self, client, init_database):
        """Test inventory routes"""
        print("🧪 Testing inventory routes...")
        
        response = client.get('/api/inventory/products')
        assert response.status_code != 404
        print("✅ Inventory products route exists")

    def test_financial_routes(self, client, init_database):
        """Test financial routes"""
        print("🧪 Testing financial routes...")
        
        response = client.get('/api/financial/invoices')
        assert response.status_code != 404
        print("✅ Financial invoices route exists")

def test_all_routes_exist():
    """Test that all expected routes are registered"""
    print("\n📋 TESTING ALL REGISTERED ROUTES...")
    print("-" * 50)
    
    app = create_app('testing')
    
    with app.app_context():
        # Get all registered routes
        routes = []
        for rule in app.url_map.iter_rules():
            if 'static' not in rule.endpoint:  # Skip static files
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
        
        # Sort routes by path
        routes.sort(key=lambda x: x['path'])
        
        print(f"📊 Found {len(routes)} registered routes:")
        
        # Group routes by category
        route_categories = {
            'Authentication': [],
            'Users': [],
            'Organizations': [],
            'Patients': [],
            'Clinical': [],
            'Analytics': [],
            'Financial': [],
            'Inventory': [],
            'System': [],
            'Other': []
        }
        
        for route in routes:
            path = route['path']
            
            if any(auth in path for auth in ['/auth', '/login', '/register', '/logout']):
                route_categories['Authentication'].append(route)
            elif '/users' in path:
                route_categories['Users'].append(route)
            elif '/organizations' in path:
                route_categories['Organizations'].append(route)
            elif '/patients' in path:
                route_categories['Patients'].append(route)
            elif any(clinical in path for clinical in ['/appointments', '/treatments', '/clinical']):
                route_categories['Clinical'].append(route)
            elif '/analytics' in path:
                route_categories['Analytics'].append(route)
            elif any(financial in path for financial in ['/financial', '/invoices', '/payments']):
                route_categories['Financial'].append(route)
            elif any(inventory in path for inventory in ['/inventory', '/products', '/suppliers']):
                route_categories['Inventory'].append(route)
            elif any(system in path for system in ['/system', '/admin', '/health']):
                route_categories['System'].append(route)
            else:
                route_categories['Other'].append(route)
        
        # Print routes by category
        for category, category_routes in route_categories.items():
            if category_routes:
                print(f"\n🔹 {category} ({len(category_routes)} routes):")
                for route in category_routes[:5]:  # Show first 5 routes per category
                    methods = ', '.join(route['methods'])
                    print(f"   {methods:20} {route['path']}")
                if len(category_routes) > 5:
                    print(f"   ... and {len(category_routes) - 5} more")
        
        print(f"\n📈 TOTAL ROUTES: {len(routes)}")
        
        # Verify we have expected routes
        expected_route_patterns = [
            '/api/__init__/',
            '/admin/',
            '/api/analytics/',
            '/api/appointments',                        
            '/api/audit',
            '/api/auth/',            
            '/api/billing/',
            '/api/clinical',
            '/api/dashboard',
            '/api/family_members',
            '/api/files',
            '/api/health',
            '/api/insurance',
            '/api/integrations/',            
            '/api/inventory/',
            '/api/labs/',
            '/api/notifications',
            '/api/organizations',
            '/api/patients',
            '/api/prescriptions',
            '/api/reports',
            '/api/roles/',
            '/api/settings/',
            '/api/telemedicine/',
            '/api/test_routes',
            '/api/uploads',
            '/api/users',
            '/api/web_auth',
            '/api/widget'
        ]
        
        missing_routes = []
        for pattern in expected_route_patterns:
            if not any(pattern in route['path'] for route in routes):
                missing_routes.append(pattern)
        
        if missing_routes:
            print(f"\n❌ MISSING ROUTE PATTERNS: {len(missing_routes)}")
            for pattern in missing_routes:
                print(f"   - {pattern}")
        else:
            print(f"\n✅ All expected route patterns are registered!")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE ROUTE TESTING")
    
    # Test route registration
    test_all_routes_exist()
    
    # Run pytest tests
    print("\n" + "=" * 80)
    print("🧪 RUNNING ROUTE FUNCTIONALITY TESTS...")
    print("=" * 80)
    
    # Run the pytest tests
    pytest.main([__file__, "-v"])