from app import db
from app.models.lookups import SecurityEventType
import uuid


def seed_security_event_types():
    """Seed Security Event Types with required code field"""
    
    data_list = [
{
    "code": "LOGIN_SUCCESS",
            "name": "Login Success",
            "description": "Successful user login",
            "severity": "info",
            "requires_notification": False,
            "log_level": "info",
            "is_active": True,
        },
{
    "code": "LOGIN_FAILED",
            "name": "Login Failed",
            "description": "Failed login attempt",
            "severity": "warning",
            "requires_notification": False,
            "log_level": "warning",
            "is_active": True,
        },
{
    "code": "PASSWORD_CHANGE",
            "name": "Password Change",
            "description": "User changed password",
            "severity": "info",
            "requires_notification": False,
            "log_level": "info",
            "is_active": True,
        },
{
    "code": "UNAUTHORIZED_ACCESS",
            "name": "Unauthorized Access",
            "description": "Attempted unauthorized access",
            "severity": "error",
            "requires_notification": True,
            "log_level": "error",
            "is_active": True,
        },
{
    "code": "DATA_EXPORT",
            "name": "Data Export",
            "description": "Bulk data export",
            "severity": "warning",
            "requires_notification": True,
            "log_level": "warning",
            "is_active": True,
        },
{
    "code": "SYSTEM_BREACH",
            "name": "System Breach",
            "description": "Potential security breach",
            "severity": "critical",
            "requires_notification": True,
            "log_level": "error",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = SecurityEventType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Security Event Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Security Event Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = SecurityEventType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Security Event Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Security Event Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_security_event_types()
