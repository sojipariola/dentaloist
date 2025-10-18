#!/usr/bin/env python3
"""
COMPREHENSIVE RELATIONSHIP CONFLICT DETECTOR
Tests all models for relationship configuration conflicts
"""

import sys
import pathlib
import importlib
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# === Ensure Backend Root is in sys.path ===
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

print("🔍 COMPREHENSIVE RELATIONSHIP CONFLICT DETECTOR")
print("=" * 80)

def test_relationship_configuration():
    """Test that all models can be configured without relationship conflicts"""
    
    print("📦 IMPORTING ALL MODELS AND TESTING RELATIONSHIPS...")
    print("-" * 50)
    
    # Import base first
    try:
        from app.models.base import BaseModel, db
        print("✅ Base models imported")
    except Exception as e:
        print(f"❌ Failed to import base models: {e}")
        return [], [("BASE_IMPORT", str(e))]
    
    # Test individual model imports and relationship configuration
    model_categories = {
        'core': [
            'User', 'Organization', 'Tenant', 'Role', 'Permission',
            'Staff', 'UserSession', 'UserOAuth', 'PasswordHistory',
            'SecurityEvent', 'LoginAttempt', 'TenantInvitation'
        ],
        'clinical': [
            'Patient', 'Appointment', 'Treatment', 'ClinicalNote',
            'Allergy', 'Prescription', 'VitalSign'
        ],
        'analytics': [
            'AnalyticsDashboard', 'AnalyticsWidget', 'Widget',
            'WidgetConfig', 'WidgetTemplate'
        ],
        'system_models': [
            'AuditTrail', 'Notification', 'RateLimiter', 'RateLimit',
            'EmailLog', 'Integration', 'IntegrationLog', 'Webhook',
            'WebhookEvent', 'FileRecord', 'AnalyticsReport', 'KPI',
            'KPIHistory', 'ReportSchedule', 'ReportRun', 'DataExport'
        ],
        'financial': [
            'Invoice', 'Payment', 'InsurancePlan', 'InsuranceClaim',
            'Expense', 'FinancialReport'
        ],
        'inventory': [
            'Product', 'ProductCategory', 'Supplier', 'PurchaseOrder',
            'InventoryItem', 'InventoryTransaction'
        ]
    }
    
    successful_models = []
    failed_models = []
    
    # Test importing each model
    for category, models in model_categories.items():
        print(f"\n📊 Testing {category} models...")
        module_name = f"app.models.{category}"
        
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name} imported successfully")
        except Exception as e:
            print(f"❌ {module_name} import failed: {e}")
            failed_models.extend([(model, category, f"Module import failed: {e}") for model in models])
            continue
        
        for model_name in models:
            try:
                model_class = getattr(module, model_name)
                successful_models.append((model_name, category))
                print(f"  ✅ {model_name} imported")
            except Exception as e:
                error_msg = str(e)
                failed_models.append((model_name, category, error_msg))
                print(f"  ❌ {model_name} import failed: {error_msg}")
                
                # Show specific relationship conflicts
                if 'backref' in error_msg and 'widget_configs' in error_msg:
                    print(f"     🎯 CONFLICT: widget_configs backref")
                elif 'backref' in error_msg and 'notifications' in error_msg:
                    print(f"     🎯 CONFLICT: notifications backref")
                elif 'backref' in error_msg:
                    # Extract backref name from error
                    import re
                    backref_match = re.search(r"backref '([^']*)'", error_msg)
                    if backref_match:
                        print(f"     🎯 CONFLICT: {backref_match.group(1)} backref")
    
    return successful_models, failed_models

def test_table_creation():
    """Test that tables can be created without relationship conflicts"""
    
    print("\n🏗️  TESTING TABLE CREATION...")
    print("-" * 50)
    
    try:
        from app.models.base import BaseModel
        from app import create_app
        
        # Create test app and database
        app = create_app('testing')
        
        with app.app_context():
            # Create in-memory database
            test_engine = create_engine('sqlite:///:memory:')
            
            try:
                # Try to create all tables
                BaseModel.metadata.create_all(test_engine)
                print("✅ All tables created successfully")
                return True, []
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Table creation failed: {error_msg}")
                
                # Analyze the error
                conflicts = []
                if 'backref' in error_msg and 'widget_configs' in error_msg:
                    conflicts.append("widget_configs backref conflict")
                if 'backref' in error_msg and 'notifications' in error_msg:
                    conflicts.append("notifications backref conflict")
                
                return False, conflicts
                
    except Exception as e:
        print(f"❌ Table creation test setup failed: {e}")
        return False, [f"Setup failed: {e}"]

def analyze_relationship_patterns():
    """Analyze relationship patterns in model files to find conflicts"""
    
    print("\n🔍 ANALYZING RELATIONSHIP PATTERNS IN FILES...")
    print("-" * 50)
    
    import os
    import re
    
    models_dir = BACKEND_ROOT / 'app' / 'models'
    conflicts = []
    
    # Track backref usage
    backref_usage = {}
    
    for model_file in ['core.py', 'analytics.py', 'system_models.py', 'clinical.py', 'financial.py', 'inventory.py']:
        file_path = models_dir / model_file
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Find backref patterns
                backref_matches = re.finditer(r"backref\s*=\s*['\"]([^'\"]+)['\"]", content)
                for match in backref_matches:
                    backref_name = match.group(1)
                    if backref_name not in backref_usage:
                        backref_usage[backref_name] = []
                    backref_usage[backref_name].append(str(file_path))
    
    # Check for duplicates
    for backref_name, files in backref_usage.items():
        if len(files) > 1:
            print(f"🔴 DUPLICATE BACKREF: '{backref_name}' in {len(files)} files")
            conflicts.append(f"Duplicate backref: '{backref_name}'")
            for file_path in files:
                print(f"   📍 {file_path}")
    
    # Check specific known conflicts
    analytics_file = models_dir / 'analytics.py'
    if analytics_file.exists():
        with open(analytics_file, 'r') as f:
            content = f.read()
            if "backref='widget_configs'" in content:
                print("📍 WidgetConfig uses backref='widget_configs'")
    
    core_file = models_dir / 'core.py'
    if core_file.exists():
        with open(core_file, 'r') as f:
            content = f.read()
            if "widget_configs = relationship" in content:
                print("📍 User has widget_configs relationship")
    
    system_file = models_dir / 'system_models.py'
    if system_file.exists():
        with open(system_file, 'r') as f:
            content = f.read()
            if "backref='notifications'" in content:
                print("📍 Notification uses backref='notifications'")
    
    return conflicts

def generate_fix_recommendations(failed_models, table_conflicts, pattern_conflicts):
    """Generate specific recommendations for fixing relationship conflicts"""
    
    print("\n🔧 FIX RECOMMENDATIONS")
    print("-" * 50)
    
    all_issues = []
    
    # Collect issues from failed models
    for model_name, category, error in failed_models:
        if 'widget_configs' in error:
            all_issues.append("widget_configs backref conflict")
        elif 'notifications' in error:
            all_issues.append("notifications backref conflict")
    
    # Add table creation conflicts
    all_issues.extend(table_conflicts)
    
    # Add pattern conflicts
    all_issues.extend(pattern_conflicts)
    
    # Remove duplicates
    unique_issues = list(set(all_issues))
    
    if not unique_issues:
        print("✅ No relationship conflicts detected!")
        return
    
    print(f"Found {len(unique_issues)} unique relationship issues:")
    
    for issue in unique_issues:
        print(f"\n🎯 {issue.upper()}")
        
        if 'widget_configs' in issue:
            print("   PROBLEM: Multiple relationships using 'widget_configs' backref")
            print("   SOLUTION:")
            print("   1. In app/models/analytics.py, change:")
            print("        FROM: user = db.relationship('User', backref='widget_configs')")
            print("        TO:   user = db.relationship('User', back_populates='widget_configs')")
            print("   2. In app/models/core.py, ensure User has:")
            print("        widget_configs = relationship('WidgetConfig', back_populates='user')")
            
        elif 'notifications' in issue:
            print("   PROBLEM: Multiple relationships using 'notifications' backref")
            print("   SOLUTION:")
            print("   1. In app/models/system_models.py, change:")
            print("        FROM: user = relationship('User', backref='notifications')")
            print("        TO:   user = relationship('User', back_populates='notifications')")
            print("   2. In app/models/core.py, ensure User has:")
            print("        notifications = relationship('Notification', back_populates='user')")

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE RELATIONSHIP CONFLICT ANALYSIS")
    
    # Test model imports
    successful_models, failed_models = test_relationship_configuration()
    
    # Test table creation
    table_success, table_conflicts = test_table_creation()
    
    # Analyze relationship patterns
    pattern_conflicts = analyze_relationship_patterns()
    
    # Generate comprehensive report
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE RELATIONSHIP CONFLICT REPORT")
    print("=" * 80)
    
    print(f"\n✅ SUCCESSFUL MODEL IMPORTS: {len(successful_models)}")
    print(f"❌ FAILED MODEL IMPORTS: {len(failed_models)}")
    print(f"🏗️  TABLE CREATION: {'SUCCESS' if table_success else 'FAILED'}")
    print(f"🔍 PATTERN CONFLICTS: {len(pattern_conflicts)}")
    
    if failed_models:
        print(f"\n📋 FAILED MODELS:")
        for model_name, category, error in failed_models[:10]:  # Show first 10
            print(f"   - {model_name} ({category}): {error.split(',')[0]}")
        if len(failed_models) > 10:
            print(f"   ... and {len(failed_models) - 10} more")
    
    # Generate fix recommendations
    generate_fix_recommendations(failed_models, table_conflicts, pattern_conflicts)
    
    total_issues = len(failed_models) + len(table_conflicts) + len(pattern_conflicts)
    
    print(f"\n📈 SUMMARY:")
    print(f"   Total issues found: {total_issues}")
    
    if total_issues == 0:
        print("\n🎉 ALL RELATIONSHIPS ARE CONFIGURED CORRECTLY!")
    else:
        print(f"\n🔧 RELATIONSHIP CONFLICTS DETECTED - NEEDS FIXING")