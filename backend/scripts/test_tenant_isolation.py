#!/usr/bin/env python3
"""
Test script for tenant isolation with proper request context handling
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, g
from app import create_app
from app.models import Organization, Patient, User, Appointment, Invoice
from app.utils.tenancy import set_current_tenant, multi_tenant_query

def test_tenant_isolation_with_context():
    """Test tenant isolation within proper Flask request context"""
    app = create_app()
    
    with app.app_context():
        with app.test_request_context('/test', method='GET'):
            # Set a tenant for the request context
            g.tenant_id = 'org_001'
            
            print("🔒 TESTING TENANT ISOLATION WITH REQUEST CONTEXT")
            print("=" * 50)
            
            # Test Organization 1
            print(f"\n🏢 Testing Organization: Bright Smile Dental Clinic (ID: org_001)")
            
            # Set current tenant
            set_current_tenant('org_001')
            
            # Query patients with tenant isolation
            patients = multi_tenant_query(Patient).all()
            print(f"✅ Patients for org_001: {len(patients)} patients")
            
            # Query users with tenant isolation
            users = multi_tenant_query(User).all()
            print(f"✅ Users for org_001: {len(users)} users")
            
            # Test Organization 2
            print(f"\n🏢 Testing Organization: Perfect Teeth Orthodontics (ID: org_002)")
            
            # Set current tenant
            set_current_tenant('org_002')
            
            # Query patients with tenant isolation
            patients = multi_tenant_query(Patient).all()
            print(f"✅ Patients for org_002: {len(patients)} patients")
            
            # Query users with tenant isolation
            users = multi_tenant_query(User).all()
            print(f"✅ Users for org_002: {len(users)} users")

def test_cross_tenant_data_leak():
    """Test that data doesn't leak between tenants"""
    app = create_app()
    
    with app.app_context():
        with app.test_request_context('/test', method='GET'):
            print(f"\n🔍 TESTING CROSS-TENANT DATA LEAK PROTECTION")
            print("=" * 50)
            
            # Get all patients without tenant filter (should show all)
            all_patients = Patient.query.all()
            print(f"📊 Total patients in database: {len(all_patients)}")
            
            # Test org_001
            set_current_tenant('org_001')
            org_001_patients = multi_tenant_query(Patient).all()
            print(f"🏢 org_001 can see: {len(org_001_patients)} patients")
            
            # Test org_002  
            set_current_tenant('org_002')
            org_002_patients = multi_tenant_query(Patient).all()
            print(f"🏢 org_002 can see: {len(org_002_patients)} patients")
            
            # Verify isolation
            org_001_ids = {p.id for p in org_001_patients}
            org_002_ids = {p.id for p in org_002_patients}
            
            common_patients = org_001_ids.intersection(org_002_ids)
            if common_patients:
                print(f"❌ DATA LEAK: {len(common_patients)} patients visible to both tenants!")
            else:
                print("✅ SUCCESS: No data leak between tenants!")

if __name__ == '__main__':
    test_tenant_isolation_with_context()
    test_cross_tenant_data_leak()
