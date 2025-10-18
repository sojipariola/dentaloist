#!/usr/bin/env python3
"""
Comprehensive route and schema checker for Dentaloist backend
"""

import sys
import os
from urllib.parse import unquote

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_routes_and_schema():
    """Check all routes and database schema"""
    
    try:
        from app import create_app, db
        from flask import url_for
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running this from the backend directory")
        return
    
    app = create_app()
    
    print("🚀 DENTALOIST ROUTE & SCHEMA CHECKER")
    print("=" * 50)
    
    with app.app_context():
        # Check database schema first
        check_database_schema(app, db)
        
        print("\n" + "=" * 50)
        
        # Check routes
        check_application_routes(app)
        
        print("\n" + "=" * 50)
        
        # Check authentication status
        check_authentication_status(app, db)

def check_database_schema(app, db):
    """Check database tables and admin users"""
    print("📊 DATABASE SCHEMA CHECK")
    print("-" * 30)
    
    try:
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Found {len(tables)} tables:")
        for table in sorted(tables):
            columns = inspector.get_columns(table)
            print(f"   📋 {table}: {len(columns)} columns")
            # Show first few column names
            column_names = [col['name'] for col in columns[:3]]
            if len(columns) > 3:
                column_names.append("...")
            print(f"      Columns: {', '.join(column_names)}")
            
    except Exception as e:
        print(f"❌ Error inspecting database: {e}")
        return
    
    # Check for admin users
    try:
        from app.models import User
        admin_users = User.query.filter_by(is_admin=True).all()
        print(f"\n👑 Admin users: {len(admin_users)}")
        
        for user in admin_users:
            print(f"   ✅ {user.email} (ID: {user.id})")
            
        if not admin_users:
            print("   ❌ No admin users found!")
            print("   💡 You need to create an admin user to access the admin interface")
            
    except Exception as e:
        print(f"❌ Error checking users: {e}")

def check_application_routes(app):
    """Check all registered routes"""
    print("🛣️  APPLICATION ROUTES")
    print("-" * 30)
    
    # Group routes by blueprint/prefix
    routes_by_prefix = {}
    
    for rule in app.url_map.iter_rules():
        if rule.endpoint == 'static':
            continue
            
        # Extract prefix (blueprint name)
        endpoint_parts = rule.endpoint.split('.')
        prefix = endpoint_parts[0] if len(endpoint_parts) > 1 else 'main'
        
        if prefix not in routes_by_prefix:
            routes_by_prefix[prefix] = []
            
        routes_by_prefix[prefix].append({
            'endpoint': rule.endpoint,
            'methods': sorted([m for m in rule.methods if m not in ['OPTIONS', 'HEAD']]),
            'path': rule.rule
        })
    
    # Print routes by category
    for prefix in sorted(routes_by_prefix.keys()):
        print(f"\n📁 {prefix.upper()} ROUTES:")
        routes = routes_by_prefix[prefix]
        
        for route in sorted(routes, key=lambda x: x['path']):
            methods = ','.join(route['methods'])
            path = route['path']
            print(f"   {methods:15} {path}")
            
            # Show endpoint for admin routes
            if 'admin' in path:
                print(f"      ↳ endpoint: {route['endpoint']}")

def check_authentication_status(app, db):
    """Check authentication configuration and test admin access"""
    print("🔐 AUTHENTICATION STATUS")
    print("-" * 30)
    
    # Check session configuration
    print(f"✅ Session cookie name: {app.config.get('SESSION_COOKIE_NAME', 'session')}")
    print(f"✅ Secret key set: {bool(app.config.get('SECRET_KEY'))}")
    print(f"✅ Debug mode: {app.config.get('DEBUG', False)}")
    
    # Test admin direct login endpoint
    with app.test_client() as client:
        print(f"\n🔍 Testing admin login endpoint...")
        
        # Test GET request
        response = client.get('/api/auth/admin-direct-login')
        print(f"   GET /api/auth/admin-direct-login: {response.status_code}")
        
        # Test POST request with test data
        response = client.post('/api/auth/admin-direct-login', data={
            'username': 'test',
            'password': 'test'
        }, follow_redirects=False)
        
        print(f"   POST /api/auth/admin-direct-login: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ↳ Redirects to: {response.headers.get('Location', 'Unknown')}")
        
        # Check if we can access admin after login attempt
        response = client.get('/admin/', follow_redirects=False)
        print(f"   GET /admin/: {response.status_code}")
        
        if response.status_code == 302:
            redirect_to = response.headers.get('Location', '')
            print(f"   ↳ Redirects to: {unquote(redirect_to)}")

def create_admin_user_if_needed():
    """Helper function to create admin user if none exists"""
    from app import create_app, db
    from app.models import User
    
    app = create_app()
    with app.app_context():
        admin_count = User.query.filter_by(is_admin=True).count()
        
        if admin_count == 0:
            print("\n🆘 NO ADMIN USERS FOUND!")
            response = input("Create a default admin user? (y/n): ")
            if response.lower() == 'y':
                try:
                    admin_user = User(
                        email='admin@dentaloist.com',
                        is_admin=True,
                        # Add other required fields based on your User model
                    )
                    # If your User model has password hashing
                    if hasattr(admin_user, 'set_password'):
                        admin_user.set_password('admin123')
                    
                    db.session.add(admin_user)
                    db.session.commit()
                    print("✅ Created admin user: admin@dentaloist.com / admin123")
                except Exception as e:
                    print(f"❌ Error creating admin user: {e}")

if __name__ == '__main__':
    try:
        check_routes_and_schema()
        
        # Optionally create admin user if needed
        if len(sys.argv) > 1 and sys.argv[1] == '--create-admin':
            create_admin_user_if_needed()
            
    except Exception as e:
        print(f"💥 Error running checker: {e}")
        print("💡 Make sure you're in the backend directory and all dependencies are installed")


'''
# Make it executable
chmod +x scripts/check_routes_and_schema.py

# Run basic check
python3 scripts/check_routes_and_schema.py

# Run check and create admin user if needed
python3 scripts/check_routes_and_schema.py --create-admin

'''