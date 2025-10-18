# backend/app/utils/encryption.py

import os
import base64
import hashlib
import hmac
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from flask import current_app
import json
import logging
from typing import Optional, Union, Any

logger = logging.getLogger(__name__)

def get_fernet_key():
    # Try to read the key from an environment variable
    key = os.getenv("ENCRYPTION_KEY")
    
    if key:
        try:
            # Ensure the key is valid
            Fernet(key.encode())
            return key
        except ValueError:
            print("⚠️ Invalid Fernet key in environment. Generating a new one...")
    
    # If no key exists or it's invalid, generate a new one
    new_key = Fernet.generate_key().decode()
    print(f"🔑 Generated new Fernet key: {new_key}")
    
    # Optional: save it to environment for this session
    os.environ["ENCRYPTION_KEY"] = new_key
    return new_key


class EncryptionManager:
    """Manager for encryption and decryption operations using Fernet symmetric encryption"""

    def __init__(self, app=None):
        self.fernet = None
        self.rotation_fernet = None
        self.initialized = False

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize encryption with Flask app configuration"""
        try:
            # Get encryption key from configuration or environment
            encryption_key = app.config.get('ENCRYPTION_KEY') or os.environ.get('ENCRYPTION_KEY')

            if not encryption_key:
                # Generate a new key if none exists (for development)
                if app.debug or app.testing:
                    encryption_key = self.generate_key()
                    logger.warning(
                        "Using auto-generated encryption key for development. "
                        "Set ENCRYPTION_KEY for production."
                    )
                else:
                    raise ValueError("ENCRYPTION_KEY not configured")

            # ✅ FIXED: use encryption_key, not fernet_key
            self.fernet = Fernet(encryption_key.encode())

            # Check if we have a rotation key for key rotation
            rotation_key = app.config.get('ENCRYPTION_ROTATION_KEY') or os.environ.get('ENCRYPTION_ROTATION_KEY')
            if rotation_key:
                self.rotation_fernet = Fernet(rotation_key.encode())
                self.fernet = MultiFernet([self.fernet, self.rotation_fernet])

            self.initialized = True
            logger.info("Encryption manager initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            if app.debug:
                # In development, we can continue without encryption
                self.fernet = None
                self.initialized = False
            else:
                raise

    def generate_key(self) -> str:
        """Generate a new Fernet encryption key"""
        return Fernet.generate_key().decode()

    def encrypt(self, data: Union[str, bytes, dict, list]) -> Optional[str]:
        """Encrypt data using Fernet symmetric encryption"""
        if not self.initialized or not self.fernet:
            logger.warning("Encryption not initialized, returning plain text")
            return json.dumps(data) if isinstance(data, (dict, list)) else str(data)

        try:
            if isinstance(data, (dict, list)):
                data_bytes = json.dumps(data).encode('utf-8')
            elif isinstance(data, str):
                data_bytes = data.encode('utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                data_bytes = str(data).encode('utf-8')

            encrypted_data = self.fernet.encrypt(data_bytes)
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')

        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return None

    def decrypt(self, encrypted_data: str, return_type: type = str) -> Optional[Any]:
        """Decrypt data that was encrypted with encrypt_data"""
        if not self.initialized or not self.fernet:
            logger.warning("Encryption not initialized, returning plain text")
            try:
                if return_type in (dict, list):
                    return json.loads(encrypted_data)
                elif return_type == bytes:
                    return encrypted_data.encode('utf-8')
                return encrypted_data
            except Exception:
                return encrypted_data

        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)

            if return_type == bytes:
                return decrypted_bytes
            elif return_type in (dict, list):
                return json.loads(decrypted_bytes.decode('utf-8'))
            return decrypted_bytes.decode('utf-8')

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None

    def rotate_key(self, new_key: str) -> bool:
        """Rotate to a new encryption key"""
        try:
            new_fernet = Fernet(new_key.encode())
            self.fernet = MultiFernet([new_fernet, self.fernet])
            return True
        except Exception as e:
            logger.error(f"Key rotation failed: {e}")
            return False

    def is_encrypted(self, data: str) -> bool:
        """Check if data appears to be encrypted by this system"""
        try:
            if not data or len(data) < 50:
                return False
            decoded = base64.urlsafe_b64decode(data.encode('utf-8'))
            return len(decoded) >= 50
        except Exception:
            return False


# Global encryption manager instance
encryption_manager = EncryptionManager()


# ===== Password hashing functions =====

def hash_password(password: str, salt: Optional[str] = None) -> dict:
    """Hash a password using PBKDF2 with HMAC-SHA256"""
    salt_bytes = base64.urlsafe_b64decode(salt.encode('utf-8')) if salt else os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
        backend=default_backend()
    )

    password_bytes = password.encode('utf-8')
    key = kdf.derive(password_bytes)

    return {
        'hash': base64.urlsafe_b64encode(key).decode('utf-8'),
        'salt': base64.urlsafe_b64encode(salt_bytes).decode('utf-8'),
        'iterations': 100000
    }


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    """Verify a password against a stored hash"""
    try:
        salt_bytes = base64.urlsafe_b64decode(salt.encode('utf-8'))
        stored_hash_bytes = base64.urlsafe_b64decode(stored_hash.encode('utf-8'))

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=100000,
            backend=default_backend()
        )

        password_bytes = password.encode('utf-8')
        new_hash = kdf.derive(password_bytes)
        return hmac.compare_digest(new_hash, stored_hash_bytes)

    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


# ===== Secure token generation =====

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token"""
    random_bytes = os.urandom(length)
    return base64.urlsafe_b64encode(random_bytes).decode('utf-8')


def generate_api_key(prefix: str = "sk_") -> str:
    """Generate a secure API key"""
    random_part = generate_secure_token(24)
    return f"{prefix}{random_part}"


# ===== Data masking for logging =====

def mask_sensitive_data(data: Any, fields_to_mask: list = None) -> Any:
    """Mask sensitive data in objects for safe logging/display"""
    if fields_to_mask is None:
        fields_to_mask = ['password', 'secret', 'token', 'key', 'credit_card', 'ssn', 'dob']

    if isinstance(data, dict):
        return {
            key: '***MASKED***' if any(mask_field in key.lower() for mask_field in fields_to_mask)
            else mask_sensitive_data(value, fields_to_mask)
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [mask_sensitive_data(item, fields_to_mask) for item in data]
    return data


# ===== Convenience functions that use the encryption manager =====

def encrypt_data(data: Union[str, bytes, dict, list]) -> Optional[str]:
    return encryption_manager.encrypt(data)


def decrypt_data(encrypted_data: str, return_type: type = str) -> Optional[Any]:
    return encryption_manager.decrypt(encrypted_data, return_type)


def encrypt_string(data: str) -> Optional[str]:
    return encryption_manager.encrypt(data)


def decrypt_string(encrypted_data: str) -> Optional[str]:
    return encryption_manager.decrypt(encrypted_data, str)


def encrypt_json(data: Union[dict, list]) -> Optional[str]:
    return encryption_manager.encrypt(data)


def decrypt_json(encrypted_data: str) -> Optional[Union[dict, list]]:
    result = encryption_manager.decrypt(encrypted_data, dict)
    if result is None:
        result = encryption_manager.decrypt(encrypted_data, list)
    return result


# ===== Configuration helper =====

def configure_encryption(app):
    app.config.setdefault('ENCRYPTION_KEY', os.environ.get('ENCRYPTION_KEY'))
    app.config.setdefault('ENCRYPTION_ROTATION_KEY', os.environ.get('ENCRYPTION_ROTATION_KEY'))
    encryption_manager.init_app(app)


# ===== Health check =====

def check_encryption_health() -> dict:
    test_data = "encryption_test_123"
    try:
        encrypted = encryption_manager.encrypt(test_data)
        decrypted = encryption_manager.decrypt(encrypted, str)
        return {
            'healthy': decrypted == test_data,
            'initialized': encryption_manager.initialized,
            'test_passed': decrypted == test_data,
            'can_encrypt': encrypted is not None,
            'can_decrypt': decrypted is not None
        }
    except Exception as e:
        return {
            'healthy': False,
            'initialized': encryption_manager.initialized,
            'error': str(e),
            'test_passed': False
        }


# ===== Migration function =====

def migrate_encryption_key(old_key: str, new_key: str, data_callback: callable) -> dict:
    results = {
        'total_processed': 0,
        'successful': 0,
        'failed': 0,
        'errors': []
    }

    try:
        old_fernet = Fernet(old_key.encode())
        new_fernet = Fernet(new_key.encode())

        data_to_migrate = data_callback()

        for item in data_to_migrate:
            try:
                results['total_processed'] += 1
                encrypted_data = base64.urlsafe_b64decode(item['encrypted_data'].encode('utf-8'))
                decrypted_data = old_fernet.decrypt(encrypted_data)

                reencrypted_data = new_fernet.encrypt(decrypted_data)
                new_encrypted_string = base64.urlsafe_b64encode(reencrypted_data).decode('utf-8')

                # TODO: update your storage here
                results['successful'] += 1

            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'item_id': item.get('id', 'unknown'),
                    'error': str(e)
                })

        return results

    except Exception as e:
        logger.error(f"Encryption migration failed: {e}")
        return {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'errors': [{'error': f'Migration failed: {str(e)}'}]
        }

# Usage in your encryption manager
encryption_key = get_fernet_key()
fernet = Fernet(encryption_key.encode())

__all__ = [
    'encrypt_data',
    'decrypt_data',
    'encrypt_string',
    'decrypt_string',
    'encrypt_json',
    'decrypt_json',
    'hash_password',
    'verify_password',
    'generate_secure_token',
    'generate_api_key',
    'mask_sensitive_data',
    'configure_encryption',
    'check_encryption_health',
    'EncryptionManager',
    'encryption_manager'
]
