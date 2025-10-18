# backend/app/seed/patient_seeds.py
from app import db
from app.models import Patient, Gender, User
from datetime import datetime, timedelta
import random
from faker import Faker

def seed_patients():
    """Seed realistic patient data"""
    fake = Faker()
    
    organizations = ["demo-dental-001", "smile-center-002"]
    genders = Gender.query.filter_by(is_active=True).all()
    
    patients = []
    
    for org_id in organizations:
        # Create 20-30 patients per organization
        for i in range(random.randint(20, 30)):
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
            gender = random.choice(genders)
            
            patient = Patient(
                organization_id=org_id,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email() if random.random() > 0.2 else None,  # 80% have email
                phone=fake.phone_number() if random.random() > 0.1 else None,  # 90% have phone
                date_of_birth=birth_date,
                gender_id=gender.id,
                address=fake.street_address() if random.random() > 0.3 else None,
                city=fake.city() if random.random() > 0.3 else None,
                state=fake.state_abbr() if random.random() > 0.3 else None,
                zip_code=fake.zipcode() if random.random() > 0.3 else None,
                emergency_contact_name=fake.name() if random.random() > 0.5 else None,
                emergency_contact_phone=fake.phone_number() if random.random() > 0.5 else None,
                insurance_provider="Delta Dental" if random.random() > 0.6 else "Cigna" if random.random() > 0.3 else None,
                insurance_id=fake.ssn() if random.random() > 0.4 else None,
                medical_conditions=fake.text(max_nb_chars=200) if random.random() > 0.7 else None,
                allergies=fake.text(max_nb_chars=150) if random.random() > 0.6 else None,
                medications=fake.text(max_nb_chars=180) if random.random() > 0.5 else None,
                created_by=1,  # Default admin user
                is_active=True
            )
            patients.append(patient)
    
    # Batch insert for performance
    db.session.bulk_save_objects(patients)
    db.session.commit()
    print(f"✅ {len(patients)} patients seeded successfully.")