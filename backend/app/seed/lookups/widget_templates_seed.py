# app/seed/lookups/widget_templates_seed.py

from app import db
from app.models import WidgetTemplate
import uuid


def seed_widget_templates():
    """Seed widget templates with predefined configurations"""
    
    widget_templates_data = [
        {
            'name': 'Monthly Revenue Overview',
            'description': 'Template for monthly revenue tracking with comparisons',
            'widget_type': 'REVENUE_CHART',
            'default_config': {
                'show_revenue': True,
                'show_expenses': True,
                'currency': 'USD',
                'time_period': 'month',
                'compare_to_previous': True
            },
            'category': 'financial',
            'is_system': True
        },
        {
            'name': 'Patient Demographics',
            'description': 'Template for patient age and gender distribution',
            'widget_type': 'PIE_CHART',
            'default_config': {
                'show_labels': True,
                'show_percentages': True,
                'donut': True,
                'color_scheme': 'pastel'
            },
            'category': 'clinical',
            'is_system': True
        },
        {
            'name': 'Appointment Status Dashboard',
            'description': 'Overview of appointment statuses and completion rates',
            'widget_type': 'BAR_CHART',
            'default_config': {
                'orientation': 'horizontal',
                'stacked': False,
                'show_legend': True,
                'color_by': 'status'
            },
            'category': 'clinical',
            'is_system': True
        },
        {
            'name': 'Staff Performance Metrics',
            'description': 'Key performance indicators for dental staff',
            'widget_type': 'NUMBER_STAT',
            'default_config': {
                'format': 'number',
                'show_comparison': True,
                'comparison_period': 'previous_month'
            },
            'category': 'operational',
            'is_system': True
        },
        {
            'name': 'Treatment Popularity',
            'description': 'Most common treatments and procedures',
            'widget_type': 'BAR_CHART',
            'default_config': {
                'orientation': 'vertical',
                'stacked': False,
                'show_legend': False,
                'sort_by': 'value'
            },
            'category': 'clinical',
            'is_system': True
        },
        {
            'name': 'Monthly New Patients',
            'description': 'Track new patient acquisition over time',
            'widget_type': 'LINE_CHART',
            'default_config': {
                'smooth': True,
                'show_points': True,
                'show_legend': False,
                'time_period': 'month'
            },
            'category': 'clinical',
            'is_system': True
        },
        {
            'name': 'Payment Status Overview',
            'description': 'Overview of invoice and payment statuses',
            'widget_type': 'PIE_CHART',
            'default_config': {
                'show_labels': True,
                'show_percentages': True,
                'donut': False,
                'max_slices': 6
            },
            'category': 'financial',
            'is_system': True
        },
        {
            'name': 'Inventory Stock Levels',
            'description': 'Current inventory levels and low stock alerts',
            'widget_type': 'DATA_TABLE',
            'default_config': {
                'page_size': 15,
                'show_search': True,
                'show_pagination': True,
                'sort_by': 'quantity'
            },
            'category': 'inventory',
            'is_system': True
        },
        {
            'name': 'Treatment Room Utilization',
            'description': 'Usage statistics for treatment rooms',
            'widget_type': 'BAR_CHART',
            'default_config': {
                'orientation': 'horizontal',
                'stacked': True,
                'show_legend': True,
                'group_by': 'room'
            },
            'category': 'operational',
            'is_system': True
        },
        {
            'name': 'Patient Satisfaction Scores',
            'description': 'Patient feedback and satisfaction metrics',
            'widget_type': 'LINE_CHART',
            'default_config': {
                'smooth': False,
                'show_points': True,
                'show_legend': True,
                'y_axis_min': 0,
                'y_axis_max': 5
            },
            'category': 'clinical',
            'is_system': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for template_data in widget_templates_data:
            # Check if template already exists by name and widget_type
            existing_template = WidgetTemplate.query.filter_by(
                name=template_data['name'],
                widget_type=template_data['widget_type']
            ).first()
            
            if existing_template:
                # Update existing template
                print(f"🔄 Updating existing widget template: {template_data['name']}")
                for key, value in template_data.items():
                    setattr(existing_template, key, value)
                updated_count += 1
            else:
                # Add new template
                print(f"✅ Adding new widget template: {template_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in template_data:
                    template_data['public_id'] = str(uuid.uuid4())
                
                template = WidgetTemplate(**template_data)
                db.session.add(template)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Widget Templates seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("🎨 Widget Templates added:")
            for template_data in widget_templates_data:
                template = WidgetTemplate.query.filter_by(
                    name=template_data['name'],
                    widget_type=template_data['widget_type']
                ).first()
                if template:
                    print(f"   • {template.name} ({template.widget_type}) - {template.category}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding widget templates: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_widget_templates()