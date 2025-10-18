from app import db
from app.models.lookups import PaymentMethod
import uuid


def seed_payment_methods():
    """Seed Payment Methods with required code field"""
    
    data_list = [
{
    "code": "CASH",
            "name": "Cash",
            "description": "Cash payment",
            "category": "cash",
            "requires_processing": False,
            "processing_fee_percentage": 0.0,
            "is_online": False,
            "is_active": True,
        },
{
    "code": "CREDIT_CARD",
            "name": "Credit Card",
            "description": "Credit card payment",
            "category": "card",
            "requires_processing": True,
            "processing_fee_percentage": 2.9,
            "is_online": True,
            "is_active": True,
        },
{
    "code": "DEBIT_CARD",
            "name": "Debit Card",
            "description": "Debit card payment",
            "category": "card",
            "requires_processing": True,
            "processing_fee_percentage": 1.5,
            "is_online": True,
            "is_active": True,
        },
{
    "code": "BANK_TRANSFER",
            "name": "Bank Transfer",
            "description": "Electronic bank transfer",
            "category": "transfer",
            "requires_processing": True,
            "processing_fee_percentage": 1.0,
            "is_online": True,
            "is_active": True,
        },
{
    "code": "INSURANCE",
            "name": "Insurance",
            "description": "Payment through insurance provider",
            "category": "insurance",
            "requires_processing": True,
            "processing_fee_percentage": 0.0,
            "is_online": False,
            "is_active": True,
        },
{
    "code": "CHECK",
            "name": "Check",
            "description": "Personal or business check",
            "category": "check",
            "requires_processing": True,
            "processing_fee_percentage": 0.5,
            "is_online": False,
            "is_active": True,
        },
{
    "code": "DIGITAL_WALLET",
            "name": "Digital Wallet",
            "description": "Payment through digital wallet (Apple Pay, Google Pay)",
            "category": "digital",
            "requires_processing": True,
            "processing_fee_percentage": 2.5,
            "is_online": True,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = PaymentMethod.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Payment Method: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Payment Method: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = PaymentMethod(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Payment Methods seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Payment Methods: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_payment_methods()
