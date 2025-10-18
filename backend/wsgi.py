
#!/usr/bin/env python3
"""
WSGI entry point for Dentaloist application
"""

# MUST BE FIRST: Eventlet monkey patching
# import eventlet
# eventlet.monkey_patch()

# Suppress deprecation warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")

import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create application instance
app = create_app()

# Generate FERNET_KEY from SECRET_KEY if not set
if not os.getenv('FERNET_KEY') and os.getenv('SECRET_KEY'):
    from cryptography.fernet import Fernet
    import base64
    import hashlib
    
    secret_key = os.getenv('SECRET_KEY')
    # Derive a Fernet key from SECRET_KEY
    key = base64.urlsafe_b64encode(hashlib.sha256(secret_key.encode()).digest())
    os.environ['FERNET_KEY'] = key.decode()
    print("Generated FERNET_KEY from SECRET_KEY")

if __name__ == '__main__':
    # Development server
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = True
    # debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting development server...")
    app.run(host=host, port=port, debug=debug)

'''
export FLASK_APP=wsgi.py
export FLASK_ENV=development
export FLASK_DEBUG=1#
python3 wsgi.py

FLASK_DEBUG=1 FLASK_APP=wsgi.py python3 -m flask run --host=0.0.0.0 --port=5000
'''


'''
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

'''