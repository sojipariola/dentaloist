#!/usr/bin/env python3
"""
Discover the actual table structure in the database
"""

import sqlite3
import os

def discover_database():
    """Discover all tables and their structure"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return
    
    print("🔍 DISCOVERING DATABASE STRUCTURE")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"📊 Found {len(tables)} tables:")
    for table in tables:
        table_name = table[0]
        print(f"\n🏷️  Table: {table_name}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"   Columns:")
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            print(f"     - {col_name} ({col_type}) {'PK' if pk else ''} {'NOT NULL' if not_null else ''}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"   📈 Row count: {count}")
        
        # Show sample data for key tables
        if table_name in ['organization', 'user', 'patient'] and count > 0:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            sample_rows = cursor.fetchall()
            print(f"   Sample data:")
            for i, row in enumerate(sample_rows):
                print(f"     Row {i+1}: {row}")
    
    conn.close()

def find_organization_tables():
    """Find tables related to organizations and tenancy"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        return
    
    print(f"\n🏢 FINDING ORGANIZATION-RELATED TABLES")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = [table[0] for table in cursor.fetchall()]
    
    # Look for organization table
    org_tables = [t for t in all_tables if 'org' in t.lower() or 'tenant' in t.lower()]
    print(f"Organization tables: {org_tables}")
    
    # Look for tables with organization_id columns
    tables_with_org_id = []
    for table in all_tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        if any('org' in col.lower() for col in columns):
            tables_with_org_id.append(table)
            print(f"📋 Table '{table}' has organization-related columns: {columns}")
    
    conn.close()

def check_actual_data_distribution():
    """Check the actual data distribution based on discovered tables"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        return
    
    print(f"\n📊 CHECKING ACTUAL DATA DISTRIBUTION")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Find the main organization table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%org%'")
    org_table_result = cursor.fetchone()
    
    if org_table_result:
        org_table = org_table_result[0]
        print(f"🏢 Using organization table: {org_table}")
        
        # Get organizations
        cursor.execute(f"SELECT * FROM {org_table} LIMIT 5")
        organizations = cursor.fetchall()
        
        print(f"Sample organizations:")
        for org in organizations:
            print(f"  {org}")
    
    # Find tables that might have tenant data
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    all_tables = [table[0] for table in cursor.fetchall()]
    
    # Check a few key tables
    key_tables = [t for t in all_tables if any(keyword in t.lower() for keyword in ['patient', 'user', 'appoint', 'invoice'])]
    
    for table in key_tables[:5]:  # Check first 5 key tables
        print(f"\n📋 Table: {table}")
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"  Columns: {columns}")
        
        # Check if there's an organization_id column
        org_columns = [col for col in columns if 'org' in col.lower()]
        if org_columns:
            org_col = org_columns[0]
            print(f"  Organization column: {org_col}")
            
            # Check distribution
            cursor.execute(f"SELECT {org_col}, COUNT(*) as count FROM {table} GROUP BY {org_col}")
            distribution = cursor.fetchall()
            
            for row in distribution:
                org_id = row[0] if row[0] is not None else 'NULL'
                count = row[1]
                print(f"    {org_id}: {count} records")
    
    conn.close()

if __name__ == '__main__':
    discover_database()
    find_organization_tables()
    check_actual_data_distribution()
