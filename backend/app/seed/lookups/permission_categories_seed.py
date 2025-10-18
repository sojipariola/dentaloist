from app import db
from app.models.lookups import PermissionCategory
import uuid


def seed_permission_categories():
    """Seed Permission Categories with required code field"""
    
    data_list = [
{
    "code": "PATIENT_MANAGEMENT",
            "name": "Patient Management",
            "description": "Permissions related to patient records",
            "module": "patient",
            "sort_order": 1,
            "is_active": True,
        },
{
    "code": "APPOINTMENT_SCHEDULING",
            "name": "Appointment Scheduling",
            "description": "Permissions for appointment management",
            "module": "appointment",
            "sort_order": 2,
            "is_active": True,
        },
{
    "code": "CLINICAL_RECORDS",
            "name": "Clinical Records",
            "description": "Permissions for clinical documentation",
            "module": "clinical",
            "sort_order": 3,
            "is_active": True,
        },
{
    "code": "FINANCIAL",
            "name": "Financial",
            "description": "Permissions for billing and payments",
            "module": "financial",
            "sort_order": 4,
            "is_active": True,
        },
{
    "code": "INVENTORY",
            "name": "Inventory",
            "description": "Permissions for inventory management",
            "module": "inventory",
            "sort_order": 5,
            "is_active": True,
        },
{
    "code": "REPORTS",
            "name": "Reports",
            "description": "Permissions for reporting and analytics",
            "module": "reports",
            "sort_order": 6,
            "is_active": True,
        },
{
    "code": "SYSTEM_ADMINISTRATION",
            "name": "System Administration",
            "description": "Permissions for system configuration",
            "module": "system",
            "sort_order": 7,
            "is_active": True,
        },
{
    "code": "USER_MANAGEMENT",
            "name": "User Management",
            "description": "Permissions for user administration",
            "module": "users",
            "sort_order": 8,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = PermissionCategory.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Permission Categorie: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Permission Categorie: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = PermissionCategory(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Permission Categories seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Permission Categories: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_permission_categories()
