# tests/test_fixed_models.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class TestFixedModels:
    """Test models with proper database handling"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_user_and_organization_creation(self, app):
        """Test creating users and organizations"""
        with app.app_context():
            from app.models import User, Organization
            
            # Clear any existing test data
            User.query.delete()
            Organization.query.delete()
            db.session.commit()
            
            # Create organization
            org = Organization(
                name="Test Dental Clinic",
                code="TEST_DENTAL"
            )
            db.session.add(org)
            db.session.flush()  # Get ID without committing
            
            # Create user
            user = User(
                email="dentist@test.com",
                first_name="Jane",
                last_name="Smith"
            )
            user.set_password("secure123")
            user.organizations.append(org)
            
            db.session.add(user)
            db.session.commit()
            
            # Verify creation
            assert user.id is not None
            assert org.id is not None
            assert user.email == "dentist@test.com"
            assert org.name == "Test Dental Clinic"
            
            # Verify relationships
            assert len(user.organizations) == 1
            assert user.organizations[0].name == "Test Dental Clinic"
            assert user in org.users
            
            # Verify password hashing
            assert user.check_password("secure123")
            assert not user.check_password("wrongpassword")
            
            print("✅ User and Organization creation test passed!")
    
    def test_analytics_dashboard_creation(self, app):
        """Test AnalyticsDashboard creation"""
        with app.app_context():
            from app.models import AnalyticsDashboard, User, Organization
            
            # Clear test data
            AnalyticsDashboard.query.delete()
            User.query.delete()
            Organization.query.delete()
            db.session.commit()
            
            # Create org and user first
            org = Organization(name="Test Org", code="TEST")
            user = User(email="user@test.com", first_name="Test", last_name="User")
            user.set_password("pass123")
            
            db.session.add_all([org, user])
            db.session.flush()  # Get IDs
            
            # Create dashboard
            dashboard = AnalyticsDashboard(
                name="Clinical Dashboard",
                description="Clinical metrics overview",
                user_id=user.id,
                organization_id=org.id,
                layout_config={"grid": "fluid"},
                is_public=False
            )
            
            db.session.add(dashboard)
            db.session.commit()
            
            # Verify dashboard creation
            assert dashboard.id is not None
            assert dashboard.name == "Clinical Dashboard"
            assert dashboard.organization_id == org.id
            assert dashboard.user_id == user.id
            assert dashboard.is_public == False
            
            # Verify relationships work
            assert dashboard.user.email == "user@test.com"
            assert dashboard.organization.name == "Test Org"
            
            print("✅ AnalyticsDashboard creation test passed!")
    
    def test_analytics_widget_creation(self, app):
        """Test AnalyticsWidget creation"""
        with app.app_context():
            from app.models import (
                AnalyticsDashboard, AnalyticsWidget, WidgetType, 
                User, Organization
            )
            
            # Clear test data
            AnalyticsWidget.query.delete()
            AnalyticsDashboard.query.delete()
            WidgetType.query.delete()
            User.query.delete()
            Organization.query.delete()
            db.session.commit()
            
            # Create required entities
            org = Organization(name="Widget Test Org", code="WIDGET_TEST")
            user = User(email="widget@test.com", first_name="Widget", last_name="Test")
            user.set_password("pass123")
            
            # Create a widget type if none exists
            widget_type = WidgetType.query.first()
            if not widget_type:
                widget_type = WidgetType(
                    name="Test Chart",
                    code="TEST_CHART",
                    component_name="TestChartWidget",
                    category="test"
                )
                db.session.add(widget_type)
            
            db.session.add_all([org, user, widget_type])
            db.session.flush()
            
            # Create dashboard
            dashboard = AnalyticsDashboard(
                name="Widget Test Dashboard",
                user_id=user.id,
                organization_id=org.id
            )
            db.session.add(dashboard)
            db.session.flush()
            
            # Create widget
            widget = AnalyticsWidget(
                name="test_widget",
                title="Test Widget",
                dashboard_id=dashboard.id,
                widget_type_id=widget_type.id,
                data_source="/api/test/data",
                width=6,
                height=4
            )
            
            db.session.add(widget)
            db.session.commit()
            
            # Verify widget creation
            assert widget.id is not None
            assert widget.name == "test_widget"
            assert widget.dashboard_id == dashboard.id
            assert widget.widget_type_id == widget_type.id
            assert widget.width == 6
            
            # Verify relationships
            assert widget.dashboard.name == "Widget Test Dashboard"
            assert widget.widget_type.name == "Test Chart"
            assert len(dashboard.widgets.all()) == 1
            
            print("✅ AnalyticsWidget creation test passed!")