# app/seed/lookups/report_categories_seed.py

from app import db
from app.models import ReportCategory
import uuid


def seed_report_categories():
    """Seed report categories with required code field"""
    
    categories_data = [
        {
            'name': 'Clinical',
            'code': 'CLINICAL',
            'description': 'Patient care and clinical operations reports',
            'icon': 'medical-bag',
            'sort_order': 0,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Financial', 
            'code': 'FINANCIAL',
            'description': 'Revenue, expenses, and financial performance reports',
            'icon': 'cash',
            'sort_order': 1,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Operational',
            'code': 'OPERATIONAL',
            'description': 'Practice operations and efficiency reports',
            'icon': 'chart-bar',
            'sort_order': 2,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Patient',
            'code': 'PATIENT',
            'description': 'Patient demographics and satisfaction reports',
            'icon': 'account-group',
            'sort_order': 3,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Inventory',
            'code': 'INVENTORY',
            'description': 'Stock levels and supply chain reports',
            'icon': 'package-variant',
            'sort_order': 4,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Staff',
            'code': 'STAFF',
            'description': 'Staff performance and scheduling reports',
            'icon': 'account-tie',
            'sort_order': 5,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Compliance',
            'code': 'COMPLIANCE',
            'description': 'Regulatory and compliance reporting',
            'icon': 'shield-check',
            'sort_order': 6,
            'requires_permission': True,
            'is_active': True
        },
        {
            'name': 'Analytics',
            'code': 'ANALYTICS',
            'description': 'Advanced analytics and business intelligence',
            'icon': 'chart-box',
            'sort_order': 7,
            'requires_permission': True,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for category_data in categories_data:
            # Check if category already exists by code
            existing_category = ReportCategory.query.filter_by(code=category_data['code']).first()
            
            if existing_category:
                # Update existing category
                print(f"🔄 Updating existing report category: {category_data['name']}")
                for key, value in category_data.items():
                    setattr(existing_category, key, value)
                updated_count += 1
            else:
                # Add new category
                print(f"✅ Adding new report category: {category_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in category_data:
                    category_data['public_id'] = str(uuid.uuid4())
                
                category = ReportCategory(**category_data)
                db.session.add(category)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Report Categories seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📋 Report Categories added:")
            for category_data in categories_data:
                category = ReportCategory.query.filter_by(code=category_data['code']).first()
                if category:
                    permission = "Requires Permission" if category.requires_permission else "Open Access"
                    print(f"   • {category.name} - {category.icon} - {permission}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding report categories: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_report_categories()