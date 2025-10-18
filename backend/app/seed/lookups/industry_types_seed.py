from app import db
from app.models.lookups import IndustryType
import uuid


def seed_industry_types():
    """Seed Industry Types with required code field"""
    
    data_list = [
{
    "code": "GENERAL_DENTISTRY",
            "name": "General Dentistry",
            "description": "General dental practice",
            "category": "dental",
            "requires_license": True,
            "special_requirements": {
                "dental_license": True,
                "malpractice_insurance": True
            },
            "is_active": True,
        },
{
    "code": "ORTHODONTICS",
            "name": "Orthodontics",
            "description": "Orthodontic specialty practice",
            "category": "dental",
            "requires_license": True,
            "special_requirements": {
                "orthodontic_specialty": True,
                "dental_license": True,
                "malpractice_insurance": True
            },
            "is_active": True,
        },
{
    "code": "ORAL_SURGERY",
            "name": "Oral Surgery",
            "description": "Oral and maxillofacial surgery",
            "category": "dental",
            "requires_license": True,
            "special_requirements": {
                "surgical_privileges": True,
                "dental_license": True,
                "medical_license": True
            },
            "is_active": True,
        },
{
    "code": "PEDIATRIC_DENTISTRY",
            "name": "Pediatric Dentistry",
            "description": "Dental care for children",
            "category": "dental",
            "requires_license": True,
            "special_requirements": {
                "pediatric_specialty": True,
                "dental_license": True
            },
            "is_active": True,
        },
{
    "code": "MEDICAL_CLINIC",
            "name": "Medical Clinic",
            "description": "General medical practice",
            "category": "medical",
            "requires_license": True,
            "special_requirements": {
                "medical_license": True,
                "clinic_license": True
            },
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = IndustryType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Industry Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Industry Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = IndustryType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Industry Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Industry Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_industry_types()
