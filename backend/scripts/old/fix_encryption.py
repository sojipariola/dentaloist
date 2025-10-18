# fix_encryption.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def fix_encryption_config():
    print("🔧 Fixing encryption configuration...")
    
    # Read the encryption.py file
    with open('app/utils/encryption.py', 'r') as f:
        content = f.read()
    
    # Check what key it's using
    if 'encryption_key = app.config.get("ENCRYPTION_KEY")' in content:
        print("❌ Found issue: Using ENCRYPTION_KEY instead of FERNET_KEY")
        
        # Replace ENCRYPTION_KEY with FERNET_KEY
        content = content.replace(
            'encryption_key = app.config.get("ENCRYPTION_KEY")',
            'encryption_key = app.config.get("FERNET_KEY")'
        )
        
        # Write the fixed content
        with open('app/utils/encryption.py', 'w') as f:
            f.write(content)
        
        print("✅ Fixed: Now using FERNET_KEY instead of ENCRYPTION_KEY")
    else:
        print("✅ Encryption configuration looks correct")
    
    return True

if __name__ == "__main__":
    fix_encryption_config()
