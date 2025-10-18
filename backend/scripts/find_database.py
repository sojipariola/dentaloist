#!/usr/bin/env python3
"""
Find where the database is located
"""

import os
import glob

def find_database():
    """Find the SQLite database file"""
    possible_paths = [
        'instance/dentaloist.db',
        'dentaloist.db', 
        'app/instance/dentaloist.db',
        'backend/instance/dentaloist.db',
        '../instance/dentaloist.db'
    ]
    
    # Also search for any .db files
    db_files = glob.glob('**/*.db', recursive=True)
    possible_paths.extend(db_files)
    
    print("🔍 SEARCHING FOR DATABASE FILES")
    print("=" * 40)
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Found: {path} ({os.path.getsize(path)} bytes)")
            found = True
        else:
            print(f"❌ Not found: {path}")
    
    if not found:
        print("\n💡 Try creating the database first:")
        print("   cd /home/soji/Documents/Projects/Dentaloist/backend")
        print("   flask db upgrade")
    
    return found

if __name__ == '__main__':
    find_database()
