# check_structure.py
import os

print("📁 App structure:")
for root, dirs, files in os.walk('app'):
    level = root.replace('app', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if file.endswith('.py') and not file.startswith('__'):
            print(f'{subindent}{file}')

print("\n🔍 Checking models...")
try:
    from app.models import BaseModel
    print("✅ BaseModel imported")
except Exception as e:
    print(f"❌ BaseModel import failed: {e}")

try:
    from app.models.user import User
    print("✅ User model imported")
except Exception as e:
    print(f"❌ User import failed: {e}")
