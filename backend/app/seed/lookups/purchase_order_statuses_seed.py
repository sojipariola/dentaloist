from app import db
from app.models.lookups import PurchaseOrderStatus
import uuid


def seed_purchase_order_statuses():
    """Seed Purchase Order Statuses with required code field"""
    
    data_list = [
{
    "code": "DRAFT",
            "name": "Draft",
            "description": "Purchase order in draft stage",
            "allows_editing": True,
            "is_final": False,
            "send_notifications": False,
            "is_active": True,
        },
{
    "code": "SUBMITTED",
            "name": "Submitted",
            "description": "Purchase order submitted to supplier",
            "allows_editing": False,
            "is_final": False,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "APPROVED",
            "name": "Approved",
            "description": "Purchase order approved",
            "allows_editing": False,
            "is_final": False,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "ORDERED",
            "name": "Ordered",
            "description": "Purchase order placed with supplier",
            "allows_editing": False,
            "is_final": False,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "RECEIVED",
            "name": "Received",
            "description": "Items received from supplier",
            "allows_editing": False,
            "is_final": False,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "COMPLETED",
            "name": "Completed",
            "description": "Purchase order fully received",
            "allows_editing": False,
            "is_final": True,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "CANCELLED",
            "name": "Cancelled",
            "description": "Purchase order cancelled",
            "allows_editing": False,
            "is_final": True,
            "send_notifications": True,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = PurchaseOrderStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Purchase Order Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Purchase Order Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = PurchaseOrderStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Purchase Order Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Purchase Order Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_purchase_order_statuses()
