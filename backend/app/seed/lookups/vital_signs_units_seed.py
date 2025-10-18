from app import db
from app.models.lookups import VitalSignsUnit
import uuid


def seed_vital_signs_units():
    """Seed Vital Signs Units with required code field"""
    
    data_list = [
{
    "code": "MMHG",
            "name": "mmHg",
            "description": "Millimeters of mercury",
            "unit_type": "pressure",
            "conversion_factor": 1.0,
            "si_unit": "Pa",
            "is_active": True,
        },
{
    "code": "BPM",
            "name": "bpm",
            "description": "Beats per minute",
            "unit_type": "rate",
            "conversion_factor": 1.0,
            "si_unit": "s⁻¹",
            "is_active": True,
        },
{
    "code": "°C",
            "name": "°C",
            "description": "Degrees Celsius",
            "unit_type": "temperature",
            "conversion_factor": 1.0,
            "si_unit": "K",
            "is_active": True,
        },
{
    "code": "°F",
            "name": "°F",
            "description": "Degrees Fahrenheit",
            "unit_type": "temperature",
            "conversion_factor": 0.5556,
            "si_unit": "K",
            "is_active": True,
        },
{
    "code": "BREATHS/MIN",
            "name": "breaths/min",
            "description": "Breaths per minute",
            "unit_type": "rate",
            "conversion_factor": 1.0,
            "si_unit": "s⁻¹",
            "is_active": True,
        },
{
    "code": "%",
            "name": "%",
            "description": "Percentage",
            "unit_type": "concentration",
            "conversion_factor": 1.0,
            "si_unit": "1",
            "is_active": True,
        },
{
    "code": "KG",
            "name": "kg",
            "description": "Kilograms",
            "unit_type": "mass",
            "conversion_factor": 1.0,
            "si_unit": "kg",
            "is_active": True,
        },
{
    "code": "CM",
            "name": "cm",
            "description": "Centimeters",
            "unit_type": "length",
            "conversion_factor": 0.01,
            "si_unit": "m",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = VitalSignsUnit.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Vital Signs Unit: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Vital Signs Unit: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = VitalSignsUnit(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Vital Signs Units seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Vital Signs Units: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_vital_signs_units()
