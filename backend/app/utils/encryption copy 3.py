# backend/app/utils/encryption.py

import os
import base64
import json
import hmac
import logging
from typing import Optional, Union, Any
from cryptography.fernet import Fernet, MultiFernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from flask import current_app

logger = logging.getLogger(__name__)
ENV_FILE = ".env"


# ===== Helper: Get or generate Fernet key =====
def get_fernet_key(env_var="ENCRYPTION_KEY") -> str:
    """Retrieve the Fernet key from environment or .env, generate if missing"""
    key = os.getenv(env_var)

    if key:
        try:
            Fernet(key.encode())
            return key
        except ValueError:
            print("⚠️ Invalid Fernet key in environment. Generating a new one...")

    # Generate new key
    new_key = Fernet.generate_key().decode()
    print(f"🔑 Generated new Fernet key: {new_key}")

    # Persist to .env
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()
        with open(ENV_FILE, "w") as f:
            found = False
            for line in lines:
                if line.startswith(f"{env_var}="):
                    f.write(f"{env_var}={new_key}\n")
                    found = True
                else:
                    f.write(line)
            if not found:
                f.write(f"{env_var}={new_key}\n")
    else:
        with open(ENV_FILE, "w") as f:
            f.write(f"{env_var}={new_key}\n")

    os.environ[env_var] = new_key
    return new_key


# ===== Encryption Manager =====
class EncryptionManager:
    """Handles encryption, decryption, and key rotation using Fernet"""

    def __init__(self, app=None):
        self.fernet: Optional[Fernet] = None
        self.rotation_fernet: Optional[Fernet] = None
        self.initialized: bool = False

        if app:
            self.init_app(app)

    def init_app(self, app):
        try:
            encryption_key = app.config.get("ENCRYPTION_KEY") or get_fernet_key()
            self.fernet = Fernet(encryption_key.encode())

            rotation_key = app.config.get("ENCRYPTION_ROTATION_KEY") or os.getenv("ENCRYPTION_ROTATION_KEY")
            if rotation_key:
                self.rotation_fernet = Fernet(rotation_key.encode())
                self.fernet = MultiFernet([self.fernet, self.rotation_fernet])

            self.initialized = True
            logger.info("Encryption manager initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize encryption: {e}")
            if app.debug:
                self.fernet = None
                self.initialized = False
            else:
                raise

    def generate_key(self) -> str:
        return Fernet.generate_key().decode()

    def encrypt(self, data: Union[str, bytes, dict, list]) -> Optional[str]:
        if not self.initialized or not self.fernet:
            logger.warning("Encryption not initialized, returning plain text")
            return json.dumps(data) if isinstance(data, (dict, list)) else str(data)

        try:
            if isinstance(data, (dict, list)):
                data_bytes = json.dumps(data).encode("utf-8")
            elif isinstance(data, str):
                data_bytes = data.encode("utf-8")
            else:
                data_bytes = bytes(data)

            encrypted = self.fernet.encrypt(data_bytes)
            return base64.urlsafe_b64encode(encrypted).decode("utf-8")

        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            return None

    def decrypt(self, encrypted_data: str, return_type: type = str) -> Optional[Any]:
        if not self.initialized or not self.fernet:
            logger.warning("Encryption not initialized, returning plain text")
            try:
                if return_type in (dict, list):
                    return json.loads(encrypted_data)
                elif return_type == bytes:
                    return encrypted_data.encode("utf-8")
                return encrypted_data
            except Exception:
                return encrypted_data

        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode("utf-8"))
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)

            if return_type == bytes:
                return decrypted_bytes
            elif return_type in (dict, list):
                return json.loads(decrypted_bytes.decode("utf-8"))
            return decrypted_bytes.decode("utf-8")

        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return None

    def rotate_key(self, new_key: str) -> bool:
        try:
            new_fernet = Fernet(new_key.encode())
            self.fernet = MultiFernet([new_fernet, self.fernet])
            return True
        except Exception as e:
            logger.error(f"Key rotation failed: {e}")
            return False

    def is_encrypted(self, data: str) -> bool:
        try:
            if not data or len(data) < 50:
                return False
            decoded = base64.urlsafe_b64decode(data.encode("utf-8"))
            return len(decoded) >= 50
        except Exception:
            return False


# ===== Global instance =====
encryption_manager = EncryptionManager()


# ===== Password hashing =====
def hash_password(password: str, salt: Optional[str] = None) -> dict:
    salt_bytes = base64.urlsafe_b64decode(salt.encode("utf-8")) if salt else os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode("utf-8"))
    return {
        "hash": base64.urlsafe_b64encode(key).decode("utf-8"),
        "salt": base64.urlsafe_b64encode(salt_bytes).decode("utf-8"),
        "iterations": 100000
    }


def verify_password(password: str, stored_hash: str, salt: str) -> bool:
    try:
        salt_bytes = base64.urlsafe_b64decode(salt.encode("utf-8"))
        stored_bytes = base64.urlsafe_b64decode(stored_hash.encode("utf-8"))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=100000,
            backend=default_backend()
        )
        return hmac.compare_digest(kdf.derive(password.encode("utf-8")), stored_bytes)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


# ===== Secure token & API key =====
def generate_secure_token(length: int = 32) -> str:
    return base64.urlsafe_b64encode(os.urandom(length)).decode("utf-8")


def generate_api_key(prefix: str = "sk_") -> str:
    return f"{prefix}{generate_secure_token(24)}"


# ===== Data masking =====
def mask_sensitive_data(data: Any, fields_to_mask: list = None) -> Any:
    if fields_to_mask is None:
        fields_to_mask = ["password", "secret", "token", "key", "credit_card", "ssn", "dob"]

    if isinstance(data, dict):
        return {
            k: "***MASKED***" if any(f in k.lower() for f in fields_to_mask) else mask_sensitive_data(v, fields_to_mask)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [mask_sensitive_data(item, fields_to_mask) for item in data]
    return data


# ===== Convenience wrappers =====
encrypt_data = encryption_manager.encrypt
decrypt_data = encryption_manager.decrypt
encrypt_string = lambda s: encryption_manager.encrypt(s)
decrypt_string = lambda s: encryption_manager.decrypt(s, str)
encrypt_json = lambda j: encryption_manager.encrypt(j)
decrypt_json = lambda j: (
    encryption_manager.decrypt(j, dict) or encryption_manager.decrypt(j, list)
)


# ===== Flask helper =====
def configure_encryption(app):
    app.config.setdefault("ENCRYPTION_KEY", os.environ.get("ENCRYPTION_KEY"))
    app.config.setdefault("ENCRYPTION_ROTATION_KEY", os.environ.get("ENCRYPTION_ROTATION_KEY"))
    encryption_manager.init_app(app)


# ===== Health check =====
def check_encryption_health() -> dict:
    test_data = "encryption_test_123"
    try:
        encrypted = encryption_manager.encrypt(test_data)
        decrypted = encryption_manager.decrypt(encrypted, str)
        return {
            "healthy": decrypted == test_data,
            "initialized": encryption_manager.initialized,
            "test_passed": decrypted == test_data,
            "can_encrypt": encrypted is not None,
            "can_decrypt": decrypted is not None,
        }
    except Exception as e:
        return {"healthy": False, "initialized": encryption_manager.initialized, "error": str(e), "test_passed": False}


__all__ = [
    "encrypt_data", "decrypt_data", "encrypt_string", "decrypt_string",
    "encrypt_json", "decrypt_json", "hash_password", "verify_password",
    "generate_secure_token", "generate_api_key", "mask_sensitive_data",
    "configure_encryption", "check_encryption_health",
    "EncryptionManager", "encryption_manager"
]
