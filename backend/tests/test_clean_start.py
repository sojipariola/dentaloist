# tests/test_clean_start.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_clean_start():
    """Test with a completely clean start"""
    # Create a fresh Flask app
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_bcrypt import Bcrypt
    
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy()
    bcrypt = Bcrypt()
    
    # Define minimal models
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), unique=True, nullable=False)
        first_name = db.Column(db.String(50), nullable=False)
        last_name = db.Column(db.String(50), nullable=False)
        password_hash = db.Column(db.String(255))
    
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        code = db.Column(db.String(50), unique=True, nullable=False)
    
    # Initialize and test
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Test basic operations
        org = Organization(name="Test Org", code="TEST")
        user = User(email="test@example.com", first_name="Test", last_name="User")
        user.password_hash = bcrypt.generate_password_hash("password123").decode('utf-8')
        
        db.session.add_all([org, user])
        db.session.commit()
        
        assert User.query.count() == 1
        assert Organization.query.count() == 1
        assert bcrypt.check_password_hash(user.password_hash, "password123")
        
        print("✅ Clean start test passed - basic models work!")
        return True

if __name__ == '__main__':
    test_clean_start()
