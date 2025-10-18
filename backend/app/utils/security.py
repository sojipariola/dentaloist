# backend/app/utils/security.py

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_fernet_key(password: str, salt: bytes = None) -> str:
    """Generate a Fernet key from a password"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key.decode()

def ensure_fernet_key():
    """Ensure a valid Fernet key exists in environment"""
    key = os.getenv('FERNET_KEY')
    
    if not key:
        # Generate from secret key or random
        secret = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')
        key = generate_fernet_key(secret)
        os.environ['FERNET_KEY'] = key
        print(f"Generated FERNET_KEY from SECRET_KEY")
    
    # Verify the key is valid
    try:
        Fernet(key.encode())
        return key
    except ValueError:
        # Generate a new random key
        key = Fernet.generate_key().decode()
        os.environ['FERNET_KEY'] = key
        print(f"Generated new random FERNET_KEY")
        return key

# Use this in your app initialization
fernet_key = ensure_fernet_key()