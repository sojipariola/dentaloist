#!/usr/bin/env python3
"""
Comprehensive tenant health check
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import g
from app import create_app
from app.models import Organization, Patient, User, Appointment, Invoice
from app.utils.tenancy import set_current_tenant, multi_tenant_query

def check_tenant_health():
    """Comprehensive tenant health check"""
    app = create_app()
    
    with app.app_context():
        with app.test_request_context('/health-check', method='GET'):
            print("🏥 TENANT HEALTH CHECK")
            print("=" * 50)
            
            organizations = Organization.query.all()
            
            for org in organizations:
                print(f"\n🏢 Checking: {org.name} (ID: {org.public_id})")
                
                # Set tenant context
                set_current_tenant(org.public_id)
                
                # Check each model
                models_to_check = [
                    ('Patients', Patient),
                    ('Users', User), 
                    ('Appointments', Appointment),
                    ('Invoices', Invoice)
                ]
                
                for model_name, model_class in models_to_check:
                    try:
                        count = multi_tenant_query(model_class).count()
                        print(f"  ✅ {model_name}: {count} records")
                        
                        # Check for orphaned records
                        if hasattr(model_class, 'organization_id'):
                            orphaned = model_class.query.filter(
                                model_class.organization_id != org.public_id
                            ).count()
                            if orphaned > 0:
                                print(f"  ⚠️  {model_name}: {orphaned} records with wrong tenant ID")
                                
                    except Exception as e:
                        print(f"  ❌ {model_name}: Error - {e}")

if __name__ == '__main__':
    check_tenant_health()
