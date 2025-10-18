# find_exact_issue.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.ablename(__file__)))

print("🔎 Finding the exact issue in encryption.py...")

with open('app/utils/encryption.py', 'r') as f:
    content = f.read()

# Find the init_app method
start = content.find('def init_app')
if start != -1:
    # Get the next 50 lines after init_app
    lines = content[start:start+2000].split('\n')
    for i, line in enumerate(lines[:50]):
        print(f"{i+1}: {line}")
        
        # Stop when we find the Fernet line
        if 'Fernet(' in line:
            print(f"\n🚨 Found the problematic line: {line.strip()}")
            break
