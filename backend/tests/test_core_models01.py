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
            last_name="Doe",
            password_hash="hashed_password"
        )
        
        session.add(user)
        session.commit()
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.full_name == "John Doe"
        assert user.is_active == True
    
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
        
        assert user.check_password("secure_password") == True
        assert user.check_password("wrong_password") == False
    
    def test_user_relationships(self, session):
        """Test user relationships"""
        # Create organization
        org = Organization(name="Test Clinic", code="TEST_CLINIC")
        session.add(org)
        
        # Create user
        user = User(
            email="doctor@example.com",
            first_name="Jane",
            last_name="Smith"
        )
        user.organizations.append(org)
        
        session.add(user)
        session.commit()
        
        assert len(user.organizations) == 1
        assert user.organizations[0].name == "Test Clinic"


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
        
        user1 = User(email="user1@example.com", first_name="User", last_name="One")
        user2 = User(email="user2@example.com", first_name="User", last_name="Two")
        
        org.users.extend([user1, user2])
        
        session.add(org)
        session.commit()
        
        assert len(org.users) == 2
        assert org.users[0].email == "user1@example.com"


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
    
    def test_role_permission_relationship(self, session):
        """Test role-permission many-to-many relationship"""
        role = Role(name="Admin")
        permission1 = Permission(name="user:create")
        permission2 = Permission(name="user:delete")
        
        role.permissions.extend([permission1, permission2])
        
        session.add(role)
        session.commit()
        
        assert len(role.permissions) == 2
        assert role.permissions[0].name == "user:create"
        