#!/usr/bin/env python3
"""
Quick verification that tenant isolation is working
"""

import sqlite3
import os

def quick_verification():
    """Quick verification of tenant isolation"""
    db_path = 'instance/dentaloist.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    print("✅ QUICK TENANT ISOLATION VERIFICATION")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
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
        GROUP BY o.public_id, o.name
        ORDER BY o.id
    """)
    
    results = cursor.fetchall()
    
    print(f"\n📊 FINAL DATA DISTRIBUTION:")
    print(f"{'Organization':<25} {'Patients':<8} {'Users':<6} {'Appointments':<12} {'Invoices':<8}")
    print("-" * 70)
    
    total_patients = 0
    total_users = 0
    
    for row in results:
        print(f"{row['name']:<25} {row['patient_count']:<8} {row['user_count']:<6} {row['appointment_count']:<12} {row['invoice_count']:<8}")
        total_patients += row['patient_count']
        total_users += row['user_count']
    
    # Verify no data leaks
    print(f"\n🔒 DATA ISOLATION CHECKS:")
    
    # Check for patients with invalid org IDs
    cursor.execute("""
        SELECT COUNT(*) as count 
        FROM patient 
        WHERE organization_id NOT IN (SELECT public_id FROM organization)
           OR organization_id IS NULL
    """)
    invalid_patients = cursor.fetchone()['count']
    
    if invalid_patients == 0:
        print("✅ All patients have valid organization IDs")
    else:
        print(f"❌ {invalid_patients} patients with invalid organization IDs")
    
    # Check balanced distribution
    cursor.execute("SELECT public_id, name FROM organization ORDER BY id")
    orgs = cursor.fetchall()
    
    balanced = True
    for org in orgs:
        cursor.execute("SELECT COUNT(*) as count FROM patient WHERE organization_id = ?", (org['public_id'],))
        count = cursor.fetchone()['count']
        
        if count < total_patients // len(orgs) * 0.8:  # Allow 20% variance
            print(f"⚠️  {org['name']} has unbalanced data: {count} patients")
            balanced = False
    
    if balanced:
        print("✅ Data distribution is balanced across organizations")
    
    conn.close()
    
    print(f"\n🎉 TENANT ISOLATION VERIFICATION COMPLETE!")

if __name__ == '__main__':
    quick_verification()
