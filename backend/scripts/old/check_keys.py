# check_keys.py
import os

print("🔑 Checking environment keys...")

# Check what keys are available
keys_to_check = ['FERNET_KEY', 'ENCRYPTION_KEY']
for key in keys_to_check:
    value = os.environ.get(key)
    if value:
        print(f"✅ {key}: {value[:20]}... (length: {len(value)})")
    else:
        print(f"❌ {key}: NOT SET")

# Check the .env file
print("\n📄 .env file contents:")
with open('.env', 'r') as f:
    for line in f:
        if any(key in line for key in keys_to_check):
            print(f"  {line.strip()}")
