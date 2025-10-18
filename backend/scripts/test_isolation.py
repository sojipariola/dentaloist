# test_isolation.py
import sys
sys.path.append('/home/soji/Documents/Projects/Dentaloist/backend')

from app import create_app
from app.models import Patient, User, Appointment, Invoice
from app.utils.tenancy import multi_tenant_query
from flask import g

def test_real_tenant_isolation():
    """Test tenant isolation with your actual data"""
    app = create_app()
    
    with app.app_context():
        print("🔐 TESTING TENANT ISOLATION WITH REAL DATA")
        print("=" * 50)
        
        # Get actual organizations from your database
        from app.models import Organization
        organizations = Organization.query.all()
        
        for org in organizations:
            print(f"\n🏢 Testing Organization: {org.name} (ID: {org.id})")
            g.tenant_id = org.id
            
            # Test multi_tenant_query
            patients = multi_tenant_query(Patient).all()
            users = multi_tenant_query(User).all()
            appointments = multi_tenant_query(Appointment).all()
            invoices = multi_tenant_query(Invoice).all()
            
            print(f"  ✅ multi_tenant_query results:")
            print(f"     Patients: {len(patients)}")
            print(f"     Users: {len(users)}")
            print(f"     Appointments: {len(appointments)}")
            print(f"     Invoices: {len(invoices)}")
            
            # Verify these actually belong to this organization
            if patients:
                org_ids = set(p.organization_id for p in patients)
                if len(org_ids) == 1 and org_ids.pop() == org.id:
                    print(f"     ✅ Patient isolation: CORRECT")
                else:
                    print(f"     ❌ Patient isolation: BROKEN - mixed organizations: {org_ids}")
            
            # Test direct query (should show the security risk)
            all_patients = Patient.query.all()
            security_gap = len(all_patients) - len(patients)
            if security_gap > 0:
                print(f"     🚨 SECURITY GAP: Direct query reveals {security_gap} patients from other tenants!")

test_real_tenant_isolation()
