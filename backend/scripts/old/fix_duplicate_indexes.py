#!/usr/bin/env python3
import re

def fix_analytics_file():
    """Fix duplicate index in analytics.py"""
    file_path = "app/models/analytics.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace the duplicate index name
    new_content = re.sub(
        r"db\.Index\('idx_report_org_type', 'organization_id', 'report_type'\)",
        "db.Index('idx_analytics_report_org_type', 'organization_id', 'report_type')",
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Fixed analytics.py: idx_report_org_type → idx_analytics_report_org_type")

def fix_financial_file():
    """Fix duplicate index in financial.py"""
    file_path = "app/models/financial.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace the duplicate index name
    new_content = re.sub(
        r"db\.Index\('idx_report_org_type', 'organization_id', 'report_type'\)",
        "db.Index('idx_financial_report_org_type', 'organization_id', 'report_type')",
        content
    )
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"✅ Fixed financial.py: idx_report_org_type → idx_financial_report_org_type")

if __name__ == "__main__":
    print("🔧 Fixing duplicate index names...")
    fix_analytics_file()
    fix_financial_file()
    print("🎉 Duplicate indexes fixed!")
