from app import db
from app.models.lookups import InventoryAdjustmentType
import uuid


def seed_inventory_adjustment_types():
    """Seed Inventory Adjustment Types with required code field"""
    
    data_list = [
{
    "code": "STOCK_COUNT",
            "name": "Stock Count",
            "description": "Adjustment from physical stock count",
            "stock_impact": "correction",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "THEFT/LOSS",
            "name": "Theft/Loss",
            "description": "Adjustment for stolen or lost items",
            "stock_impact": "decrease",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "DAMAGE",
            "name": "Damage",
            "description": "Adjustment for damaged items",
            "stock_impact": "decrease",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "EXPIRATION",
            "name": "Expiration",
            "description": "Adjustment for expired items",
            "stock_impact": "decrease",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "DONATION",
            "name": "Donation",
            "description": "Items donated or given away",
            "stock_impact": "decrease",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "FOUND_STOCK",
            "name": "Found Stock",
            "description": "Previously unaccounted stock found",
            "stock_impact": "increase",
            "requires_reason": True,
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "SYSTEM_CORRECTION",
            "name": "System Correction",
            "description": "System-generated correction",
            "stock_impact": "correction",
            "requires_reason": True,
            "requires_approval": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = InventoryAdjustmentType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Inventory Adjustment Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Inventory Adjustment Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = InventoryAdjustmentType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Inventory Adjustment Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Inventory Adjustment Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_inventory_adjustment_types()
