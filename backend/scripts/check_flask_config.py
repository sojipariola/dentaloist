# check_flask_config.py
import os
import sys
sys.path.append('/home/soji/Documents/Projects/Dentaloist/backend')

from app import create_app

def check_flask_config():
    """Check Flask application configuration"""
    app = create_app()
    
    print("🔧 Flask Configuration:")
    print(f"   ENV: {app.config.get('ENV', 'Not set')}")
    print(f"   DEBUG: {app.config.get('DEBUG', 'Not set')}")
    print(f"   TESTING: {app.config.get('TESTING', 'Not set')}")
    
    # Database configuration
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not set')
    print(f"   DATABASE URI: {db_uri}")
    
    # Instance path
    print(f"   INSTANCE PATH: {app.instance_path}")
    
    # Check if we're using SQLite
    if 'sqlite' in db_uri.lower():
        print("   🗄️ Using SQLite database")
        # Extract database file path
        if '///' in db_uri:
            db_file = db_uri.split('///')[-1]
            print(f"   📁 Database file: {db_file}")
            
            # Check if file exists
            if os.path.exists(db_file):
                size = os.path.getsize(db_file)
                print(f"   📊 Database size: {size} bytes")
            else:
                print("   ❌ Database file not found!")
    else:
        print(f"   🗄️ Using: {db_uri.split(':')[0] if ':' in db_uri else db_uri}")

if __name__ == "__main__":
    check_flask_config()
