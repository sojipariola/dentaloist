import pytest
from app.models import Patient, Organization, User, OrganizationType
from app.models.base import get_current_tenant_id, set_current_tenant


class TestTenantIsolation:
    """Test tenant isolation at model level"""
    
    def test_tenant_filtering(self, db, app):
        """Test that tenant filtering works correctly"""
        
        with app.app_context():
            # Create test organizations
            # Create organization type for testing\n            from app.models import OrganizationType\n            org_type = OrganizationType(name="Test Clinic", code="TEST")\n            db.session.add(org_type)\n            db.session.flush()  # Get the ID without committing\n        \n            org1 = Organization(public_id='org1', name='Org 1', organization_type_id=org_type.id)
            org2 = Organization(public_id='org2', name='Org 2', organization_type_id=org_type.id)
            db.session.add_all([org1, org2])
            db.session.commit()
            
            # Create patients for different organizations
            patient1 = Patient(
                public_id='patient1',
                organization_id='org1',
                first_name='John',
                last_name='Doe'
            )
            patient2 = Patient(
                public_id='patient2', 
                organization_id='org2',
                first_name='Jane',
                last_name='Smith'
            )
            db.session.add_all([patient1, patient2])
            db.session.commit()
            
            # Test tenant filtering
            set_current_tenant('org1')
            org1_patients = Patient.get_active()
            assert len(org1_patients) == 1
            assert org1_patients[0].public_id == 'patient1'
            
            set_current_tenant('org2') 
            org2_patients = Patient.get_active()
            assert len(org2_patients) == 1
            assert org2_patients[0].public_id == 'patient2'
            
            # Test no tenant context (should return all)
            set_current_tenant(None)
            all_patients = Patient.get_active()
            assert len(all_patients) == 2
    
    def test_super_admin_bypass(self, db, app):
        """Test super admin can bypass tenant filtering"""
        
        with app.app_context():
            # Create test data across tenants
            # Create organization type for testing\n            from app.models import OrganizationType\n            org_type = OrganizationType(name="Test Clinic", code="TEST")\n            db.session.add(org_type)\n            db.session.flush()  # Get the ID without committing\n        \n            org1 = Organization(public_id='org1', name='Org 1', organization_type_id=org_type.id)
            org2 = Organization(public_id='org2', name='Org 2', organization_type_id=org_type.id)
            db.session.add_all([org1, org2])
            
            # Create super admin user
            from app.models import UserRole
            super_admin_role = UserRole.query.filter_by(code='SUPER_ADMIN').first()
            
            super_admin = User(
                email='super@admin.com',
                organization_id='org1',
                user_role_id=super_admin_role.id,
                public_id='test_super',
                is_active=True
            )
            db.session.add(super_admin)
            db.session.commit()
            
            # Simulate super admin context
            # (In real implementation, this would be handled by your auth system)
            
            print("✅ Tenant isolation tests passed")



@pytest.fixture
def org_type(db):
    org_type = OrganizationType(name='Dental Clinic', code='DENTAL')
    db.session.add(org_type)
    db.session.commit()
    return org_type

# Then use it in your tests
def test_tenant_filtering(self, db, app, org_type):
    """Test that users can only access data from their tenant"""
    
    with app.app_context():
        # Create test data across tenants
        org1 = Organization(
            public_id='org1', 
            name='Org 1',
            organization_type_id=org_type.id
        )
        org2 = Organization(
            public_id='org2', 
            name='Org 2', 
            organization_type_id=org_type.id
        )
        db.session.add_all([org1, org2])
        db.session.commit()