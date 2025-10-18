# tests/find_ratelimiter_relationship.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def find_ratelimiter_relationship():
    """Find where the rate_limiters relationship is defined"""
    print("🔍 Searching for rate_limiters relationship definition...")
    
    # Search in all model files
    model_files = [
        'app/models/core.py',
        'app/models/analytics.py', 
        'app/models/system_models.py',
        'app/models/__init__.py'
    ]
    
    for file_path in model_files:
        if os.path.exists(file_path):
            print(f"\n📁 Checking {file_path}:")
            with open(file_path, 'r') as f:
                content = f.read()
                if 'rate_limiters' in content:
                    # Find the line with rate_limiters
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'rate_limiters' in line:
                            print(f"  Line {i+1}: {line.strip()}")
    
    print("\n🔍 Also checking for backref definitions...")
    # Check for backrefs that might create this relationship
    for file_path in model_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                if 'backref' in content and 'rate_limiter' in content:
                    print(f"\n📁 Backref found in {file_path}:")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'backref' in line and 'rate_limiter' in line:
                            print(f"  Line {i+1}: {line.strip()}")

if __name__ == '__main__':
    find_ratelimiter_relationship()
