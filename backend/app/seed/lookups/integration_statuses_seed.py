from app import db
from app.models.lookups import IntegrationStatus
import uuid


def seed_integration_statuses():
    """Seed Integration Statuses with required code field"""
    
    data_list = [
{
    "code": "ACTIVE",
            "name": "Active",
            "description": "Integration is active and syncing",
            "allows_sync": True,
            "requires_attention": False,
            "retry_allowed": True,
            "is_active": True,
        },
{
    "code": "INACTIVE",
            "name": "Inactive",
            "description": "Integration is inactive",
            "allows_sync": False,
            "requires_attention": False,
            "retry_allowed": False,
            "is_active": True,
        },
{
    "code": "ERROR",
            "name": "Error",
            "description": "Integration has errors",
            "allows_sync": False,
            "requires_attention": True,
            "retry_allowed": True,
            "is_active": True,
        },
{
    "code": "PENDING",
            "name": "Pending",
            "description": "Integration is being set up",
            "allows_sync": False,
            "requires_attention": False,
            "retry_allowed": True,
            "is_active": True,
        },
{
    "code": "MAINTENANCE",
            "name": "Maintenance",
            "description": "Integration in maintenance mode",
            "allows_sync": False,
            "requires_attention": False,
            "retry_allowed": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = IntegrationStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Integration Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Integration Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = IntegrationStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Integration Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Integration Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_integration_statuses()
