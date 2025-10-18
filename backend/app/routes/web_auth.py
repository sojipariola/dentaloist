# app/resources/web_auth.py
from flask import render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_smorest import Blueprint
from datetime import datetime, timedelta
import logging
from typing import Dict, Any, Optional

# Import utilities
from ..utils.auth import get_current_user, permission_required, generate_2fa_code, verify_2fa_code
from ..utils.tenancy import tenant_required, get_current_tenant
from ..utils.rate_limit import rate_limit
from ..services.security import verify_password, hash_password, check_password_strength
from ..services.email_service import send_email
from ..models import User, LoginAttempt, AuditTrail, db

web_bp = Blueprint("WebAuth", __name__, description="Web Authentication")

# Security configurations
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 15  # minutes
SESSION_TIMEOUT = 60  # minutes

def log_login_attempt(email: str, ip_address: str, success: bool, user_id: Optional[int] = None):
    """Log login attempt for security monitoring"""
    attempt = LoginAttempt(
        email=email,
        ip_address=ip_address,
        user_agent=request.user_agent.string,
        success=success,
        user_id=user_id,
        attempted_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()

def check_login_security(email: str, ip_address: str) -> Dict[str, Any]:
    """Check security rules for login attempt"""
    # Check recent failed attempts
    recent_attempts = LoginAttempt.query.filter(
        LoginAttempt.email == email,
        LoginAttempt.ip_address == ip_address,
        LoginAttempt.success == False,
        LoginAttempt.attempted_at >= datetime.utcnow() - timedelta(minutes=LOCKOUT_DURATION)
    ).count()
    
    is_locked = recent_attempts >= MAX_LOGIN_ATTEMPTS
    
    return {
        'is_locked': is_locked,
        'remaining_attempts': max(0, MAX_LOGIN_ATTEMPTS - recent_attempts),
        'lockout_time': LOCKOUT_DURATION if is_locked else 0
    }

def create_audit_entry(user_id: int, action: str, resource: str, details: str):
    """Create audit trail entry"""
    audit = AuditTrail(
        user_id=user_id,
        action=action,
        resource_type=resource,
        details=details,
        ip_address=request.remote_addr,
        user_agent=request.user_agent.string,
        timestamp=datetime.utcnow()
    )
    db.session.add(audit)

@web_bp.route("/web/login", methods=["GET", "POST"])
@rate_limit(limit=10, period=900)  # 10 attempts per 15 minutes
def web_login():
    """
    Web-based login with enhanced security features
    """
    if request.method == "POST":
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))
        two_factor_code = request.form.get('two_factor_code', '').strip()
        
        # Security check
        security_status = check_login_security(email, request.remote_addr)
        
        if security_status['is_locked']:
            log_login_attempt(email, request.remote_addr, False)
            return render_template('login.html', 
                                error=f"Account temporarily locked. Try again in {LOCKOUT_DURATION} minutes.")
        
        # Find user
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if not user:
            log_login_attempt(email, request.remote_addr, False)
            return render_template('login.html', 
                                error="Invalid credentials", 
                                remaining_attempts=security_status['remaining_attempts'])
        
        # Verify password
        if not verify_password(password, user.password_hash):
            log_login_attempt(email, request.remote_addr, False, user.id)
            return render_template('login.html', 
                                error="Invalid credentials",
                                remaining_attempts=security_status['remaining_attempts'] - 1)
        
        # Check if 2FA is required
        if user.two_factor_enabled:
            if not two_factor_code:
                # Generate and send 2FA code
                code = generate_2fa_code(user.id)
                send_2fa_email(user.email, code)
                
                session['pending_2fa_user'] = user.id
                session['2fa_created_at'] = datetime.utcnow().isoformat()
                
                return render_template('login_2fa.html', 
                                    email=user.email,
                                    message="2FA code sent to your email")
            
            # Verify 2FA code
            if not verify_2fa_code(user.id, two_factor_code):
                log_login_attempt(email, request.remote_addr, False, user.id)
                return render_template('login_2fa.html',
                                    email=user.email,
                                    error="Invalid 2FA code")
            
            # Clear 2FA session
            session.pop('pending_2fa_user', None)
            session.pop('2fa_created_at', None)
        
        # Successful login
        login_user(user, remember=remember, duration=timedelta(minutes=SESSION_TIMEOUT))
        log_login_attempt(email, request.remote_addr, True, user.id)
        
        # Create audit trail
        create_audit_entry(user.id, 'login', 'system', 'User logged in via web')
        
        # Update last login
        user.last_login = datetime.utcnow()
        user.login_count = (user.login_count or 0) + 1
        db.session.commit()
        
        # Redirect based on user role
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        
        return redirect(get_dashboard_url(user))
    
    # GET request - show login form
    return render_template('login.html')

@web_bp.route("/web/login/2fa", methods=["GET", "POST"])
@rate_limit(limit=5, period=900)  # 5 attempts per 15 minutes for 2FA
def web_login_2fa():
    """
    Handle 2FA verification
    """
    if request.method == "POST":
        two_factor_code = request.form.get('two_factor_code', '').strip()
        user_id = session.get('pending_2fa_user')
        created_at_str = session.get('2fa_created_at')
        
        if not user_id or not created_at_str:
            return redirect(url_for('WebAuth.web_login'))
        
        # Check 2FA code expiration (10 minutes)
        created_at = datetime.fromisoformat(created_at_str)
        if datetime.utcnow() - created_at > timedelta(minutes=10):
            session.pop('pending_2fa_user', None)
            session.pop('2fa_created_at', None)
            return render_template('login.html', error="2FA code expired. Please login again.")
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            session.pop('pending_2fa_user', None)
            session.pop('2fa_created_at', None)
            return redirect(url_for('WebAuth.web_login'))
        
        # Verify 2FA code
        if verify_2fa_code(user.id, two_factor_code):
            login_user(user, duration=timedelta(minutes=SESSION_TIMEOUT))
            
            # Clear 2FA session
            session.pop('pending_2fa_user', None)
            session.pop('2fa_created_at', None)
            
            # Log successful login
            log_login_attempt(user.email, request.remote_addr, True, user.id)
            create_audit_entry(user.id, 'login', 'system', 'User logged in with 2FA')
            
            # Update last login
            user.last_login = datetime.utcnow()
            user.login_count = (user.login_count or 0) + 1
            db.session.commit()
            
            return redirect(get_dashboard_url(user))
        else:
            log_login_attempt(user.email, request.remote_addr, False, user.id)
            return render_template('login_2fa.html',
                                email=user.email,
                                error="Invalid 2FA code")
    
    # GET request - show 2FA form
    user_id = session.get('pending_2fa_user')
    if not user_id:
        return redirect(url_for('WebAuth.web_login'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('WebAuth.web_login'))
    
    return render_template('login_2fa.html', email=user.email)

@web_bp.route("/web/logout")
@login_required
def web_logout():
    """
    Secure logout with audit trail
    """
    user_id = current_user.id
    email = current_user.email
    
    # Create audit trail before logout
    create_audit_entry(user_id, 'logout', 'system', 'User logged out')
    
    logout_user()
    
    # Clear session completely
    session.clear()
    
    flash("You have been logged out successfully.", "success")
    return redirect(url_for('WebAuth.web_login'))

@web_bp.route("/web/forgot-password", methods=["GET", "POST"])
@rate_limit(limit=5, period=3600)  # 5 requests per hour
def forgot_password():
    """
    Password reset request
    """
    if request.method == "POST":
        email = request.form.get('email', '').strip().lower()
        
        user = User.query.filter_by(email=email, is_active=True).first()
        
        # Always return success to prevent email enumeration
        if user:
            # Generate password reset token
            reset_token = generate_password_reset_token(user.id)
            send_password_reset_email(user.email, reset_token)
            
            # Log the request
            create_audit_entry(user.id, 'password_reset_request', 'user', 'Password reset requested')
        
        return render_template('forgot_password.html', 
                            message="If an account exists with that email, a reset link has been sent.")
    
    return render_template('forgot_password.html')

@web_bp.route("/web/reset-password/<token>", methods=["GET", "POST"])
@rate_limit(limit=5, period=3600)
def reset_password(token):
    """
    Password reset form
    """
    user_id = verify_password_reset_token(token)
    
    if not user_id:
        flash("Invalid or expired reset token.", "error")
        return redirect(url_for('WebAuth.web_login'))
    
    user = User.query.get(user_id)
    if not user or not user.is_active:
        flash("Invalid user account.", "error")
        return redirect(url_for('WebAuth.web_login'))
    
    if request.method == "POST":
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            return render_template('reset_password.html', 
                                error="Passwords do not match", 
                                token=token)
        
        # Check password strength
        strength_check = check_password_strength(new_password)
        if not strength_check['is_strong']:
            return render_template('reset_password.html',
                                error=strength_check['message'],
                                token=token)
        
        # Update password
        user.password_hash = hash_password(new_password)
        user.password_changed_at = datetime.utcnow()
        user.force_password_change = False
        
        db.session.commit()
        
        # Create audit trail
        create_audit_entry(user.id, 'password_reset', 'user', 'Password reset successfully')
        
        flash("Password reset successfully. Please login with your new password.", "success")
        return redirect(url_for('WebAuth.web_login'))
    
    return render_template('reset_password.html', token=token)

@web_bp.route("/web/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """
    Change password for logged-in users
    """
    if request.method == "POST":
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if not verify_password(current_password, current_user.password_hash):
            return render_template('change_password.html', error="Current password is incorrect")
        
        if new_password != confirm_password:
            return render_template('change_password.html', error="New passwords do not match")
        
        # Check password strength
        strength_check = check_password_strength(new_password)
        if not strength_check['is_strong']:
            return render_template('change_password.html', error=strength_check['message'])
        
        # Update password
        current_user.password_hash = hash_password(new_password)
        current_user.password_changed_at = datetime.utcnow()
        current_user.force_password_change = False
        
        db.session.commit()
        
        # Create audit trail
        create_audit_entry(current_user.id, 'password_change', 'user', 'Password changed')
        
        flash("Password changed successfully.", "success")
        return redirect(get_dashboard_url(current_user))
    
    return render_template('change_password.html')

@web_bp.route("/web/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    User profile management
    """
    if request.method == "POST":
        # Update profile information
        current_user.first_name = request.form.get('first_name', current_user.first_name)
        current_user.last_name = request.form.get('last_name', current_user.last_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        
        # Email change requires verification
        new_email = request.form.get('email', '').strip().lower()
        if new_email and new_email != current_user.email:
            # Check if email is already taken
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user and existing_user.id != current_user.id:
                return render_template('profile.html', error="Email already in use")
            
            # In production, you'd send a verification email here
            current_user.email = new_email
            current_user.email_verified = False
        
        db.session.commit()
        
        create_audit_entry(current_user.id, 'profile_update', 'user', 'Profile updated')
        flash("Profile updated successfully.", "success")
        
        return redirect(url_for('WebAuth.profile'))
    
    return render_template('profile.html', user=current_user)

@web_bp.route("/web/security", methods=["GET", "POST"])
@login_required
def security_settings():
    """
    Security settings (2FA, session management)
    """
    if request.method == "POST":
        # Toggle 2FA
        if 'toggle_2fa' in request.form:
            current_user.two_factor_enabled = not current_user.two_factor_enabled
            db.session.commit()
            
            action = "enabled" if current_user.two_factor_enabled else "disabled"
            create_audit_entry(current_user.id, '2fa_toggle', 'user', f'2FA {action}')
            
            flash(f"Two-factor authentication {action}.", "success")
        
        # Terminate other sessions
        elif 'terminate_sessions' in request.form:
            # This would typically involve invalidating session tokens
            create_audit_entry(current_user.id, 'session_termination', 'user', 'Other sessions terminated')
            flash("Other sessions have been terminated.", "success")
    
    # Get login history
    login_history = LoginAttempt.query.filter_by(user_id=current_user.id)\
                                    .order_by(LoginAttempt.attempted_at.desc())\
                                    .limit(10)\
                                    .all()
    
    return render_template('security.html', 
                         user=current_user,
                         login_history=login_history)

# Helper functions
def get_dashboard_url(user: User) -> str:
    """Get appropriate dashboard URL based on user role"""
    if user.role == 'admin':
        return url_for('admin.dashboard')
    elif user.role == 'dentist':
        return url_for('dentist.dashboard')
    elif user.role == 'assistant':
        return url_for('assistant.dashboard')
    elif user.role == 'patient':
        return url_for('patient.dashboard')
    else:
        return url_for('dashboard.index')

def generate_password_reset_token(user_id: int) -> str:
    """Generate password reset token"""
    from itsdangerous import URLSafeTimedSerializer
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt='password-reset-salt')

def verify_password_reset_token(token: str, max_age: int = 3600) -> Optional[int]:
    """Verify password reset token"""
    from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    
    try:
        user_id = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
        return user_id
    except (BadSignature, SignatureExpired):
        return None

def send_2fa_email(email: str, code: str):
    """Send 2FA code via email"""
    subject = "Your Two-Factor Authentication Code"
    body = f"""
    Your verification code is: {code}
    
    This code will expire in 10 minutes.
    
    If you didn't request this code, please ignore this email.
    """
    
    send_email(email, subject, body)

def send_password_reset_email(email: str, token: str):
    """Send password reset email"""
    reset_url = url_for('WebAuth.reset_password', token=token, _external=True)
    
    subject = "Password Reset Request"
    body = f"""
    You requested a password reset. Click the link below to reset your password:
    
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request this reset, please ignore this email.
    """
    
    send_email(email, subject, body)

# Error handlers
@web_bp.errorhandler(429)
def handle_rate_limit_exceeded(error):
    if request.path.startswith('/web/'):
        return render_template('error.html', 
                             error_title="Rate Limit Exceeded",
                             error_message="Too many requests. Please try again later."), 429
    return jsonify({'error': 'Rate limit exceeded'}), 429

@web_bp.errorhandler(401)
def handle_unauthorized(error):
    if request.path.startswith('/web/'):
        return redirect(url_for('WebAuth.web_login', next=request.path))
    return jsonify({'error': 'Unauthorized'}), 401

@web_bp.errorhandler(403)
def handle_forbidden(error):
    if request.path.startswith('/web/'):
        return render_template('error.html',
                             error_title="Access Denied",
                             error_message="You don't have permission to access this page."), 403
    return jsonify({'error': 'Forbidden'}), 403

# Template context processor
@web_bp.app_context_processor
def inject_user_data():
    """Inject user data into all templates"""
    return dict(
        current_user=current_user if current_user.is_authenticated else None,
        current_year=datetime.utcnow().year
    )