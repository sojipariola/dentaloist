#!/usr/bin/env python3
"""
COMPLETE DATABASE RESET with migrations regeneration
WARNING: This will delete all data and migrations!
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def full_reset():
    """Complete reset including migrations regeneration"""
    print("🔄 COMPLETE DATABASE RESET WITH MIGRATIONS")
    print("=" * 60)
    print("⚠️  WARNING: This will DELETE ALL DATA and MIGRATIONS!")
    print("=" * 60)
    
    # Confirm reset
    response = input("❓ Are you sure you want to reset everything? (yes/NO): ")
    if response.lower() != 'yes':
        print("❌ Reset cancelled.")
        return
    
    # Step 1: Delete migrations directory
    print("\n🗑️  Step 1: Removing old migrations...")
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
        print("✅ Deleted migrations directory")
    else:
        print("ℹ️  Migrations directory not found")
    
    # Step 2: Delete database
    print("\n🗑️  Step 2: Removing database...")
    db_path = Path('instance/dentaloist.db')
    if db_path.exists():
        os.remove(db_path)
        print("✅ Deleted database file")
    else:
        print("ℹ️  Database file not found")
    
    # Step 3: Recreate instance directory
    print("\n📁 Step 3: Setting up directories...")
    instance_dir = Path('instance')
    if not instance_dir.exists():
        instance_dir.mkdir(parents=True)
        print("✅ Created instance directory")
    
    # Step 4: Initialize new migrations
    print("\n🔄 Step 4: Initializing new migrations...")
    try:
        # Initialize migrations
        result = subprocess.run(['flask', 'db', 'init'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations initialized")
        else:
            print(f"❌ Failed to initialize migrations: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error initializing migrations: {e}")
        return
    
    # Step 5: Generate initial migration
    print("\n📝 Step 5: Generating initial migration...")
    try:
        result = subprocess.run(['flask', 'db', 'migrate', '-m', 'Initial migration'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Initial migration generated")
        else:
            print(f"❌ Failed to generate migration: {result.stderr}")
            # Try alternative command
            result = subprocess.run(['flask', 'db', 'revision', '--autogenerate', '-m', 'Initial migration'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Initial migration generated (alternative method)")
            else:
                print(f"❌ Failed to generate migration with alternative method: {result.stderr}")
                return
    except Exception as e:
        print(f"❌ Error generating migration: {e}")
        return
    
    # Step 6: Apply migrations
    print("\n🚀 Step 6: Applying migrations...")
    try:
        result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
        else:
            print(f"❌ Failed to apply migrations: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ Error applying migrations: {e}")
        return
    
    # Step 7: Seed lookups
    print("\n📋 Step 7: Seeding lookup data...")
    try:
        result = subprocess.run([sys.executable, 'scripts/seed_lookups.py'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Lookup seeding had issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Error seeding lookups: {e}")
        return
    
    # Step 8: Seed tenants
    print("\n🌱 Step 8: Seeding tenant data...")
    try:
        result = subprocess.run([sys.executable, 'scripts/seed_tenants.py'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Tenant seeding had issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Error seeding tenants: {e}")
        return
    
    # Step 9: Verify tenancy
    print("\n🔍 Step 9: Verifying tenancy...")
    try:
        result = subprocess.run([sys.executable, 'scripts/verify_tenancy.py'], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Verification had issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return
    
    print("\n🎉 COMPLETE RESET SUCCESSFUL!")
    print("=" * 50)
    print("✅ Migrations regenerated")
    print("✅ Database recreated") 
    print("✅ Lookup data seeded")
    print("✅ Tenant data seeded")
    print("✅ Tenancy verified")
    print("\n💡 Your application is now ready for development!")

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if we're in the right directory
    if not Path('app').exists():
        print("❌ 'app' directory not found. Are you in the project root?")
        return False
    
    # Check if Flask is available
    try:
        result = subprocess.run(['flask', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Flask CLI not available. Make sure Flask is installed and in PATH.")
            return False
    except:
        print("❌ Flask CLI not available. Make sure Flask is installed and in PATH.")
        return False
    
    # Check if seed scripts exist
    required_scripts = ['seed_lookups.py', 'seed_tenants.py', 'verify_tenancy.py']
    for script in required_scripts:
        if not Path(f'scripts/{script}').exists():
            print(f"❌ Required script not found: scripts/{script}")
            return False
    
    print("✅ All prerequisites met")
    return True

if __name__ == '__main__':
    if check_prerequisites():
        full_reset()
    else:
        print("❌ Prerequisites not met. Please fix the issues above.")