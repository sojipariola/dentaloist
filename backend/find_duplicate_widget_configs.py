#!/usr/bin/env python3
"""
Find the exact locations of the duplicate widget_configs backref
"""
import os
import sys
import re

backend_dir = os.path.dirname(os.path.abspath(__file__))

print("�� FINDING EXACT DUPLICATE LOCATIONS")
print("=" * 80)

# Search for the exact files and lines
duplicate_files = []

for root, dirs, files in os.walk(backend_dir):
    if any(skip in root for skip in ['.venv', '__pycache__', '.git']):
        continue
        
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    for i, line in enumerate(lines, 1):
                        # Look for backref with widget_configs
                        if 'backref' in line and 'widget_configs' in line:
                            duplicate_files.append({
                                'file': file_path,
                                'line_number': i,
                                'line_content': line.strip()
                            })
                            print(f"🔴 DUPLICATE FOUND:")
                            print(f"   File: {file_path}")
                            print(f"   Line: {i}")
                            print(f"   Content: {line.strip()}")
                            
                            # Show context
                            start = max(0, i-3)
                            end = min(len(lines), i+4)
                            print(f"   Context:")
                            for j in range(start, end):
                                prefix = ">>> " if j == i-1 else "    "
                                print(f"{prefix}{j+1}: {lines[j]}")
                            print()
                            
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

print(f"\n📊 TOTAL DUPLICATES FOUND: {len(duplicate_files)}")

if duplicate_files:
    print("\n🔧 FIX INSTRUCTIONS:")
    print("   For each duplicate found above, change one of the backref names to be unique.")
    print("   For example:")
    print("   - Change backref='widget_configs' to backref='widget_config_settings'")
    print("   - Or use back_populates instead of backref")
