#!/usr/bin/env python3
"""
Diagnostic script to find duplicate relationship backrefs
"""
import sys
import os
import inspect
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import relationship

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

def find_all_relationships():
    """Find all relationships in all models"""
    print("🔍 SEARCHING FOR ALL RELATIONSHIPS IN MODELS...")
    
    # Track all relationships by backref
    backrefs = {}
    relationships_found = []
    
    # Import all model modules
    model_modules = []
    for root, dirs, files in os.walk(backend_dir):
        for file in files:
            if file.endswith('.py') and 'model' in file.lower():
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, backend_dir)
                module_path = rel_path.replace('/', '.').replace('\\', '.').replace('.py', '')
                if module_path not in model_modules:
                    model_modules.append(module_path)
    
    print(f"📦 Found {len(model_modules)} potential model files")
    
    # Import and inspect each module
    for module_path in model_modules:
        try:
            module = __import__(module_path, fromlist=['*'])
            print(f"\n🔎 Inspecting module: {module_path}")
            
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, '__table__'):
                    print(f"  📊 Class: {name}")
                    
                    # Check class attributes for relationships
                    for attr_name, attr_value in obj.__dict__.items():
                        if isinstance(attr_value, relationship):
                            rel_info = {
                                'class': name,
                                'module': module_path,
                                'attribute': attr_name,
                                'relationship': attr_value,
                                'backref': getattr(attr_value, 'backref', None),
                                'back_populates': getattr(attr_value, 'back_populates', None)
                            }
                            relationships_found.append(rel_info)
                            
                            if rel_info['backref']:
                                backref_name = rel_info['backref']
                                if backref_name not in backrefs:
                                    backrefs[backref_name] = []
                                backrefs[backref_name].append(rel_info)
                                print(f"    🔗 {attr_name} -> backref: '{backref_name}'")
                            elif rel_info['back_populates']:
                                print(f"    🔗 {attr_name} -> back_populates: '{rel_info['back_populates']}'")
                            else:
                                print(f"    🔗 {attr_name} -> no backref")
                                
        except Exception as e:
            print(f"    ❌ Error inspecting {module_path}: {e}")
    
    return backrefs, relationships_found

def analyze_duplicates(backrefs):
    """Analyze duplicate backrefs"""
    print("\n" + "="*80)
    print("📊 DUPLICATE BACKREF ANALYSIS")
    print("="*80)
    
    duplicates_found = False
    
    for backref_name, rels in backrefs.items():
        if len(rels) > 1:
            duplicates_found = True
            print(f"\n🔴 DUPLICATE BACKREF: '{backref_name}'")
            print(f"   Found {len(rels)} relationships using this backref:")
            
            for rel in rels:
                print(f"   - {rel['class']}.{rel['attribute']} (module: {rel['module']})")
    
    if not duplicates_found:
        print("✅ No duplicate backrefs found!")
    
    return duplicates_found

def find_widget_configs_relationships():
    """Specifically look for WidgetConfig relationships"""
    print("\n" + "="*80)
    print("🔧 SPECIFIC WIDGETCONFIG RELATIONSHIP SEARCH")
    print("="*80)
    
    # Search for WidgetConfig class and its relationships
    widget_config_relationships = []
    
    for module_name, module in sys.modules.items():
        if module and hasattr(module, '__dict__'):
            if 'WidgetConfig' in module.__dict__:
                widget_config_class = module.__dict__['WidgetConfig']
                print(f"📦 WidgetConfig found in: {module_name}")
                
                # Check WidgetConfig relationships
                for attr_name, attr_value in widget_config_class.__dict__.items():
                    if isinstance(attr_value, relationship):
                        rel_info = {
                            'class': 'WidgetConfig',
                            'module': module_name,
                            'attribute': attr_name,
                            'relationship': attr_value,
                            'backref': getattr(attr_value, 'backref', None),
                            'back_populates': getattr(attr_value, 'back_populates', None)
                        }
                        widget_config_relationships.append(rel_info)
                        print(f"  🔗 {attr_name}: backref='{rel_info['backref']}', back_populates='{rel_info['back_populates']}'")
    
    return widget_config_relationships

def check_user_model_backrefs():
    """Check what backrefs exist on User model"""
    print("\n" + "="*80)
    print("👤 USER MODEL BACKREF ANALYSIS")
    print("="*80)
    
    user_backrefs = []
    
    for module_name, module in sys.modules.items():
        if module and hasattr(module, '__dict__'):
            if 'User' in module.__dict__:
                user_class = module.__dict__['User']
                print(f"📦 User model found in: {module_name}")
                
                # Get all relationships from User model
                for attr_name, attr_value in user_class.__dict__.items():
                    if isinstance(attr_value, relationship):
                        user_backrefs.append(attr_name)
                        print(f"  🔗 User.{attr_name}")
    
    print(f"\n📋 User model has {len(user_backrefs)} relationships: {user_backrefs}")
    return user_backrefs

if __name__ == "__main__":
    print("🚀 STARTING RELATIONSHIP DIAGNOSIS...")
    
    # First, let's see what's already loaded
    print("📦 Currently loaded modules with 'model' in name:")
    for name in sorted(sys.modules.keys()):
        if 'model' in name.lower() and sys.modules[name] is not None:
            print(f"  - {name}")
    
    # Run diagnostics
    backrefs, all_relationships = find_all_relationships()
    duplicates = analyze_duplicates(backrefs)
    widget_config_rels = find_widget_configs_relationships()
    user_backrefs = check_user_model_backrefs()
    
    print("\n" + "="*80)
    print("🎯 SUMMARY")
    print("="*80)
    print(f"Total relationships found: {len(all_relationships)}")
    print(f"Duplicate backrefs: {duplicates}")
    print(f"WidgetConfig relationships: {len(widget_config_rels)}")
    print(f"User model relationships: {len(user_backrefs)}")
    
    if duplicates:
        print("\n❌ FOUND DUPLICATE BACKREFS - This is causing your error!")
        print("   The fix is to rename one of the duplicate backrefs to be unique.")
