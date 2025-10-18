# tests/test_analytics_models.py

import pytest
from app.models import AnalyticsDashboard, AnalyticsWidget, WidgetType, db


class TestAnalyticsDashboard:
    """Test AnalyticsDashboard model"""
    
    def test_dashboard_creation(self, session):
        """Test basic dashboard creation"""
        dashboard = AnalyticsDashboard(
            name="Clinical Overview",
            description="Overview of clinical metrics",
            layout_config={"grid": "fluid"},
            is_public=False
        )
        
        session.add(dashboard)
        session.commit()
        
        assert dashboard.id is not None
        assert dashboard.name == "Clinical Overview"
        assert dashboard.is_public == False
    
    def test_dashboard_widgets_relationship(self, session):
        """Test dashboard-widgets relationship"""
        dashboard = AnalyticsDashboard(name="Test Dashboard")
        
        widget1 = AnalyticsWidget(name="Widget 1", title="First Widget")
        widget2 = AnalyticsWidget(name="Widget 2", title="Second Widget")
        
        dashboard.widgets.extend([widget1, widget2])
        
        session.add(dashboard)
        session.commit()
        
        assert len(dashboard.widgets) == 2
        assert dashboard.widgets[0].name == "Widget 1"


class TestAnalyticsWidget:
    """Test AnalyticsWidget model"""
    
    def test_widget_creation(self, session):
        """Test basic widget creation"""
        widget = AnalyticsWidget(
            name="revenue_chart",
            title="Revenue Overview",
            data_source="/api/analytics/revenue",
            width=6,
            height=4,
            configuration={"chartType": "line"}
        )
        
        session.add(widget)
        session.commit()
        
        assert widget.id is not None
        assert widget.name == "revenue_chart"
        assert widget.width == 6
        assert widget.height == 4


class TestWidgetType:
    """Test WidgetType model"""
    
    def test_widget_type_creation(self, session):
        """Test basic widget type creation"""
        widget_type = WidgetType(
            name="Bar Chart",
            code="BAR_CHART",
            component_name="BarChartWidget",
            category="charts",
            supports_refresh=True,
            supports_export=True
        )
        
        session.add(widget_type)
        session.commit()
        
        assert widget_type.id is not None
        assert widget_type.code == "BAR_CHART"
        assert widget_type.supports_refresh == True