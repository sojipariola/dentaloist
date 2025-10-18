from app import db
from app.models.lookups import NotificationType
import uuid


def seed_notification_types():
    """Seed Notification Types with required code field"""
    
    data_list = [
{
    "code": "APPOINTMENT_REMINDER",
            "name": "Appointment Reminder",
            "description": "Reminder for upcoming appointments",
            "priority": "normal",
            "auto_expire_days": 1,
            "requires_action": False,
            "template": "Reminder: You have an appointment with {patient} on {date} at {time}",
            "is_active": True,
        },
{
    "code": "PAYMENT_DUE",
            "name": "Payment Due",
            "description": "Notification for overdue payments",
            "priority": "high",
            "auto_expire_days": 7,
            "requires_action": True,
            "template": "Payment overdue for {patient}. Amount: {amount}",
            "is_active": True,
        },
{
    "code": "LOW_STOCK_ALERT",
            "name": "Low Stock Alert",
            "description": "Inventory items running low",
            "priority": "normal",
            "auto_expire_days": 3,
            "requires_action": True,
            "template": "Low stock alert: {item} is below minimum level",
            "is_active": True,
        },
{
    "code": "NEW_MESSAGE",
            "name": "New Message",
            "description": "New message from patient or staff",
            "priority": "normal",
            "auto_expire_days": 30,
            "requires_action": True,
            "template": "New message from {sender}",
            "is_active": True,
        },
{
    "code": "SYSTEM_ALERT",
            "name": "System Alert",
            "description": "Important system notifications",
            "priority": "high",
            "auto_expire_days": 7,
            "requires_action": True,
            "template": "System Alert: {message}",
            "is_active": True,
        },
{
    "code": "INSURANCE_CLAIM_STATUS",
            "name": "Insurance Claim Status",
            "description": "Update on insurance claim processing",
            "priority": "normal",
            "auto_expire_days": 14,
            "requires_action": False,
            "template": "Insurance claim {claim_id} status updated to {status}",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = NotificationType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Notification Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Notification Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = NotificationType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Notification Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Notification Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_notification_types()
