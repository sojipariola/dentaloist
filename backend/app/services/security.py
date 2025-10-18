# backend/app/services/security.py
import re
import secrets
import string
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
import jwt
from flask import current_app
from flask_bcrypt import generate_password_hash, check_password_hash
import logging
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

# Import models for database operations
from ..models import User, PasswordHistory, SecurityEvent, db

logger = logging.getLogger(__name__)

class SecurityService:
    """
    Comprehensive security service with password management, token handling, and security monitoring
    """
    
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security service with Flask app"""
        self.app = app
        self.config = app.config
        
        # JWT configuration
        self.jwt_secret = app.config.get('JWT_SECRET_KEY', 'fallback-secret-key-change-in-production')
        self.jwt_algorithm = app.config.get('JWT_ALGORITHM', 'HS256')
        self.jwt_expiration = app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)  # 1 hour default
        
        # Password policy
        self.password_min_length = app.config.get('PASSWORD_MIN_LENGTH', 8)
        self.password_require_uppercase = app.config.get('PASSWORD_REQUIRE_UPPERCASE', True)
        self.password_require_lowercase = app.config.get('PASSWORD_REQUIRE_LOWERCASE', True)
        self.password_require_numbers = app.config.get('PASSWORD_REQUIRE_NUMBERS', True)
        self.password_require_special = app.config.get('PASSWORD_REQUIRE_SPECIAL', True)
        self.password_history_size = app.config.get('PASSWORD_HISTORY_SIZE', 5)
        
        # Security settings
        self.max_login_attempts = app.config.get('MAX_LOGIN_ATTEMPTS', 5)
        self.lockout_duration = app.config.get('LOCKOUT_DURATION', 900)  # 15 minutes
        self.session_timeout = app.config.get('SESSION_TIMEOUT', 3600)  # 1 hour
    
    def hash_password(self, password: str) -> str:
        """
        Hash password with bcrypt and log security event
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        try:
            hashed = generate_password_hash(password).decode("utf-8")
            return hashed
        except Exception as e:
            logger.error(f"Password hashing failed: {str(e)}")
            raise SecurityException("Password hashing failed")
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash with timing attack protection
        
        Args:
            password: Plain text password to verify
            password_hash: Stored password hash
            
        Returns:
            bool: True if password matches
        """
        try:
            return check_password_hash(password_hash, password)
        except Exception as e:
            logger.error(f"Password verification failed: {str(e)}")
            return False
    
    def check_password_strength(self, password: str) -> Dict[str, Any]:
        """
        Check password strength against policy
        
        Args:
            password: Password to check
            
        Returns:
            Dict with strength analysis
        """
        issues = []
        score = 0
        
        # Length check
        if len(password) < self.password_min_length:
            issues.append(f"Password must be at least {self.password_min_length} characters long")
        else:
            score += 1
        
        # Uppercase check
        if self.password_require_uppercase and not re.search(r'[A-Z]', password):
            issues.append("Password must contain at least one uppercase letter")
        else:
            score += 1
        
        # Lowercase check
        if self.password_require_lowercase and not re.search(r'[a-z]', password):
            issues.append("Password must contain at least one lowercase letter")
        else:
            score += 1
        
        # Numbers check
        if self.password_require_numbers and not re.search(r'[0-9]', password):
            issues.append("Password must contain at least one number")
        else:
            score += 1
        
        # Special characters check
        if self.password_require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Password must contain at least one special character")
        else:
            score += 1
        
        # Common password check
        if self._is_common_password(password):
            issues.append("Password is too common or easily guessable")
            score = max(0, score - 2)
        
        # Sequential characters check
        if self._has_sequential_chars(password):
            issues.append("Password contains sequential characters")
            score = max(0, score - 1)
        
        # Calculate strength level
        if score >= 5:
            strength = "very_strong"
        elif score >= 4:
            strength = "strong"
        elif score >= 3:
            strength = "moderate"
        else:
            strength = "weak"
        
        return {
            'is_strong': len(issues) == 0,
            'strength': strength,
            'score': score,
            'max_score': 5,
            'issues': issues,
            'message': 'Password meets all requirements' if len(issues) == 0 else 'Password needs improvement'
        }
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate cryptographically secure random token
        
        Args:
            length: Token length in bytes
            
        Returns:
            str: Secure random token
        """
        return secrets.token_urlsafe(length)
    
    def generate_2fa_code(self, user_id: int, length: int = 6) -> str:
        """
        Generate time-based 2FA code
        
        Args:
            user_id: User ID for code association
            length: Code length
            
        Returns:
            str: 2FA code
        """
        # In production, use TOTP algorithm
        # For now, generate random numeric code
        digits = string.digits
        code = ''.join(secrets.choice(digits) for _ in range(length))
        
        # Store code in database with expiration
        from ..models import TwoFactorCode
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        two_fa_code = TwoFactorCode(
            user_id=user_id,
            code=code,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        
        db.session.add(two_fa_code)
        db.session.commit()
        
        return code
    
    def verify_2fa_code(self, user_id: int, code: str) -> bool:
        """
        Verify 2FA code
        
        Args:
            user_id: User ID
            code: Code to verify
            
        Returns:
            bool: True if code is valid
        """
        from ..models import TwoFactorCode
        
        # Find valid, unexpired code
        valid_code = TwoFactorCode.query.filter(
            TwoFactorCode.user_id == user_id,
            TwoFactorCode.code == code,
            TwoFactorCode.expires_at > datetime.utcnow(),
            TwoFactorCode.used == False
        ).first()
        
        if valid_code:
            # Mark code as used
            valid_code.used = True
            valid_code.used_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    def generate_jwt_token(self, user_id: int, tenant_id: str, additional_claims: Dict = None) -> str:
        """
        Generate JWT token with user claims
        
        Args:
            user_id: User ID
            tenant_id: Tenant ID
            additional_claims: Additional claims to include
            
        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user_id,
            'tenant_id': tenant_id,
            'exp': datetime.utcnow() + timedelta(seconds=self.jwt_expiration),
            'iat': datetime.utcnow(),
            'type': 'access'
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """
        Verify JWT token and return payload
        
        Args:
            token: JWT token to verify
            
        Returns:
            Dict: Token payload if valid
            
        Raises:
            SecurityException: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise SecurityException("Token has expired")
        except jwt.InvalidTokenError as e:
            raise SecurityException(f"Invalid token: {str(e)}")
    
    def generate_password_reset_token(self, user_id: int) -> str:
        """
        Generate secure password reset token
        
        Args:
            user_id: User ID
            
        Returns:
            str: Reset token
        """
        serializer = URLSafeTimedSerializer(self.config.get('SECRET_KEY'))
        return serializer.dumps(user_id, salt='password-reset')
    
    def verify_password_reset_token(self, token: str, max_age: int = 3600) -> Optional[int]:
        """
        Verify password reset token
        
        Args:
            token: Reset token
            max_age: Maximum token age in seconds
            
        Returns:
            Optional[int]: User ID if token is valid, None otherwise
        """
        serializer = URLSafeTimedSerializer(self.config.get('SECRET_KEY'))
        
        try:
            user_id = serializer.loads(token, salt='password-reset', max_age=max_age)
            return user_id
        except (BadSignature, SignatureExpired):
            return None
    
    def check_password_history(self, user_id: int, new_password: str) -> bool:
        """
        Check if password has been used before
        
        Args:
            user_id: User ID
            new_password: New password to check
            
        Returns:
            bool: True if password is not in history
        """
        # Get recent password history
        recent_passwords = PasswordHistory.query.filter_by(user_id=user_id)\
                                              .order_by(PasswordHistory.created_at.desc())\
                                              .limit(self.password_history_size)\
                                              .all()
        
        for history in recent_passwords:
            if self.verify_password(new_password, history.password_hash):
                return False  # Password found in history
        
        return True  # Password not in history
    
    def update_password_history(self, user_id: int, password_hash: str):
        """
        Update password history for user
        
        Args:
            user_id: User ID
            password_hash: New password hash
        """
        # Create new history entry
        history_entry = PasswordHistory(
            user_id=user_id,
            password_hash=password_hash,
            created_at=datetime.utcnow()
        )
        
        db.session.add(history_entry)
        
        # Remove old entries beyond history size
        old_entries = PasswordHistory.query.filter_by(user_id=user_id)\
                                         .order_by(PasswordHistory.created_at.desc())\
                                         .offset(self.password_history_size)\
                                         .all()
        
        for entry in old_entries:
            db.session.delete(entry)
        
        db.session.commit()
    
    def log_security_event(self, 
                          user_id: int, 
                          event_type: str, 
                          description: str, 
                          ip_address: str = None,
                          user_agent: str = None,
                          severity: str = 'info'):
        """
        Log security event for monitoring
        
        Args:
            user_id: User ID
            event_type: Type of security event
            description: Event description
            ip_address: IP address
            user_agent: User agent string
            severity: Event severity
        """
        security_event = SecurityEvent(
            user_id=user_id,
            event_type=event_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            occurred_at=datetime.utcnow()
        )
        
        db.session.add(security_event)
        db.session.commit()
        
        # Also log to application logs
        logger.info(f"Security event: {event_type} - {description} - User: {user_id}")
    
    def check_account_lockout(self, user_id: int) -> Tuple[bool, int]:
        """
        Check if account is locked out due to failed attempts
        
        Args:
            user_id: User ID
            
        Returns:
            Tuple[bool, int]: (is_locked, remaining_time_seconds)
        """
        from ..models import LoginAttempt
        
        # Get recent failed attempts
        lockout_time = datetime.utcnow() - timedelta(seconds=self.lockout_duration)
        failed_attempts = LoginAttempt.query.filter(
            LoginAttempt.user_id == user_id,
            LoginAttempt.success == False,
            LoginAttempt.attempted_at >= lockout_time
        ).count()
        
        if failed_attempts >= self.max_login_attempts:
            # Calculate remaining lockout time
            oldest_attempt = LoginAttempt.query.filter(
                LoginAttempt.user_id == user_id,
                LoginAttempt.success == False
            ).order_by(LoginAttempt.attempted_at.asc()).first()
            
            if oldest_attempt:
                lockout_until = oldest_attempt.attempted_at + timedelta(seconds=self.lockout_duration)
                remaining = max(0, int((lockout_until - datetime.utcnow()).total_seconds()))
                return True, remaining
        
        return False, 0
    
    def generate_api_key(self, user_id: int, name: str) -> Tuple[str, str]:
        """
        Generate API key for user
        
        Args:
            user_id: User ID
            name: API key name/description
            
        Returns:
            Tuple[str, str]: (api_key_id, plain_text_key)
        """
        from ..models import ApiKey
        
        # Generate key
        plain_text_key = self.generate_secure_token(32)
        key_hash = self.hash_password(plain_text_key)
        
        # Create API key record
        api_key = ApiKey(
            user_id=user_id,
            name=name,
            key_hash=key_hash,
            created_at=datetime.utcnow(),
            last_used=None,
            is_active=True
        )
        
        db.session.add(api_key)
        db.session.commit()
        
        return str(api_key.id), plain_text_key
    
    def verify_api_key(self, api_key_id: str, provided_key: str) -> bool:
        """
        Verify API key
        
        Args:
            api_key_id: API key ID
            provided_key: Provided API key
            
        Returns:
            bool: True if key is valid
        """
        from ..models import ApiKey
        
        api_key = ApiKey.query.filter_by(id=api_key_id, is_active=True).first()
        
        if not api_key:
            return False
        
        # Verify key
        if self.verify_password(provided_key, api_key.key_hash):
            # Update last used timestamp
            api_key.last_used = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    def _is_common_password(self, password: str) -> bool:
        """Check if password is common"""
        common_passwords = {
            'password', '123456', '12345678', '1234', 'qwerty', 'letmein',
            'admin', 'welcome', 'monkey', 'password1', '1234567'
        }
        return password.lower() in common_passwords
    
    def _has_sequential_chars(self, password: str) -> bool:
        """Check for sequential characters"""
        # Check for sequential numbers
        for i in range(len(password) - 2):
            if (password[i:i+3].isdigit() and 
                ord(password[i+1]) - ord(password[i]) == 1 and
                ord(password[i+2]) - ord(password[i+1]) == 1):
                return True
        
        # Check for sequential letters
        for i in range(len(password) - 2):
            if (password[i:i+3].isalpha() and 
                ord(password[i+1].lower()) - ord(password[i].lower()) == 1 and
                ord(password[i+2].lower()) - ord(password[i+1].lower()) == 1):
                return True
        
        return False

class SecurityException(Exception):
    """Security-related exception"""
    pass

# Global security service instance
security_service = SecurityService()

# Convenience functions
def hash_password(password: str) -> str:
    """Convenience function for password hashing"""
    return security_service.hash_password(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Convenience function for password verification"""
    return security_service.verify_password(password, password_hash)

def check_password_strength(password: str) -> Dict[str, Any]:
    """Convenience function for password strength checking"""
    return security_service.check_password_strength(password)

def generate_secure_token(length: int = 32) -> str:
    """Convenience function for token generation"""
    return security_service.generate_secure_token(length)

def generate_jwt_token(user_id: int, tenant_id: str, additional_claims: Dict = None) -> str:
    """Convenience function for JWT generation"""
    return security_service.generate_jwt_token(user_id, tenant_id, additional_claims)

def init_security_service(app):
    """Initialize security service with Flask app"""
    security_service.init_app(app)