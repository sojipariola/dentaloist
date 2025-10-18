# tests/test_clinical_models.py

import pytest
from datetime import datetime, timedelta
from app.models import Patient, Appointment, Treatment, db


class TestPatientModel:
    """Test Patient model functionality"""
    
    def test_patient_creation(self, session):
        """Test basic patient creation"""
        patient = Patient(
            first_name="Alice",
            last_name="Johnson",
            email="alice@example.com",
            date_of_birth=datetime(1990, 1, 1).date(),
            gender="Female"
        )
        
        session.add(patient)
        session.commit()
        
        assert patient.id is not None
        assert patient.full_name == "Alice Johnson"
        assert patient.email == "alice@example.com"
        assert patient.is_active == True
    
    def test_patient_medical_record_number(self, session):
        """Test patient MRN generation"""
        patient = Patient(
            first_name="Bob",
            last_name="Smith",
            date_of_birth=datetime(1985, 5, 15).date()
        )
        
        session.add(patient)
        session.commit()
        
        # MRN should be auto-generated
        assert patient.mrn is not None
        assert len(patient.mrn) > 0


class TestAppointmentModel:
    """Test Appointment model functionality"""
    
    def test_appointment_creation(self, session):
        """Test basic appointment creation"""
        start_time = datetime.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        appointment = Appointment(
            title="Dental Checkup",
            start_time=start_time,
            end_time=end_time,
            description="Regular dental examination"
        )
        
        session.add(appointment)
        session.commit()
        
        assert appointment.id is not None
        assert appointment.title == "Dental Checkup"
        assert appointment.duration_minutes == 60


class TestTreatmentModel:
    """Test Treatment model functionality"""
    
    def test_treatment_creation(self, session):
        """Test basic treatment creation"""
        treatment = Treatment(
            name="Teeth Cleaning",
            description="Professional teeth cleaning procedure",
            cost=150.00,
            duration_minutes=30
        )
        
        session.add(treatment)
        session.commit()
        
        assert treatment.id is not None
        assert treatment.name == "Teeth Cleaning"
        assert treatment.cost == 150.00