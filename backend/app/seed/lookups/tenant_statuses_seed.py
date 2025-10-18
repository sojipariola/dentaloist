from app import db
from app.models.lookups import TenantStatus
import uuid


def seed_tenant_statuses():
    """Seed Tenant Statuses with required code field"""
    
    data_list = [
{
    "code": "ACTIVE",
            "name": "Active",
            "description": "Tenant is active and operational",
            "allows_login": True,
            "requires_action": False,
            "is_trial_status": False,
            "is_active": True,
        },
{
    "code": "TRIAL",
            "name": "Trial",
            "description": "Tenant in trial period",
            "allows_login": True,
            "requires_action": False,
            "is_trial_status": True,
            "is_active": True,
        },
{
    "code": "SUSPENDED",
            "name": "Suspended",
            "description": "Tenant access suspended",
            "allows_login": False,
            "requires_action": True,
            "is_trial_status": False,
            "is_active": True,
        },
{
    "code": "EXPIRED",
            "name": "Expired",
            "description": "Trial or subscription expired",
            "allows_login": False,
            "requires_action": True,
            "is_trial_status": False,
            "is_active": True,
        },
{
    "code": "PENDING_SETUP",
            "name": "Pending Setup",
            "description": "Tenant being set up",
            "allows_login": False,
            "requires_action": True,
            "is_trial_status": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = TenantStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Tenant Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Tenant Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = TenantStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Tenant Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Tenant Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_tenant_statuses()
