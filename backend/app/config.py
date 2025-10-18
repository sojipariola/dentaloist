# backend/app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ===== APPLICATION METADATA =====
    API_TITLE = os.getenv("APP_NAME", "Digital Dentistry API")
    API_VERSION = "1.1.0"
    OPENAPI_VERSION = "3.1.0"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/docs"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    PROPAGATE_EXCEPTIONS = True

    # ===== SECURITY =====
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secure-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secure-secret")

    # ===== DATABASE =====
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://olusoji:Soji1111@localhost:5432/dentaloist'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ===== FILE UPLOADS =====
    # UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "/tmp/uploads")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))  # 10MB

    # ===== MULTI-TENANCY =====
    MULTI_TENANCY_ENABLED = os.environ.get('MULTI_TENANCY_ENABLED', 'True').lower() == 'true'
    DEFAULT_TENANT_ID = os.environ.get('DEFAULT_TENANT_ID', '1')
    try:
        DEFAULT_TENANT_ID = int(DEFAULT_TENANT_ID)
    except ValueError:
        pass

    # ===== PAYMENT PROCESSING =====
    STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "")

    # ===== CORS =====
    CORS_ORIGINS = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:3000,http://127.0.0.1:3000'
    ).split(',')

    # ===== FLASK-LOGIN =====
    REMEMBER_COOKIE_DURATION = 3600
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = os.getenv('REMEMBER_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_PROTECTION = 'strong'

    # ===== FLASK-ADMIN =====
    FLASK_ADMIN_SWATCH = 'bootstrap4'

    # ===== DEBUGGING & LOGGING =====
    DEBUG = False
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # ===== FILE STORAGE =====
    FILE_STORAGE_TYPE = os.environ.get('FILE_STORAGE_TYPE', 'local')
    LOCAL_STORAGE_PATH = os.environ.get(
        'LOCAL_STORAGE_PATH',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    )

    # ===== ENCRYPTION =====
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')
    ENCRYPTION_ROTATION_KEY = os.environ.get('ENCRYPTION_ROTATION_KEY')

    if not ENCRYPTION_KEY:
        raise ValueError("❌ ENCRYPTION_KEY is required. Please set it in your .env file.")

    # ===== HEALTH CHECKS =====
    HEALTH_CHECK_TIMEOUT = 5
    APP_VERSION = '1.0.0'
    APP_NAME = 'Dentaloist Backend'

    # External service URLs
    REDIS_URL = os.environ.get('REDIS_URL')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    FILE_STORAGE_PATH = os.environ.get('FILE_STORAGE_PATH')

    # Email settings
    # Email Configuration
    SMTP_SERVER = 'smtp.gmail.com'  # or your SMTP server
    SMTP_PORT = 587
    SMTP_USERNAME = 'your-email@gmail.com'
    SMTP_PASSWORD = 'your-app-password'
    DEFAULT_SENDER = 'noreply@dentaloist.com'
    APP_NAME = 'Dentaloist'
    SUPPORT_EMAIL = 'support@dentaloist.com'
    
    # Social Auth Config
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    REMEMBER_COOKIE_SECURE = False


class ProductionConfig(Config):
    DEBUG = False
    PROPAGATE_EXCEPTIONS = False
    REMEMBER_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:testpass@localhost:5432/dentaloist_test'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])




"""
# Database setup instructions

# PostgreSQL Setup:
1. Install PostgreSQL: sudo apt-get install postgresql postgresql-contrib
2. Start PostgreSQL: sudo service postgresql start
3. Create database and user:
   sudo -u postgres psql
   CREATE DATABASE dentaloist;
   CREATE USER dentaloist_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE dentaloist TO dentaloist_user;
   \q

# Flask Database Commands:
flask db init           # Initialize migrations
flask db migrate -m "Initial migration"
flask db upgrade        # Apply migrations
flask run              # Start development server

# Environment Setup:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# check current migration state
flask db current

# check migration history
flask db history

# downgrade to previous migration
flask db downgrade

# upgrade to latest migration
flask db upgrade

# stamp the database with the latest migration
flask db stamp head

# Generate a new migration after model changes
flask db migrate -m "Describe your changes here"

# Apply the new migration to the database
flask db upgrade


# If you encounter issues, you can reset migrations:
rm -rf migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade





"""