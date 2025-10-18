from app import db
from app.models.lookups import NoteType
import uuid


def seed_note_types():
    """Seed Note Types with required code field"""
    
    data_list = [
{
    "code": "SOAP_NOTE",
            "name": "SOAP Note",
            "description": "Standard SOAP format clinical note",
            "requires_soap_format": True,
            "template": "Subjective:\nObjective:\nAssessment:\nPlan:",
            "is_active": True,
        },
{
    "code": "PROGRESS_NOTE",
            "name": "Progress Note",
            "description": "Clinical progress and treatment update",
            "requires_soap_format": False,
            "template": "Treatment Progress:\nFindings:\nNext Steps:",
            "is_active": True,
        },
{
    "code": "CONSULTATION_NOTE",
            "name": "Consultation Note",
            "description": "Initial consultation and assessment",
            "requires_soap_format": True,
            "template": "Chief Complaint:\nHistory:\nExamination:\nAssessment:\nRecommendations:",
            "is_active": True,
        },
{
    "code": "PROCEDURE_NOTE",
            "name": "Procedure Note",
            "description": "Detailed procedure documentation",
            "requires_soap_format": False,
            "template": "Procedure:\nMaterials Used:\nComplications:\nPost-op Instructions:",
            "is_active": True,
        },
{
    "code": "PHONE_NOTE",
            "name": "Phone Note",
            "description": "Telephone conversation summary",
            "requires_soap_format": False,
            "template": "Call Summary:\nAction Taken:\nFollow-up Required:",
            "is_active": True,
        },
{
    "code": "ADMINISTRATIVE_NOTE",
            "name": "Administrative Note",
            "description": "Non-clinical administrative notes",
            "requires_soap_format": False,
            "template": "Administrative Note:",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = NoteType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Note Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Note Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = NoteType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Note Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Note Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_note_types()
