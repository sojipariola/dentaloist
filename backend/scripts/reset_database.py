#!/usr/bin/env python3
"""
COMPLETE DATABASE RESET for development
WARNING: This will delete all data!
"""

import os
import sys
import sqlite3
from pathlib import Path

def reset_database():
    """Completely reset the database"""
    db_path = 'instance/dentaloist.db'
    
    print("🚨 DATABASE RESET - DEVELOPMENT")
    print("=" * 50)
    print("⚠️  WARNING: This will DELETE ALL DATA!")
    print("=" * 50)
    
    # Confirm reset
    response = input("❓ Are you sure you want to reset the database? (yes/NO): ")
    if response.lower() != 'yes':
        print("❌ Reset cancelled.")
        return
    
    # Close any existing connections
    print("🔒 Closing database connections...")
    
    # Delete database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Deleted database: {db_path}")
    else:
        print(f"ℹ️  Database file not found: {db_path}")
    
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    print("✅ Created instance directory")
    
    # Recreate database with migrations
    print("🔄 Recreating database...")
    os.system('flask db upgrade')
    
    print("🎉 Database reset complete!")
    print("💡 Now run: python scripts/seed_tenants.py")

if __name__ == '__main__':
    reset_database()