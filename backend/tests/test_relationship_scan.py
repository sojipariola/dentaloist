# tests/test_relationship_scan.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

def scan_all_relationships():
    """Quick scan to identify relationship errors without running operations"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    all_errors = []
    
    with app.app_context():
        print("🔍 QUICK RELATIONSHIP SCAN")
        print("=" * 50)
        
        # Test if models can be loaded without errors
        model_categories = {
            'Core Models': ['User', 'Organization', 'Role', 'Permission', 'Tenant', 'Staff'],
            'Clinical Models': ['Patient', 'Appointment', 'Treatment', 'ClinicalNote', 'Allergy'],
            'Analytics Models': ['AnalyticsDashboard', 'AnalyticsWidget', 'WidgetType', 'Widget', 'WidgetConfig', 'WidgetTemplate'],
            'System Models': ['RateLimiter', 'RateLimit', 'EmailLog', 'Integration', 'Webhook', 'FileRecord']
        }
        
        for category, models in model_categories.items():
            print(f"\n📁 {category}:")
            for model_name in models:
                try:
                    module = __import__('app.models', fromlist=[model_name])
                    model_class = getattr(module, model_name)
                    # Just try to access the class - if this fails, there's a relationship issue
                    _ = model_class.__name__
                    print(f"  ✅ {model_name}")
                except Exception as e:
                    error_msg = f"{model_name}: {str(e)}"
                    all_errors.append(error_msg)
                    print(f"  ❌ {error_msg}")
        
        # Try table creation as final test
        print(f"\n📊 Final table creation test:")
        try:
            db.create_all()
            print("  ✅ All tables can be created")
        except Exception as e:
            error_msg = f"Table creation failed: {str(e)}"
            all_errors.append(error_msg)
            print(f"  ❌ {error_msg}")
        
        return all_errors

def analyze_errors(errors):
    """Analyze errors and provide specific fixes"""
    print("\n🔧 ERROR ANALYSIS")
    print("=" * 50)
    
    if not errors:
        print("🎉 No relationship errors found!")
        return
    
    error_types = {}
    
    for error in errors:
        if "backref" in error and "exists" in error:
            error_types.setdefault("duplicate_backref", []).append(error)
        elif "has no property" in error:
            error_types.setdefault("missing_property", []).append(error)
        elif "no foreign keys" in error:
            error_types.setdefault("missing_foreign_key", []).append(error)
        elif "Table creation failed" in error:
            error_types.setdefault("table_creation", []).append(error)
        else:
            error_types.setdefault("other", []).append(error)
    
    # Provide specific fixes for each error type
    for error_type, type_errors in error_types.items():
        print(f"\n📋 {error_type.upper().replace('_', ' ')} ERRORS ({len(type_errors)}):")
        for error in type_errors:
            print(f"  • {error}")
            
            # Provide specific fix suggestions
            if error_type == "duplicate_backref":
                print("    💡 FIX: Change the backref name to something unique")
            elif error_type == "missing_property":
                model = error.split("'")[1] if "'" in error else "unknown"
                prop = error.split("'")[3] if "'" in error else "unknown"
                print(f"    💡 FIX: Add '{prop}' relationship to {model} model")
            elif error_type == "missing_foreign_key":
                print("    💡 FIX: Add proper foreign key columns")
            elif error_type == "table_creation":
                print("    💡 FIX: Check all model relationships and foreign keys")

if __name__ == '__main__':
    print("🚀 Starting quick relationship scan...")
    errors = scan_all_relationships()
    
    if errors:
        analyze_errors(errors)
        print(f"\n📝 Total errors found: {len(errors)}")
        print("💡 Run the comprehensive test for more detailed analysis.")
        sys.exit(1)
    else:
        print(f"\n🎉 No relationship errors detected!")
        sys.exit(0)
