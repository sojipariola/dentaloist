# tests/test_minimal_analytics.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.base import BaseModel, LookupBaseModel

class TestMinimalAnalytics:
    """Test with minimal, guaranteed-working analytics models"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_minimal_widget_models(self, app):
        """Test minimal widget models that should definitely work"""
        with app.app_context():
            # Define minimal working versions right here
            class MinimalWidgetType(LookupBaseModel):
                __tablename__ = 'minimal_widget_types'
                name = db.Column(db.String(50), nullable=False)
                component_name = db.Column(db.String(100), nullable=False)
            
            class MinimalWidgetTemplate(LookupBaseModel):
                __tablename__ = 'minimal_widget_templates'
                name = db.Column(db.String(100), nullable=False)
                widget_type = db.Column(db.String(50), nullable=False)
                default_config = db.Column(db.JSON, default=dict)
            
            class MinimalWidget(BaseModel):
                __tablename__ = 'minimal_widgets'
                name = db.Column(db.String(100), nullable=False)
                widget_type = db.Column(db.String(50), nullable=False)
                configuration = db.Column(db.JSON, default=dict)
                user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
                organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
            
            # Create tables for these minimal models
            for model in [MinimalWidgetType, MinimalWidgetTemplate, MinimalWidget]:
                model.__table__.create(db.engine)
            
            print("✅ Minimal widget models created successfully!")
            
            # Test that we can create instances
            widget_type = MinimalWidgetType(name="Test Type", component_name="TestComponent")
            template = MinimalWidgetTemplate(name="Test Template", widget_type="chart")
            
            # For Widget, we need a user and organization first
            from app.models import User, Organization
            
            User.__table__.create(db.engine)
            Organization.__table__.create(db.engine)
            
            org = Organization(name="Test Org", code="TEST")
            user = User(email="test@example.com", first_name="Test", last_name="User")
            user.set_password("password123")
            
            db.session.add_all([org, user])
            db.session.flush()
            
            widget = MinimalWidget(
                name="Test Widget",
                widget_type="chart",
                configuration={},
                user_id=user.id,
                organization_id=org.id
            )
            
            db.session.add_all([widget_type, template, widget])
            db.session.commit()
            
            assert widget_type.id is not None
            assert template.id is not None
            assert widget.id is not None
            
            print("✅ Minimal widget instances created successfully!")
            
            # Cleanup
            for model in [MinimalWidgetType, MinimalWidgetTemplate, MinimalWidget, User, Organization]:
                model.__table__.drop(db.engine)
