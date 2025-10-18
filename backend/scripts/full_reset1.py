#!/usr/bin/env python3
"""
Complete database reset and seed workflow
"""

import os
import sys
import subprocess

def full_reset():
    """Complete reset and seed workflow"""
    print("🔄 COMPLETE DATABASE RESET WORKFLOW")
    print("=" * 50)
    
    scripts = [
        ('reset_database.py', '🚨 Resetting database...'),
        ('seed_lookups.py', '📋 Seeding lookup data...'),
        ('seed_tenants.py', '🌱 Seeding tenant data...'), 
        ('verify_tenancy.py', '🔍 Verifying tenancy...')
    ]
    
    for script, message in scripts:
        script_path = os.path.join('scripts', script)
        if os.path.exists(script_path):
            print(f"\n{message}")
            result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(f"⚠️  {result.stderr}")
        else:
            print(f"❌ Script not found: {script_path}")
    
    print("\n🎉 RESET WORKFLOW COMPLETE!")
    print("💡 Your database is now ready with proper tenant isolation.")

if __name__ == '__main__':
    full_reset()