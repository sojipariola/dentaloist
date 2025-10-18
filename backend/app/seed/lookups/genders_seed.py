# app/seed/lookups/genders_seed.py

from app import db
from app.models import Gender
import uuid


def seed_genders():
    """Seed gender types with required code field"""
    
    genders_data = [
        {
            'name': 'Male',
            'code': 'MALE',  # ← ADD THIS REQUIRED FIELD
            'description': 'Male gender identity',
            'pronoun': 'he/him',
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Female', 
            'code': 'FEMALE',  # ← ADD THIS REQUIRED FIELD
            'description': 'Female gender identity',
            'pronoun': 'she/her',
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Non-Binary',
            'code': 'NON_BINARY',  # ← ADD THIS REQUIRED FIELD
            'description': 'Non-binary gender identity',
            'pronoun': 'they/them',
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Other',
            'code': 'OTHER',  # ← ADD THIS REQUIRED FIELD
            'description': 'Other gender identity',
            'pronoun': 'they/them',
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Prefer not to say',
            'code': 'PREFER_NOT_TO_SAY',  # ← ADD THIS REQUIRED FIELD
            'description': 'Prefer not to disclose gender',
            'pronoun': 'they/them',
            'sort_order': 4,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for gender_data in genders_data:
            # Check if gender already exists by code
            existing_gender = Gender.query.filter_by(code=gender_data['code']).first()
            
            if existing_gender:
                # Update existing gender
                print(f"🔄 Updating existing gender: {gender_data['name']}")
                for key, value in gender_data.items():
                    setattr(existing_gender, key, value)
                updated_count += 1
            else:
                # Add new gender
                print(f"✅ Adding new gender: {gender_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in gender_data:
                    gender_data['public_id'] = str(uuid.uuid4())
                
                gender = Gender(**gender_data)
                db.session.add(gender)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Genders seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("👤 Genders added:")
            for gender_data in genders_data:
                gender = Gender.query.filter_by(code=gender_data['code']).first()
                if gender:
                    print(f"   • {gender.name} ({gender.code}) - {gender.pronoun}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding genders: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_genders()