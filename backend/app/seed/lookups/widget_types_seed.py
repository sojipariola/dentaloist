# app/seed/lookups/widget_types_seed.py

from app import db
from app.models import WidgetType
import uuid


def seed_widget_types():
    """Seed widget types with required code field"""
    
    widget_types_data = [
        {
            'name': 'Bar Chart',
            'code': 'BAR_CHART',
            'description': 'Vertical or horizontal bar chart for comparing categories',
            'component_name': 'BarChartWidget',
            'default_config': {
                'orientation': 'vertical',
                'stacked': False,
                'show_legend': True,
                'show_grid': True
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'orientation': {'type': 'string', 'enum': ['vertical', 'horizontal']},
                    'stacked': {'type': 'boolean'},
                    'show_legend': {'type': 'boolean'},
                    'show_grid': {'type': 'boolean'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'label': {'type': 'string'},
                        'value': {'type': 'number'},
                        'category': {'type': 'string'}
                    }
                }
            },
            'category': 'charts',
            'subcategory': 'comparison',
            'tags': ['chart', 'comparison', 'categorical'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': True,
            'max_data_points': 50,
            'icon': 'chart-bar',
            'color': '#3498db',
            'default_size': 'medium',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 0
        },
        {
            'name': 'Line Chart',
            'code': 'LINE_CHART',
            'description': 'Line chart for showing trends over time',
            'component_name': 'LineChartWidget',
            'default_config': {
                'smooth': True,
                'show_points': True,
                'show_legend': True,
                'show_grid': True
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'smooth': {'type': 'boolean'},
                    'show_points': {'type': 'boolean'},
                    'show_legend': {'type': 'boolean'},
                    'show_grid': {'type': 'boolean'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'x': {'type': 'string'},
                        'y': {'type': 'number'},
                        'series': {'type': 'string'}
                    }
                }
            },
            'category': 'charts',
            'subcategory': 'trends',
            'tags': ['chart', 'trend', 'time-series'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': True,
            'max_data_points': 100,
            'icon': 'chart-line',
            'color': '#e74c3c',
            'default_size': 'medium',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 1
        },
        {
            'name': 'Pie Chart',
            'code': 'PIE_CHART',
            'description': 'Pie chart for showing proportions and percentages',
            'component_name': 'PieChartWidget',
            'default_config': {
                'show_labels': True,
                'show_percentages': True,
                'donut': False
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'show_labels': {'type': 'boolean'},
                    'show_percentages': {'type': 'boolean'},
                    'donut': {'type': 'boolean'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'label': {'type': 'string'},
                        'value': {'type': 'number'},
                        'color': {'type': 'string'}
                    }
                }
            },
            'category': 'charts',
            'subcategory': 'proportions',
            'tags': ['chart', 'percentage', 'proportion'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': False,
            'max_data_points': 20,
            'icon': 'chart-pie',
            'color': '#9b59b6',
            'default_size': 'small',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 2
        },
        {
            'name': 'Number Stat',
            'code': 'NUMBER_STAT',
            'description': 'Single number statistic with optional comparison',
            'component_name': 'NumberStatWidget',
            'default_config': {
                'prefix': '',
                'suffix': '',
                'show_comparison': True,
                'format': 'number'
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'prefix': {'type': 'string'},
                    'suffix': {'type': 'string'},
                    'show_comparison': {'type': 'boolean'},
                    'format': {'type': 'string', 'enum': ['number', 'currency', 'percentage']}
                }
            },
            'data_schema': {
                'type': 'object',
                'properties': {
                    'value': {'type': 'number'},
                    'previous_value': {'type': 'number'},
                    'change_percentage': {'type': 'number'}
                }
            },
            'category': 'metrics',
            'subcategory': 'kpi',
            'tags': ['metric', 'kpi', 'number'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': False,
            'supports_drilldown': False,
            'max_data_points': 1,
            'icon': 'numeric',
            'color': '#27ae60',
            'default_size': 'small',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 3
        },
        {
            'name': 'Data Table',
            'code': 'DATA_TABLE',
            'description': 'Tabular data display with sorting and filtering',
            'component_name': 'DataTableWidget',
            'default_config': {
                'page_size': 10,
                'show_search': True,
                'show_pagination': True,
                'striped': True
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'page_size': {'type': 'number'},
                    'show_search': {'type': 'boolean'},
                    'show_pagination': {'type': 'boolean'},
                    'striped': {'type': 'boolean'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object'
                }
            },
            'category': 'tables',
            'subcategory': 'data',
            'tags': ['table', 'data', 'tabular'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': True,
            'max_data_points': 1000,
            'icon': 'table',
            'color': '#f39c12',
            'default_size': 'large',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 4
        },
        {
            'name': 'Patient Summary',
            'code': 'PATIENT_SUMMARY',
            'description': 'Overview of patient statistics and demographics',
            'component_name': 'PatientSummaryWidget',
            'default_config': {
                'show_new_patients': True,
                'show_active_patients': True,
                'time_period': 'month'
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'show_new_patients': {'type': 'boolean'},
                    'show_active_patients': {'type': 'boolean'},
                    'time_period': {'type': 'string', 'enum': ['day', 'week', 'month', 'year']}
                }
            },
            'data_schema': {
                'type': 'object',
                'properties': {
                    'total_patients': {'type': 'number'},
                    'new_patients': {'type': 'number'},
                    'active_patients': {'type': 'number'}
                }
            },
            'category': 'clinical',
            'subcategory': 'patients',
            'tags': ['clinical', 'patients', 'demographics'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': True,
            'max_data_points': 10,
            'icon': 'account-group',
            'color': '#e74c3c',
            'default_size': 'medium',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 5
        },
        {
            'name': 'Appointment Calendar',
            'code': 'APPOINTMENT_CALENDAR',
            'description': 'Calendar view of appointments and schedule',
            'component_name': 'AppointmentCalendarWidget',
            'default_config': {
                'view': 'week',
                'show_staff': True,
                'show_rooms': True
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'view': {'type': 'string', 'enum': ['day', 'week', 'month']},
                    'show_staff': {'type': 'boolean'},
                    'show_rooms': {'type': 'boolean'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'number'},
                        'title': {'type': 'string'},
                        'start': {'type': 'string'},
                        'end': {'type': 'string'},
                        'status': {'type': 'string'}
                    }
                }
            },
            'category': 'clinical',
            'subcategory': 'appointments',
            'tags': ['clinical', 'appointments', 'calendar'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': False,
            'supports_drilldown': True,
            'max_data_points': 100,
            'icon': 'calendar',
            'color': '#3498db',
            'default_size': 'xlarge',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 6
        },
        {
            'name': 'Revenue Chart',
            'code': 'REVENUE_CHART',
            'description': 'Financial revenue and payment tracking',
            'component_name': 'RevenueChartWidget',
            'default_config': {
                'show_revenue': True,
                'show_expenses': False,
                'currency': 'USD'
            },
            'config_schema': {
                'type': 'object',
                'properties': {
                    'show_revenue': {'type': 'boolean'},
                    'show_expenses': {'type': 'boolean'},
                    'currency': {'type': 'string'}
                }
            },
            'data_schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'date': {'type': 'string'},
                        'revenue': {'type': 'number'},
                        'expenses': {'type': 'number'}
                    }
                }
            },
            'category': 'financial',
            'subcategory': 'revenue',
            'tags': ['financial', 'revenue', 'payments'],
            'supports_filters': True,
            'supports_refresh': True,
            'supports_export': True,
            'supports_drilldown': True,
            'max_data_points': 30,
            'icon': 'cash',
            'color': '#27ae60',
            'default_size': 'medium',
            'is_system': True,
            'is_active': True,
            'version': '1.0.0',
            'sort_order': 7
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for widget_type_data in widget_types_data:
            # Check if widget type already exists by code
            existing_widget_type = WidgetType.query.filter_by(code=widget_type_data['code']).first()
            
            if existing_widget_type:
                # Update existing widget type
                print(f"🔄 Updating existing widget type: {widget_type_data['name']}")
                for key, value in widget_type_data.items():
                    setattr(existing_widget_type, key, value)
                updated_count += 1
            else:
                # Add new widget type
                print(f"✅ Adding new widget type: {widget_type_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in widget_type_data:
                    widget_type_data['public_id'] = str(uuid.uuid4())
                
                widget_type = WidgetType(**widget_type_data)
                db.session.add(widget_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Widget Types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📊 Widget Types added:")
            for widget_type_data in widget_types_data:
                widget_type = WidgetType.query.filter_by(code=widget_type_data['code']).first()
                if widget_type:
                    print(f"   • {widget_type.name} ({widget_type.code}) - {widget_type.category}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding widget types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_widget_types()