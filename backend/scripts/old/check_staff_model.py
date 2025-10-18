# backend/scripts/check_staff_model.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import Staff, Organization, User

app = create_app()

with app.app_context():
    print("🔍 Checking Staff model structure...")
    
    # Check Staff model columns
    staff_columns = [column.name for column in Staff.__table__.columns]
    print(f"Staff columns: {staff_columns}")
    
    # Check Staff model relationships
    staff_relationships = [rel.key for rel in Staff.__mapper__.relationships]
    print(f"Staff relationships: {staff_relationships}")
    
    # Check for hybrid properties
    staff_hybrids = [name for name, obj in Staff.__dict__.items() if hasattr(obj, '__is_hybrid_property__')]
    print(f"Staff hybrid properties: {staff_hybrids}")
    
    # Try to create a minimal staff
    try:
        # First create minimal org and user
        from app import db
        org = Organization(
            public_id="test_org_staff",
            name="Test Org Staff",
            organization_type_id=1,
            address="123 Test St",
            city="Test City",
            state="TS",
            country="USA",
            postal_code="12345",
            phone="123-456-7890",
            email="test@test.com",
            is_active=True
        )
        db.session.add(org)
        
        user = User(
            public_id="test_user_staff",
            email="staff@test.com",
            password_hash="test",
            first_name="Test",
            last_name="Staff",
            is_active=True
        )
        db.session.add(user)
        
        db.session.flush()
        
        # Now try to create staff
        staff = Staff(
            user_id=user.id,
            organization_id=org.id,
            employee_id="EMP001",
            job_title="Test Job",
            department="Test Dept",
            is_active=True
        )
        print("✅ Staff model can be instantiated with minimal fields")
        
        db.session.add(staff)
        db.session.flush()
        print("✅ Staff can be added to session")
        db.session.rollback()
        
    except Exception as e:
        print(f"❌ Error with Staff: {e}")
        import traceback
        traceback.print_exc()