#!/usr/bin/env python3
"""
QUICK ROUTE MAPPER
Shows all available routes in a clean format
"""

import sys
import pathlib

# Add backend to path
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app import create_app

def map_all_routes():
    """Map all available routes"""
    print("🗺️  ROUTE MAPPER - ALL AVAILABLE ROUTES")
    print("=" * 80)
    
    app = create_app('development')
    
    with app.app_context():
        routes = []
        for rule in app.url_map.iter_rules():
            if 'static' not in rule.endpoint:
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
        
        # Sort by path
        routes.sort(key=lambda x: x['path'])
        
        print(f"📍 Found {len(routes)} routes:\n")
        
        # Group by API sections
        api_sections = {}
        
        for route in routes:
            path = route['path']
            
            # Extract API section
            if path.startswith('/api/'):
                parts = path.split('/')
                if len(parts) > 2:
                    section = parts[2]  # /api/<section>/...
                else:
                    section = 'core'
            else:
                section = 'other'
            
            if section not in api_sections:
                api_sections[section] = []
            api_sections[section].append(route)
        
        # Print by section
        for section in sorted(api_sections.keys()):
            section_routes = api_sections[section]
            print(f"🔹 {section.upper()} ({len(section_routes)} routes):")
            
            for route in section_routes:
                methods = ', '.join([m for m in route['methods'] if m in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']])
                if methods:
                    print(f"   {methods:15} {route['path']}")
            
            print()

def test_key_routes():
    """Test key routes for basic connectivity"""
    print("\n🔍 TESTING KEY ROUTES")
    print("=" * 80)
    
    app = create_app('development')
    
    test_routes = [
        ('GET', '/api/health', 'Health Check'),
        ('GET', '/api/docs', 'API Documentation'),
        ('GET', '/admin/', 'Admin Interface'),
        ('GET', '/api/users', 'Users API'),
        ('GET', '/api/patients', 'Patients API'),
        ('GET', '/api/appointments', 'Appointments API'),
        ('GET', '/api/organizations', 'Organizations API'),
    ]
    
    with app.test_client() as client:
        print("Route".ljust(40) + "Status".ljust(15) + "Description")
        print("-" * 80)
        
        for method, route, description in test_routes:
            try:
                if method == 'GET':
                    response = client.get(route)
                elif method == 'POST':
                    response = client.post(route)
                
                status = response.status_code
                
                if status == 200:
                    status_text = "✅ 200 OK"
                elif status == 302:
                    status_text = "🔄 302 Redirect"
                elif status == 401:
                    status_text = "🔐 401 Auth Required"
                elif status == 404:
                    status_text = "❌ 404 Not Found"
                else:
                    status_text = f"⚠️  {status}"
                
                print(f"{route:40} {status_text:15} {description}")
                
            except Exception as e:
                print(f"{route:40} ❌ ERROR: {str(e):15} {description}")

if __name__ == "__main__":
    map_all_routes()
    test_key_routes()