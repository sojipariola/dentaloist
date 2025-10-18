# debug_encryption.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Debugging encryption configuration...")

# Check the exact line that's causing the error
with open('app/utils/encryption.py', 'r') as f:
    lines = f.readlines()

print("Lines around the error (lines 40-55):")
for i in range(40-1, min(55, len(lines))):
    print(f"{i+1}: {lines[i].rstrip()}")

print("\nLooking for the encryption_key assignment:")
for i, line in enumerate(lines):
    if 'encryption_key' in line and '=' in line:
        print(f"Line {i+1}: {line.strip()}")
