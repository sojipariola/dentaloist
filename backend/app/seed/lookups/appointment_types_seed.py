from app import db
from app.models.lookups import AppointmentType
import uuid


def seed_appointment_types():
    """Seed Appointment Types with required code field"""
    
    data_list = [
{
    "code": "CONSULTATION",
            "name": "Consultation",
            "description": "Initial patient consultation and assessment",
            "default_duration": 30,
            "requires_specialist": False,
            "category": "consultation",
            "is_active": True,
        },
{
    "code": "ROUTINE_CHECKUP",
            "name": "Routine Checkup",
            "description": "Regular dental checkup and cleaning",
            "default_duration": 45,
            "requires_specialist": False,
            "category": "preventive",
            "is_active": True,
        },
{
    "code": "FILLING",
            "name": "Filling",
            "description": "Dental filling procedure",
            "default_duration": 60,
            "requires_specialist": False,
            "category": "restorative",
            "is_active": True,
        },
{
    "code": "ROOT_CANAL",
            "name": "Root Canal",
            "description": "Root canal treatment",
            "default_duration": 90,
            "requires_specialist": True,
            "category": "endodontic",
            "is_active": True,
        },
{
    "code": "CROWN_PLACEMENT",
            "name": "Crown Placement",
            "description": "Dental crown placement",
            "default_duration": 75,
            "requires_specialist": False,
            "category": "restorative",
            "is_active": True,
        },
{
    "code": "EMERGENCY",
            "name": "Emergency",
            "description": "Emergency dental treatment",
            "default_duration": 30,
            "requires_specialist": False,
            "category": "emergency",
            "is_active": True,
        },
{
    "code": "ORTHODONTIC",
            "name": "Orthodontic",
            "description": "Braces adjustment and orthodontic treatment",
            "default_duration": 30,
            "requires_specialist": True,
            "category": "orthodontic",
            "is_active": True,
        },
{
    "code": "SURGICAL",
            "name": "Surgical",
            "description": "Oral surgery procedures",
            "default_duration": 120,
            "requires_specialist": True,
            "category": "surgical",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = AppointmentType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Appointment Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Appointment Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = AppointmentType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Appointment Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Appointment Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_appointment_types()
