# backend/app/__init__.py

import os
from flask import Flask, jsonify
from .config import Config
from .models import db
from datetime import datetime

from .extensions import (
    init_db,
    init_cors,
    init_jwt,
    init_login_manager,
    init_api,
    init_socket,
    init_error_handlers,
    init_upload_folder,
    init_tenancy_middleware,
)
from .routes import register_routes
# from .utils.tenancy import TenancyMiddleware
from .utils.encryption import configure_encryption
from .utils.security import ensure_fernet_key
from .cli import register_commands

# from .admin import init_admin

ensure_fernet_key()

def format_datetime(value, format='medium'):
    """Format a datetime object or string to a formatted string."""
    # If it's already a string, try to parse it
    if isinstance(value, str):
        try:
            # Try different datetime formats
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']:
                try:
                    value = datetime.strptime(value, fmt)
                    break
                except ValueError:
                    continue
        except:
            # If we can't parse it, return the original string
            return value
    
    # If it's a datetime object, format it
    if isinstance(value, datetime):
        if format == 'full':
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif format == 'medium':
            return value.strftime("%Y-%m-%d %H:%M")
        else:
            return value.strftime("%Y-%m-%d")
    
    # If it's neither, return as is
    return str(value)


# Add this function in app/__init__.py
def validate_config(app):
    """Validate critical configuration settings"""
    required_settings = [
        'SECRET_KEY',
        'JWT_SECRET_KEY', 
        'SQLALCHEMY_DATABASE_URI'
    ]
    
    missing = [setting for setting in required_settings if not app.config.get(setting)]
    if missing:
        app.logger.error(f"❌ Missing required configuration: {missing}")
        raise ValueError(f"Missing required configuration: {missing}")
    
    # Validate database URI format
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if db_uri.startswith('sqlite:///'):
        app.logger.info("✅ Using SQLite database")
    elif db_uri.startswith('postgresql://') or db_uri.startswith('mysql://'):
        app.logger.info("✅ Using production database")
    else:
        app.logger.warning("⚠️ Unknown database type")
    
    return True

def configure_environment(app):
    """Configure environment-specific settings"""
    env = os.getenv('FLASK_ENV', 'production')
    
    if env == 'development':
        app.logger.setLevel('DEBUG')
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
        app.logger.info("🔧 Development environment configured")
        
    elif env == 'production':
        app.logger.setLevel('INFO')
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
        # Ensure secure settings in production
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['REMEMBER_COOKIE_SECURE'] = True
        app.logger.info("🚀 Production environment configured")
        
    elif env == 'testing':
        app.logger.setLevel('DEBUG')
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.logger.info("🧪 Testing environment configured")



def create_app(test_config=None, template_folder=None):    
    if template_folder is None:
        template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    
    app = Flask(__name__, template_folder=template_folder)

    # In development, add tenant simulation
    if os.environ.get('FLASK_ENV') == 'development':
        from app.middleware.development_tenancy import development_tenant_middleware
        
        @app.before_request
        def dev_tenant_setup():
            development_tenant_middleware()
            
                
    # Add startup logging
    app.logger.info("🚀 Starting Dentaloist application initialization...")
    
    configure_encryption(app)

    # ---- Config ----
    if test_config is None:
        app.config.from_object(Config)
        app.logger.info("✅ Configuration loaded from Config class")
    else:
        if isinstance(test_config, dict):
            app.config.from_object(Config)
            app.config.update(test_config)
            app.logger.info("✅ Configuration loaded from Config class with test overrides")
        else:
            app.config.from_object(test_config)
            app.logger.info("✅ Configuration loaded from test config")

    # Configure the environment
    configure_environment(app)

    # Validate configuration
    validate_config(app)

    # Jinja2 configuration
    app.jinja_env.globals['getattr'] = getattr
    app.jinja_env.filters['datetime'] = format_datetime
    app.logger.info("✅ Jinja2 configured")

    # ---- Admin ----
    try:
        from .admin.routes import init_admin
        init_admin(app)
        app.logger.info("✅ Admin interface initialized")
    except Exception as e:
        app.logger.warning(f"⚠️ Admin setup failed: {e}. Continuing without admin.")

    # ---- Initialize Extensions with Error Handling ----
    extension_initializers = [
        ('Database', init_db),
        ('CORS', init_cors),
        ('JWT', init_jwt),
        ('Login Manager', init_login_manager),
        ('API', init_api),
        ('Socket.IO', init_socket),
        ('Error Handlers', init_error_handlers),
        ('Upload Folder', init_upload_folder),
        ('Tenancy Middleware', init_tenancy_middleware),
    ]

    for name, initializer in extension_initializers:
        try:
            initializer(app)
            app.logger.info(f"✅ {name} initialized successfully")
        except Exception as e:
            app.logger.error(f"❌ Failed to initialize {name}: {e}")
            # Re-raise for critical extensions
            if name in ['Database', 'Tenancy Middleware']:
                raise

    # ---- Rate Limiter ----
    try:
        from app.utils.rate_limit import configure_rate_limiter
        configure_rate_limiter(app)
        app.logger.info("✅ Rate limiter configured")
    except Exception as e:
        app.logger.warning(f"⚠️ Rate limiter setup failed: {e}")

    # ---- Routes ----
    register_routes(app)
    app.logger.info("✅ Routes registered")

    # ---- CLI Commands ----
    register_commands(app)
    app.logger.info("✅ CLI commands registered")

    # ---- Health Endpoints ----
    @app.get("/")
    def root():
        return jsonify({
            "message": "Dentaloist API is running",
            "version": app.config.get("API_VERSION", "1.0.0"),
            "status": "healthy"
        })

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

    @app.route("/health")
    def health():
        return jsonify({
            "status": "ok", 
            "timestamp": datetime.utcnow().isoformat(),
            "service": "dentaloist-api"
        }), 200

    app.logger.info("🎉 Dentaloist application initialized successfully!")
    return app

# Make db available for import
__all__ = ['create_app', 'db']


'''




sudo pkill -f "flask run" || true
sudo pkill -f "python" || true
rm -f instance/dentaloist.db
rm -f instance/dentaloist.db-journal
rm -rf migrations/
find . -type d -name "__pycache__" -exec rm -rf {} +
sleep 5
python3 -m flask db init
sleep 2
python3 scripts/fix_migration_file.py
python3 scripts/verify_fix.py
sleep 2
python3 scripts/force_create_tables.py
python3 scripts/verify_fix.py
sleep 2

sleep 2
python3 -m flask db migrate -m "Initial migration"
python3 -m flask db upgrade
sleep 2
python3 scripts/setup_database.py
sleep 2
python3 scripts/seed_demo_data.py
sleep 2
python3 scripts/fix_seeder_imports.py
sleep 2
python scripts/debug_import_issue.py
sleep 2
python3 wsgi.py


lsof -i :5000
kill -9 <PID>

sudo netstat -tulpn | grep :5000
# or
sudo ss -tulpn | grep :5000

# If you found the PID from lsof/netstat
kill -9 <PID>

# Or kill all processes on port 5000
sudo fuser -k 5000/tcp







# Diagnostic curl
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS --verbose http://localhost:5000/api/test-cors

# Test OPTIONS preflight request
curl -X OPTIONS http://localhost:5000/api/auth/login \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v

# Test actual request
curl -X GET http://localhost:5000/api/health \
  -H "Origin: http://localhost:3000" \
  -v

curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{
    "email": "sojipariola@gmail.com",
    "password": "Soji1111"
  }' \
  -v
  
'''

