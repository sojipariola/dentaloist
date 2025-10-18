from app import db
from app.models.lookups import TreatmentPriority
import uuid


def seed_treatment_priorities():
    """Seed Treatment Priorities with required code field"""
    
    data_list = [
{
    "code": "ROUTINE",
            "name": "Routine",
            "description": "Standard treatment that can be scheduled normally",
            "is_active": True,
        },
{
    "code": "URGENT",
            "name": "Urgent",
            "description": "Treatment requiring prompt attention within days",
            "is_active": True,
        },
{
    "code": "EMERGENCY",
            "name": "Emergency",
            "description": "Immediate treatment required for pain or infection",
            "is_active": True,
        },
{
    "code": "PREVENTIVE",
            "name": "Preventive",
            "description": "Preventive care and routine maintenance",
            "is_active": True,
        },
{
    "code": "COSMETIC",
            "name": "Cosmetic",
            "description": "Elective cosmetic procedures",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = TreatmentPriority.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Treatment Prioritie: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Treatment Prioritie: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = TreatmentPriority(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Treatment Priorities seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Treatment Priorities: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_treatment_priorities()
