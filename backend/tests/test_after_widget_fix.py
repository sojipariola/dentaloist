# tests/test_after_widget_fix.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class TestAfterWidgetFix:
    """Test after fixing widget model relationships"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_all_models_can_load(self, app):
        """Test that all models can be loaded without errors"""
        with app.app_context():
            # Try to import all models - this should not raise errors
            from app.models import (
                User, Organization, 
                AnalyticsDashboard, AnalyticsWidget, WidgetType,
                Widget, WidgetConfig, WidgetTemplate
            )
            
            models = [
                User, Organization, 
                AnalyticsDashboard, AnalyticsWidget, WidgetType,
                Widget, WidgetConfig, WidgetTemplate
            ]
            
            for model in models:
                assert model.__tablename__ is not None
                print(f"✅ {model.__name__} loaded successfully")
            
            print("✅ All models loaded without errors!")
    
    def test_basic_widget_creation(self, app):
        """Test basic widget creation after fixes"""
        with app.app_context():
            from app.models import User, Organization, Widget, WidgetConfig
            
            # Clear data
            for model in [WidgetConfig, Widget, User, Organization]:
                model.query.delete()
            db.session.commit()
            
            # Create org and user
            org = Organization(name="Widget Test Org", code="WIDGET_ORG")
            user = User(email="widgetuser@test.com", first_name="Widget", last_name="User")
            user.set_password("pass123")
            
            db.session.add_all([org, user])
            db.session.flush()
            
            # Create widget
            widget = Widget(
                name="test_widget",
                description="Test widget description",
                widget_type="chart",
                user_id=user.id,
                organization_id=org.id,
                configuration={"type": "bar", "color": "blue"}
            )
            
            db.session.add(widget)
            db.session.flush()
            
            # Create widget config
            config = WidgetConfig(
                widget_id=widget.id,
                config_key="refresh_interval",
                config_value="300",
                config_type="number",
                user_id=user.id,
                organization_id=org.id
            )
            
            db.session.add(config)
            db.session.commit()
            
            # Verify
            assert widget.id is not None
            assert config.id is not None
            assert config.widget_id == widget.id
            assert config.user_id == user.id
            assert config.organization_id == org.id
            
            # Verify relationships
            assert len(widget.configs) == 1
            assert widget.configs[0].config_key == "refresh_interval"
            assert config.widget.name == "test_widget"
            
            print("✅ Basic widget creation test passed!")