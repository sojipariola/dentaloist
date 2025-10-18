from app import db
from app.models.lookups import TreatmentType
import uuid


def seed_treatment_types():
    """Seed Treatment Types with required code field"""
    
    data_list = [
{
    "code": "DENTAL_CLEANING",
            "name": "Dental Cleaning",
            "description": "Professional teeth cleaning and polishing",
            "category": "preventive",
            "complexity_level": "simple",
            "typical_duration": 45,
            "is_active": True,
        },
{
    "code": "COMPOSITE_FILLING",
            "name": "Composite Filling",
            "description": "Tooth-colored composite resin filling",
            "category": "restorative",
            "complexity_level": "simple",
            "typical_duration": 60,
            "is_active": True,
        },
{
    "code": "ROOT_CANAL_THERAPY",
            "name": "Root Canal Therapy",
            "description": "Endodontic treatment for infected pulp",
            "category": "endodontic",
            "complexity_level": "complex",
            "typical_duration": 90,
            "is_active": True,
        },
{
    "code": "DENTAL_CROWN",
            "name": "Dental Crown",
            "description": "Tooth restoration with dental crown",
            "category": "restorative",
            "complexity_level": "moderate",
            "typical_duration": 75,
            "is_active": True,
        },
{
    "code": "TOOTH_EXTRACTION",
            "name": "Tooth Extraction",
            "description": "Surgical removal of a tooth",
            "category": "surgical",
            "complexity_level": "moderate",
            "typical_duration": 45,
            "is_active": True,
        },
{
    "code": "DENTAL_IMPLANT",
            "name": "Dental Implant",
            "description": "Surgical placement of dental implant",
            "category": "surgical",
            "complexity_level": "complex",
            "typical_duration": 120,
            "is_active": True,
        },
{
    "code": "TEETH_WHITENING",
            "name": "Teeth Whitening",
            "description": "Professional teeth whitening treatment",
            "category": "cosmetic",
            "complexity_level": "simple",
            "typical_duration": 60,
            "is_active": True,
        },
{
    "code": "ORTHODONTIC_ADJUSTMENT",
            "name": "Orthodontic Adjustment",
            "description": "Braces or aligner adjustment",
            "category": "orthodontic",
            "complexity_level": "simple",
            "typical_duration": 30,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = TreatmentType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Treatment Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Treatment Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = TreatmentType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Treatment Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Treatment Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_treatment_types()
