#!/usr/bin/env python3
"""
Verify tenant isolation after seeding
"""

import sqlite3
import os

def verify_tenancy():
    """Verify tenant isolation is working"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found. Run seeding first.")
        return
    
    print("🔍 VERIFYING TENANT ISOLATION")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check organization distribution
    cursor.execute("""
        SELECT o.public_id, o.name, 
               COUNT(DISTINCT p.id) as patients,
               COUNT(DISTINCT u.id) as users,
               COUNT(DISTINCT a.id) as appointments,
               COUNT(DISTINCT i.id) as invoices
        FROM organizations o
        LEFT JOIN patients p ON o.public_id = p.organization_id
        LEFT JOIN users u ON o.public_id = u.organization_id
        LEFT JOIN appointments a ON o.public_id = a.organization_id  
        LEFT JOIN invoices i ON o.public_id = i.organization_id
        GROUP BY o.public_id, o.name
        ORDER BY o.id
    """)
    
    results = cursor.fetchall()
    
    print(f"\n📊 DATA DISTRIBUTION:")
    print(f"{'Organization':<30} {'Patients':<8} {'Users':<6} {'Appointments':<12} {'Invoices':<8}")
    print("-" * 80)
    
    for row in results:
        print(f"{row['name']:<30} {row['patients']:<8} {row['users']:<6} {row['appointments']:<12} {row['invoices']:<8}")
    
    # Test tenant isolation
    print(f"\n🔒 TESTING TENANT ISOLATION:")
    
    all_good = True
    
    # Check for cross-tenant data
    for org in results:
        org_id = org['public_id']
        
        # Check if any patients belong to wrong org
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM patients 
            WHERE organization_id != ? AND organization_id IS NOT NULL
        """, (org_id,))
        wrong_patients = cursor.fetchone()['count']
        
        if wrong_patients > 0:
            print(f"❌ {org['name']}: {wrong_patients} patients from other tenants!")
            all_good = False
        else:
            print(f"✅ {org['name']}: Patient data properly isolated")
    
    # Check for orphaned records
    cursor.execute("SELECT COUNT(*) as count FROM patients WHERE organization_id IS NULL")
    orphaned_patients = cursor.fetchone()['count']
    if orphaned_patients > 0:
        print(f"❌ {orphaned_patients} patients with no organization!")
        all_good = False
    else:
        print("✅ No orphaned patients")
    
    conn.close()
    
    if all_good:
        print(f"\n🎉 SUCCESS: Tenant isolation is working correctly!")
    else:
        print(f"\n⚠️  Tenant isolation issues found!")

def test_multi_tenant_queries():
    """Test multi-tenant query functionality"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        return
    
    print(f"\n🧪 TESTING MULTI-TENANT QUERIES")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get organizations
    cursor.execute("SELECT public_id, name FROM organizations ORDER BY id")
    organizations = cursor.fetchall()
    
    # Test querying as each tenant
    for org in organizations:
        print(f"\n🔍 Querying as {org['name']}:")
        
        # Patients for this tenant
        cursor.execute("SELECT COUNT(*) as count FROM patients WHERE organization_id = ?", (org['public_id'],))
        patients = cursor.fetchone()['count']
        print(f"   👤 Can see {patients} patients")
        
        # Users for this tenant
        cursor.execute("SELECT COUNT(*) as count FROM users WHERE organization_id = ?", (org['public_id'],))
        users = cursor.fetchone()['count']
        print(f"   👥 Can see {users} users")
        
        # Verify no access to other tenants' data
        cursor.execute("SELECT COUNT(*) as count FROM patients WHERE organization_id != ?", (org['public_id'],))
        other_patients = cursor.fetchone()['count']
        if other_patients == 0:
            print(f"   ✅ Cannot see other tenants' data")
        else:
            print(f"   ❌ Can see {other_patients} patients from other tenants!")
    
    conn.close()

if __name__ == '__main__':
    verify_tenancy()
    test_multi_tenant_queries()