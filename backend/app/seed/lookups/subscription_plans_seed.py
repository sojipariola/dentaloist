from app import db
from app.models.lookups import SubscriptionPlan
import uuid


def seed_subscription_plans():
    """Seed Subscription Plans with required code field"""
    
    data_list = [
{
            'name': 'Free',
            'code': 'FREE',
            'description': 'Basic access for individual practitioners.',
            'price_monthly': 0.0,
            'price_yearly': 0.0,
            'max_users': 1,
            'max_patients': 50,
            'max_entries': 200,
            'features': {
                'appointments': True,
                'patient_records': True,
                'basic_reports': True,
                'advanced_reports': False,
                'cloud_backup': False,
                'multi_device_sync': False,
                'priority_support': False,
                'custom_branding': False,
                'api_access': False,
                'team_collaboration': False,
            },
            'is_active': True,
            'sort_order': 0,
            'color': '#6B7280'
        },
{
            'name': 'Professional',
            'code': 'PROFESSIONAL',
            'description': 'For growing practices with multiple practitioners.',
            'price_monthly': 49.99,
            'price_yearly': 499.99,
            'max_users': 5,
            'max_patients': 1000,
            'max_entries': 5000,
            'features': {
                'appointments': True,
                'patient_records': True,
                'basic_reports': True,
                'advanced_reports': True,
                'cloud_backup': True,
                'multi_device_sync': True,
                'priority_support': False,
                'custom_branding': False,
                'api_access': False,
                'team_collaboration': True,
            },
            'is_active': True,
            'sort_order': 1,
            'color': '#3B82F6'
        },
{
            "name": "Business",
            "code": "BUSINESS",
            "description": "For established practices with multiple locations.",
            "price_monthly": 99.99,
            "price_yearly": 999.99,
            "max_users": 25,
            "max_patients": 10000,
            "max_entries": 50000,
            "features": {
                "appointments": True,
                "patient_records": True,
                "basic_reports": True,
                "advanced_reports": True,
                "cloud_backup": True,
                "multi_device_sync": True,
                "priority_support": True,
                "custom_branding": True,
                "api_access": True,
                "team_collaboration": True,
            },
            'is_active': True,
            'sort_order': 2,
            'color': '#8B5CF6'
        },
{
            "name": "Enterprise",
            "code": "ENTERPRISE",
            "description": "Fully scalable plan for hospitals and dental networks.",
            "price_monthly": 249.99,
            "price_yearly": 2499.99,
            "max_users": 100,
            "max_patients": 50000,
            "max_entries": 200000,
            "features": {
                "appointments": True,
                "patient_records": True,
                "basic_reports": True,
                "advanced_reports": True,
                "cloud_backup": True,
                "multi_device_sync": True,
                "priority_support": True,
                "custom_branding": True,
                "api_access": True,
                "team_collaboration": True,
                "dedicated_support_manager": True,
                "custom_integrations": True,
            },
            'is_active': True,
            'sort_order': 3,
            'color': '#10B981'
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = SubscriptionPlan.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Subscription Plan: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Subscription Plan: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = SubscriptionPlan(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Subscription Plans seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Subscription Plans: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_subscription_plans()
