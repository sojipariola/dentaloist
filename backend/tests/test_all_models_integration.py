# tests/test_all_models_integration.py

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db

class TestAllModelsIntegration:
    """Integration test for all models working together"""
    
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app
    
    def test_complete_analytics_workflow(self, app):
        """Test complete analytics workflow"""
        with app.app_context():
            from app.models import (
                User, Organization, AnalyticsDashboard, 
                AnalyticsWidget, WidgetType
            )
            
            # Clear any existing data
            for model in [AnalyticsWidget, AnalyticsDashboard, WidgetType, User, Organization]:
                model.query.delete()
            db.session.commit()
            
            # 1. Create organization and user
            org = Organization(name="Dental Excellence", code="DENTAL_EX")
            user = User(
                email="admin@dentalex.com", 
                first_name="Sarah", 
                last_name="Johnson"
            )
            user.set_password("admin123")
            user.organizations.append(org)
            
            # 2. Create widget types
            bar_chart_type = WidgetType(
                name="Bar Chart",
                code="BAR_CHART",
                component_name="BarChartWidget",
                category="charts",
                supports_refresh=True,
                supports_export=True
            )
            
            number_stat_type = WidgetType(
                name="Number Stat", 
                code="NUMBER_STAT",
                component_name="NumberStatWidget",
                category="metrics",
                supports_refresh=True,
                supports_export=False
            )
            
            # 3. Create dashboard
            dashboard = AnalyticsDashboard(
                name="Practice Overview",
                description="Key metrics for dental practice",
                user_id=user.id,
                organization_id=org.id,
                layout_config={"columns": 12},
                is_public=False
            )
            
            # 4. Create widgets
            revenue_widget = AnalyticsWidget(
                name="revenue_chart",
                title="Monthly Revenue",
                dashboard_id=dashboard.id,
                widget_type_id=bar_chart_type.id,
                data_source="/api/analytics/revenue",
                width=8,
                height=6,
                configuration={"chartType": "bar", "color": "#3498db"}
            )
            
            patient_widget = AnalyticsWidget(
                name="patient_stats",
                title="Patient Count",
                dashboard_id=dashboard.id,
                widget_type_id=number_stat_type.id,
                data_source="/api/analytics/patients",
                width=4,
                height=3,
                configuration={"format": "number", "showComparison": True}
            )
            
            # Add everything to session
            db.session.add_all([
                org, user, bar_chart_type, number_stat_type,
                dashboard, revenue_widget, patient_widget
            ])
            db.session.commit()
            
            # Verify everything was created
            assert org.id is not None
            assert user.id is not None
            assert dashboard.id is not None
            assert revenue_widget.id is not None
            assert patient_widget.id is not None
            
            # Verify relationships
            assert len(user.organizations) == 1
            assert user.organizations[0].name == "Dental Excellence"
            
            assert len(dashboard.widgets.all()) == 2
            widget_names = [w.name for w in dashboard.widgets.all()]
            assert "revenue_chart" in widget_names
            assert "patient_stats" in widget_names
            
            # Verify widget configurations
            assert revenue_widget.configuration["chartType"] == "bar"
            assert patient_widget.configuration["showComparison"] == True
            
            print("✅ Complete analytics workflow test passed!")
    
    def test_model_count_queries(self, app):
        """Test that we can query model counts"""
        with app.app_context():
            from app.models import User, Organization, AnalyticsDashboard
            
            # Clear test data
            for model in [AnalyticsDashboard, User, Organization]:
                model.query.delete()
            db.session.commit()
            
            # Create some test data
            org1 = Organization(name="Clinic A", code="CLINIC_A")
            org2 = Organization(name="Clinic B", code="CLINIC_B")
            
            user1 = User(email="user1@test.com", first_name="User1", last_name="Test")
            user2 = User(email="user2@test.com", first_name="User2", last_name="Test")
            user1.set_password("pass1")
            user2.set_password("pass2")
            
            user1.organizations.append(org1)
            user2.organizations.append(org2)
            
            dashboard1 = AnalyticsDashboard(
                name="Dashboard A", 
                user_id=user1.id, 
                organization_id=org1.id
            )
            dashboard2 = AnalyticsDashboard(
                name="Dashboard B", 
                user_id=user2.id, 
                organization_id=org2.id
            )
            
            db.session.add_all([org1, org2, user1, user2, dashboard1, dashboard2])
            db.session.commit()
            
            # Test queries
            assert User.query.count() == 2
            assert Organization.query.count() == 2
            assert AnalyticsDashboard.query.count() == 2
            
            # Test relationship queries
            user1_dashboards = AnalyticsDashboard.query.filter_by(user_id=user1.id).all()
            assert len(user1_dashboards) == 1
            assert user1_dashboards[0].name == "Dashboard A"
            
            org1_users = User.query.filter(User.organizations.any(id=org1.id)).all()
            assert len(org1_users) == 1
            assert org1_users[0].email == "user1@test.com"
            
            print("✅ Model count queries test passed!")