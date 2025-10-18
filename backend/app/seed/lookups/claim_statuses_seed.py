from app import db
from app.models.lookups import ClaimStatus
import uuid


def seed_claim_statuses():
    """Seed Claim Statuses with required code field"""
    
    data_list = [
{
    "code": "DRAFT",
            "name": "Draft",
            "description": "Claim is being prepared",
            "is_active": True,
            "requires_action": False,
            "allows_resubmission": True,
            "is_active": True,
        },
{
    "code": "SUBMITTED",
            "name": "Submitted",
            "description": "Claim submitted to insurance",
            "is_active": True,
            "requires_action": False,
            "allows_resubmission": True,
            "is_active": True,
        },
{
    "code": "PROCESSING",
            "name": "Processing",
            "description": "Insurance is processing claim",
            "is_active": True,
            "requires_action": False,
            "allows_resubmission": False,
            "is_active": True,
        },
{
    "code": "APPROVED",
            "name": "Approved",
            "description": "Claim approved by insurance",
            "is_active": True,
            "requires_action": False,
            "allows_resubmission": False,
            "is_active": True,
        },
{
    "code": "PARTIAL_APPROVAL",
            "name": "Partial Approval",
            "description": "Claim partially approved",
            "is_active": True,
            "requires_action": True,
            "allows_resubmission": True,
            "is_active": True,
        },
{
    "code": "DENIED",
            "name": "Denied",
            "description": "Claim denied by insurance",
            "is_active": True,
            "requires_action": True,
            "allows_resubmission": True,
            "is_active": True,
        },
{
    "code": "PAID",
            "name": "Paid",
            "description": "Claim payment received",
            "is_active": True,
            "requires_action": False,
            "allows_resubmission": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = ClaimStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Claim Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Claim Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = ClaimStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Claim Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Claim Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_claim_statuses()
