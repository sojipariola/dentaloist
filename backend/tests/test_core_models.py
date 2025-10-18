# tests/test_core_models.py

import pytest
from app.models import User, Organization, Tenant, Role, Permission, db


class TestUserModel:
    """Test User model functionality"""
    
    def test_user_creation(self, session):
        """Test basic user creation"""
        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        user.set_password("password123")
        
        session.add(user)
        session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "John Doe"
        assert user.is_active == True
        assert user.check_password("password123") == True
    
    def test_user_password_verification(self, session):
        """Test password verification"""
        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        user.set_password("secure_password")
        
        session.add(user)
        session.commit()
        
        # Retrieve user to ensure password hash is stored
        retrieved_user = session.query(User).filter_by(email="test@example.com").first()
        
        assert retrieved_user.check_password("secure_password") == True
        assert retrieved_user.check_password("wrong_password") == False
    
    def test_user_relationships(self, session):
        """Test user relationships"""
        # Create organization
        org = Organization(name="Test Clinic", code="TEST_CLINIC")
        session.add(org)
        session.flush()  # Flush to get org ID
        
        # Create user
        user = User(
            email="doctor@example.com",
            first_name="Jane",
            last_name="Smith"
        )
        user.set_password("password123")
        user.organizations.append(org)
        
        session.add(user)
        session.commit()
        
        # Test relationship
        assert len(user.organizations) == 1
        assert user.organizations[0].name == "Test Clinic"
        assert org in user.organizations


class TestOrganizationModel:
    """Test Organization model functionality"""
    
    def test_organization_creation(self, session):
        """Test basic organization creation"""
        org = Organization(
            name="Dental Clinic",
            code="DENTAL_001",
            email="clinic@example.com",
            phone="+1234567890"
        )
        
        session.add(org)
        session.commit()
        
        assert org.id is not None
        assert org.name == "Dental Clinic"
        assert org.code == "DENTAL_001"
        assert org.is_active == True
    
    def test_organization_users_relationship(self, session):
        """Test organization-users relationship"""
        org = Organization(name="Test Clinic", code="TEST_CLINIC")
        session.add(org)
        session.flush()
        
        user1 = User(email="user1@example.com", first_name="User", last_name="One")
        user1.set_password("pass1")
        
        user2 = User(email="user2@example.com", first_name="User", last_name="Two") 
        user2.set_password("pass2")
        
        org.users.extend([user1, user2])
        
        session.add_all([user1, user2])
        session.commit()
        
        # Test relationships
        assert len(org.users) == 2
        assert org.users[0].email == "user1@example.com"
        assert org.users[1].email == "user2@example.com"
        
        # Test backref
        assert user1.organizations[0].name == "Test Clinic"


class TestRolePermissionModels:
    """Test Role and Permission models"""
    
    def test_role_creation(self, session):
        """Test role creation"""
        role = Role(
            name="Dentist",
            description="Dental practitioner role"
        )
        
        session.add(role)
        session.commit()
        
        assert role.id is not None
        assert role.name == "Dentist"
        assert role.description == "Dental practitioner role"
    
    def test_permission_creation(self, session):
        """Test permission creation"""
        permission = Permission(
            name="patient:create",
            description="Create new patients"
        )
        
        session.add(permission)
        session.commit()
        
        assert permission.id is not None
        assert permission.name == "patient:create"
        assert permission.description == "Create new patients"
    
    def test_role_permission_relationship(self, session):
        """Test role-permission many-to-many relationship"""
        role = Role(name="Admin", description="Administrator role")
        permission1 = Permission(name="user:create", description="Create users")
        permission2 = Permission(name="user:delete", description="Delete users")
        
        role.permissions.extend([permission1, permission2])
        
        session.add(role)
        session.add_all([permission1, permission2])
        session.commit()
        
        # Test relationships
        assert len(role.permissions) == 2
        permission_names = [p.name for p in role.permissions]
        assert "user:create" in permission_names
        assert "user:delete" in permission_names
        
        # Test backref
        assert permission1 in role.permissions
        assert role in permission1.roles