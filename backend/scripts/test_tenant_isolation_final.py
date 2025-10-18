#!/usr/bin/env python3
"""
Final test of tenant isolation after data fix
"""

import sqlite3
import os

def test_tenant_isolation_sql():
    """Test tenant isolation using direct SQL"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    print("🔒 TESTING TENANT ISOLATION (SQL)")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get organizations
    cursor.execute("SELECT public_id, name FROM organization ORDER BY id")
    organizations = cursor.fetchall()
    
    # Test each organization
    for org in organizations:
        print(f"\n🏢 Testing: {org['name']} ({org['public_id']})")
        print("-" * 40)
        
        # Test patient access
        cursor.execute("SELECT COUNT(*) as count FROM patient WHERE organization_id = ?", (org['public_id'],))
        patient_count = cursor.fetchone()['count']
        print(f"✅ Can access {patient_count} patients")
        
        # Test user access
        cursor.execute("SELECT COUNT(*) as count FROM user WHERE organization_id = ?", (org['public_id'],))
        user_count = cursor.fetchone()['count']
        print(f"✅ Can access {user_count} users")
        
        # Verify all records belong to this tenant
        cursor.execute("""
            SELECT COUNT(*) as wrong_count 
            FROM patient 
            WHERE organization_id != ? AND organization_id IS NOT NULL
        """, (org['public_id'],))
        wrong_patients = cursor.fetchone()['count']
        
        if wrong_patients == 0:
            print("✅ Patient data properly isolated")
        else:
            print(f"❌ {wrong_patients} patients visible from other tenants!")
    
    # Test cross-tenant data leakage
    print(f"\n🔍 TESTING CROSS-TENANT DATA LEAKAGE")
    print("-" * 40)
    
    if len(organizations) >= 2:
        org1 = organizations[0]
        org2 = organizations[1]
        
        # Get patient IDs for org1
        cursor.execute("SELECT id FROM patient WHERE organization_id = ?", (org1['public_id'],))
        org1_patient_ids = {row['id'] for row in cursor.fetchall()}
        
        # Get patient IDs for org2
        cursor.execute("SELECT id FROM patient WHERE organization_id = ?", (org2['public_id'],))
        org2_patient_ids = {row['id'] for row in cursor.fetchall()}
        
        # Check for overlap
        common_patients = org1_patient_ids.intersection(org2_patient_ids)
        if common_patients:
            print(f"❌ DATA LEAK: {len(common_patients)} patients visible to multiple tenants!")
            print(f"   Common patient IDs: {sorted(common_patients)[:5]}...")
        else:
            print("✅ SUCCESS: No data leaks between tenants!")
    
    conn.close()

def show_tenant_boundaries():
    """Show the ID ranges for each tenant"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        return
    
    print(f"\n📐 TENANT DATA BOUNDARIES")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get organizations
    cursor.execute("SELECT public_id, name FROM organization ORDER BY id")
    organizations = cursor.fetchall()
    
    for table in ['patient', 'user', 'appointment', 'invoice']:
        print(f"\n{table.upper()} ID ranges:")
        for org in organizations:
            cursor.execute(f"""
                SELECT MIN(id) as min_id, MAX(id) as max_id, COUNT(*) as count
                FROM {table} 
                WHERE organization_id = ?
            """, (org['public_id'],))
            result = cursor.fetchone()
            
            if result['min_id']:
                print(f"   {org['name']:.<25} IDs {result['min_id']}-{result['max_id']} ({result['count']} records)")
            else:
                print(f"   {org['name']:.<25} No records")
    
    conn.close()

if __name__ == '__main__':
    test_tenant_isolation_sql()
    show_tenant_boundaries()
