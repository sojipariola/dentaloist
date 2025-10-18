# backend/app/admin/auth.py

from flask import redirect, url_for, flash, request, session, current_app
from flask_login import current_user, login_user
from functools import wraps
import datetime

def admin_required(f):
    """Decorator to require admin access - FIXED VERSION"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Debug information
        print(f"🔐 ADMIN_REQUIRED CHECK:")
        print(f"   User authenticated: {current_user.is_authenticated}")
        print(f"   User is_admin: {getattr(current_user, 'is_admin', False)}")
        print(f"   User email: {getattr(current_user, 'email', 'No email')}")
        print(f"   Request endpoint: {request.endpoint}")
        print(f"   Request path: {request.path}")
        
        if not current_user.is_authenticated:
            print("❌ User not authenticated, redirecting to login")
            flash('Please log in to access the admin area.', 'warning')
            return redirect_to_login()
        
        if not getattr(current_user, 'is_admin', False):
            print("❌ User not admin, redirecting to login")
            flash('Admin access required.', 'error')
            return redirect_to_login()
        
        print("✅ Admin access granted")
        return f(*args, **kwargs)
    return decorated_function

def redirect_to_login():
    """Smart redirect to login page - IMPROVED VERSION"""
    # Store the intended destination
    next_url = request.url
    
    # Try different login endpoints
    login_endpoints = [
        'auth.admin_direct_login',
        'auth.login_form', 
        'auth.login',
        'admin.login'
    ]
    
    for endpoint in login_endpoints:
        try:
            url = url_for(endpoint, next=next_url)
            print(f"🔑 Redirecting to login: {url}")
            return redirect(url)
        except Exception as e:
            print(f"⚠️ Failed to generate URL for {endpoint}: {e}")
            continue
    
    # Fallback to direct path
    print("🔄 Using fallback login redirect")
    return redirect(f"/api/auth/admin-direct-login?next={next_url}")

def get_main_index():
    """Get main index URL"""
    try:
        return url_for('main.index')
    except:
        return '/'

# Add session-based admin verification
def verify_admin_session():
    """Verify admin session is valid"""
    if not current_user.is_authenticated:
        return False
    
    # Check if user has admin role
    if not getattr(current_user, 'is_admin', False):
        return False
    
    # Optional: Check session timeout
    session_timeout = current_app.config.get('ADMIN_SESSION_TIMEOUT', 3600)  # 1 hour default
    last_activity = session.get('admin_last_activity')
    
    if last_activity:
        last_activity_time = datetime.datetime.fromisoformat(last_activity)
        if (datetime.datetime.now() - last_activity_time).total_seconds() > session_timeout:
            flash('Admin session has expired. Please log in again.', 'warning')
            return False
    
    # Update last activity
    session['admin_last_activity'] = datetime.datetime.now().isoformat()
    return True