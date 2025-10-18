# tests/test_core_only.py

import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class TestCoreOnly:
    """Test core models in complete isolation"""
    
    def test_user_in_isolation(self):
        """Test User model without loading other models"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy()
        
        # Define minimal User model
        class User(db.Model):
            __tablename__ = 'users'
            id = db.Column(db.Integer, primary_key=True)
            email = db.Column(db.String(120), unique=True, nullable=False)
            first_name = db.Column(db.String(50), nullable=False)
            last_name = db.Column(db.String(50), nullable=False)
            password_hash = db.Column(db.String(255))
            is_active = db.Column(db.Boolean, default=True)
            created_at = db.Column(db.DateTime, default=db.func.now())
            updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
        
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            
            user = User(
                email="test@example.com",
                first_name="John",
                last_name="Doe"
            )
            db.session.add(user)
            db.session.commit()
            
            assert user.id is not None
            assert user.email == "test@example.com"
            
            db.drop_all()
    
    def test_organization_in_isolation(self):
        """Test Organization model without loading other models"""
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db = SQLAlchemy()
        
        class Organization(db.Model):
            __tablename__ = 'organizations'
            id = db.Column(db.Integer, primary_key=True)
            name = db.Column(db.String(100), nullable=False)
            code = db.Column(db.String(50), unique=True, nullable=False)
            is_active = db.Column(db.Boolean, default=True)
            created_at = db.Column(db.DateTime, default=db.func.now())
            updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
        
        db.init_app(app)
        
        with app.app_context():
            db.create_all()
            
            org = Organization(
                name="Test Clinic",
                code="TEST_CLINIC"
            )
            db.session.add(org)
            db.session.commit()
            
            assert org.id is not None
            assert org.name == "Test Clinic"
            
            db.drop_all()