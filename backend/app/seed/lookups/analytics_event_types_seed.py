# app/seed/lookups/analytics_event_types_seed.py

from app import db
from app.models import AnalyticsEventType
import uuid


def seed_analytics_event_types():
    """Seed analytics event types with required code field"""
    
    event_types_data = [
        {
            'name': 'User Action',
            'code': 'USER_ACTION',
            'description': 'User-initiated actions in the system',
            'category': 'user',
            'severity': 'info',
            'requires_user_context': True,
            'is_system_event': False,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'System Event', 
            'code': 'SYSTEM_EVENT',
            'description': 'Automated system events and background processes',
            'category': 'system',
            'severity': 'info',
            'requires_user_context': False,
            'is_system_event': True,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Business Metric',
            'code': 'BUSINESS_METRIC',
            'description': 'Key business performance indicators and metrics',
            'category': 'business',
            'severity': 'info',
            'requires_user_context': False,
            'is_system_event': False,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Security Event',
            'code': 'SECURITY_EVENT',
            'description': 'Security-related events and access attempts',
            'category': 'security',
            'severity': 'warning',
            'requires_user_context': True,
            'is_system_event': False,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Error Event',
            'code': 'ERROR_EVENT',
            'description': 'System errors and exceptions',
            'category': 'system',
            'severity': 'error',
            'requires_user_context': False,
            'is_system_event': True,
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Performance Event',
            'code': 'PERFORMANCE_EVENT',
            'description': 'Performance metrics and timing events',
            'category': 'system',
            'severity': 'info',
            'requires_user_context': False,
            'is_system_event': True,
            'sort_order': 5,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for event_type_data in event_types_data:
            # Check if event type already exists by code
            existing_event_type = AnalyticsEventType.query.filter_by(code=event_type_data['code']).first()
            
            if existing_event_type:
                # Update existing event type
                print(f"🔄 Updating existing analytics event type: {event_type_data['name']}")
                for key, value in event_type_data.items():
                    setattr(existing_event_type, key, value)
                updated_count += 1
            else:
                # Add new event type
                print(f"✅ Adding new analytics event type: {event_type_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in event_type_data:
                    event_type_data['public_id'] = str(uuid.uuid4())
                
                event_type = AnalyticsEventType(**event_type_data)
                db.session.add(event_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Analytics Event Types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📊 Analytics Event Types added:")
            for event_type_data in event_types_data:
                event_type = AnalyticsEventType.query.filter_by(code=event_type_data['code']).first()
                if event_type:
                    print(f"   • {event_type.name} ({event_type.code}) - {event_type.category}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding analytics event types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_analytics_event_types()