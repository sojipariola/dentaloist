#!/usr/bin/env python3
"""
Quick status check
"""

import sqlite3
from pathlib import Path

def quick_status():
    """Quick status check"""
    db_path = Path('instance/dentaloist.db')
    
    if not db_path.exists():
        print("❌ Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 QUICK STATUS CHECK")
    print("=" * 30)
    
    tables = ['organizations', 'users', 'patients', 'appointments', 'invoices']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"📊 {table}: {count} records")
    
    conn.close()
    
    print(f"\n💡 If you see data above, your seeding was successful!")

if __name__ == '__main__':
    quick_status()
    