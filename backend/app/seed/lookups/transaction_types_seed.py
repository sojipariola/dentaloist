from app import db
from app.models.lookups import TransactionType
import uuid


def seed_transaction_types():
    """Seed Transaction Types with required code field"""
    
    data_list = [
{
            "code": "INV_PAYMENT",
            "name": "Invoice Payment",
            "description": "Payment received for invoice",
            "category": "revenue",
            "is_system": False,
            "requires_verification": False,
            "is_active": True,
        },
{
            "code": "REFUND",
            "name": "Payment Refund",
            "description": "Refund issued to patient",
            "category": "expense",
            "is_system": False,
            "requires_verification": True,
            "is_active": True,
        },
{
            "code": "ADJUSTMENT",
            "name": "Payment Adjustment",
            "description": "Payment amount adjustment",
            "category": "adjustment",
            "is_system": False,
            "requires_verification": True,
            "is_active": True,
        },
{
            "code": "WRITE_OFF",
            "name": "Write Off",
            "description": "Uncollectible amount written off",
            "category": "adjustment",
            "is_system": False,
            "requires_verification": True,
            "is_active": True,
        },
{
            "code": "INSURANCE_PAYMENT",
            "name": "Insurance Payment",
            "description": "Payment received from insurance",
            "category": "revenue",
            "is_system": False,
            "requires_verification": False,
            "is_active": True,
        },
{
            "code": "EXPENSE",
            "name": "Expense",
            "description": "Practice expense",
            "category": "expense",
            "is_system": False,
            "requires_verification": True,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = TransactionType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Transaction Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Transaction Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = TransactionType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Transaction Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Transaction Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_transaction_types()
