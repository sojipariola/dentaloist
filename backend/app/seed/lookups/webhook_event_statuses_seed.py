from app import db
from app.models.lookups import WebhookEventStatus
import uuid


def seed_webhook_event_statuses():
    """Seed Webhook Event Statuses with required code field"""
    
    data_list = [
{
    "code": "PENDING",
            "name": "Pending",
            "description": "Event is pending processing",
            "is_final_status": False,
            "allows_retry": True,
            "max_retries": 3,
            "is_active": True,
        },
{
    "code": "PROCESSING",
            "name": "Processing",
            "description": "Event is being processed",
            "is_final_status": False,
            "allows_retry": False,
            "max_retries": 3,
            "is_active": True,
        },
{
    "code": "DELIVERED",
            "name": "Delivered",
            "description": "Event successfully delivered",
            "is_final_status": True,
            "allows_retry": False,
            "max_retries": 3,
            "is_active": True,
        },
{
    "code": "FAILED",
            "name": "Failed",
            "description": "Event delivery failed",
            "is_final_status": False,
            "allows_retry": True,
            "max_retries": 3,
            "is_active": True,
        },
{
    "code": "RETRY_EXHAUSTED",
            "name": "Retry Exhausted",
            "description": "All retry attempts exhausted",
            "is_final_status": True,
            "allows_retry": False,
            "max_retries": 3,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = WebhookEventStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Webhook Event Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Webhook Event Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = WebhookEventStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Webhook Event Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Webhook Event Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_webhook_event_statuses()
