# check_schema.py
#!/usr/bin/env python3
import sys
import os

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db

def check_schema():
    """Check database schema and tables"""
    app = create_app()
    with app.app_context():
        print("🔍 Checking database schema...")
        
        # Get all tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"✅ Found {len(tables)} tables:")
        for table in sorted(tables):
            columns = inspector.get_columns(table)
            print(f"   📊 {table}: {len(columns)} columns")
            
        # Check if users table exists and has admin users
        if 'users' in tables:
            try:
                from app.models import User
                admin_count = User.query.filter_by(is_admin=True).count()
                print(f"   👑 Admin users: {admin_count}")
                
                # List all users
                users = User.query.all()
                print(f"   👥 Total users: {len(users)}")
                for user in users:
                    print(f"      - {user.email} (Admin: {getattr(user, 'is_admin', False)})")
            except Exception as e:
                print(f"   ❌ Error querying users: {e}")

if __name__ == '__main__':
    check_schema()