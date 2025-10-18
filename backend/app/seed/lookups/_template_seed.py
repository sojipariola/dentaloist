"""
TEMPLATE for lookup seeder files
Copy this template and replace placeholders for new lookup seeders
"""

from app import db
from app.models.lookups import [MODEL_CLASS]
import uuid


def seed_[TABLE_NAME]():
    """Seed [HUMAN_READABLE_NAME] with required code field"""
    
    data_list = [
        {
            'name': 'Name 1',
            'code': 'CODE_1',  # ← REQUIRED - unique code
            'description': 'Description 1',
            'sort_order': 0,
            'is_active': True
            # ... other fields specific to this model
        },
        {
            'name': 'Name 2', 
            'code': 'CODE_2',  # ← REQUIRED - unique code
            'description': 'Description 2',
            'sort_order': 1,
            'is_active': True
            # ... other fields specific to this model
        },
        # Add more entries as needed
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = [MODEL_CLASS].query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing [SINGULAR_NAME]: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new [SINGULAR_NAME]: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = [MODEL_CLASS](**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ [HUMAN_READABLE_NAME] seeded: {seeded_count} added, {updated_count} updated")
        
        # Optional: Print summary
        if seeded_count > 0:
            print(f"📋 [HUMAN_READABLE_NAME] added:")
            for data_item in data_list:
                record = [MODEL_CLASS].query.filter_by(code=data_item['code']).first()
                if record:
                    print(f"   • {record.name} ({record.code})")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding [HUMAN_READABLE_NAME]: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_[TABLE_NAME]()