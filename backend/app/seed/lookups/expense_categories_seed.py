from app import db
from app.models.lookups import ExpenseCategory
import uuid


def seed_expense_categories():
    """Seed Expense Categories with required code field"""
    
    data_list = [
{
    "code": "OFFICE_SUPPLIES",
            "name": "Office Supplies",
            "description": "General office supplies and stationery",
            "is_tax_deductible": True,
            "requires_approval": False,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "MEDICAL_SUPPLIES",
            "name": "Medical Supplies",
            "description": "Medical and dental supplies",
            "is_tax_deductible": True,
            "requires_approval": False,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "EQUIPMENT_PURCHASE",
            "name": "Equipment Purchase",
            "description": "Purchase of medical equipment",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "capital",
            "is_active": True,
        },
{
    "code": "EQUIPMENT_MAINTENANCE",
            "name": "Equipment Maintenance",
            "description": "Equipment repair and maintenance",
            "is_tax_deductible": True,
            "requires_approval": False,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "STAFF_SALARIES",
            "name": "Staff Salaries",
            "description": "Employee salaries and wages",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "personnel",
            "is_active": True,
        },
{
    "code": "RENT",
            "name": "Rent",
            "description": "Office and facility rent",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "UTILITIES",
            "name": "Utilities",
            "description": "Electricity, water, internet, etc.",
            "is_tax_deductible": True,
            "requires_approval": False,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "PROFESSIONAL_FEES",
            "name": "Professional Fees",
            "description": "Legal, accounting, and consulting fees",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "MARKETING",
            "name": "Marketing",
            "description": "Advertising and marketing expenses",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "operational",
            "is_active": True,
        },
{
    "code": "TRAVEL",
            "name": "Travel",
            "description": "Business travel expenses",
            "is_tax_deductible": True,
            "requires_approval": True,
            "budget_category": "operational",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = ExpenseCategory.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Expense Categorie: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Expense Categorie: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = ExpenseCategory(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Expense Categories seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Expense Categories: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_expense_categories()
