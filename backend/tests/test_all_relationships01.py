#!/usr/bin/env python3
"""
COMPREHENSIVE RELATIONSHIP ERROR DETECTOR - FIXED VERSION
Tests all models for relationship configuration errors
"""

import sys
import os
import traceback
import re

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

print("🔍 COMPREHENSIVE RELATIONSHIP ERROR DETECTOR")
print("=" * 80)

def test_model_imports():
    """Test importing all models and identify specific errors"""
    
    errors = []
    successful_imports = []
    failed_imports = []
    
    print("📦 TESTING MODEL IMPORTS...")
    print("-" * 40)
    
    # Test core models
    core_models = [
        'User', 'Organization', 'Tenant', 'Role', 'Permission',
        'Staff', 'UserSession', 'UserOAuth', 'PasswordHistory',
        'SecurityEvent', 'LoginAttempt', 'TenantInvitation'
    ]
    
    for model_name in core_models:
        try:
            module = __import__('app.models.core', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'core'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'core', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
            
            # Show detailed error for specific known issues
            if 'widget_configs' in error_msg:
                print(f"   🎯 RELATED TO: widget_configs backref conflict")
            elif 'notifications' in error_msg:
                print(f"   🎯 RELATED TO: notifications backref conflict")
    
    # Test clinical models
    clinical_models = [
        'Patient', 'Appointment', 'Treatment', 'ClinicalNote',
        'Allergy', 'Prescription', 'VitalSign'
    ]
    
    for model_name in clinical_models:
        try:
            module = __import__('app.models.clinical', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'clinical'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'clinical', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
    
    # Test analytics models
    analytics_models = [
        'AnalyticsDashboard', 'AnalyticsWidget', 'Widget',
        'WidgetConfig', 'WidgetTemplate'
    ]
    
    for model_name in analytics_models:
        try:
            module = __import__('app.models.analytics', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'analytics'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'analytics', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
    
    # Test system models
    system_models = [
        'AuditTrail', 'Notification', 'RateLimiter', 'RateLimit',
        'EmailLog', 'Integration', 'IntegrationLog', 'Webhook',
        'WebhookEvent', 'FileRecord', 'AnalyticsReport', 'KPI',
        'KPIHistory', 'ReportSchedule', 'ReportRun', 'DataExport'
    ]
    
    for model_name in system_models:
        try:
            module = __import__('app.models.system_models', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'system'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'system', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
    
    # Test financial models
    financial_models = [
        'Invoice', 'Payment', 'InsurancePlan', 'InsuranceClaim',
        'Expense', 'FinancialReport'
    ]
    
    for model_name in financial_models:
        try:
            module = __import__('app.models.financial', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'financial'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'financial', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
    
    # Test inventory models
    inventory_models = [
        'Product', 'ProductCategory', 'Supplier', 'PurchaseOrder',
        'InventoryItem', 'InventoryTransaction'
    ]
    
    for model_name in inventory_models:
        try:
            module = __import__('app.models.inventory', fromlist=[model_name])
            model_class = getattr(module, model_name)
            successful_imports.append((model_name, 'inventory'))
            print(f"✅ {model_name} imported successfully")
        except Exception as e:
            error_msg = str(e)
            failed_imports.append((model_name, 'inventory', error_msg))
            print(f"❌ {model_name} import failed: {error_msg}")
    
    return successful_imports, failed_imports

def analyze_relationship_patterns():
    """Analyze relationship patterns in model files"""
    
    print("\n🔗 ANALYZING RELATIONSHIP PATTERNS...")
    print("-" * 40)
    
    relationship_issues = []
    backref_patterns = {}
    
    models_dir = os.path.join(backend_dir, 'app', 'models')
    
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Find backref patterns
                        backref_matches = re.finditer(r"backref\s*=\s*['\"]([^'\"]+)['\"]", content)
                        
                        for match in backref_matches:
                            backref_name = match.group(1)
                            if backref_name not in backref_patterns:
                                backref_patterns[backref_name] = []
                            backref_patterns[backref_name].append({
                                'file': file_path,
                                'line': match.group(0)
                            })
                            
                        # Find back_populates patterns
                        back_populates_matches = re.finditer(r"back_populates\s*=\s*['\"]([^'\"]+)['\"]", content)
                        
                        for match in back_populates_matches:
                            back_populates_name = match.group(1)
                            if back_populates_name not in backref_patterns:
                                backref_patterns[back_populates_name] = []
                            backref_patterns[back_populates_name].append({
                                'file': file_path,
                                'line': match.group(0),
                                'type': 'back_populates'
                            })
                            
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    # Analyze for duplicates
    print("\n📊 BACKREF/BACK_POPULATES ANALYSIS:")
    for backref_name, occurrences in backref_patterns.items():
        if len(occurrences) > 1:
            print(f"🔴 DUPLICATE: '{backref_name}' used {len(occurrences)} times")
            for occ in occurrences:
                print(f"   📍 {occ['file']}")
                if 'type' in occ:
                    print(f"      {occ['line']} (back_populates)")
                else:
                    print(f"      {occ['line']}")
            relationship_issues.append(f"Duplicate: '{backref_name}'")
        else:
            print(f"✅ UNIQUE: '{backref_name}'")
    
    return relationship_issues, backref_patterns

def check_specific_relationship_conflicts():
    """Check for specific known relationship conflicts"""
    
    print("\n🎯 CHECKING SPECIFIC RELATIONSHIP CONFLICTS...")
    print("-" * 40)
    
    conflicts = []
    
    # Check for widget_configs conflicts
    analytics_file = os.path.join(backend_dir, 'app', 'models', 'analytics.py')
    core_file = os.path.join(backend_dir, 'app', 'models', 'core.py')
    
    if os.path.exists(analytics_file):
        with open(analytics_file, 'r') as f:
            content = f.read()
            widget_configs_count = content.count("backref='widget_configs'")
            if widget_configs_count > 0:
                print(f"📍 WidgetConfig backref found in analytics.py")
                conflicts.append("WidgetConfig backref in analytics.py")
    
    if os.path.exists(core_file):
        with open(core_file, 'r') as f:
            content = f.read()
            if 'widget_configs = relationship' in content:
                print(f"📍 User widget_configs relationship found in core.py")
                conflicts.append("User widget_configs relationship in core.py")
    
    # Check for notifications conflicts
    system_models_file = os.path.join(backend_dir, 'app', 'models', 'system_models.py')
    
    if os.path.exists(system_models_file):
        with open(system_models_file, 'r') as f:
            content = f.read()
            notifications_count = content.count("backref='notifications'")
            if notifications_count > 0:
                print(f"📍 Notification backref found in system_models.py")
                conflicts.append("Notification backref in system_models.py")
    
    return conflicts

def generate_detailed_error_analysis(failed_imports):
    """Generate detailed analysis of import errors"""
    
    print("\n🔍 DETAILED ERROR ANALYSIS...")
    print("-" * 40)
    
    analysis = []
    
    for model_name, category, error_msg in failed_imports:
        print(f"\n📋 {model_name} ({category}):")
        print(f"   Error: {error_msg}")
        
        # Analyze common patterns
        if 'backref' in error_msg and 'widget_configs' in error_msg:
            print("   🎯 ISSUE: widget_configs backref conflict")
            print("   💡 SOLUTION: Check User and WidgetConfig relationships")
            analysis.append(f"{model_name}: widget_configs backref conflict")
            
        elif 'backref' in error_msg and 'notifications' in error_msg:
            print("   🎯 ISSUE: notifications backref conflict") 
            print("   💡 SOLUTION: Check User and Notification relationships")
            analysis.append(f"{model_name}: notifications backref conflict")
            
        elif 'backref' in error_msg:
            # Extract the backref name from error
            backref_match = re.search(r"backref '([^']*)'", error_msg)
            if backref_match:
                backref_name = backref_match.group(1)
                print(f"   🎯 ISSUE: {backref_name} backref conflict")
                print(f"   💡 SOLUTION: Check relationships using backref '{backref_name}'")
                analysis.append(f"{model_name}: {backref_name} backref conflict")
                
        elif 'Mapper' in error_msg and 'failed to initialize' in error_msg:
            print("   🎯 ISSUE: Mapper initialization failed due to relationship conflict")
            print("   💡 SOLUTION: Check for duplicate backref or back_populates names")
            analysis.append(f"{model_name}: Mapper initialization failed")
            
        else:
            print("   🎯 ISSUE: Unknown relationship error")
            analysis.append(f"{model_name}: Unknown error")
    
    return analysis

if __name__ == "__main__":
    print("🚀 STARTING COMPREHENSIVE RELATIONSHIP ANALYSIS")
    print("=" * 80)
    
    # Test model imports
    successful_imports, failed_imports = test_model_imports()
    
    # Analyze relationship patterns
    relationship_issues, backref_patterns = analyze_relationship_patterns()
    
    # Check specific conflicts
    specific_conflicts = check_specific_relationship_conflicts()
    
    # Generate detailed error analysis
    error_analysis = generate_detailed_error_analysis(failed_imports)
    
    # Generate comprehensive report
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE RELATIONSHIP ANALYSIS REPORT")
    print("=" * 80)
    
    print(f"\n✅ SUCCESSFUL IMPORTS: {len(successful_imports)}")
    for model_name, category in successful_imports[:10]:  # Show first 10
        print(f"   - {model_name} ({category})")
    if len(successful_imports) > 10:
        print(f"   ... and {len(successful_imports) - 10} more")
    
    print(f"\n❌ FAILED IMPORTS: {len(failed_imports)}")
    for model_name, category, error in failed_imports:
        print(f"   - {model_name} ({category}): {error.split(',')[0]}")
    
    print(f"\n🔗 RELATIONSHIP PATTERN ISSUES: {len(relationship_issues)}")
    for issue in relationship_issues:
        print(f"   - {issue}")
    
    print(f"\n🎯 SPECIFIC CONFLICTS: {len(specific_conflicts)}")
    for conflict in specific_conflicts:
        print(f"   - {conflict}")
    
    print(f"\n🔍 ERROR ANALYSIS: {len(error_analysis)}")
    for analysis in error_analysis:
        print(f"   - {analysis}")
    
    # Summary and recommendations
    total_issues = len(failed_imports) + len(relationship_issues) + len(specific_conflicts)
    
    print(f"\n📈 SUMMARY:")
    print(f"   Total models: {len(successful_imports) + len(failed_imports)}")
    print(f"   Successful: {len(successful_imports)}")
    print(f"   Failed: {len(failed_imports)}")
    print(f"   Total issues: {total_issues}")
    
    if total_issues == 0:
        print("\n🎉 ALL RELATIONSHIPS ARE CONFIGURED CORRECTLY!")
    else:
        print(f"\n🔧 RELATIONSHIP ISSUES DETECTED - NEEDS FIXING")
        print("\n💡 RECOMMENDED ACTIONS:")
        
        if any('widget_configs' in str(item) for item in failed_imports + relationship_issues + specific_conflicts):
            print("   1. Fix widget_configs backref conflict")
            print("      - Check User model in core.py")
            print("      - Check WidgetConfig model in analytics.py")
            
        if any('notifications' in str(item) for item in failed_imports + relationship_issues + specific_conflicts):
            print("   2. Fix notifications backref conflict")
            print("      - Check User model in core.py") 
            print("      - Check Notification model in system_models.py")
            
        if relationship_issues:
            print("   3. Fix duplicate backref names:")
            for issue in relationship_issues:
                if 'Duplicate' in issue:
                    backref_name = issue.split("'")[1]
                    print(f"      - {backref_name}")