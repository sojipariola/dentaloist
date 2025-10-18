# manual_fix.py
import os

def manual_fix():
    print("🛠️ Manually fixing encryption.py...")
    
    with open('app/utils/encryption.py', 'r') as f:
        content = f.read()
    
    # Find and replace the problematic line
    # Look for the line that creates the Fernet instance
    old_pattern = 'self.fernet = Fernet(encryption_key.encode())'
    new_pattern = 'self.fernet = Fernet(fernet_key.encode())'
    
    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print("✅ Fixed Fernet creation line")
    else:
        print("❌ Could not find the exact Fernet creation line")
        # Let's try to find any Fernet line
        if 'Fernet(' in content:
            print("Found Fernet usage but pattern didn't match")
    
    # Also make sure we're getting the right key
    if 'encryption_key = app.config.get("ENCRYPTION_KEY")' in content:
        content = content.replace(
            'encryption_key = app.config.get("ENCRYPTION_KEY")',
            'fernet_key = app.config.get("FERNET_KEY")'
        )
        print("✅ Fixed key assignment")
    
    # Write the fixed content
    with open('app/utils/encryption.py', 'w') as f:
        f.write(content)
    
    print("✅ Manual fix applied")
    return True

if __name__ == "__main__":
    manual_fix()
