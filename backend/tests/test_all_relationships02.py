#!/usr/bin/env python3
"""
Show exact duplicate backref locations in system_models.py
"""
import re

with open('app/models/system_models.py', 'r') as f:
    content = f.read()
    lines = content.split('\n')
    
    backrefs = {}
    
    for i, line in enumerate(lines, 1):
        if 'backref=' in line:
            match = re.search(r"backref\s*=\s*['\"]([^'\"]+)['\"]", line)
            if match:
                backref_name = match.group(1)
                if backref_name not in backrefs:
                    backrefs[backref_name] = []
                backrefs[backref_name].append((i, line.strip()))
    
    print("📋 DUPLICATE BACKREFS IN SYSTEM_MODELS.PY:")
    for backref_name, occurrences in backrefs.items():
        if len(occurrences) > 1:
            print(f"\n🔴 '{backref_name}' used {len(occurrences)} times:")
            for line_num, line_content in occurrences:
                print(f"   Line {line_num}: {line_content}")