# check_tenant_data.py
import sqlite3
import pandas as pd
from pathlib import Path

def analyze_tenant_isolation():
    """Analyze current data for tenant isolation"""
    db_path = Path('/home/soji/Documents/Projects/Dentaloist/backend/instance/dentaloist.db')
    
    conn = sqlite3.connect(db_path)
    
    print("🏢 ORGANIZATIONS ANALYSIS")
    print("=" * 50)
    
    # Check organizations
    organizations = pd.read_sql("SELECT * FROM organizations;", conn)
    print("Organizations:")
    print(organizations[['id', 'name', 'email']].to_string(index=False))
    print()
    
    # Check patients distribution by organization
    patients_by_org = pd.read_sql("""
        SELECT organization_id, COUNT(*) as patient_count 
        FROM patients 
        GROUP BY organization_id;
    """, conn)
    print("Patients by Organization:")
    print(patients_by_org.to_string(index=False))
    print()
    
    # Check users distribution by organization
    users_by_org = pd.read_sql("""
        SELECT organization_id, COUNT(*) as user_count 
        FROM users 
        GROUP BY organization_id;
    """, conn)
    print("Users by Organization:")
    print(users_by_org.to_string(index=False))
    print()
    
    # Check appointments distribution
    appointments_by_org = pd.read_sql("""
        SELECT organization_id, COUNT(*) as appointment_count 
        FROM appointments 
        GROUP BY organization_id;
    """, conn)
    print("Appointments by Organization:")
    print(appointments_by_org.to_string(index=False))
    print()
    
    # Check invoices distribution
    invoices_by_org = pd.read_sql("""
        SELECT organization_id, COUNT(*) as invoice_count 
        FROM invoices 
        GROUP BY organization_id;
    """, conn)
    print("Invoices by Organization:")
    print(invoices_by_org.to_string(index=False))
    print()
    
    # Check for potential cross-tenant data issues
    print("🔍 CHECKING FOR CROSS-TENANT DATA ISSUES")
    print("=" * 50)
    
    # Check if any users belong to non-existent organizations
    orphaned_users = pd.read_sql("""
        SELECT u.id, u.email, u.organization_id 
        FROM users u 
        LEFT JOIN organizations o ON u.organization_id = o.id 
        WHERE o.id IS NULL;
    """, conn)
    
    if len(orphaned_users) > 0:
        print("❌ Orphaned Users (no organization):")
        print(orphaned_users.to_string(index=False))
    else:
        print("✅ No orphaned users found")
    print()
    
    # Check if any patients belong to non-existent organizations
    orphaned_patients = pd.read_sql("""
        SELECT p.id, p.first_name, p.last_name, p.organization_id 
        FROM patients p 
        LEFT JOIN organizations o ON p.organization_id = o.id 
        WHERE o.id IS NULL;
    """, conn)
    
    if len(orphaned_patients) > 0:
        print("❌ Orphaned Patients (no organization):")
        print(orphaned_patients.to_string(index=False))
    else:
        print("✅ No orphaned patients found")
    print()
    
    conn.close()

def check_tenant_context_in_app():
    """Check if tenant context is properly set in the application"""
    import sys
    sys.path.append('/home/soji/Documents/Projects/Dentaloist/backend')
    
    from app import create_app
    from app.models import Patient, User, Appointment, Invoice
    from app.utils.tenancy import multi_tenant_query
    from flask import g
    
    app = create_app()
    
    with app.app_context():
        print("🧪 TESTING TENANT ISOLATION IN APPLICATION")
        print("=" * 50)
        
        # Test with different tenant contexts
        test_tenants = ['test-tenant-001', 'demo-dental-001', 'smile-center-002']
        
        for tenant_id in test_tenants:
            print(f"\nTesting with tenant: {tenant_id}")
            g.tenant_id = tenant_id
            
            try:
                patients = multi_tenant_query(Patient).count()
                users = multi_tenant_query(User).count()
                appointments = multi_tenant_query(Appointment).count()
                invoices = multi_tenant_query(Invoice).count()
                
                print(f"  Patients: {patients}")
                print(f"  Users: {users}")
                print(f"  Appointments: {appointments}")
                print(f"  Invoices: {invoices}")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")

def check_direct_query_vs_multi_tenant():
    """Compare direct queries vs multi_tenant_query"""
    import sys
    sys.path.append('/home/soji/Documents/Projects/Dentaloist/backend')
    
    from app import create_app
    from app.models import Patient
    from app.utils.tenancy import multi_tenant_query
    from flask import g
    
    app = create_app()
    
    with app.app_context():
        print("\n🔒 COMPARING DIRECT QUERY VS MULTI_TENANT_QUERY")
        print("=" * 50)
        
        g.tenant_id = "demo-dental-001"
        
        # Using multi_tenant_query (safe)
        safe_patients = multi_tenant_query(Patient).all()
        print(f"multi_tenant_query patients: {len(safe_patients)}")
        
        # Using direct query (unsafe - shows SQLite vulnerability)
        all_patients = Patient.query.all()
        print(f"Direct Patient.query.all(): {len(all_patients)}")
        
        print(f"🚨 SECURITY RISK: Direct query returns {len(all_patients) - len(safe_patients)} extra patients from other tenants!")

if __name__ == "__main__":
    analyze_tenant_isolation()
    check_tenant_context_in_app()
    check_direct_query_vs_multi_tenant()
