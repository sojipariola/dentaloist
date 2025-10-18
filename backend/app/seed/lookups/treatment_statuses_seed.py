from app import db
from app.models.lookups import TreatmentStatus
import uuid


def seed_treatment_statuses():
    """Seed Treatment Statuses with required code field"""
    
    data_list = [
{
    "code": "PLANNED",
            "name": "Planned",
            "description": "Treatment has been planned but not started",
            "allows_modification": True,
            "is_completed_status": False,
            "is_active": True,
        },
{
    "code": "IN_PROGRESS",
            "name": "In Progress",
            "description": "Treatment is currently being administered",
            "allows_modification": True,
            "is_completed_status": False,
            "is_active": True,
        },
{
    "code": "ON_HOLD",
            "name": "On Hold",
            "description": "Treatment has been temporarily paused",
            "allows_modification": True,
            "is_completed_status": False,
            "is_active": True,
        },
{
    "code": "COMPLETED",
            "name": "Completed",
            "description": "Treatment has been successfully completed",
            "allows_modification": False,
            "is_completed_status": True,
            "is_active": True,
        },
{
    "code": "CANCELLED",
            "name": "Cancelled",
            "description": "Treatment was cancelled before completion",
            "allows_modification": False,
            "is_completed_status": True,
            "is_active": True,
        },
{
    "code": "FOLLOW_UP_REQUIRED",
            "name": "Follow-up Required",
            "description": "Treatment completed but follow-up is needed",
            "allows_modification": True,
            "is_completed_status": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = TreatmentStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Treatment Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Treatment Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = TreatmentStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Treatment Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Treatment Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_treatment_statuses()
