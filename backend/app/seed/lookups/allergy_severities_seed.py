from app import db
from app.models.lookups import AllergySeverity
import uuid


def seed_allergy_severities():
    """Seed Allergy Severities with required code field"""
    
    data_list = [
{
    "code": "MILD",
            "name": "Mild",
            "description": "Minor reaction, no treatment required",
            "requires_emergency_care": False,
            "risk_level": "low",
            "is_active": True,
        },
{
    "code": "MODERATE",
            "name": "Moderate",
            "description": "Significant reaction, may require treatment",
            "requires_emergency_care": False,
            "risk_level": "medium",
            "is_active": True,
        },
{
    "code": "SEVERE",
            "name": "Severe",
            "description": "Serious reaction requiring medical attention",
            "requires_emergency_care": True,
            "risk_level": "high",
            "is_active": True,
        },
{
    "code": "ANAPHYLACTIC",
            "name": "Anaphylactic",
            "description": "Life-threatening allergic reaction",
            "requires_emergency_care": True,
            "risk_level": "critical",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = AllergySeverity.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Allergy Severitie: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Allergy Severitie: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = AllergySeverity(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Allergy Severities seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Allergy Severities: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_allergy_severities()
