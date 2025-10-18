from app import db
from app.models.lookups import PaymentStatus
import uuid


def seed_payment_statuses():
    """Seed Payment Statuses with required code field"""
    
    data_list = [
{
    "code": "PENDING",
            "name": "Pending",
            "description": "Payment is pending processing",
            "is_completed": False,
            "allows_refund": False,
            "requires_action": False,
            "is_active": True,
        },
{
    "code": "PROCESSING",
            "name": "Processing",
            "description": "Payment is being processed",
            "is_completed": False,
            "allows_refund": False,
            "requires_action": False,
            "is_active": True,
        },
{
    "code": "COMPLETED",
            "name": "Completed",
            "description": "Payment successfully completed",
            "is_completed": True,
            "allows_refund": True,
            "requires_action": False,
            "is_active": True,
        },
{
    "code": "FAILED",
            "name": "Failed",
            "description": "Payment processing failed",
            "is_completed": False,
            "allows_refund": False,
            "requires_action": True,
            "is_active": True,
        },
{
    "code": "REFUNDED",
            "name": "Refunded",
            "description": "Payment has been refunded",
            "is_completed": True,
            "allows_refund": False,
            "requires_action": False,
            "is_active": True,
        },
{
    "code": "PARTIALLY_REFUNDED",
            "name": "Partially Refunded",
            "description": "Partial refund processed",
            "is_completed": False,
            "allows_refund": True,
            "requires_action": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = PaymentStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Payment Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Payment Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = PaymentStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Payment Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Payment Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_payment_statuses()
