from app import db
from app.models.lookups import InvoiceStatus
import uuid


def seed_invoice_statuses():
    """Seed Invoice Statuses with required code field"""
    
    data_list = [
{
    "code": "DRAFT",
            "name": "Draft",
            "description": "Invoice is in draft stage",
            "is_final": False,
            "allows_editing": True,
            "send_notifications": False,
            "is_active": True,
        },
{
    "code": "SENT",
            "name": "Sent",
            "description": "Invoice has been sent to patient",
            "is_final": False,
            "allows_editing": True,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "VIEWED",
            "name": "Viewed",
            "description": "Patient has viewed the invoice",
            "is_final": False,
            "allows_editing": True,
            "send_notifications": False,
            "is_active": True,
        },
{
    "code": "PARTIAL",
            "name": "Partial",
            "description": "Partial payment received",
            "is_final": False,
            "allows_editing": True,
            "send_notifications": False,
            "is_active": True,
        },
{
    "code": "PAID",
            "name": "Paid",
            "description": "Invoice fully paid",
            "is_final": True,
            "allows_editing": False,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "OVERDUE",
            "name": "Overdue",
            "description": "Invoice payment is overdue",
            "is_final": False,
            "allows_editing": True,
            "send_notifications": True,
            "is_active": True,
        },
{
    "code": "VOID",
            "name": "Void",
            "description": "Invoice voided",
            "is_final": True,
            "allows_editing": False,
            "send_notifications": False,
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = InvoiceStatus.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing Invoice Statuse: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new Invoice Statuse: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = InvoiceStatus(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Invoice Statuses seeded: {seeded_count} added, {updated_count} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding Invoice Statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_invoice_statuses()
