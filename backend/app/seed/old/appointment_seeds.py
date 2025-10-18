# backend/app/seed/appointment_seeds.py
from app import db
from app.models import Appointment, AppointmentStatus, AppointmentType, Patient, User
from datetime import datetime, timedelta
import random

def seed_appointments():
    """Seed realistic appointment data"""
    
    # Get reference data
    orgs = ["demo-dental-001", "smile-center-002"]
    statuses = AppointmentStatus.query.filter_by(is_active=True).all()
    types = AppointmentType.query.filter_by(is_active=True).all()
    
    appointments = []
    
    for org_id in orgs:
        # Get patients and staff for this organization
        patients = Patient.query.filter_by(organization_id=org_id).all()
        staff = User.query.filter_by(organization_id=org_id, is_active=True).all()
        
        if not patients or not staff:
            continue
            
        # Create appointments for the next 30 days and past 30 days
        base_date = datetime.utcnow()
        
        for i in range(random.randint(40, 60)):  # 40-60 appointments per org
            patient = random.choice(patients)
            staff_member = random.choice(staff)
            appointment_type = random.choice(types)
            status = random.choice(statuses)
            
            # Random date within ±30 days
            days_offset = random.randint(-30, 30)
            appointment_date = base_date + timedelta(days=days_offset)
            
            # Random time between 8 AM and 5 PM
            hour = random.randint(8, 16)
            minute = random.choice([0, 15, 30, 45])
            start_time = appointment_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Duration based on appointment type or random
            duration = appointment_type.default_duration or random.choice([30, 45, 60])
            end_time = start_time + timedelta(minutes=duration)
            
            appointment = Appointment(
                organization_id=org_id,
                patient_id=patient.id,
                staff_id=staff_member.id,
                appointment_type_id=appointment_type.id,
                status_id=status.id,
                title=f"{appointment_type.name} - {patient.first_name} {patient.last_name}",
                description=f"Routine {appointment_type.name.lower()} appointment",
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                notes=fake.text(max_nb_chars=200) if random.random() > 0.7 else None,
                created_by=staff_member.id
            )
            appointments.append(appointment)
    
    db.session.bulk_save_objects(appointments)
    db.session.commit()
    print(f"✅ {len(appointments)} appointments seeded successfully.")