# backend/app/extensions.py

import os
import tempfile
from flask import jsonify, request
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from flask_login import LoginManager
from flask_cors import CORS

from .models import db, bcrypt
from .utils.socket_utils import init_socketio

# ---- Instantiate (unbound) extensions ----
migrate = Migrate()
jwt = JWTManager()
login_manager = LoginManager()
api = Api()
socketio = SocketIO()
cors = CORS()

# ---- Setup Functions ----

def init_db(app):
    """Initialize database and migrations"""
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    app.logger.info("✅ Database and migrations initialized")

def init_cors(app):
    """Initialize CORS safely for API and web routes, environment-aware."""
    ENV = os.getenv("FLASK_ENV", "production").lower()
    FRONTEND_URL = os.getenv("FRONTEND_URL")
    TENANT_ID = os.getenv("TENANT_ID", "default-tenant")

    # Allowed origins
    if ENV in ["development", "dev"]:
        origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    else:
        origins = [FRONTEND_URL] if FRONTEND_URL else [
            "https://dentaloist.com",
            "https://www.dentaloist.com",
        ]

    # Attach Flask-CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": origins,
                "supports_credentials": True,
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    "X-Tenant-ID",
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            },
            r"/web/*": {
                "origins": origins,
                "supports_credentials": True,
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                    "X-Requested-With",
                    "X-Tenant-ID",
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            },
        },
    )

    # Global after_request hook for ensuring all responses carry CORS + tenant info
    @app.after_request
    def after_request(response):
        origin = request.headers.get("Origin")
        if origin in origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Vary"] = "Origin"

        response.headers["Access-Control-Allow-Headers"] = (
            "Content-Type, Authorization, X-Requested-With, X-Tenant-ID"
        )
        response.headers["Access-Control-Allow-Methods"] = (
            "GET, POST, PUT, DELETE, OPTIONS"
        )
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["X-Tenant-ID"] = TENANT_ID
        return response
    
    app.logger.info("✅ CORS initialized")

# backend/app/extensions.py - Fix the JWT configuration

def init_jwt(app):
    """Initialize JWT manager"""
    jwt.init_app(app)

    from .models import User

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return getattr(user, "id", user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data.get("sub")
        try:
            identity = int(identity)
        except (TypeError, ValueError):
            pass
        return User.query.get(identity)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(user):
        # Fix: Ensure all values are JSON serializable
        role_value = getattr(user, "role", None)
        
        # If role is an object with a value attribute, get the value
        if hasattr(role_value, 'value'):
            role_value = role_value.value
        elif not isinstance(role_value, (str, int, float, bool, type(None))):
            # Convert to string if it's a complex object
            role_value = str(role_value)
        
        # Ensure permissions are serializable
        permissions = []
        if hasattr(user, 'get_permissions'):
            try:
                permissions = user.get_permissions()
                if not isinstance(permissions, list):
                    permissions = []
            except:
                permissions = []
        
        return {
            "tenant_id": str(getattr(user, "organization_id", "")),
            "role": role_value,
            "permissions": permissions,
        }
    
    app.logger.info("✅ JWT manager initialized")
    

def init_login_manager(app):
    """Initialize Flask-Login"""
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except (TypeError, ValueError):
            return None
    
    app.logger.info("✅ Login manager initialized")

def init_api(app):
    """Initialize Flask-RESTful API"""
    api.init_app(app)
    app.logger.info("✅ API initialized")

def init_socket(app):
    """Initialize Socket.IO"""
    init_socketio(app)  # your custom init
    socketio.init_app(app, cors_allowed_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"])

    @socketio.on("connect")
    def handle_connect():
        app.logger.info("Client connected")
        socketio.emit("connection_response", {"data": "Connected to Dentaloist server"})

    @socketio.on("disconnect")
    def handle_disconnect():
        app.logger.info("Client disconnected")

    @socketio.on("widget_event")
    def handle_widget_event(data):
        app.logger.debug(f"Widget event: {data}")
        socketio.emit(
            "widget_response",
            {
                "status": "success",
                "message": "Widget event processed",
                "data": data,
            },
        )

    @socketio.on("widget_update")
    def handle_widget_update(data):
        app.logger.debug(f"Widget update: {data}")
        socketio.emit("widget_broadcast", data, broadcast=True)
    
    app.logger.info("✅ Socket.IO initialized")

def init_error_handlers(app):
    """Initialize global error handlers"""
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405
    
    app.logger.info("✅ Error handlers initialized")

def init_upload_folder(app):
    """Initialize upload folder with fallback"""
    upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
    try:
        abs_upload_path = os.path.join(os.getcwd(), upload_folder)
        os.makedirs(abs_upload_path, exist_ok=True)
        app.config["UPLOAD_FOLDER"] = abs_upload_path
        app.logger.info(f"✅ Upload folder set to: {abs_upload_path}")
    except (PermissionError, OSError) as e:
        fallback_folder = os.path.join(tempfile.gettempdir(), "dentaloist_uploads")
        os.makedirs(fallback_folder, exist_ok=True)
        app.config["UPLOAD_FOLDER"] = fallback_folder
        app.logger.warning(
            f"⚠️ Could not create {upload_folder}: {e}. Using fallback: {fallback_folder}"
        )

def init_tenancy_middleware(app):
    """Initialize tenancy middleware with the Flask app"""
    from .utils.tenancy import TenancyMiddleware
    
    # Create and initialize the middleware
    tenancy_middleware = TenancyMiddleware()
    tenancy_middleware.init_app(app)
    
    # Store reference in app context for potential future access
    app.tenancy_middleware = tenancy_middleware
    
    app.logger.info("✅ Tenancy middleware initialized")
    return tenancy_middleware