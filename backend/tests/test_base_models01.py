# tests/test_base_models.py

import pytest
from datetime import datetime
from app.models import BaseModel, LookupBaseModel, db
from sqlalchemy import Column, Integer, String


class TestBaseModel:
    """Test BaseModel functionality"""
    
    def test_base_model_creation(self, session):
        """Test BaseModel creation with default values"""
        class TestModel(BaseModel):
            __tablename__ = 'test_model'
            name = db.Column(db.String(100))
        
        # Create table
        TestModel.__table__.create(session.bind)
        
        # Test instance creation
        instance = TestModel(name="Test Instance")
        session.add(instance)
        session.commit()
        
        assert instance.id is not None
        assert instance.public_id is not None
        assert isinstance(instance.created_at, datetime)
        assert isinstance(instance.updated_at, datetime)
        assert instance.is_active == True
    
    def test_base_model_soft_delete(self, session):
        """Test soft delete functionality"""
        class TestModel(BaseModel):
            __tablename__ = 'test_model_soft_delete'
            name = db.Column(db.String(100))
        
        TestModel.__table__.create(session.bind)
        
        instance = TestModel(name="Test Soft Delete")
        session.add(instance)
        session.commit()
        
        # Soft delete
        instance.soft_delete()
        session.commit()
        
        assert instance.is_active == False
        assert instance.deleted_at is not None
    
    def test_base_model_to_dict(self, session):
        """Test to_dict method"""
        class TestModel(BaseModel):
            __tablename__ = 'test_model_dict'
            name = db.Column(db.String(100))
            secret = db.Column(db.String(100))
        
        TestModel.__table__.create(session.bind)
        
        instance = TestModel(name="Test Dict", secret="hidden")
        session.add(instance)
        session.commit()
        
        data = instance.to_dict()
        
        assert 'id' in data
        assert 'public_id' in data
        assert 'name' in data
        assert 'created_at' in data
        assert 'updated_at' in data
        assert 'secret' not in data  # Private fields should be excluded


class TestLookupBaseModel:
    """Test LookupBaseModel functionality"""
    
    def test_lookup_model_creation(self, session):
        """Test LookupBaseModel creation"""
        class TestLookup(LookupBaseModel):
            __tablename__ = 'test_lookup'
            code = db.Column(db.String(50), unique=True, nullable=False)
            description = db.Column(db.Text)
        
        TestLookup.__table__.create(session.bind)
        
        lookup = TestLookup(
            name="Test Lookup",
            code="TEST_LOOKUP",
            description="Test description",
            sort_order=1
        )
        session.add(lookup)
        session.commit()
        
        assert lookup.id is not None
        assert lookup.name == "Test Lookup"
        assert lookup.code == "TEST_LOOKUP"
        assert lookup.sort_order == 1
        assert lookup.is_active == True
    
    def test_lookup_model_to_dict(self, session):
        """Test LookupBaseModel to_dict method"""
        class TestLookup(LookupBaseModel):
            __tablename__ = 'test_lookup_dict'
            code = db.Column(db.String(50), unique=True, nullable=False)
        
        TestLookup.__table__.create(session.bind)
        
        lookup = TestLookup(name="Test Lookup", code="TEST_DICT")
        session.add(lookup)
        session.commit()
        
        data = lookup.to_dict()
        
        assert 'id' in data
        assert 'name' in data
        assert 'code' in data
        assert 'sort_order' in data
        assert 'is_active' in data