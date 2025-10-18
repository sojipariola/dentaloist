# check_config.py
import os
from pathlib import Path

def check_current_config():
    """Check current environment configuration"""
    env_path = Path('/home/soji/Documents/Projects/Dentaloist/backend/.env')
    
    if env_path.exists():
        print("📋 CURRENT .ENV CONFIGURATION:")
        print("=" * 40)
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.strip().startswith('#'):
                    if 'DATABASE' in line or 'SQL' in line or 'DB' in line:
                        print(f"  {line.strip()}")
    
    # Check Flask app configuration
    import sys
    sys.path.append('/home/soji/Documents/Projects/Dentaloist/backend')
    
    from app import create_app
    app = create_app()
    
    print(f"\n🔧 FLASK APP DATABASE CONFIG:")
    print(f"  SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f"  SQLALCHEMY_TRACK_MODIFICATIONS: {app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS')}")
    print(f"  ENV: {app.config.get('ENV')}")
    print(f"  DEBUG: {app.config.get('DEBUG')}")

check_current_config()
