# backend/scripts/find_before_request.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def find_before_request():
    print("🔍 FINDING BEFORE_REQUEST HANDLER")
    print("=" * 50)
    
    # Search for before_request in the codebase
    search_paths = [
        'app/__init__.py',
        'app/admin/',
        'app/routes/',
        'app/auth/'
    ]
    
    for path in search_paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.py'):
                        filepath = os.path.join(root, file)
                        with open(filepath, 'r') as f:
                            content = f.read()
                            if 'before_request' in content:
                                print(f"📁 Found in: {filepath}")
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if 'before_request' in line:
                                        print(f"   Line {i+1}: {line.strip()}")
                                        # Show context
                                        for j in range(max(0, i-3), min(len(lines), i+4)):
                                            prefix = ">>>" if j == i else "   "
                                            print(f"{prefix} {j+1}: {lines[j].strip()}")
                                        print()
        elif os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
                if 'before_request' in content:
                    print(f"📁 Found in: {path}")
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'before_request' in line:
                            print(f"   Line {i+1}: {line.strip()}")
                            # Show context
                            for j in range(max(0, i-3), min(len(lines), i+4)):
                                prefix = ">>>" if j == i else "   "
                                print(f"{prefix} {j+1}: {lines[j].strip()}")
                            print()

if __name__ == '__main__':
    find_before_request()