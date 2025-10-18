from flask import redirect, url_for, flash, request
from flask_login import current_user
from functools import wraps

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            flash('Admin access required.', 'error')
            return redirect_to_login()
        return f(*args, **kwargs)
    return decorated_function

def redirect_to_login():
    """Smart redirect to login page - replicates Flask-Admin behavior"""
    login_options = [
        ('auth.admin_direct_login', '/api/auth/admin-direct-login'),
        ('auth.login_form', '/api/auth/login-form'),
        ('auth.login', '/api/auth/login'),
    ]
    
    for endpoint, path in login_options:
        try:
            url = url_for(endpoint, next=request.url)
            return redirect(url)
        except:
            continue
    
    return redirect(f"/api/auth/admin-direct-login?next={request.url}")

def get_main_index():
    """Get main index URL"""
    try:
        return url_for('main.index')
    except:
        return '/'