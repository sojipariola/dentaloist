#!/usr/bin/env python3
"""
Comprehensive route and schema checker for Dentaloist backend
"""

import sys
import os
from urllib.parse import unquote
from datetime import datetime

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class OutputLogger:
    """Logger that writes to both console and file"""
    def __init__(self, filename='scripts/check_routes_schema_tables.txt'):
        self.console = sys.stdout
        self.log_file = open(filename, 'w', encoding='utf-8')
        
    def write(self, message):
        self.console.write(message)
        self.log_file.write(message)
        self.log_file.flush()
        
    def flush(self):
        self.console.flush()
        self.log_file.flush()
        
    def close(self):
        self.log_file.close()

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
    print(f"📅 Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
    """Check database tables and admin users with detailed column info"""
    print("📊 DATABASE SCHEMA CHECK")
    print("-" * 30)
    
    try:
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Found {len(tables)} tables:")
        for table in sorted(tables):
            columns = inspector.get_columns(table)
            primary_keys = inspector.get_pk_constraint(table)['constrained_columns']
            indexes = inspector.get_indexes(table)
            foreign_keys = inspector.get_foreign_keys(table)
            
            print(f"\n   📋 {table}: {len(columns)} columns")
            
            # Print each column with details
            for col in columns:
                pk_indicator = "🔑" if col['name'] in primary_keys else "  "
                nullable_indicator = "NULL" if col['nullable'] else "NOT NULL"
                default_value = f" DEFAULT {col['default']}" if col['default'] is not None else ""
                
                print(f"      {pk_indicator} {col['name']:20} {col['type']} {nullable_indicator}{default_value}")
            
            # Show primary key info
            if primary_keys:
                print(f"      🗝️  Primary Key: {', '.join(primary_keys)}")
            
            # Show foreign keys
            if foreign_keys:
                print(f"      🔗 Foreign Keys: {len(foreign_keys)}")
                for fk in foreign_keys[:3]:  # Show first 3 FKs
                    print(f"          {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
                if len(foreign_keys) > 3:
                    print(f"          ... and {len(foreign_keys) - 3} more foreign keys")
            
            # Show index info (non-primary)
            non_pk_indexes = [idx for idx in indexes if not idx['unique'] or not idx.get('primary', False)]
            if non_pk_indexes:
                print(f"      📑 Indexes: {len(non_pk_indexes)}")
                for idx in non_pk_indexes[:2]:  # Show first 2 indexes
                    unique_flag = "UNIQUE " if idx['unique'] else ""
                    print(f"          {unique_flag}{idx['name']}: {', '.join(idx['column_names'])}")
                if len(non_pk_indexes) > 2:
                    print(f"          ... and {len(non_pk_indexes) - 2} more indexes")
            
            # Show row count if available
            try:
                result = db.session.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = result.scalar()
                print(f"      📊 Row count: {row_count}")
                
                # Show sample data for small tables
                if row_count > 0 and row_count <= 5:
                    sample = db.session.execute(f"SELECT * FROM {table} LIMIT 3").fetchall()
                    print(f"      📝 Sample data:")
                    for row in sample:
                        print(f"          {dict(row._mapping)}")
            except Exception as e:
                print(f"      ⚠️  Could not get row count: {e}")
                
    except Exception as e:
        print(f"❌ Error inspecting database: {e}")
        import traceback
        traceback.print_exc()
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
            
        # Show all users if few exist
        all_users = User.query.limit(10).all()
        if all_users:
            print(f"\n👥 All users ({len(all_users)} total, showing first 10):")
            for user in all_users:
                admin_flag = "🔑" if getattr(user, 'is_admin', False) else "  "
                print(f"   {admin_flag} {user.email} (ID: {user.id})")
                
    except Exception as e:
        print(f"❌ Error checking users: {e}")
        import traceback
        traceback.print_exc()

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
    total_routes = sum(len(routes) for routes in routes_by_prefix.values())
    print(f"Total routes: {total_routes}")
    
    for prefix in sorted(routes_by_prefix.keys()):
        routes = routes_by_prefix[prefix]
        print(f"\n📁 {prefix.upper()} ROUTES ({len(routes)}):")
        
        for route in sorted(routes, key=lambda x: x['path']):
            methods = ','.join(route['methods'])
            path = route['path']
            print(f"   {methods:15} {path}")
            
            # Show endpoint for important routes
            if any(keyword in path for keyword in ['admin', 'auth', 'api']):
                print(f"      ↳ endpoint: {route['endpoint']}")

def check_authentication_status(app, db):
    """Check authentication configuration and test admin access"""
    print("🔐 AUTHENTICATION STATUS")
    print("-" * 30)
    
    # Check session configuration
    print(f"✅ Session cookie name: {app.config.get('SESSION_COOKIE_NAME', 'session')}")
    print(f"✅ Secret key set: {bool(app.config.get('SECRET_KEY'))}")
    print(f"✅ Debug mode: {app.config.get('DEBUG', False)}")
    print(f"✅ Testing mode: {app.config.get('TESTING', False)}")
    
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
        
        # Test session after login attempt
        with client.session_transaction() as session:
            print(f"\n🔍 Session contents after login attempt:")
            for key, value in session.items():
                print(f"   {key}: {value}")

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
    # Set up logging to file
    logger = OutputLogger('scripts/check_routes_schema_tables.txt')
    sys.stdout = logger
    
    try:
        print("=" * 60)
        print("DENTALOIST SYSTEM ANALYSIS REPORT")
        print("=" * 60)
        
        check_routes_and_schema()
        
        # Optionally create admin user if needed
        if len(sys.argv) > 1 and sys.argv[1] == '--create-admin':
            create_admin_user_if_needed()
            
        print("\n" + "=" * 60)
        print("✅ Report complete! Check 'scripts/check_routes_schema_tables.txt'")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 Error running checker: {e}")
        import traceback
        traceback.print_exc()
        print("💡 Make sure you're in the backend directory and all dependencies are installed")
    
    finally:
        # Restore stdout and close logger
        sys.stdout = logger.console
        logger.close()