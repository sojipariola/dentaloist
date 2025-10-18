from app import db
from app.models.lookups import ReportType
import uuid


def seed_report_types():
    """Seed Report Types with required code field"""
    
    data_list = [
{
    "code": "FINANCIAL_SUMMARY",
            "name": "Financial Summary",
            "description": "Monthly financial performance summary",
            "category": "financial",
            "requires_parameters": True,
            "data_retention_days": 1095,
            "template_available": True,
            "is_active": True,
        },
{
    "code": "PATIENT_DEMOGRAPHICS",
            "name": "Patient Demographics",
            "description": "Patient demographic analysis",
            "category": "clinical",
            "requires_parameters": True,
            "data_retention_days": 365,
            "template_available": True,
            "is_active": True,
        },
{
    "code": "APPOINTMENT_STATISTICS",
            "name": "Appointment Statistics",
            "description": "Appointment volume and trends",
            "category": "operational",
            "requires_parameters": True,
            "data_retention_days": 730,
            "template_available": True,
            "is_active": True,
        },
{
    "code": "TREATMENT_ANALYSIS",
            "name": "Treatment Analysis",
            "description": "Treatment types and outcomes",
            "category": "clinical",
            "requires_parameters": True,
            "data_retention_days": 1825,
            "template_available": True,
            "is_active": True,
        },
{
    "code": "INVENTORY_REPORT",
            "name": "Inventory Report",
            "description": "Inventory levels and usage",
            "category": "operational",
            "requires_parameters": False,
            "data_retention_days": 365,
            "template_available": True,
            "is_active": True,
        },
{
    "code": "STAFF_PERFORMANCE",
            "name": "Staff Performance",
            "description": "Staff productivity and efficiency",
            "category": "operational",
            "requires_parameters": True,
            "data_retention_days": 365,
            "template_available": True,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = ReportType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Report Type: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Report Type: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = ReportType(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Report Types seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Report Types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_report_types()
