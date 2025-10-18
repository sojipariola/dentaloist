from app import db
from app.models.lookups import InventoryTransactionType
import uuid


def seed_inventory_transaction_types():
    """Seed Inventory Transaction Types with required code field"""
    
    data_list = [
{
    "code": "PURCHASE",
            "name": "Purchase",
            "description": "Inventory purchase from supplier",
            "affects_stock": True,
            "stock_direction": "in",
            "requires_approval": False,
            "is_active": True,
        },
{
    "code": "SALE",
            "name": "Sale",
            "description": "Inventory sale to patient",
            "affects_stock": True,
            "stock_direction": "out",
            "requires_approval": False,
            "is_active": True,
        },
{
    "code": "ADJUSTMENT",
            "name": "Adjustment",
            "description": "Stock level adjustment",
            "affects_stock": True,
            "stock_direction": "neutral",
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "TRANSFER",
            "name": "Transfer",
            "description": "Transfer between locations",
            "affects_stock": True,
            "stock_direction": "neutral",
            "requires_approval": False,
            "is_active": True,
        },
{
    "code": "RETURN",
            "name": "Return",
            "description": "Return to supplier",
            "affects_stock": True,
            "stock_direction": "out",
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "WRITE_OFF",
            "name": "Write-off",
            "description": "Inventory write-off",
            "affects_stock": True,
            "stock_direction": "out",
            "requires_approval": True,
            "is_active": True,
        },
{
    "code": "PRODUCTION",
            "name": "Production",
            "description": "Internal production",
            "affects_stock": True,
            "stock_direction": "in",
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
            existing = InventoryTransactionType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Inventory Transaction Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Inventory Transaction Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = InventoryTransactionType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Inventory Transaction Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Inventory Transaction Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_inventory_transaction_types()
