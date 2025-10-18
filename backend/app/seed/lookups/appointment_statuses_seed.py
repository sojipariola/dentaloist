from app import db
from app.models import AppointmentStatus
import uuid


def seed_appointment_statuses():
    """Seed appointment statuses with proper code fields and error handling"""
    
    statuses = [
        {
            "name": "Scheduled",
            "code": "SCHEDULED",  # ← COMMA ADDED
            "description": "Appointment is scheduled for future date",
            "allows_editing": True,
            "is_final_status": False,
            "sort_order": 1,
            "color": "#3B82F6",
            "is_active": True,
        },
        {
            "name": "Confirmed",
            "code": "CONFIRMED",  # ← COMMA ADDED
            "description": "Appointment has been confirmed by patient",
            "allows_editing": True,
            "is_final_status": False,
            "sort_order": 2,
            "color": "#10B981",
            "is_active": True,
        },
        {
            "name": "Checked In",
            "code": "CHECKED_IN",  # ← COMMA ADDED
            "description": "Patient has arrived and checked in",
            "allows_editing": True,
            "is_final_status": False,
            "sort_order": 3,
            "color": "#8B5CF6",
            "is_active": True,
        },
        {
            "name": "In Progress",
            "code": "IN_PROGRESS",  # ← COMMA ADDED
            "description": "Appointment is currently in progress",
            "allows_editing": True,
            "is_final_status": False,
            "sort_order": 4,
            "color": "#F59E0B",
            "is_active": True,
        },
        {
            "name": "Completed",
            "code": "COMPLETED",  # ← COMMA ADDED
            "description": "Appointment has been completed successfully",
            "allows_editing": False,
            "is_final_status": True,
            "sort_order": 5,
            "color": "#059669",
            "is_active": True,
        },
        {
            "name": "Cancelled",
            "code": "CANCELLED",  # ← COMMA ADDED
            "description": "Appointment was cancelled",
            "allows_editing": False,
            "is_final_status": True,
            "sort_order": 6,
            "color": "#EF4444",
            "is_active": True,
        },
        {
            "name": "No Show",
            "code": "NO_SHOW",  # ← COMMA ADDED
            "description": "Patient did not show up for appointment",
            "allows_editing": False,
            "is_final_status": True,
            "sort_order": 7,
            "color": "#6B7280",
            "is_active": True,
        },
        {
            "name": "Rescheduled",
            "code": "RESCHEDULED",  # ← COMMA ADDED
            "description": "Appointment has been rescheduled",
            "allows_editing": True,
            "is_final_status": False,
            "sort_order": 8,
            "color": "#F97316",
            "is_active": True,
        },
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in statuses:
            # Check by code instead of name for better reliability
            existing = AppointmentStatus.query.filter_by(code=data["code"]).first()
            
            if existing:
                print(f"🔄 Updating existing appointment status: {data['name']}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                print(f"✅ Adding new appointment status: {data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                db.session.add(AppointmentStatus(**data))
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Appointment statuses: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📅 Appointment statuses added:")
            for status_data in statuses:
                status = AppointmentStatus.query.filter_by(code=status_data['code']).first()
                if status:
                    status_emoji = {
                        'SCHEDULED': '📅',
                        'CONFIRMED': '✅',
                        'CHECKED_IN': '🏥',
                        'IN_PROGRESS': '🔄',
                        'COMPLETED': '🎯',
                        'CANCELLED': '❌',
                        'NO_SHOW': '😴',
                        'RESCHEDULED': '📆'
                    }.get(status.code, '📋')
                    
                    final_status = "🏁 Final" if status.is_final_status else "✏️ Editable"
                    print(f"   • {status_emoji} {status.name} - {final_status}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding appointment statuses: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_appointment_statuses()