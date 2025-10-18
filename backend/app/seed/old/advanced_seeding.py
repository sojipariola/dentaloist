# backend/app/seed/advanced_seeding.py
from faker import Faker
from faker.providers import person, phone_number, address, date_time, lorem
import random
from datetime import datetime, timedelta

class DentalDataGenerator:
    def __init__(self):
        self.fake = Faker()
        self.fake.add_provider(person)
        self.fake.add_provider(phone_number)
        self.fake.add_provider(address)
        self.fake.add_provider(date_time)
        self.fake.add_provider(lorem)
    
    def generate_patient(self, organization_id):
        """Generate realistic patient data"""
        gender = random.choice(['Male', 'Female'])
        first_name = self.fake.first_name_male() if gender == 'Male' else self.fake.first_name_female()
        
        return {
            "organization_id": organization_id,
            "first_name": first_name,
            "last_name": self.fake.last_name(),
            "email": self.fake.email() if random.random() > 0.15 else None,
            "phone": self.fake.phone_number() if random.random() > 0.1 else None,
            "date_of_birth": self.fake.date_of_birth(minimum_age=18, maximum_age=85),
            "gender": gender,
            "address": self.fake.street_address() if random.random() > 0.2 else None,
            "city": self.fake.city() if random.random() > 0.2 else None,
            "state": self.fake.state_abbr() if random.random() > 0.2 else None,
            "zip_code": self.fake.zipcode() if random.random() > 0.2 else None,
        }
    
    def generate_appointment(self, patient_id, staff_id, org_id):
        """Generate realistic appointment data"""
        base_date = datetime.utcnow()
        days_offset = random.randint(-60, 60)
        appointment_date = base_date + timedelta(days=days_offset)
        
        return {
            "organization_id": org_id,
            "patient_id": patient_id,
            "staff_id": staff_id,
            "start_time": appointment_date.replace(hour=random.randint(8, 16), minute=0, second=0),
            "duration": random.choice([30, 45, 60]),
            "description": self.fake.sentence(),
        }