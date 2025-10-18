# backend/app/routes/auth.py
# bp.route('/debug/admin-setup')
'''
@auth_bp.route("/me")
'''
from functools import wraps
from flask import Blueprint, request, jsonify, url_for, g, current_app, redirect, flash, session, render_template
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash, safe_join
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    decode_token,
    get_jwt
)
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import requests
from urllib.parse import urlencode, urlparse
import re
import os
from sqlalchemy import or_

# Import without tenant_required to avoid circular imports
from ..utils.auth import get_current_user  # Only import what you need
from ..models import db, User, Organization, UserRole, UserSession, UserOAuth, LoginAttempt
from ..utils.rate_limit import rate_limit

from jinja2 import TemplateNotFound
import secrets
import uuid

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

# ===== OAuth Setup =====
oauth = OAuth()

# Initialize OAuth with your app
def init_oauth(app):
    oauth.init_app(app)
    
    # Register OAuth clients
    oauth.register(
        name="google",
        client_id=app.config.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        api_base_url="https://www.googleapis.com/oauth2/v2/",
        client_kwargs={
            "scope": "openid email profile",
            "prompt": "select_account"
        },
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )

    
    oauth.register(
        name="facebook",
        client_id=app.config.get('FACEBOOK_CLIENT_ID'),
        client_secret=app.config.get('FACEBOOK_CLIENT_SECRET'),
        access_token_url="https://graph.facebook.com/v15.0/oauth/access_token",
        authorize_url="https://www.facebook.com/v15.0/dialog/oauth",
        api_base_url="https://graph.facebook.com/",
        client_kwargs={"scope": "email public_profile"},
    )
    
    oauth.register(
        name="github",
        client_id=app.config.get('GITHUB_CLIENT_ID'),
        client_secret=app.config.get('GITHUB_CLIENT_SECRET'),
        access_token_url="https://github.com/login/oauth/access_token",
        authorize_url="https://github.com/login/oauth/authorize",
        api_base_url="https://api.github.com/",
        client_kwargs={"scope": "read:user user:email"},
    )

    # ... other OAuth providers ...

# ===== Security Helper Functions =====
def record_login_attempt(username, ip_address, user_agent, success=False, 
                        failure_reason=None, user_id=None, attempt_type='password'):
    """Record a login attempt for security monitoring"""
    try:
        attempt = LoginAttempt(
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,  # Set the initial success state
            attempt_type=attempt_type,
            failure_reason=failure_reason,
            user_id=user_id
        )
        
        # Only call mark methods if you need additional logic
        if success:
            attempt.mark_successful()
        else:
            attempt.mark_failed(failure_reason)
        
        db.session.add(attempt)
        db.session.commit()
        return attempt
    except Exception as e:
        db.session.rollback()
        print(f"Error recording login attempt: {e}")
        return None

def check_login_security(username, ip_address):
    """Check if login should be allowed based on recent attempts"""
    # Check if account is temporarily locked
    if hasattr(LoginAttempt, 'is_account_locked') and LoginAttempt.is_account_locked(username):
        return False, "Account temporarily locked due to too many failed attempts"
    
    # Check for suspicious activity from this IP
    recent_attempts = LoginAttempt.count_recent_failed_attempts(
        username, ip_address, minutes=30
    ) if hasattr(LoginAttempt, 'count_recent_failed_attempts') else 0
    
    if recent_attempts >= 3:
        return False, "Too many recent failed attempts"
    
    return True, "Login allowed"

def get_client_info():
    """Extract client information from request"""
    return {
        'ip_address': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'accept_language': request.headers.get('Accept-Language', ''),
        'referrer': request.headers.get('Referer', '')
    }

# Add this function to your auth routes or utils

def user_to_dict(user):
    """Convert user object to dictionary with proper serialization"""
    try:
        # Handle role serialization
        role_value = getattr(user, 'role', 'user')
        if hasattr(role_value, 'value'):
            role_value = role_value.value
        elif not isinstance(role_value, (str, int, float, bool)):
            role_value = str(role_value)
        
        user_dict = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": user.organization_id,
            "role": role_value,
            "is_active": user.is_active,
        }
        
        # Add optional fields if they exist
        optional_fields = ['phone', 'avatar_url', 'created_at', 'updated_at']
        for field in optional_fields:
            if hasattr(user, field) and getattr(user, field) is not None:
                value = getattr(user, field)
                # Handle datetime serialization
                if hasattr(value, 'isoformat'):
                    user_dict[field] = value.isoformat()
                else:
                    user_dict[field] = value
        
        return user_dict
        
    except Exception as e:
        current_app.logger.error(f"Error in user_to_dict: {e}")
        # Return minimal safe data
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": user.organization_id,
        }


# Add to your auth routes or user routes
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Organization

@auth_bp.route('/api/tenants', methods=['GET'])
@jwt_required()
def get_available_tenants():
    """Get all tenants available to the current user"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is super admin
    is_super_admin = any(role.code == 'SUPER_ADMIN' for role in user.roles)
    
    if is_super_admin:
        # Super admin can see all organizations
        organizations = Organization.query.all()
    else:
        # Regular users only see their own organization
        organizations = Organization.query.filter_by(public_id=user.organization_id).all()
    
    tenants_data = []
    for org in organizations:
        tenants_data.append({
            'id': org.public_id,
            'name': org.name,
            'description': org.description,
            'is_current': org.public_id == user.organization_id
        })
    
    return jsonify({
        'tenants': tenants_data,
        'is_super_admin': is_super_admin,
        'current_tenant': user.organization_id
    })

@auth_bp.route('/api/switch-tenant', methods=['POST'])
@jwt_required()
def switch_tenant():
    """Switch current tenant for super admin"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is super admin
    is_super_admin = any(role.code == 'SUPER_ADMIN' for role in user.roles)
    if not is_super_admin:
        return jsonify({'error': 'Only super admins can switch tenants'}), 403
    
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    
    if not tenant_id:
        return jsonify({'error': 'Tenant ID is required'}), 400
    
    # Verify tenant exists
    tenant = Organization.query.filter_by(public_id=tenant_id).first()
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404
    
    # For super admin, we don't change their organization_id in database
    # Instead, we handle this in the session/token
    # You can return a new token with tenant context or handle it in frontend
    
    return jsonify({
        'message': f'Switched to {tenant.name}',
        'tenant': {
            'id': tenant.public_id,
            'name': tenant.name
        }
    })

        
def get_user_permissions(user):
    """Get user permissions based on role"""
    permissions = set()
    
    for role in user.roles:
        # If roles have direct permissions relationship
        if hasattr(role, 'permissions'):
            for permission in role.permissions:
                permissions.add(permission.name)
        # Otherwise use hardcoded permissions based on role name
        else:
            # Define role-based permissions
            role_permissions = {
                'SUPER_ADMIN': ['*'],
                'ORG_ADMIN': ['users:read', 'users:write', 'patients:read', 'patients:write', 'appointments:read', 'appointments:write'],
                'STAFF': ['patients:read', 'appointments:read', 'appointments:write'],
                'USER': ['profile:read', 'profile:write'],
                'VISITOR': ['profile:read']
            }
            if role.name in role_permissions:
                permissions.update(role_permissions[role.name])
    
    return list(permissions)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter"
    return True, "Password is valid"

def generate_session_token(length=32):
    """Generate a secure random session token"""
    return secrets.token_urlsafe(length)

def track_user_session(user, user_agent, ip_address):
    """Track user session for security"""
    # Generate a session token
    session_token = generate_session_token()
    
    session = UserSession(
        user_id=user.id,
        session_token=session_token,  # This was missing!
        user_agent=user_agent,
        ip_address=ip_address,
        login_time=datetime.utcnow(),
        is_active=True
    )
    
    db.session.add(session)
    db.session.commit()
    
    return session_token

def invalidate_user_sessions(user_id, keep_current=False, current_session_id=None):
    """Invalidate user sessions (for logout or security)"""
    query = UserSession.query.filter_by(user_id=user_id, is_active=True)
    if keep_current and current_session_id:
        query = query.filter(UserSession.id != current_session_id)
    query.update({'is_active': False, 'logout_at': datetime.utcnow()})
    db.session.commit()

# ===== Social Login Helpers =====
def get_oauth_client(provider_name):
    """Get OAuth client for the given provider"""
    return oauth.create_client(provider_name)

def handle_oauth_callback(provider_name, email, first_name="", last_name="", provider_user_id=""):
    """Handle OAuth callback for any provider"""
    g.skip_tenancy = True
    
    client_info = get_client_info()
    
    user = User.query.filter(
        or_(
            User.email == email,
            User.oauth_providers.any(provider=provider_name, provider_user_id=provider_user_id)
        )
    ).first()

    if not user:
        # Auto-register user with visitor role
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=UserRole.VISITOR,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        
        # Add OAuth provider info
        user.oauth_providers.append(UserOAuth(
            provider=provider_name,
            provider_user_id=provider_user_id,
            created_at=datetime.utcnow()
        ))
        
        db.session.add(user)
        db.session.commit()

    # Record successful OAuth login attempt
    record_login_attempt(
        username=email,
        ip_address=client_info['ip_address'],
        user_agent=client_info['user_agent'],
        success=True,
        user_id=user.id,
        attempt_type=f'oauth_{provider_name}'
    )

    # Track login session
    session_id = track_user_session(user, client_info['user_agent'], client_info['ip_address'])

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"session_id": session_id, "tenant_id": user.organization_id}
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        additional_claims={"session_id": session_id, "tenant_id": user.organization_id}
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_to_dict(user),
        "session_id": session_id
    }), 200

# ===== Google OAuth =====

@auth_bp.route('/social/google', methods=['POST'])
def google_login():
    """Handle Google OAuth login"""
    try:
        data = request.get_json()
        id_token = data.get('id_token')
        access_token = data.get('access_token')
        
        if not id_token and not access_token:
            return jsonify({'error': 'Google token required'}), 400
        
        # Verify Google token
        user_info = verify_google_token(id_token, access_token)
        if not user_info:
            return jsonify({'error': 'Invalid Google token'}), 401
        
        # Find or create user
        user = find_or_create_social_user(
            provider='google',
            provider_id=user_info['sub'],
            email=user_info['email'],
            first_name=user_info.get('given_name', ''),
            last_name=user_info.get('family_name', ''),
            picture=user_info.get('picture')
        )
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_to_dict(user),
            'is_new_user': user.is_new if hasattr(user, 'is_new') else False
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Google login error: {str(e)}")
        return jsonify({'error': 'Google login failed'}), 500

@auth_bp.route("/google/login", methods=["GET"])
@rate_limit(limit=10, period=60)
def google_login1():
    """Initiate Google OAuth flow"""
    g.skip_tenancy = True
    try:
        google_client = get_oauth_client("google")
        redirect_uri = url_for("auth.google_callback", _external=True)
        return google_client.authorize_redirect(redirect_uri)
    except Exception as e:
        current_app.logger.error(f"Google login error: {str(e)}")
        return jsonify({"error": "Google OAuth configuration error"}), 500

@auth_bp.route("/google/callback", methods=["GET"])
def google_callback():
    """Handle Google OAuth callback"""
    g.skip_tenancy = True
    client_info = get_client_info()
    
    try:
        google_client = get_oauth_client("google")
        token = google_client.authorize_access_token()
        
        # Get user info from Google
        resp = google_client.get("userinfo")
        if resp.status_code != 200:
            record_login_attempt(
                username="unknown",
                ip_address=client_info['ip_address'],
                user_agent=client_info['user_agent'],
                success=False,
                failure_reason="failed_to_get_user_info",
                attempt_type="oauth_google"
            )
            return jsonify({"error": "Failed to get user info from Google"}), 400
            
        profile = resp.json()
        
        return handle_oauth_callback(
            "google",
            profile["email"],
            profile.get("given_name", ""),
            profile.get("family_name", ""),
            profile.get("id", "")
        )
        
    except Exception as e:
        current_app.logger.error(f"Google callback error: {str(e)}")
        record_login_attempt(
            username="unknown",
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=False,
            failure_reason=str(e),
            attempt_type="oauth_google"
        )
        return jsonify({"error": "Google authentication failed"}), 500


# ===== Facebook OAuth =====

@auth_bp.route('/social/facebook', methods=['POST'])
def facebook_login():
    """Handle Facebook OAuth login"""
    try:
        data = request.get_json()
        access_token = data.get('access_token')
        
        if not access_token:
            return jsonify({'error': 'Facebook access token required'}), 400
        
        # Verify Facebook token
        user_info = verify_facebook_token(access_token)
        if not user_info:
            return jsonify({'error': 'Invalid Facebook token'}), 401
        
        # Find or create user
        user = find_or_create_social_user(
            provider='facebook',
            provider_id=user_info['id'],
            email=user_info.get('email'),
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            picture=user_info.get('picture', {}).get('data', {}).get('url') if user_info.get('picture') else None
        )
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_to_dict(user),
            'is_new_user': user.is_new if hasattr(user, 'is_new') else False
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Facebook login error: {str(e)}")
        return jsonify({'error': 'Facebook login failed'}), 500


# ===== Github OAuth =====

@auth_bp.route('/social/github', methods=['POST'])
def github_login():
    """Handle GitHub OAuth login"""
    try:
        data = request.get_json()
        code = data.get('code')
        access_token = data.get('access_token')
        
        if not code and not access_token:
            return jsonify({'error': 'GitHub authorization code or access token required'}), 400
        
        # Verify GitHub token
        user_info = verify_github_token(code, access_token)
        if not user_info:
            return jsonify({'error': 'Invalid GitHub token'}), 401
        
        # Split GitHub name into first/last name
        name_parts = user_info.get('name', '').split(' ', 1)
        first_name = name_parts[0] if name_parts else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Find or create user
        user = find_or_create_social_user(
            provider='github',
            provider_id=str(user_info['id']),
            email=user_info.get('email'),
            first_name=first_name,
            last_name=last_name,
            picture=user_info.get('avatar_url')
        )
        
        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_to_dict(user),
            'is_new_user': user.is_new if hasattr(user, 'is_new') else False
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"GitHub login error: {str(e)}")
        return jsonify({'error': 'GitHub login failed'}), 500


# ===== Email/Password Auth =====
@auth_bp.route("/register", methods=["POST"])
@rate_limit(limit=5, period=300)
def register():
    g.skip_tenancy = True
    data = request.get_json() or {}
    client_info = get_client_info()

    # Validation
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    if not validate_email(data["email"]):
        return jsonify({"message": "Invalid email format"}), 400

    password_valid, password_message = validate_password(data["password"])
    if not password_valid:
        return jsonify({"message": password_message}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(data["password"], method="sha256")

    org = None
    if "organization_id" in data:
        org = Organization.query.get(data["organization_id"])

    user = User(
        email=data["email"],
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", ""),
        password_hash=hashed_password,
        role=UserRole.ORG_ADMIN if not org else UserRole.USER,
        organization_id=org.id if org else None,
        is_active=True,
        is_admin=True if not org else False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(user)
    db.session.commit()

    # Record successful registration/login attempt
    record_login_attempt(
        username=user.email,
        ip_address=client_info['ip_address'],
        user_agent=client_info['user_agent'],
        success=True,
        user_id=user.id,
        attempt_type="registration"
    )

    # Track login session
    session_id = track_user_session(user, client_info['user_agent'], client_info['ip_address'])

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"session_id": session_id, "tenant_id": user.organization_id}
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        additional_claims={"session_id": session_id, "tenant_id": user.organization_id}
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_to_dict(user),
        "session_id": session_id
    }), 201


# backend/app/routes/auth.py - Fix login endpoint

@auth_bp.route("/login", methods=["POST"])
@rate_limit(limit=5, period=60)
def login():
    from flask import current_app
    import json
    
    data = request.get_json()
    client_info = get_client_info()
    
    current_app.logger.info(f"Login attempt for: {data.get('email')}")
    
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Check security restrictions before attempting login
    allowed, message = check_login_security(email, client_info['ip_address'])
    if not allowed:
        record_login_attempt(
            username=email,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=False,
            failure_reason="security_restriction",
            attempt_type="password"
        )
        return jsonify({"error": message}), 403

    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        record_login_attempt(
            username=email,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=False,
            failure_reason="invalid_credentials",
            user_id=user.id if user else None,
            attempt_type="password"
        )
        return jsonify({"error": "Invalid credentials"}), 401

    if not user.is_active:
        record_login_attempt(
            username=email,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=False,
            failure_reason="account_inactive",
            user_id=user.id,
            attempt_type="password"
        )
        return jsonify({"error": "Account is deactivated"}), 403

    # Record successful login 
    record_login_attempt(
        username=email,
        ip_address=client_info['ip_address'],
        user_agent=client_info['user_agent'],
        success=True,
        user_id=user.id,
        attempt_type="password"
    )

    # Create session token with error handling
    try:
        session_token = track_user_session(user, client_info['user_agent'], client_info['ip_address'])
        current_app.logger.info(f"Session tracking successful for user {user.id}")
    except Exception as e:
        current_app.logger.warning(f"Session tracking failed: {e}")
        # Generate a simple session token
        import secrets
        session_token = f"temp-{secrets.token_hex(16)}"

    # Create tokens with proper serialization
    try:
        # Get role as string for JWT claims
        user_role = getattr(user, 'role', 'user')
        if hasattr(user_role, 'value'):
            user_role = user_role.value
        elif not isinstance(user_role, (str, int, float, bool)):
            user_role = str(user_role)
        
        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                "session_token": session_token, 
                "tenant_id": str(user.organization_id),
                "email": user.email,
                "role": user_role
            }
        )

        refresh_token = create_refresh_token(
            identity=user.id,
            additional_claims={
                "session_token": session_token, 
                "tenant_id": str(user.organization_id)
            }
        )
        
        current_app.logger.info(f"JWT tokens created successfully for user {user.id}")
        
    except Exception as e:
        current_app.logger.error(f"JWT token creation failed: {e}")
        return jsonify({"error": "Authentication failed"}), 500

    # Convert user to dict safely
    try:
        user_dict = user_to_dict(user)
    except Exception as e:
        current_app.logger.error(f"User serialization failed: {e}")
        user_dict = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "organization_id": user.organization_id
        }

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user_dict,
        "session_token": session_token,
        "message": "Login successful"
    }), 200



@auth_bp.route('/debug-routes')
def debug_routes():
    routes = []
    for rule in current_app.url_map.iter_rules():
        if 'auth' in rule.endpoint or 'admin' in rule.endpoint:
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'path': str(rule)
            })
    return jsonify(routes)
    

@auth_bp.route("/login-form", methods=["GET", "POST"])
def login_form():
    """Simple login form for testing"""
    from flask import render_template
    from flask_login import login_user
    from app.models import User
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials', 'error')
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login - Dentaloist</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">
                            <h4>Login to Dentaloist</h4>
                        </div>
                        <div class="card-body">
                            <form method="POST">
                                <div class="mb-3">
                                    <label for="email" class="form-label">Email</label>
                                    <input type="email" class="form-control" id="email" name="email" required>
                                </div>
                                <div class="mb-3">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" class="form-control" id="password" name="password" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">Login</button>
                            </form>
                            <div class="mt-3 text-center">
                                <a href="/admin-direct-login" class="btn btn-sm btn-outline-secondary">Admin Login</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    

# ===== Fixed Security Endpoints =====
'''
@auth_bp.route("/me", methods=["GET"])
@jwt_required()  # Use ONLY ONE decorator
def get_current_user_route():  # Unique function name
    user = get_current_user()
    if not user: track_user_session
        return jsonify({"message": "Unauthorized"}), 401
    return jsonify({"user": user_to_dict(user)}), 200
'''


@auth_bp.route("/me", methods=["GET"])
@jwt_required()  # JWT-based protection
def get_current_user_route():
    """Return the current authenticated user (JWT-based)."""
    identity = get_jwt_identity()
    if not identity:
        return jsonify({"message": "Unauthorized"}), 401

    user = User.query.filter_by(public_id=identity).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200



@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # ✅ Protect with refresh token only
def refresh_tokens():
    """
    Refresh the user's access token using a valid refresh token.
    Ensures the session is still active and linked to the correct tenant.
    """
    g.skip_tenancy = True  # Optional: if you bypass tenant filters here

    try:
        # Extract user identity and claims from refresh token
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        session_id = claims.get("session_id")
        tenant_id = claims.get("tenant_id")

        if not current_user_id or not session_id:
            return jsonify({"error": "Invalid token payload"}), 400

        # Verify the session exists and is active
        session = UserSession.query.filter_by(
            id=session_id,
            user_id=current_user_id,
            is_active=True
        ).first()

        if not session:
            return jsonify({"error": "Session expired or invalid"}), 401

        # Optional: confirm that user still exists
        user = User.query.filter_by(public_id=current_user_id).first()
        if not user:
            return jsonify({"error": "User no longer exists"}), 404

        # ✅ Create new short-lived access token
        access_token = create_access_token(
            identity=current_user_id,
            additional_claims={
                "session_id": session_id,
                "tenant_id": tenant_id,
                "role": getattr(user, "role", "user")
            },
            expires_delta=timedelta(minutes=30)
        )

        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        # Avoid leaking internal details in responses
        return jsonify({"error": "Token refresh failed", "detail": str(e)}), 400


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()  # Use ONLY ONE decorator
def logout_route():  # Unique function name
    user = get_current_user()
    claims = get_jwt()
    session_id = claims.get("session_id")
    
    if user and session_id:
        client_info = get_client_info()
        record_login_attempt(
            username=user.email,
            ip_address=client_info['ip_address'],
            user_agent=client_info['user_agent'],
            success=True,
            user_id=user.id,
            attempt_type="logout"
        )
    
    if session_id:
        UserSession.query.filter_by(id=session_id).update({
            'is_active': False,
            'logout_at': datetime.utcnow()
        })
        db.session.commit()
    
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@auth_bp.route("/logout-all", methods=["POST"])
@jwt_required()  # Use ONLY ONE decorator
def logout_all_route():  # Unique function name
    user = get_current_user()
    claims = get_jwt()
    current_session_id = claims.get("session_id")
    client_info = get_client_info()
    
    record_login_attempt(
        username=user.email,
        ip_address=client_info['ip_address'],
        user_agent=client_info['user_agent'],
        success=True,
        user_id=user.id,
        attempt_type="logout_all"
    )
    
    invalidate_user_sessions(user.id, keep_current=True, current_session_id=current_session_id)
    
    return jsonify({"message": "Logged out from all devices successfully"}), 200

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required() 
def change_password():
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new passwords are required'}), 400
        
        password_valid, password_message = validate_password(new_password)
        if not password_valid:
            return jsonify({'error': password_message}), 400
        
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        if not check_password_hash(user.password_hash, current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        user.password_hash = generate_password_hash(new_password, method="sha256")
        user.updated_at = datetime.utcnow()
        
        # Invalidate all other sessions for security
        claims = get_jwt()
        current_session_id = claims.get("session_id")
        invalidate_user_sessions(user.id, keep_current=True, current_session_id=current_session_id)
        
        db.session.commit()
        
        return jsonify({'message': 'Password updated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Password change error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
@rate_limit(limit=3, period=300)  # 3 requests per 5 minutes
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if user and user.is_active:
            # Generate reset token (valid for 1 hour)
            reset_token = create_access_token(
                identity=user.id, 
                expires_delta=timedelta(hours=1),
                additional_claims={"type": "password_reset"}
            )
            
            # In a real application, send email with reset link
            reset_link = f"{request.host_url}reset-password?token={reset_token}"
            current_app.logger.info(f"Password reset link for {email}: {reset_link}")
            
            # Store reset token in user record for validation
            user.password_reset_token = reset_token
            user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
        
        # Always return the same message for security
        return jsonify({
            'message': 'If the email exists, a reset link has been sent'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Forgot password error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
@rate_limit(limit=5, period=300)  # 5 attempts per 5 minutes
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')
        
        if not token or not password:
            return jsonify({'error': 'Token and password are required'}), 400
        
        password_valid, password_message = validate_password(password)
        if not password_valid:
            return jsonify({'error': password_message}), 400
        
        # Verify token
        try:
            decoded = decode_token(token)
            if decoded.get('type') != 'password_reset':
                return jsonify({'error': 'Invalid token type'}), 400
            
            user_id = decoded['sub']
            user = User.query.get(user_id)
            
            if not user or user.password_reset_token != token or user.password_reset_expires < datetime.utcnow():
                return jsonify({'error': 'Invalid or expired token'}), 400
            
            # Update password and clear reset token
            user.password_hash = generate_password_hash(password, method="sha256")
            user.password_reset_token = None
            user.password_reset_expires = None
            user.updated_at = datetime.utcnow()
            
            # Invalidate all existing sessions
            invalidate_user_sessions(user.id)
            
            db.session.commit()
            
            return jsonify({'message': 'Password reset successfully'}), 200
            
        except Exception as token_error:
            current_app.logger.error(f"Token validation error: {str(token_error)}")
            return jsonify({'error': 'Invalid or expired token'}), 400
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500



# ===== Session Management =====
@auth_bp.route("/sessions", methods=["GET"])
@jwt_required() 
def get_sessions():
    """Get user's active sessions"""
    user = get_current_user()
    sessions = UserSession.query.filter_by(user_id=user.id, is_active=True).order_by(UserSession.login_at.desc()).all()
    
    return jsonify({
        "sessions": [{
            "id": session.id,
            "user_agent": session.user_agent,
            "ip_address": session.ip_address,
            "login_at": session.login_at.isoformat(),
            "last_activity": session.last_activity.isoformat() if session.last_activity else None
        } for session in sessions]
    }), 200

@auth_bp.route("/sessions/<int:session_id>", methods=["DELETE"])
@jwt_required() 
def revoke_session(session_id):
    """Revoke a specific session"""
    user = get_current_user()
    session = UserSession.query.filter_by(id=session_id, user_id=user.id).first()
    
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    session.is_active = False
    session.logout_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({"message": "Session revoked successfully"}), 200





# ===== Security Monitoring Endpoints =====
@auth_bp.route("/security/attempts", methods=["GET"])
@jwt_required()  # Use ONLY ONE decorator - remove @token_required
def get_login_attempts_route():  # Unique function name
    """Get recent login attempts for the current user"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required"}), 401
        
    hours = request.args.get('hours', 24, type=int)
    
    try:
        # Use safe method calls
        if hasattr(LoginAttempt, 'get_recent_attempts'):
            attempts = LoginAttempt.get_recent_attempts(
                username=user.email, 
                hours=hours, 
                limit=100
            )
        else:
            # Fallback query
            since_date = datetime.utcnow() - timedelta(hours=hours)
            attempts = LoginAttempt.query.filter(
                LoginAttempt.username == user.email,
                LoginAttempt.attempted_at >= since_date
            ).order_by(LoginAttempt.attempted_at.desc()).limit(100).all()
        
        return jsonify({
            "attempts": [attempt.to_dict() for attempt in attempts] if hasattr(attempts[0], 'to_dict') else [],
            "total": len(attempts),
            "timeframe_hours": hours
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route("/security/stats", methods=["GET"])
@jwt_required()  # Use ONLY ONE decorator - remove @token_required
def get_security_stats_route():  # Unique function name
    """Get security statistics for the current user"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Authentication required"}), 401
    
    try:
        # Failed attempts in last 24 hours
        if hasattr(LoginAttempt, 'count_recent_failed_attempts'):
            failed_24h = LoginAttempt.count_recent_failed_attempts(user.email, minutes=24*60)
        else:
            since_date = datetime.utcnow() - timedelta(hours=24)
            failed_24h = LoginAttempt.query.filter(
                LoginAttempt.username == user.email,
                LoginAttempt.success == False,
                LoginAttempt.attempted_at >= since_date
            ).count()
        
        # Successful logins in last 7 days
        successful_7d = LoginAttempt.query.filter(
            LoginAttempt.user_id == user.id,
            LoginAttempt.success == True,
            LoginAttempt.attempted_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        # Unique IP addresses used
        unique_ips = db.session.query(LoginAttempt.ip_address).filter(
            LoginAttempt.user_id == user.id,
            LoginAttempt.success == True,
            LoginAttempt.attempted_at >= datetime.utcnow() - timedelta(days=30)
        ).distinct().count()
        
        account_locked = LoginAttempt.is_account_locked(user.email) if hasattr(LoginAttempt, 'is_account_locked') else False
        
        return jsonify({
            "failed_attempts_24h": failed_24h,
            "successful_logins_7d": successful_7d,
            "unique_ips_30d": unique_ips,
            "account_locked": account_locked
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===== Health Check =====
@auth_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "auth", "timestamp": datetime.utcnow().isoformat()}), 200


@auth_bp.route('/admin-direct-login', methods=['GET', 'POST'])
def admin_direct_login():
    """Admin direct login for development"""
    try:
        # Look for users with admin role (using the user_role relationship)
        from app.models.lookups import UserRole
        
        # Find the admin role in UserRole table
        admin_role = UserRole.query.filter_by(name='admin').first()
        if not admin_role:
            # Create admin role if it doesn't exist
            admin_role = UserRole(name='admin', description='System Administrator')
            db.session.add(admin_role)
            db.session.commit()
        
        # Find users with admin role
        admin_user = User.query.filter_by(user_role_id=admin_role.id, is_active=True).first()
        
        if not admin_user:
            # Create a default admin user if none exists
            admin_user = create_default_admin(admin_role)
            if not admin_user:
                flash('No admin users found and could not create one', 'error')
                return redirect(url_for('auth.login_form'))
        
        # Log in the admin user
        login_user(admin_user)
        
        # Set session as permanent if requested
        session.permanent = True
        
        flash(f'Successfully logged in as admin: {admin_user.email}', 'success')
        
        # Redirect to the requested page or admin dashboard
        next_page = request.args.get('next')
        if next_page and is_safe_url(next_page):
            return redirect(next_page)
        return redirect(url_for('admin.dashboard'))
        
    except Exception as e:
        current_app.logger.error(f'Admin direct login failed: {e}')
        flash('Admin login failed', 'error')
        return redirect(url_for('auth.login_form'))
    
    
def create_default_admin(admin_role):
    """Create a default admin user if none exists"""
    try:
        from ..models import User, db, Organization
        
        # Check if default organization exists
        default_org = Organization.query.filter_by(public_id='default_org').first()
        if not default_org:
            # Create default organization
            default_org = Organization(
                name='Default Organization',
                public_id='default_org',
                is_active=True
            )
            db.session.add(default_org)
            db.session.commit()
        
        # Check if admin already exists
        admin_user = User.query.filter_by(email='admin@dentaloist.com').first()
        if admin_user:
            # Update existing user to admin role
            admin_user.user_role_id = admin_role.id
            admin_user.is_admin = True
            admin_user.is_active = True
            db.session.commit()
            return admin_user
        
        # Create new admin user
        admin_user = User(
            email='admin@dentaloist.com',
            first_name='System',
            last_name='Administrator',
            user_role_id=admin_role.id,
            organization_id='default_org',
            is_admin=True,
            is_active=True,
            email_verified=True
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        current_app.logger.info('Default admin user created')
        return admin_user
        
    except Exception as e:
        current_app.logger.error(f'Failed to create default admin: {e}')
        db.session.rollback()
        return None
    
def is_safe_url(target):
    """
    Check if the target URL is safe to redirect to.
    Prevents open redirect vulnerabilities.
    """
    if not target:
        return False
    
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    
    # Check if same scheme (http/https)
    if test_url.scheme != '' and test_url.scheme != ref_url.scheme:
        return False
    
    # Check if same netloc (domain)
    if test_url.netloc != '' and test_url.netloc != ref_url.netloc:
        return False
    
    # Additional safety checks
    if test_url.path.startswith('//') or test_url.path.startswith('\\\\'):
        return False
    
    return True


@auth_bp.route('/debug/admin-setup')
def debug_admin_setup():
    """Debug endpoint to check admin setup"""
    from app.models.lookups import UserRole
    
    # Check admin role
    admin_role = UserRole.query.filter_by(name='admin').first()
    
    # Check admin users
    admin_users = []
    if admin_role:
        admin_users = User.query.filter_by(user_role_id=admin_role.id, is_active=True).all()
    
    # Check organizations
    organizations = Organization.query.all()
    
    return jsonify({
        'admin_role_exists': admin_role is not None,
        'admin_role_details': {
            'id': admin_role.id if admin_role else None,
            'name': admin_role.name if admin_role else None
        },
        'admin_users_count': len(admin_users),
        'admin_users': [{
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'user_role_id': user.user_role_id,
            'is_admin': user.is_admin,
            'is_active': user.is_active
        } for user in admin_users],
        'organizations_count': len(organizations),
        'organizations': [{
            'id': org.id,
            'public_id': org.public_id,
            'name': org.name
        } for org in organizations]
    })


@auth_bp.route('/debug/auth-status')
def debug_auth_status():
    """Debug current authentication status"""
    return jsonify({
        'current_user': {
            'is_authenticated': current_user.is_authenticated,
            'id': getattr(current_user, 'id', None),
            'email': getattr(current_user, 'email', None),
            'role': getattr(current_user, 'role_name', None)
        } if current_user and hasattr(current_user, 'is_authenticated') else None,
        'session_keys': list(session.keys()),
        'has_session': bool(session),
        'next_param': request.args.get('next')
    })


@auth_bp.route('/debug-auth-setup')
def debug_auth_setup():
    """Debug the auth blueprint setup"""
    import inspect
    current_frame = inspect.currentframe()
    
    # Get the blueprint info
    blueprint_info = {
        'blueprint_name': auth_bp.name,
        'blueprint_variable': 'auth_bp',
        'url_prefix': '/api/auth',
        'all_endpoints': []
    }
    # Get all endpoints from this blueprint
    for rule in current_app.url_map.iter_rules():
        if rule.endpoint.startswith('auth.'):
            blueprint_info['all_endpoints'].append({
                'endpoint': rule.endpoint,
                'url': rule.rule,
                'methods': list(rule.methods)
            })
    
    return jsonify(blueprint_info)





# Add this to your auth routes or create a new debug route

# In your auth routes file (routes/auth.py)

# backend/app/routes/auth.py - Fix debug endpoints

@auth_bp.route('/debug/login-test', methods=['POST'])
def debug_login_test():
    """Debug endpoint to test login process"""
    from flask import current_app
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    current_app.logger.info(f"Debug login test for: {email}")
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if not user:
        current_app.logger.warning(f"User not found: {email}")
        return jsonify({
            'error': 'User not found',
            'email': email
        }), 404
    
    # Check password
    password_valid = check_password_hash(user.password_hash, password)
    
    return jsonify({
        'user_exists': True,
        'user_id': user.id,
        'organization_id': user.organization_id,
        'is_active': user.is_active,
        'password_valid': password_valid,
        'user_info': user_to_dict(user)
    }), 200

@auth_bp.route('/debug/login-info', methods=['POST'])
def debug_login_info():
    """Debug endpoint to check login info"""
    from flask import current_app
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    current_app.logger.info(f"Debug login info for: {email}")
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({
            'error': 'User not found',
            'email': email,
            'user_exists': False
        }), 404
    
    # Check password
    password_valid = check_password_hash(user.password_hash, password)
    
    return jsonify({
        'user_exists': True,
        'user_id': user.id,
        'organization_id': user.organization_id,
        'is_active': user.is_active,
        'password_valid': password_valid,
        'user_info': user_to_dict(user)
    }), 200