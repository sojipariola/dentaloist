# Read models/__init__.py
with open('app/models/__init__.py', 'r') as f:
    content = f.read()

# Comment out analytics imports
content = content.replace(
    'from .analytics import (',
    '# from .analytics import ('
)
content = content.replace(
    '    AnalyticsDashboard,',
    '#     AnalyticsDashboard,'
)
content = content.replace(
    '    AnalyticsWidget,',
    '#     AnalyticsWidget,'
)
content = content.replace(
    '    WidgetType,',
    '#     WidgetType,'
)
content = content.replace(
    '    DashboardLayout,',
    '#     DashboardLayout,'
)
content = content.replace(
    "    'AnalyticsDashboard', 'AnalyticsWidget', 'WidgetType', 'DashboardLayout'",
    "#     'AnalyticsDashboard', 'AnalyticsWidget', 'WidgetType', 'DashboardLayout'"
)

# Write back
with open('app/models/__init__.py', 'w') as f:
    f.write(content)

print("Temporarily disabled analytics models")
