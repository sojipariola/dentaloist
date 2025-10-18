#!/usr/bin/env python3
"""
Quick verification that tenant fix worked
"""

import sqlite3

def quick_verify():
    """Quick verification using SQLite"""
    conn = sqlite3.connect('instance/dentaloist.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("✅ QUICK TENANT FIX VERIFICATION")
    print("=" * 40)
    
    # Check organization distribution
    cursor.execute("""
        SELECT o.public_id, o.name, 
               COUNT(p.id) as patient_count,
               COUNT(u.id) as user_count,
               COUNT(a.id) as appointment_count,
               COUNT(i.id) as invoice_count
        FROM organization o
        LEFT JOIN patient p ON o.public_id = p.organization_id
        LEFT JOIN user u ON o.public_id = u.organization_id  
        LEFT JOIN appointment a ON o.public_id = a.organization_id
        LEFT JOIN invoice i ON o.public_id = i.organization_id
        WHERE o.is_active = 1
        GROUP BY o.public_id, o.name
    """)
    
    results = cursor.fetchall()
    
    print(f"\n📊 FINAL DATA DISTRIBUTION:")
    print(f"{'Organization':<25} {'Patients':<8} {'Users':<6} {'Appointments':<12} {'Invoices':<8}")
    print("-" * 70)
    
    for row in results:
        print(f"{row['name']:<25} {row['patient_count']:<8} {row['user_count']:<6} {row['appointment_count']:<12} {row['invoice_count']:<8}")
    
    # Check for any remaining cross-tenant data
    print(f"\n🔍 CHECKING FOR REMAINING ISSUES:")
    
    # Patients with wrong org
    cursor.execute("SELECT COUNT(*) as count FROM patient WHERE organization_id NOT IN (SELECT public_id FROM organization)")
    wrong_org_patients = cursor.fetchone()['count']
    if wrong_org_patients == 0:
        print("✅ All patients have valid organization IDs")
    else:
        print(f"❌ {wrong_org_patients} patients with invalid organization IDs")
    
    # Any null organization IDs
    cursor.execute("SELECT COUNT(*) as count FROM patient WHERE organization_id IS NULL")
    null_org_patients = cursor.fetchone()['count']
    if null_org_patients == 0:
        print("✅ No patients with null organization IDs")
    else:
        print(f"❌ {null_org_patients} patients with null organization IDs")
    
    conn.close()

if __name__ == '__main__':
    quick_verify()
