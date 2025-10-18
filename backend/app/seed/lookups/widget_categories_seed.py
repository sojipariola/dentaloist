# app/seed/lookups/widget_categories_seed.py

from app import db
from app.models import WidgetCategory
import uuid


def seed_widget_categories():
    """Seed widget categories with required code field"""
    
    categories_data = [
        {
            'name': 'Clinical Overview',
            'code': 'CLINICAL_OVERVIEW',
            'description': 'Patient care and clinical performance widgets',
            'icon': 'medical-bag',
            'color': '#e74c3c',
            'sort_order': 0,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Financial Metrics', 
            'code': 'FINANCIAL_METRICS',
            'description': 'Revenue, expenses, and financial performance widgets',
            'icon': 'cash',
            'color': '#27ae60',
            'sort_order': 1,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Operational Efficiency',
            'code': 'OPERATIONAL_EFFICIENCY',
            'description': 'Practice operations and workflow widgets',
            'icon': 'chart-bar',
            'color': '#3498db',
            'sort_order': 2,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Patient Analytics',
            'code': 'PATIENT_ANALYTICS',
            'description': 'Patient demographics and satisfaction widgets',
            'icon': 'account-group',
            'color': '#9b59b6',
            'sort_order': 3,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Staff Performance',
            'code': 'STAFF_PERFORMANCE',
            'description': 'Staff productivity and scheduling widgets',
            'icon': 'account-tie',
            'color': '#f39c12',
            'sort_order': 4,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Inventory Management',
            'code': 'INVENTORY_MANAGEMENT',
            'description': 'Stock levels and supply chain widgets',
            'icon': 'package-variant',
            'color': '#16a085',
            'sort_order': 5,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Appointment Tracking',
            'code': 'APPOINTMENT_TRACKING',
            'description': 'Appointment scheduling and status widgets',
            'icon': 'calendar',
            'color': '#d35400',
            'sort_order': 6,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'System Health',
            'code': 'SYSTEM_HEALTH',
            'description': 'System performance and monitoring widgets',
            'icon': 'monitor-dashboard',
            'color': '#7f8c8d',
            'sort_order': 7,
            'is_system': True,
            'is_active': True
        },
        {
            'name': 'Custom Widgets',
            'code': 'CUSTOM_WIDGETS',
            'description': 'User-created custom widgets',
            'icon': 'puzzle',
            'color': '#95a5a6',
            'sort_order': 8,
            'is_system': False,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for category_data in categories_data:
            # Check if category already exists by code
            existing_category = WidgetCategory.query.filter_by(code=category_data['code']).first()
            
            if existing_category:
                # Update existing category
                print(f"🔄 Updating existing widget category: {category_data['name']}")
                for key, value in category_data.items():
                    setattr(existing_category, key, value)
                updated_count += 1
            else:
                # Add new category
                print(f"✅ Adding new widget category: {category_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in category_data:
                    category_data['public_id'] = str(uuid.uuid4())
                
                category = WidgetCategory(**category_data)
                db.session.add(category)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Widget Categories seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📊 Widget Categories added:")
            for category_data in categories_data:
                category = WidgetCategory.query.filter_by(code=category_data['code']).first()
                if category:
                    category_type = "System" if category.is_system else "Custom"
                    print(f"   • {category.name} - {category.color} - {category_type}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding widget categories: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_widget_categories()