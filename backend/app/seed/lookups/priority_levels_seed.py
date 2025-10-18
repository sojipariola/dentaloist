from app import db
from app.models.lookups import PriorityLevel
import uuid


def seed_priority_levels():
    """Seed Priority Levels with required code field"""
    
    data_list = [
{
    "code": "LOW",
            "name": "Low",
            "description": "Non-urgent matter that can be addressed later",
            "escalation_hours": 72,
            "requires_immediate_attention": False,
            "is_active": True,
        },
{
    "code": "NORMAL",
            "name": "Normal",
            "description": "Standard priority for routine matters",
            "escalation_hours": 48,
            "requires_immediate_attention": False,
            "is_active": True,
        },
{
    "code": "HIGH",
            "name": "High",
            "description": "Important matter requiring prompt attention",
            "escalation_hours": 24,
            "requires_immediate_attention": False,
            "is_active": True,
        },
{
    "code": "URGENT",
            "name": "Urgent",
            "description": "Critical matter requiring immediate attention",
            "escalation_hours": 4,
            "requires_immediate_attention": True,
            "is_active": True,
        },
{
    "code": "EMERGENCY",
            "name": "Emergency",
            "description": "Life-threatening or critical emergency",
            "escalation_hours": 1,
            "requires_immediate_attention": True,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = PriorityLevel.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Priority Level: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Priority Level: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = PriorityLevel(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Priority Levels seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Priority Levels: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_priority_levels()
