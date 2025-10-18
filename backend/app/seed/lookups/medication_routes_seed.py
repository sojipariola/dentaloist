from app import db
from app.models.lookups import MedicationRoute
import uuid


def seed_medication_routes():
    """Seed Medication Routes with required code field"""
    
    data_list = [
{
    "code": "ORAL",
            "name": "Oral",
            "description": "Taken by mouth",
            "administration_instructions": "Take with water as directed",
            "requires_training": False,
            "is_active": True,
        },
{
    "code": "TOPICAL",
            "name": "Topical",
            "description": "Applied to skin or mucous membranes",
            "administration_instructions": "Apply to affected area as directed",
            "requires_training": False,
            "is_active": True,
        },
{
    "code": "SUBLINGUAL",
            "name": "Sublingual",
            "description": "Placed under the tongue",
            "administration_instructions": "Place under tongue and allow to dissolve",
            "requires_training": False,
            "is_active": True,
        },
{
    "code": "INTRAVENOUS",
            "name": "Intravenous",
            "description": "Injected into vein",
            "administration_instructions": "Administer by qualified healthcare professional",
            "requires_training": True,
            "is_active": True,
        },
{
    "code": "INTRAMUSCULAR",
            "name": "Intramuscular",
            "description": "Injected into muscle",
            "administration_instructions": "Administer by qualified healthcare professional",
            "requires_training": True,
            "is_active": True,
        },
{
    "code": "SUBCUTANEOUS",
            "name": "Subcutaneous",
            "description": "Injected under the skin",
            "administration_instructions": "Administer by qualified healthcare professional",
            "requires_training": True,
            "is_active": True,
        },
{
    "code": "INHALATION",
            "name": "Inhalation",
            "description": "Breathed into lungs",
            "administration_instructions": "Use inhaler as directed",
            "requires_training": True,
            "is_active": True,
        },
{
    "code": "RECTAL",
            "name": "Rectal",
            "description": "Administered via rectum",
            "administration_instructions": "Insert as directed",
            "requires_training": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = MedicationRoute.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Medication Route: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Medication Route: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = MedicationRoute(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Medication Routes seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Medication Routes: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_medication_routes()
