from app import db
from app.models.lookups import Currency
import uuid


def seed_currencies():
    """Seed Currencies with required code field"""
    
    data_list = [
{
            "name": "US Dollar",
            "description": "United States Dollar",
            "symbol": "$",
            "code": "USD",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Euro",
            "description": "European Euro",
            "symbol": "€",
            "code": "EUR",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "British Pound",
            "description": "British Pound Sterling",
            "symbol": "£",
            "code": "GBP",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Japanese Yen",
            "description": "Japanese Yen",
            "symbol": "¥",
            "code": "JPY",
            "decimal_places": 0,
            "is_active": True,
        },
{
            "name": "Canadian Dollar",
            "description": "Canadian Dollar",
            "symbol": "C$",
            "code": "CAD",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Australian Dollar",
            "description": "Australian Dollar",
            "symbol": "A$",
            "code": "AUD",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Swiss Franc",
            "description": "Swiss Franc",
            "symbol": "CHF",
            "code": "CHF",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Chinese Yuan",
            "description": "Chinese Yuan Renminbi",
            "symbol": "¥",
            "code": "CNY",
            "decimal_places": 2,
            "is_active": True,
        },
{
            "name": "Naira",
            "description": "Nigerian Naira",
            "symbol": "₦",
            "code": "NGN",
            "decimal_places": 2,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = Currency.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Currencie: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Currencie: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = Currency(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Currencies seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Currencies: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_currencies()
