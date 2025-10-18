# backend/app/models/clinical.py


from sqlalchemy import (Text, DateTime, Float, Integer, String, Boolean, ForeignKey, 
                       Numeric, CheckConstraint, LargeBinary, Date, Time)
from sqlalchemy.dialects.postgresql import JSON 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, date, time, timedelta
import uuid

from .base import BaseModel
from .lookups import (
    AppointmentStatus, AppointmentType, PriorityLevel, TreatmentStatus,
    TreatmentType, TreatmentPriority, NoteType, AllergySeverity,
    MedicationRoute, VitalSignsUnit
)
from . import db

class Patient(BaseModel):
    __tablename__ = 'patients'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    
    # Personal information
    first_name = db.Column(db.String(50), nullable=False, index=True)
    last_name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(120), index=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date, index=True)
    gender = db.Column(db.String(20))  # male, female, other, prefer_not_to_say
    
    # Contact information
    address = db.Column(db.JSON)  # Structured address 
    emergency_contact = db.Column(db.JSON)  # Emergency contact details

    # Medical information
    medical_history = db.Column(db.JSON)  # Comprehensive medical history
    allergies = db.Column(db.JSON)  # Allergies list
    medications = db.Column(db.JSON)  # Current medications
    insurance_info = db.Column(db.JSON)  # Insurance information
    
    # Dental-specific information
    dental_history = db.Column(db.JSON)  # Previous dental treatments
    oral_hygiene = db.Column(db.String(50))  # Good, Fair, Poor
    last_dental_visit = db.Column(db.Date)
    next_recall_date = db.Column(db.Date)  # Next recommended visit
    
    # Status and preferences
    status = db.Column(db.String(20), default='active')  # active, inactive, deceased
    preferred_language = db.Column(db.String(50), default='English')
    communication_preferences = db.Column(db.JSON)  # Email, SMS, Phone
    
    # Relationships
    organization = db.relationship('Organization', back_populates='patients')
    appointments = db.relationship('Appointment', back_populates='patient')
    treatments = db.relationship('Treatment', back_populates='patient')
    insurance_plans = db.relationship('InsurancePlan', back_populates='patient')
    patient_family_members = db.relationship('FamilyMember', back_populates='patient', lazy=True)
    insurance_claims = db.relationship('InsuranceClaim', back_populates='patient', lazy=True)
    family_members = db.relationship('FamilyMember', back_populates='patient', overlaps="patient_family_members")
    
    allergies_list = db.relationship('Allergy', back_populates='patient')
    prescriptions = db.relationship('Prescription', back_populates='patient')
    vital_signs = db.relationship('VitalSign', back_populates='patient')
    medical_records = db.relationship('MedicalRecord', back_populates='patient')
    notes = db.relationship('Note', back_populates='patient')
    lab_orders = db.relationship('LabOrder', back_populates='patient')
    invoices = db.relationship('Invoice', back_populates='patient')
    payments = db.relationship('Payment', back_populates='patient')
    treatment_plans = db.relationship('TreatmentPlan', back_populates='patient')
    financial_transactions = db.relationship('FinancialTransaction', back_populates='patient')
  
    # Indexes
    __table_args__ = (
        db.Index('idx_patient_org_name', 'organization_id', 'last_name', 'first_name'),
        db.Index('idx_patient_dob', 'date_of_birth'),
        db.Index('idx_patient_status', 'status'),
        db.Index('idx_patient_email', 'email'),
    )

    @hybrid_property
    def full_name(self):
        """Get patient's full name"""
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def age(self):
        """Calculate patient's age"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    @hybrid_property
    def has_active_treatments(self):
        """Check if patient has active treatments"""
        scheduled_status = TreatmentStatus.query.filter_by(code='scheduled').first()
        in_progress_status = TreatmentStatus.query.filter_by(code='in_progress').first()
        
        if scheduled_status and in_progress_status:
            return any(treatment.status_id in [scheduled_status.id, in_progress_status.id] 
                      for treatment in self.treatments)
        return False

    def _to_dict_impl(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'age': self.age,
            'gender': self.gender,
            'status': self.status,
            'medical_history': self.medical_history or {},
            'allergies': self.allergies or [],
            'last_dental_visit': self.last_dental_visit.isoformat() if self.last_dental_visit else None,
            'next_recall_date': self.next_recall_date.isoformat() if self.next_recall_date else None,
            'has_active_treatments': self.has_active_treatments
        }

    def get_upcoming_appointments(self, limit=5):
        """Get patient's upcoming appointments"""
        scheduled_status = AppointmentStatus.query.filter_by(code='scheduled').first()
        confirmed_status = AppointmentStatus.query.filter_by(code='confirmed').first()
        
        if scheduled_status and confirmed_status:
            return Appointment.query.filter(
                Appointment.patient_id == self.id,
                Appointment.status_id.in_([scheduled_status.id, confirmed_status.id]),
                Appointment.start_time >= datetime.utcnow()
            ).order_by(Appointment.start_time.asc()).limit(limit).all()
        return []

    def get_medical_summary(self):
        """Get comprehensive medical summary"""
        scheduled_status = TreatmentStatus.query.filter_by(code='scheduled').first()
        in_progress_status = TreatmentStatus.query.filter_by(code='in_progress').first()
        
        active_treatments = []
        if scheduled_status and in_progress_status:
            active_treatments = [t.to_dict() for t in self.treatments 
                               if t.status_id in [scheduled_status.id, in_progress_status.id]]
        
        return {
            'patient_info': self.to_dict(),
            'active_treatments': active_treatments,
            'recent_appointments': [a.to_dict() for a in self.appointments[:5]],
            'current_medications': self.medications or [],
            'known_allergies': self.allergies or [],
            'vital_signs_trend': self.get_vital_signs_trend()
        }

    def get_vital_signs_trend(self, days=30):
        """Get vital signs trend over specified days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_vitals = VitalSign.query.filter(
            VitalSign.patient_id == self.id,
            VitalSign.record_date >= cutoff_date
        ).order_by(VitalSign.record_date.desc()).all()
        
        return [v.to_dict() for v in recent_vitals]

    def schedule_recall(self, months=6):
        """Schedule next recall appointment"""
        self.next_recall_date = date.today() + timedelta(days=30*months)
        return self.next_recall_date

    @classmethod
    def search_patients(cls, organization_id, query, limit=20):
        """Search patients by name, email, or phone"""
        return cls.query.filter(
            cls.organization_id == organization_id,
            cls.is_active == True,
            db.or_(
                cls.first_name.ilike(f"%{query}%"),
                cls.last_name.ilike(f"%{query}%"),
                cls.email.ilike(f"%{query}%"),
                cls.phone.ilike(f"%{query}%")
            )
        ).limit(limit).all()

class Appointment(BaseModel):
    __tablename__ = 'appointments'
    
    # Foreign keys
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)

    dentist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    availability_slot_id = db.Column(db.Integer, db.ForeignKey('availability_slots.id'), nullable=True)
    
    # Lookup foreign keys
    appointment_type_id = db.Column(db.Integer, db.ForeignKey('appointment_types.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('appointment_statuses.id'), nullable=False)
    priority_id = db.Column(db.Integer, db.ForeignKey('priority_levels.id'), nullable=True)
    
    # Appointment details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Timing
    start_time = db.Column(DateTime, nullable=False, index=True)
    end_time = db.Column(DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    actual_start_time = db.Column(DateTime)
    actual_end_time = db.Column(DateTime)
    actual_duration = db.Column(db.Integer)  # actual duration in minutes
    
    # Location and resources
    treatment_room = db.Column(db.String(50))
    location = db.Column(db.String(200))
    equipment_needed = db.Column(db.JSON)  # List of required equipment
    
    # Clinical information
    chief_complaint = db.Column(db.Text)  # Patient's main concern
    treatment_notes = db.Column(db.Text)
    prescribed_medications = db.Column(db.JSON)
    follow_up_required = db.Column(db.Boolean, default=False)
    follow_up_date = db.Column(DateTime)
    
    # Financial information
    estimated_cost = db.Column(Numeric(10, 2))
    insurance_covered = db.Column(Numeric(10, 2))
    patient_payment = db.Column(Numeric(10, 2))
    payment_status = db.Column(db.String(20), default='pending')
    
    # Reminders and communication
    reminder_sent = db.Column(db.Boolean, default=False)
    confirmation_sent = db.Column(db.Boolean, default=False)
    sms_reminder = db.Column(db.Boolean, default=False)
    email_reminder = db.Column(db.Boolean, default=False)
    reminder_sent_at = db.Column(DateTime)
    
    # Cancellation information
    cancellation_reason = db.Column(db.Text)
    cancelled_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cancellation_date = db.Column(DateTime)
    
    # Relationships
    organization = relationship('Organization', back_populates='appointments')
    patient = relationship('Patient', back_populates='appointments')
    dentist = relationship('User', foreign_keys=[dentist_id])
    treatment = relationship('Treatment', back_populates='appointments')
    staff = relationship('Staff', back_populates='appointments')
    availability_slot = relationship('AvailabilitySlot', back_populates='appointments', lazy=True)
    cancelled_by = relationship('User', foreign_keys=[cancelled_by_id])
    procedures = relationship('Procedure', back_populates='appointment')
    telehealth_session = relationship('TelehealthSession', back_populates='appointment', uselist=False)
    invoices = relationship('Invoice', back_populates='appointment')
    
    # Lookup relationships
    appointment_type = relationship('AppointmentType')
    status = relationship('AppointmentStatus')
    priority = relationship('PriorityLevel')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_appointment_org_date', 'organization_id', 'start_time'),
        db.Index('idx_appointment_patient', 'patient_id', 'start_time'),
        db.Index('idx_appointment_dentist', 'dentist_id', 'start_time'),
        db.Index('idx_appointment_status', 'status_id'),
        db.Index('idx_appointment_type', 'appointment_type_id'),
        CheckConstraint('end_time > start_time', name='check_appointment_duration'),
    )

    @hybrid_property
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        scheduled_status = AppointmentStatus.query.filter_by(code='scheduled').first()
        confirmed_status = AppointmentStatus.query.filter_by(code='confirmed').first()
        
        if scheduled_status and confirmed_status:
            return (self.start_time > datetime.utcnow() and 
                    self.status_id in [scheduled_status.id, confirmed_status.id])
        return False

    @hybrid_property
    def is_past(self):
        """Check if appointment is in the past"""
        return self.end_time < datetime.utcnow()

    @hybrid_property
    def is_ongoing(self):
        """Check if appointment is currently ongoing"""
        in_progress_status = AppointmentStatus.query.filter_by(code='in_progress').first()
        if not in_progress_status:
            return False
            
        now = datetime.utcnow()
        return (self.start_time <= now <= self.end_time and 
                self.status_id == in_progress_status.id)

    def _to_dict_impl(self):
        return {
            'title': self.title,
            'description': self.description,
            'type': self.appointment_type.to_dict() if self.appointment_type else None,
            'status': self.status.to_dict() if self.status else None,
            'priority': self.priority.to_dict() if self.priority else None,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'actual_start_time': self.actual_start_time.isoformat() if self.actual_start_time else None,
            'actual_duration': self.actual_duration,
            'treatment_room': self.treatment_room,
            'location': self.location,
            'chief_complaint': self.chief_complaint,
            'treatment_notes': self.treatment_notes,
            'follow_up_required': self.follow_up_required,
            'follow_up_date': self.follow_up_date.isoformat() if self.follow_up_date else None,
            'estimated_cost': float(self.estimated_cost) if self.estimated_cost else None,
            'payment_status': self.payment_status,
            'is_upcoming': self.is_upcoming,
            'is_ongoing': self.is_ongoing,
            'is_past': self.is_past,
            'patient_name': self.patient.full_name if self.patient else None,
            'dentist_name': f"{self.dentist.first_name} {self.dentist.last_name}" if self.dentist else None
        }

    def check_availability(self):
        """Check if the appointment time slot is available"""
        scheduled_status = AppointmentStatus.query.filter_by(code='scheduled').first()
        confirmed_status = AppointmentStatus.query.filter_by(code='confirmed').first()
        in_progress_status = AppointmentStatus.query.filter_by(code='in_progress').first()
        
        if not all([scheduled_status, confirmed_status, in_progress_status]):
            return True
            
        conflicting_appointments = Appointment.query.filter(
            Appointment.organization_id == self.organization_id,
            Appointment.dentist_id == self.dentist_id,
            Appointment.status_id.in_([scheduled_status.id, confirmed_status.id, in_progress_status.id]),
            Appointment.id != self.id,
            Appointment.start_time < self.end_time,
            Appointment.end_time > self.start_time
        ).count()
        
        return conflicting_appointments == 0

    def start_appointment(self):
        """Mark appointment as in progress"""
        scheduled_status = AppointmentStatus.query.filter_by(code='scheduled').first()
        confirmed_status = AppointmentStatus.query.filter_by(code='confirmed').first()
        in_progress_status = AppointmentStatus.query.filter_by(code='in_progress').first()
        
        if not all([scheduled_status, confirmed_status, in_progress_status]):
            return False
            
        if self.status_id in [scheduled_status.id, confirmed_status.id]:
            self.status_id = in_progress_status.id
            self.actual_start_time = datetime.utcnow()
            return True
        return False

    def complete_appointment(self, notes=None, procedures=None):
        """Mark appointment as completed"""
        in_progress_status = AppointmentStatus.query.filter_by(code='in_progress').first()
        completed_status = AppointmentStatus.query.filter_by(code='completed').first()
        
        if not all([in_progress_status, completed_status]):
            return False
            
        if self.status_id == in_progress_status.id:
            self.status_id = completed_status.id
            self.actual_end_time = datetime.utcnow()
            self.actual_duration = int((self.actual_end_time - self.actual_start_time).total_seconds() / 60)
            
            if notes:
                self.treatment_notes = notes
            
            return True
        return False

    def cancel_appointment(self, reason, cancelled_by_user):
        """Cancel appointment with reason"""
        cancelled_status = AppointmentStatus.query.filter_by(code='cancelled').first()
        if not cancelled_status:
            return False
            
        if self.status_id != cancelled_status.id:
            self.status_id = cancelled_status.id
            self.cancellation_reason = reason
            self.cancelled_by_id = cancelled_by_user.id
            self.cancellation_date = datetime.utcnow()
            return True
        return False

    def send_reminder(self, method='email'):
        """Send appointment reminder"""
        if method == 'email':
            self.email_reminder = True
        elif method == 'sms':
            self.sms_reminder = True
        
        self.reminder_sent = True
        self.reminder_sent_at = datetime.utcnow()

    def calculate_estimated_cost(self):
        """Calculate estimated cost based on procedures"""
        # This would calculate based on procedure codes and insurance
        # Placeholder implementation
        return 0.0

    @classmethod
    def get_daily_schedule(cls, organization_id, schedule_date, dentist_id=None):
        """Get daily schedule for organization or specific dentist"""
        start_of_day = datetime.combine(schedule_date, time.min)
        end_of_day = datetime.combine(schedule_date, time.max)
        
        scheduled_status = AppointmentStatus.query.filter_by(code='scheduled').first()
        confirmed_status = AppointmentStatus.query.filter_by(code='confirmed').first()
        in_progress_status = AppointmentStatus.query.filter_by(code='in_progress').first()
        
        if not all([scheduled_status, confirmed_status, in_progress_status]):
            return []
            
        query = cls.query.filter(
            cls.organization_id == organization_id,
            cls.start_time.between(start_of_day, end_of_day),
            cls.status_id.in_([scheduled_status.id, confirmed_status.id, in_progress_status.id])
        )
        
        if dentist_id:
            query = query.filter(cls.dentist_id == dentist_id)
        
        return query.order_by(cls.start_time.asc()).all()

class TreatmentPlan(BaseModel):
    __tablename__ = 'treatment_plans'
    
    # Foreign keys
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Treatment plan details    
    diagnosis = db.Column(db.Text, nullable=False)
    procedures = db.Column(db.JSON, nullable=False)
    medications = db.Column(db.JSON)
    status = db.Column(db.String(20), default='active')
    notes = db.Column(db.Text) 

    # Relationships
    treating_staff = db.relationship('Staff', back_populates='treatment_plans')
    patient = db.relationship('Patient', back_populates='treatment_plans')
    organization = db.relationship('Organization')
    creator = db.relationship('User', foreign_keys=[created_by])

    def _to_dict_impl(self):
        return {
            'diagnosis': self.diagnosis,
            'procedures': self.procedures or [],
            'medications': self.medications or [],
            'status': self.status,
            'notes': self.notes,
            'patient_name': self.patient.full_name if self.patient else None,
            'treating_staff': self.treating_staff.user.full_name if self.treating_staff and self.treating_staff.user else None,
            'creator_name': f"{self.creator.first_name} {self.creator.last_name}" if self.creator else None
        }

class Treatment(BaseModel):
    __tablename__ = 'treatments'
    
    # Foreign keys
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    dentist_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assistant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Lookup foreign keys
    treatment_type_id = db.Column(db.Integer, db.ForeignKey('treatment_types.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('treatment_statuses.id'), nullable=False)
    priority_id = db.Column(db.Integer, db.ForeignKey('treatment_priorities.id'), nullable=False)
    
    # Treatment details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    procedure_code = db.Column(db.String(50), index=True)  # CDT codes
    diagnosis_codes = db.Column(db.JSON)  # ICD-10 codes
    
    # Timing
    scheduled_date = db.Column(DateTime, nullable=False, index=True)
    estimated_duration = db.Column(db.Integer)  # minutes
    actual_start_time = db.Column(DateTime)
    actual_end_time = db.Column(DateTime)
    actual_duration = db.Column(db.Integer)  # minutes
    
    # Clinical details
    tooth_numbers = db.Column(db.JSON)  # FDI tooth numbering
    surfaces = db.Column(db.JSON)  # Tooth surfaces involved
    anesthesia_used = db.Column(db.JSON)
    complications = db.Column(db.Text)
    post_treatment_instructions = db.Column(db.Text)
    
    # Financial information
    cost_estimate = db.Column(Numeric(10, 2))
    actual_cost = db.Column(Numeric(10, 2))
    insurance_covered = db.Column(Numeric(10, 2))
    patient_responsibility = db.Column(Numeric(10, 2))
    
    # Treatment metadata
    duration = db.Column(db.Integer)  # Treatment duration in minutes
    price = db.Column(Numeric(10, 2))
    category = db.Column(db.String(50))
    
    # Relationships
    tenant = relationship('Tenant', back_populates='treatments')
    patient = relationship('Patient', back_populates='treatments')
    dentist = relationship('User', foreign_keys=[dentist_id])
    assistant = relationship('User', foreign_keys=[assistant_id])
    appointments = relationship('Appointment', back_populates='treatment')
    prescriptions = relationship('Prescription', back_populates='treatment')
    lab_orders = relationship('LabOrder', back_populates='treatment')
    clinical_notes = relationship('ClinicalNote', back_populates='treatment')
    medical_records = relationship('MedicalRecord', back_populates='treatment')
    invoices = relationship('Invoice', back_populates='treatment')
    
    # Lookup relationships
    treatment_type = relationship('TreatmentType')
    status = relationship('TreatmentStatus')
    priority = relationship('TreatmentPriority')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_treatment_patient_status', 'patient_id', 'status_id'),
        db.Index('idx_treatment_dentist_date', 'dentist_id', 'scheduled_date'),
        db.Index('idx_treatment_type', 'treatment_type_id'),
        db.Index('idx_treatment_procedure_code', 'procedure_code'),
    )

    @hybrid_property
    def is_ongoing(self):
        """Check if treatment is currently in progress"""
        in_progress_status = TreatmentStatus.query.filter_by(code='in_progress').first()
        return in_progress_status and self.status_id == in_progress_status.id

    @hybrid_property
    def is_completed(self):
        """Check if treatment is completed"""
        completed_status = TreatmentStatus.query.filter_by(code='completed').first()
        return completed_status and self.status_id == completed_status.id

    def _to_dict_impl(self):
        return {
            'name': self.name,
            'description': self.description,
            'type': self.treatment_type.to_dict() if self.treatment_type else None,
            'status': self.status.to_dict() if self.status else None,
            'priority': self.priority.to_dict() if self.priority else None,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'estimated_duration': self.estimated_duration,
            'actual_duration': self.actual_duration,
            'tooth_numbers': self.tooth_numbers or [],
            'surfaces': self.surfaces or [],
            'cost_estimate': float(self.cost_estimate) if self.cost_estimate else None,
            'actual_cost': float(self.actual_cost) if self.actual_cost else None,
            'is_ongoing': self.is_ongoing,
            'is_completed': self.is_completed,
            'patient_name': self.patient.full_name if self.patient else None,
            'dentist_name': f"{self.dentist.first_name} {self.dentist.last_name}" if self.dentist else None
        }

    def start_treatment(self):
        """Start the treatment"""
        scheduled_status = TreatmentStatus.query.filter_by(code='scheduled').first()
        in_progress_status = TreatmentStatus.query.filter_by(code='in_progress').first()
        
        if not all([scheduled_status, in_progress_status]):
            return False
            
        if self.status_id == scheduled_status.id:
            self.status_id = in_progress_status.id
            self.actual_start_time = datetime.utcnow()
            return True
        return False

    def complete_treatment(self, actual_cost=None):
        """Complete the treatment"""
        in_progress_status = TreatmentStatus.query.filter_by(code='in_progress').first()
        completed_status = TreatmentStatus.query.filter_by(code='completed').first()
        
        if not all([in_progress_status, completed_status]):
            return False
            
        if self.status_id == in_progress_status.id:
            self.status_id = completed_status.id
            self.actual_end_time = datetime.utcnow()
            
            if self.actual_start_time and self.actual_end_time:
                self.actual_duration = int((self.actual_end_time - self.actual_start_time).total_seconds() / 60)
            
            if actual_cost is not None:
                self.actual_cost = actual_cost
            
            return True
        return False

    def add_clinical_note(self, author_id, content, note_type_code="progress"):
        """Add clinical note to treatment"""
        note_type = NoteType.query.filter_by(code=note_type_code).first()
        if not note_type:
            return None
            
        note = ClinicalNote(
            treatment_id=self.id,
            author_id=author_id,
            note_type_id=note_type.id,
            content=content
        )
        self.clinical_notes.append(note)
        return note

    def get_treatment_plan(self):
        """Get associated treatment plan"""
        # This would query related treatment plan
        return None

class ClinicalNote(BaseModel):
    __tablename__ = 'clinical_notes'
    
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_type_id = db.Column(db.Integer, db.ForeignKey('note_types.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # SOAP note components
    subjective = db.Column(db.Text)  # Patient's subjective complaints
    objective = db.Column(db.Text)   # Objective findings
    assessment = db.Column(db.Text)  # Assessment/diagnosis
    plan = db.Column(db.Text)        # Treatment plan
    
    # Relationships
    treatment = relationship('Treatment', back_populates='clinical_notes')
    author = relationship('User')
    note_type = relationship('NoteType')
    
    __table_args__ = (
        db.Index('idx_clinical_note_treatment', 'treatment_id', 'created_at'),
        db.Index('idx_clinical_note_author', 'author_id'),
        db.Index('idx_clinical_note_type', 'note_type_id'),
    )

    def _to_dict_impl(self):
        return {
            'note_type': self.note_type.to_dict() if self.note_type else None,
            'content': self.content,
            'subjective': self.subjective,
            'objective': self.objective,
            'assessment': self.assessment,
            'plan': self.plan,
            'author_name': f"{self.author.first_name} {self.author.last_name}" if self.author else None,
            'treatment_name': self.treatment.name if self.treatment else None
        }

class Allergy(BaseModel):
    __tablename__ = 'allergies'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    allergen = db.Column(db.String(100), nullable=False)
    reaction = db.Column(db.String(255))
    severity_id = db.Column(db.Integer, db.ForeignKey('allergy_severities.id'))
    onset_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    patient = relationship('Patient', back_populates='allergies_list')
    recorded_by_user = relationship('User')
    severity = relationship('AllergySeverity')
    
    __table_args__ = (
        db.Index('idx_allergy_patient', 'patient_id', 'is_active'),
        db.Index('idx_allergy_allergen', 'allergen'),
    )

    def _to_dict_impl(self):
        return {
            'allergen': self.allergen,
            'reaction': self.reaction,
            'severity': self.severity.to_dict() if self.severity else None,
            'onset_date': self.onset_date.isoformat() if self.onset_date else None,
            'is_active': self.is_active,
            'notes': self.notes,
            'recorded_by': self.recorded_by,
            'patient_name': self.patient.full_name if self.patient else None
        }

class Prescription(BaseModel):
    __tablename__ = 'prescriptions'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    prescribed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Lookup foreign key
    route_id = db.Column(db.Integer, db.ForeignKey('medication_routes.id'))
    
    # Medication details
    medication_name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)  # e.g., 500mg
    frequency = db.Column(db.String(100), nullable=False)  # e.g., twice daily
    quantity = db.Column(db.Integer)
    refills = db.Column(db.Integer, default=0)
    
    # Timing
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date)
    duration_days = db.Column(db.Integer)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    
    # Instructions and notes
    instructions = db.Column(db.Text)
    side_effects = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    
    # Relationships
    patient = relationship('Patient', back_populates='prescriptions')
    treatment = relationship('Treatment', back_populates='prescriptions')
    prescriber = relationship('User', foreign_keys=[prescribed_by])
    route = relationship('MedicationRoute')
    
    __table_args__ = (
        db.Index('idx_prescription_patient', 'patient_id', 'is_active'),
        db.Index('idx_prescription_prescriber', 'prescribed_by'),
        db.Index('idx_prescription_medication', 'medication_name'),
    )

    def _to_dict_impl(self):
        return {
            'medication_name': self.medication_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'route': self.route.to_dict() if self.route else None,
            'quantity': self.quantity,
            'refills': self.refills,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'duration_days': self.duration_days,
            'is_active': self.is_active,
            'instructions': self.instructions,
            'patient_name': self.patient.full_name if self.patient else None,
            'prescriber_name': f"{self.prescriber.first_name} {self.prescriber.last_name}" if self.prescriber else None
        }

    def calculate_end_date(self):
        """Calculate end date based on start date and duration"""
        if self.start_date and self.duration_days:
            self.end_date = self.start_date + timedelta(days=self.duration_days)
        return self.end_date

class VitalSign(BaseModel):
    __tablename__ = 'vital_signs'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Vital signs measurements
    blood_pressure_systolic = db.Column(db.Integer)  # mmHg
    blood_pressure_diastolic = db.Column(db.Integer)  # mmHg
    heart_rate = db.Column(db.Integer)  # bpm
    respiratory_rate = db.Column(db.Integer)  # breaths per minute
    temperature = db.Column(Numeric(4, 1))  # Celsius
    oxygen_saturation = db.Column(Numeric(4, 1))  # Percentage
    height = db.Column(Numeric(4, 1))  # cm
    weight = db.Column(Numeric(5, 2))  # kg
    
    # Calculated values
    bmi = db.Column(Numeric(4, 1))  # Body Mass Index
    
    # Context
    record_date = db.Column(DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    position = db.Column(db.String(50))  # sitting, standing, lying
    
    # Relationships
    patient = relationship('Patient', back_populates='vital_signs')
    recorded_by_user = relationship('User')
    
    __table_args__ = (
        db.Index('idx_vital_sign_patient_date', 'patient_id', 'record_date'),
        db.Index('idx_vital_sign_date', 'record_date'),
    )

    def _to_dict_impl(self):
        return {
            'blood_pressure': f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}" 
                            if self.blood_pressure_systolic and self.blood_pressure_diastolic else None,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'heart_rate': self.heart_rate,
            'respiratory_rate': self.respiratory_rate,
            'temperature': float(self.temperature) if self.temperature else None,
            'oxygen_saturation': float(self.oxygen_saturation) if self.oxygen_saturation else None,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'bmi': float(self.bmi) if self.bmi else None,
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'position': self.position,
            'notes': self.notes,
            'patient_name': self.patient.full_name if self.patient else None
        }

    def calculate_bmi(self):
        """Calculate BMI from height and weight"""
        if self.height and self.weight:
            # Convert height from cm to meters
            height_m = float(self.height) / 100
            self.bmi = float(self.weight) / (height_m ** 2)
        return self.bmi

    def is_abnormal(self):
        """Check if any vital signs are outside normal range"""
        # Define normal ranges
        normal_ranges = {
            'systolic_bp': (90, 120),
            'diastolic_bp': (60, 80),
            'heart_rate': (60, 100),
            'respiratory_rate': (12, 20),
            'temperature': (36.1, 37.2),  # Celsius
            'oxygen_saturation': (95, 100)
        }
        
        abnormalities = []
        
        if self.blood_pressure_systolic:
            if not (normal_ranges['systolic_bp'][0] <= self.blood_pressure_systolic <= normal_ranges['systolic_bp'][1]):
                abnormalities.append('systolic_bp')
        
        if self.blood_pressure_diastolic:
            if not (normal_ranges['diastolic_bp'][0] <= self.blood_pressure_diastolic <= normal_ranges['diastolic_bp'][1]):
                abnormalities.append('diastolic_bp')
        
        return abnormalities

class LabOrder(BaseModel):
    __tablename__ = 'lab_orders'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    ordered_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    test_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='pending')
    order_date = db.Column(DateTime, default=datetime.utcnow)
    completion_date = db.Column(DateTime)
    results = db.Column(db.Text)
    results_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    patient = relationship('Patient', back_populates='lab_orders')
    treatment = relationship('Treatment', back_populates='lab_orders')
    ordered_by_user = relationship('User', foreign_keys=[ordered_by])

    def _to_dict_impl(self):
        return {
            'test_type': self.test_type,
            'status': self.status,
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'results': self.results,
            'results_url': self.results_url,
            'notes': self.notes,
            'patient_name': self.patient.full_name if self.patient else None,
            'ordered_by_name': f"{self.ordered_by_user.first_name} {self.ordered_by_user.last_name}" if self.ordered_by_user else None
        }

class MedicalRecord(BaseModel):
    __tablename__ = 'medical_records'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    record_type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_url = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    
    patient = relationship('Patient', back_populates='medical_records')
    treatment = relationship('Treatment', back_populates='medical_records')
    uploaded_by_user = relationship('User', foreign_keys=[uploaded_by])

    def _to_dict_impl(self):
        return {
            'record_type': self.record_type,
            'title': self.title,
            'description': self.description,
            'file_url': self.file_url,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'patient_name': self.patient.full_name if self.patient else None,
            'uploaded_by_name': f"{self.uploaded_by_user.first_name} {self.uploaded_by_user.last_name}" if self.uploaded_by_user else None
        }

class Procedure(BaseModel):
    __tablename__ = 'procedures'
    
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    performed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    code = db.Column(db.String(20), nullable=False)
    procedure_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    tooth_number = db.Column(db.String(10))
    surface = db.Column(db.String(10))
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(Numeric(10, 2), nullable=False)
    total_price = db.Column(Numeric(10, 2), nullable=False)
    
    appointment = relationship('Appointment', back_populates='procedures')
    performed_by_user = relationship('User', foreign_keys=[performed_by])

    def _to_dict_impl(self):
        return {
            'code': self.code,
            'procedure_type': self.procedure_type,
            'description': self.description,
            'tooth_number': self.tooth_number,
            'surface': self.surface,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'total_price': float(self.total_price) if self.total_price else None,
            'appointment_title': self.appointment.title if self.appointment else None,
            'performed_by_name': f"{self.performed_by_user.first_name} {self.performed_by_user.last_name}" if self.performed_by_user else None
        }

class Note(BaseModel):
    __tablename__ = 'notes'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    content = db.Column(db.Text, nullable=False)
    tags = db.Column(db.JSON)
    
    patient = relationship('Patient', back_populates='notes')
    created_by_user = relationship('User', foreign_keys=[created_by])

    def _to_dict_impl(self):
        return {
            'content': self.content,
            'tags': self.tags or [],
            'patient_name': self.patient.full_name if self.patient else None,
            'created_by_name': f"{self.created_by_user.first_name} {self.created_by_user.last_name}" if self.created_by_user else None
        }

class AvailabilitySlot(BaseModel):
    __tablename__ = 'availability_slots'
    
    # Foreign keys
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('treatment_rooms.id'), nullable=True)
    
    # Slot timing
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Slot details
    slot_type = db.Column(db.String(50), nullable=False, default='regular')  # regular, emergency, break, meeting
    status = db.Column(db.String(20), nullable=False, default='available')  # available, booked, blocked, cancelled
    recurrence_pattern = db.Column(db.String(50))  # daily, weekly, monthly, none
    recurrence_end_date = db.Column(db.Date)
    
    # Capacity and constraints
    max_patients = db.Column(db.Integer, default=1)
    current_bookings = db.Column(db.Integer, default=0)
    is_bookable = db.Column(db.Boolean, default=True)
    is_online = db.Column(db.Boolean, default=False)  # for tele-dentistry
    
    # Special considerations
    special_notes = db.Column(db.Text)
    allowed_appointment_types = db.Column(db.String(200))  # comma-separated types
    min_advance_booking_hours = db.Column(db.Integer, default=24)
    max_advance_booking_days = db.Column(db.Integer, default=30)
    
    # Required equipment
    required_equipment = db.Column(db.Text)  # comma-separated equipment IDs
    
    # Soft delete
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    staff = db.relationship('Staff', back_populates='availability_slots', lazy=True)
    organization = db.relationship('Organization', back_populates='availability_slots', lazy=True)
    room = db.relationship('TreatmentRoom', back_populates='availability_slots', lazy=True)
    appointments = db.relationship('Appointment', back_populates='availability_slot', lazy=True)
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('end_time > start_time', name='check_end_time_after_start'),
        db.CheckConstraint('current_bookings <= max_patients', name='check_bookings_within_capacity'),
        db.CheckConstraint('max_patients > 0', name='check_positive_capacity'),
        db.Index('idx_clinical_idx_slot_datetime', 'date', 'start_time', 'end_time'),
        db.Index('idx_clinical_idx_staff_availability', 'staff_id', 'date', 'status'),
        db.Index('idx_slot_organization', 'organization_id', 'date'),
    )

    @hybrid_property
    def duration_minutes(self):
        """Calculate slot duration in minutes"""
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = datetime.combine(self.date, self.end_time)
        return int((end_dt - start_dt).total_seconds() / 60)

    @hybrid_property
    def is_available(self):
        """Check if slot is currently available"""
        return (self.status == 'available' and 
                self.is_bookable and 
                self.current_bookings < self.max_patients and
                self.deleted_at is None)

    @hybrid_property
    def is_in_future(self):
        """Check if slot is in the future"""
        now = datetime.now()
        slot_datetime = datetime.combine(self.date, self.start_time)
        return slot_datetime > now

    @hybrid_property
    def is_within_booking_window(self):
        """Check if slot is within advance booking window"""
        now = datetime.now()
        slot_datetime = datetime.combine(self.date, self.start_time)
        
        # Check minimum advance booking
        min_advance = now + timedelta(hours=self.min_advance_booking_hours)
        if slot_datetime < min_advance:
            return False
        
        # Check maximum advance booking
        max_advance = now + timedelta(days=self.max_advance_booking_days)
        if slot_datetime > max_advance:
            return False
        
        return True

    def can_book_appointment_type(self, appointment_type_code):
        """Check if this slot allows the given appointment type"""
        if not self.allowed_appointment_types:
            return True
        allowed_types = [at.strip() for at in self.allowed_appointment_types.split(',')]
        return appointment_type_code in allowed_types

    def book_slot(self):
        """Mark slot as booked (increment booking count)"""
        if self.current_bookings < self.max_patients:
            self.current_bookings += 1
            if self.current_bookings >= self.max_patients:
                self.status = 'booked'
            return True
        return False

    def release_slot(self):
        """Release a booked slot (decrement booking count)"""
        if self.current_bookings > 0:
            self.current_bookings -= 1
            if self.status == 'booked' and self.current_bookings < self.max_patients:
                self.status = 'available'
            return True
        return False

    def _to_dict_impl(self):
        return {
            'date': self.date.isoformat(),
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'duration_minutes': self.duration_minutes,
            'slot_type': self.slot_type,
            'status': self.status,
            'is_available': self.is_available,
            'is_in_future': self.is_in_future,
            'is_within_booking_window': self.is_within_booking_window,
            'max_patients': self.max_patients,
            'current_bookings': self.current_bookings,
            'is_online': self.is_online,
            'special_notes': self.special_notes,
            'staff': {
                'id': self.staff.id,
                'staff_number': self.staff.staff_number,
                'job_title': self.staff.job_title,
                'specialization': self.staff.specialization
            } if self.staff else None,
            'room': {
                'id': self.room.id,
                'name': self.room.name,
                'room_number': self.room.room_number
            } if self.room else None,
            'organization': {
                'id': self.organization.id,
                'name': self.organization.name
            } if self.organization else None
        }

    @classmethod
    def get_available_slots(cls, staff_id, date, appointment_type_code=None):
        """Get available slots for a staff member on a specific date"""
        query = cls.query.filter(
            cls.staff_id == staff_id,
            cls.date == date,
            cls.status == 'available',
            cls.is_bookable == True,
            cls.deleted_at.is_(None)
        )
        
        if appointment_type_code:
            query = query.filter(
                cls.allowed_appointment_types.contains(appointment_type_code) | 
                (cls.allowed_appointment_types.is_(None))
            )
        
        return query.order_by(cls.start_time).all()

    @classmethod
    def create_recurring_slots(cls, staff_id, start_date, end_date, start_time, end_time, 
                             days_of_week, slot_type='regular', max_patients=1):
        """Create recurring slots for a date range"""
        current_date = start_date
        created_slots = []
        
        while current_date <= end_date:
            if current_date.weekday() in days_of_week:  # 0=Monday, 6=Sunday
                slot = cls(
                    staff_id=staff_id,
                    date=current_date,
                    start_time=start_time,
                    end_time=end_time,
                    slot_type=slot_type,
                    max_patients=max_patients,
                    status='available'
                )
                created_slots.append(slot)
            
            current_date += timedelta(days=1)
        
        return created_slots

    def block_slot(self, reason):
        """Block this slot from being booked"""
        self.status = 'blocked'
        self.special_notes = f"Blocked: {reason}"
        return True

    def unblock_slot(self):
        """Unblock a previously blocked slot"""
        if self.status == 'blocked':
            self.status = 'available'
            self.special_notes = None
            return True
        return False

    def __repr__(self):
        return f'<AvailabilitySlot {self.date} {self.start_time}-{self.end_time} - {self.status}>'
    
class TreatmentRoom(BaseModel):
    __tablename__ = 'treatment_rooms'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(20))
    description = db.Column(db.Text)
    room_type = db.Column(db.String(50))  # operatory, consultation, surgery, etc.
    equipment = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    
    # Relationships
    organization = db.relationship('Organization', back_populates='treatment_rooms')
    availability_slots = db.relationship('AvailabilitySlot', back_populates='room')
    
    def _to_dict_impl(self):
        return {
            'name': self.name,
            'room_number': self.room_number,
            'room_type': self.room_type,
            'status': self.status,
            'equipment': self.equipment,
            'organization_name': self.organization.name if self.organization else None
        }


class TelehealthSession(db.Model):
    __tablename__ = 'telehealth_sessions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    session_url = db.Column(db.String(500), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    appointment = db.relationship('Appointment', back_populates='telehealth_session')

    def to_dict(self):
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'session_url': self.session_url,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'appointment_title': self.appointment.title if self.appointment else None
        }


