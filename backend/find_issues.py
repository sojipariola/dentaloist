#!/usr/bin/env python3
"""
Find ALL relationship conflicts with widget_configs
"""
import os
import sys
import re

backend_dir = os.path.dirname(os.path.abspath(__file__))

print("🎯 COMPREHENSIVE SEARCH FOR WIDGETCONFIG RELATIONSHIP CONFLICTS")
print("=" * 80)

def search_all_relationship_patterns():
    """Search for all possible relationship patterns"""
    
    patterns_to_search = [
        r"backref\s*=\s*[\"']widget_configs[\"']",
        r"back_populates\s*=\s*[\"']widget_configs[\"']",
        r"relationship.*widget_configs",
        r"widget_configs.*relationship",
    ]
    
    all_matches = []
    
    for root, dirs, files in os.walk(backend_dir):
        if any(skip in root for skip in ['.venv', '__pycache__', '.git', 'scripts']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        lines = content.split('\n')
                        
                        for pattern in patterns_to_search:
                            for i, line in enumerate(lines, 1):
                                if re.search(pattern, line, re.IGNORECASE):
                                    all_matches.append({
                                        'file': file_path,
                                        'line_number': i,
                                        'line_content': line.strip(),
                                        'pattern': pattern
                                    })
                                    
                except Exception as e:
                    continue
    
    return all_matches

def check_analytics_file_specifically():
    """Check the analytics.py file specifically for the exact issue"""
    
    analytics_file = os.path.join(backend_dir, 'app', 'models', 'analytics.py')
    print(f"\n🔍 SPECIFICALLY CHECKING: {analytics_file}")
    
    if os.path.exists(analytics_file):
        with open(analytics_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Find WidgetConfig class specifically
            widget_config_match = re.search(r'class WidgetConfig.*?(?=class|\Z)', content, re.DOTALL)
            if widget_config_match:
                widget_config_content = widget_config_match.group(0)
                print("📋 WidgetConfig class found. Checking relationships...")
                
                # Find all relationships in WidgetConfig
                relationships = re.findall(r'(\w+)\s*=\s*db\.relationship\([^)]*\)', widget_config_content)
                print(f"Found {len(relationships)} relationships in WidgetConfig:")
                
                for rel in relationships:
                    print(f"  - {rel}")
                    
                # Check for user relationship specifically
                user_rel_match = re.search(r'user\s*=\s*db\.relationship\([^)]*\)', widget_config_content)
                if user_rel_match:
                    print(f"\n🎯 User relationship found:")
                    print(f"   {user_rel_match.group(0)}")
                    
                    # Check what backref it's using
                    if 'backref' in user_rel_match.group(0):
                        backref_match = re.search(r"backref\s*=\s*['\"]([^'\"]*)['\"]", user_rel_match.group(0))
                        if backref_match:
                            print(f"   🔍 Using backref: '{backref_match.group(1)}'")
    
    return analytics_file

def check_for_multiple_widgetconfig_classes():
    """Check if there are multiple WidgetConfig classes defined"""
    
    print(f"\n🔍 CHECKING FOR MULTIPLE WIDGETCONFIG CLASSES")
    
    widgetconfig_locations = []
    
    for root, dirs, files in os.walk(backend_dir):
        if any(skip in root for skip in ['.venv', '__pycache__', '.git']):
            continue
            
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'class WidgetConfig' in content:
                            widgetconfig_locations.append(file_path)
                            print(f"📍 WidgetConfig class found in: {file_path}")
                            
                except Exception as e:
                    continue
    
    return widgetconfig_locations

def check_circular_imports_in_init():
    """Check __init__.py files for circular imports"""
    
    print(f"\n🔍 CHECKING FOR CIRCULAR IMPORTS IN __INIT__.PY FILES")
    
    init_files = []
    
    for root, dirs, files in os.walk(os.path.join(backend_dir, 'app', 'models')):
        for file in files:
            if file == '__init__.py':
                init_file = os.path.join(root, file)
                init_files.append(init_file)
                
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'WidgetConfig' in content:
                        print(f"📍 WidgetConfig imported in: {init_file}")
                        # Show import lines
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'WidgetConfig' in line:
                                print(f"   Line {i}: {line.strip()}")

if __name__ == "__main__":
    # Search for all relationship patterns
    all_matches = search_all_relationship_patterns()
    
    print(f"📊 FOUND {len(all_matches)} MATCHES:")
    for match in all_matches:
        print(f"📍 {match['file']}:{match['line_number']}")
        print(f"   {match['line_content']}")
        print()
    
    # Check analytics file specifically
    analytics_file = check_analytics_file_specifically()
    
    # Check for multiple WidgetConfig classes
    widgetconfig_locations = check_for_multiple_widgetconfig_classes()
    
    # Check for circular imports
    check_circular_imports_in_init()
    
    print("\n" + "=" * 80)
    print("🎯 SUMMARY")
    print("=" * 80)
    print(f"Total matches: {len(all_matches)}")
    print(f"WidgetConfig locations: {len(widgetconfig_locations)}")
    
    if len(widgetconfig_locations) > 1:
        print("❌ MULTIPLE WIDGETCONFIG CLASSES FOUND - This is the problem!")
