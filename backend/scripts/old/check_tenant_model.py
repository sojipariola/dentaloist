# backend/scripts/check_tenant_model.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import Tenant

app = create_app()

with app.app_context():
    print("🔍 Checking Tenant model structure...")
    
    # Check Tenant model columns and relationships
    tenant_columns = [column.name for column in Tenant.__table__.columns]
    print(f"Tenant columns: {tenant_columns}")
    
    tenant_relationships = [rel.key for rel in Tenant.__mapper__.relationships]
    print(f"Tenant relationships: {tenant_relationships}")
    
    # Try to create a minimal tenant
    try:
        tenant = Tenant(name="Test Tenant", domain="test.local")
        print("✅ Tenant model can be instantiated")
        
        # Check what happens when we add it
        from app import db
        db.session.add(tenant)
        db.session.flush()
        print("✅ Tenant can be added to session")
        db.session.rollback()
        
    except Exception as e:
        print(f"❌ Error with Tenant: {e}")
        import traceback
        traceback.print_exc()