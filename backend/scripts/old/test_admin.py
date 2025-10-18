# test_admin.py
import os
os.environ['FLASK_APP'] = 'wsgi.py'
os.environ['FLASK_ENV'] = 'development'

from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("Testing database connection...")
    try:
        count = User.query.count()
        print(f"✅ Database OK: {count} users")
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    print("Testing admin setup...")
    try:
        from app.admin import init_admin
        init_admin(app)
        print("✅ Admin setup OK")
    except Exception as e:
        print(f"❌ Admin error: {e}")
        import traceback
        traceback.print_exc()