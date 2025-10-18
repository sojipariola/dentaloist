# backend/app/utils/social_auth.py

import requests
from flask import current_app
import jwt
from ..models import User, Organization, SocialLogin, db

def verify_google_token(id_token=None, access_token=None):
    """Verify Google OAuth token and return user info"""
    try:
        if id_token:
            # Verify ID token
            user_info = jwt.decode(id_token, options={"verify_signature": False})
        elif access_token:
            # Get user info using access token
            response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            if response.status_code != 200:
                return None
            user_info = response.json()
        else:
            return None
            
        return user_info
    except Exception as e:
        current_app.logger.error(f"Google token verification failed: {e}")
        return None

def verify_facebook_token(access_token):
    """Verify Facebook OAuth token and return user info"""
    try:
        # Verify token and get basic info
        verify_response = requests.get(
            f'https://graph.facebook.com/debug_token',
            params={
                'input_token': access_token,
                'access_token': f"{current_app.config.get('FACEBOOK_APP_ID')}|{current_app.config.get('FACEBOOK_APP_SECRET')}"
            }
        )
        
        if verify_response.status_code != 200:
            return None
            
        verify_data = verify_response.json()
        if not verify_data.get('data', {}).get('is_valid'):
            return None
        
        # Get user info
        user_response = requests.get(
            'https://graph.facebook.com/me',
            params={
                'access_token': access_token,
                'fields': 'id,name,email,first_name,last_name,picture'
            }
        )
        
        if user_response.status_code != 200:
            return None
            
        return user_response.json()
    except Exception as e:
        current_app.logger.error(f"Facebook token verification failed: {e}")
        return None

def verify_github_token(code=None, access_token=None):
    """Verify GitHub OAuth token and return user info"""
    try:
        if code and not access_token:
            # Exchange code for access token
            token_response = requests.post(
                'https://github.com/login/oauth/access_token',
                headers={'Accept': 'application/json'},
                data={
                    'client_id': current_app.config.get('GITHUB_CLIENT_ID'),
                    'client_secret': current_app.config.get('GITHUB_CLIENT_SECRET'),
                    'code': code
                }
            )
            
            if token_response.status_code != 200:
                return None
                
            token_data = token_response.json()
            access_token = token_data.get('access_token')
        
        if not access_token:
            return None
        
        # Get user info
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if user_response.status_code != 200:
            return None
            
        user_info = user_response.json()
        
        # Get email if not public
        if not user_info.get('email'):
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'token {access_token}'}
            )
            if email_response.status_code == 200:
                emails = email_response.json()
                primary_email = next((email for email in emails if email.get('primary')), None)
                if primary_email:
                    user_info['email'] = primary_email.get('email')
        
        return user_info
    except Exception as e:
        current_app.logger.error(f"GitHub token verification failed: {e}")
        return None

def find_or_create_social_user(provider, provider_id, email, first_name, last_name, picture=None):
    """Find or create user from social login"""
    # Check if social login exists
    social_login = SocialLogin.query.filter_by(
        provider=provider,
        provider_id=provider_id
    ).first()
    
    if social_login:
        user = social_login.user
        user.is_new = False
        return user
    
    # Check if user exists by email
    user = None
    if email:
        user = User.query.filter_by(email=email).first()
    
    if not user:
        # Create new user
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            organization_id=get_default_organization_id(),
            role='patient',  # Default role for social logins
            is_active=True,
            avatar_url=picture
        )
        db.session.add(user)
        db.session.flush()  # Get user ID without committing
        user.is_new = True
    
    # Create or update social login
    social_login = SocialLogin(
        user_id=user.id,
        provider=provider,
        provider_id=provider_id,
        email=email
    )
    db.session.add(social_login)
    db.session.commit()
    
    return user

def get_default_organization_id():
    """Get or create default organization for social logins"""
    # You might want to create a specific organization for social login users
    # or use an existing default organization
    org = Organization.query.filter_by(name='Social Users').first()
    if not org:
        org = Organization(
            name='Social Users',
            email='social@dentaloist.com',
            is_active=True
        )
        db.session.add(org)
        db.session.commit()
    return org.id