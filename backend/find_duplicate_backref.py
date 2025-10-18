#!/usr/bin/env python3
"""
Fixed script to find the duplicate widget_configs backref
"""
import os
import sys
import re

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def search_for_widget_configs_backref():
    """Search all Python files for widget_configs backref"""
    
    print("🔍 SEARCHING FOR 'widget_configs' BACKREF IN ALL FILES...")
    print("=" * 80)
    
    matches = []
    
    for root, dirs, files in os.walk(backend_dir):
        # Skip virtual environment and cache directories
        if any(skip in root for skip in ['.venv', '__pycache__', '.git']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Look for backref patterns
                        patterns = [
                            r"backref\s*=\s*[\"']widget_configs[\"']",
                            r"back_populates\s*=\s*[\"']widget_configs[\"']",
                        ]
                        
                        for pattern in patterns:
                            if re.search(pattern, content):
                                matches.append({
                                    'file': file_path,
                                    'pattern': pattern,
                                    'content': content
                                })
                                print(f"📍 FOUND in: {file_path}")
                                
                                # Show the specific lines
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if re.search(pattern, line):
                                        start = max(0, i-2)
                                        end = min(len(lines), i+3)
                                        print(f"   Lines {start+1}-{end}:")
                                        for j in range(start, end):
                                            prefix = ">>> " if j == i else "    "
                                            print(f"{prefix}{lines[j]}")
                                        print()
                                break
                                
                except Exception as e:
                    print(f"❌ Error reading {file_path}: {e}")
    
    return matches

def analyze_widget_config_model():
    """Specifically analyze the WidgetConfig model"""
    
    print("\n" + "=" * 80)
    print("🔧 ANALYZING WIDGETCONFIG MODEL")
    print("=" * 80)
    
    widget_config_path = os.path.join(backend_dir, 'app', 'models', 'analytics.py')
    
    if os.path.exists(widget_config_path):
        print(f"📦 WidgetConfig model found at: {widget_config_path}")
        
        with open(widget_config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find the WidgetConfig class
            class_match = re.search(r'class WidgetConfig.*?(?=class|\Z)', content, re.DOTALL)
            if class_match:
                class_content = class_match.group(0)
                print("📋 WidgetConfig class content:")
                print("-" * 40)
                
                # Find relationships in WidgetConfig
                relationships = re.findall(r'(\w+)\s*=\s*relationship\(.*?\)', class_content, re.DOTALL)
                print(f"Found {len(relationships)} relationships in WidgetConfig:")
                for rel in relationships:
                    print(f"  - {rel}")
                
                # Find the specific user relationship
                user_rel_match = re.search(r'(\w+)\s*=\s*relationship\([^)]*User[^)]*\)', class_content)
                if user_rel_match:
                    print(f"\n🎯 User relationship found: {user_rel_match.group(1)}")
                    
                    # Get the full relationship line
                    lines = class_content.split('\n')
                    for line in lines:
                        if 'relationship' in line and 'User' in line:
                            print(f"   Full line: {line.strip()}")
                            
                            # Check for backref
                            if 'backref' in line and 'widget_configs' in line:
                                print("   🔴 CONTAINS: backref='widget_configs'")
    
    else:
        print(f"❌ WidgetConfig model not found at {widget_config_path}")

def find_all_user_relationships():
    """Find all relationships to User model"""
    
    print("\n" + "=" * 80)
    print("👤 FINDING ALL RELATIONSHIPS TO USER MODEL")
    print("=" * 80)
    
    user_relationships = []
    
    for root, dirs, files in os.walk(backend_dir):
        if any(skip in root for skip in ['.venv', '__pycache__', '.git']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Look for relationships to User
                        pattern = r'(\w+)\s*=\s*relationship\([^)]*User[^)]*\)'
                        matches = re.finditer(pattern, content, re.DOTALL)
                        
                        for match in matches:
                            rel_name = match.group(1)
                            user_relationships.append({
                                'file': file_path,
                                'relationship': rel_name,
                                'line': match.group(0)
                            })
                            
                except Exception as e:
                    continue
    
    print(f"Found {len(user_relationships)} relationships to User model:")
    for rel in user_relationships:
        print(f"  📍 {rel['file']}")
        print(f"     {rel['relationship']}: {rel['line'][:100]}...")
    
    return user_relationships

def check_for_circular_imports():
    """Check for potential circular import issues"""
    
    print("\n" + "=" * 80)
    print("�� CHECKING FOR CIRCULAR IMPORTS")
    print("=" * 80)
    
    # Check if models are imported in multiple places
    import_patterns = [
        r'from\s+app\.models\.analytics\s+import',
        r'from\s+\.analytics\s+import',
        r'import\s+app\.models\.analytics',
    ]
    
    for root, dirs, files in os.walk(backend_dir):
        if any(skip in root for skip in ['.venv', '__pycache__', '.git', 'tests']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        for pattern in import_patterns:
                            if re.search(pattern, content):
                                print(f"📦 {file_path} imports analytics models")
                                break
                                
                except Exception as e:
                    continue

if __name__ == "__main__":
    print("🚀 STARTING DUPLICATE BACKREF INVESTIGATION...")
    
    # Search for the problematic backref
    matches = search_for_widget_configs_backref()
    
    # Analyze the WidgetConfig model specifically
    analyze_widget_config_model()
    
    # Find all relationships to User
    user_rels = find_all_user_relationships()
    
    # Check for circular imports
    check_for_circular_imports()
    
    print("\n" + "=" * 80)
    print("🎯 SUMMARY")
    print("=" * 80)
    
    if matches:
        print(f"❌ FOUND {len(matches)} FILES WITH 'widget_configs' BACKREF")
        print("   This confirms the duplicate backref issue!")
    else:
        print("✅ No files found with explicit 'widget_configs' backref")
        print("   The issue might be due to dynamic relationship creation or circular imports")
