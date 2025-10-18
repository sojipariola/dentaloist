# test_db.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.core import Tenant, User, Organization

app = create_app()

with app.app_context():
    print("🧪 Testing database...")
    
    # Create sample data
    tenant = Tenant(
        name="Test Dental Clinic",
        contact_email="clinic@test.com",
        subdomain="test"
    )
    db.session.add(tenant)
    db.session.commit()
    print(f"✅ Created tenant: {tenant.name}")
    
    org = Organization(
        name="Main Clinic",
        type="DENTAL_CLINIC", 
        tenant_id=tenant.id
    )
    db.session.add(org)
    db.session.commit()
    print(f"✅ Created organization: {org.name}")
    
    user = User(
        email="doctor@test.com",
        first_name="John",
        last_name="Doe",
        password_hash="temp",
        organization_id=org.public_id,
        tenant_id=tenant.id
    )
    db.session.add(user)
    db.session.commit()
    print(f"✅ Created user: {user.email}")
    
    print(f"\n📊 Database summary:")
    print(f"  - Tenants: {Tenant.query.count()}")
    print(f"  - Organizations: {Organization.query.count()}")
    print(f"  - Users: {User.query.count()}")
