import os
import sys
sys.path.insert(0, '.')

from app import create_app
from app.models import User, UserRole

app = create_app()
with app.app_context():
    print("🔍 Checking User-Role Relationships...")
    print("=" * 50)
    
    # Check User model relationships
    print("👤 User model relationships:")
    for rel_name in dir(User):
        if not rel_name.startswith('_'):
            attr = getattr(User, rel_name)
            if hasattr(attr, 'property') and hasattr(attr.property, 'direction'):
                print(f"   • {rel_name}: {attr.property}")
    
    print("\n👑 UserRole model relationships:")
    for rel_name in dir(UserRole):
        if not rel_name.startswith('_'):
            attr = getattr(UserRole, rel_name)
            if hasattr(attr, 'property') and hasattr(attr.property, 'direction'):
                print(f"   • {rel_name}: {attr.property}")
    
    # Check if we can query roles
    roles = UserRole.query.all()
    print(f"\n📋 Available roles: {len(roles)}")
    for role in roles:
        print(f"   • {role.name} (Code: {role.code})")
