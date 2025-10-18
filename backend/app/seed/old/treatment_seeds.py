# backend/app/seed/treatment_seeds.py
from app import db
from app.models import Treatment, TreatmentType, TreatmentStatus, Patient, User
from datetime import datetime, timedelta
import random

def seed_treatments():
    """Seed treatment records"""
    
    orgs = ["demo-dental-001", "smile-center-002"]
    treatment_types = TreatmentType.query.filter_by(is_active=True).all()
    treatment_statuses = TreatmentStatus.query.filter_by(is_active=True).all()
    
    treatments = []
    
    for org_id in orgs:
        patients = Patient.query.filter_by(organization_id=org_id).all()
        staff = User.query.filter_by(organization_id=org_id, is_active=True).all()
        
        for patient in random.sample(patients, min(15, len(patients))):  # 15 patients per org get treatments
            for i in range(random.randint(1, 4)):  # 1-4 treatments per patient
                treatment_type = random.choice(treatment_types)
                status = random.choice(treatment_statuses)
                staff_member = random.choice(staff)
                
                treatment_date = datetime.utcnow() - timedelta(days=random.randint(1, 180))
                
                treatment = Treatment(
                    organization_id=org_id,
                    patient_id=patient.id,
                    treatment_type_id=treatment_type.id,
                    status_id=status.id,
                    treated_by=staff_member.id,
                    treatment_date=treatment_date,
                    tooth_numbers=",".join(random.sample([str(i) for i in range(1, 33)], random.randint(1, 4))),
                    description=f"{treatment_type.name} procedure completed",
                    notes=f"Patient tolerated procedure well. {fake.text(max_nb_chars=100)}",
                    cost=round(random.uniform(50, 500), 2),
                    duration=random.randint(30, 120),
                    created_by=staff_member.id
                )
                treatments.append(treatment)
    
    db.session.bulk_save_objects(treatments)
    db.session.commit()
    print(f"✅ {len(treatments)} treatments seeded successfully.")