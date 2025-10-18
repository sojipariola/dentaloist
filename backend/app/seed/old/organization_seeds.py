# backend/app/seed/organization_seeds.py
from app import db
from app.models import Organization, Tenant, SubscriptionPlan
from datetime import datetime, timedelta
import secrets

def seed_organizations():
    """Seed sample organizations and tenants"""
    organizations = [
        {
            "id": "demo-dental-001",
            "name": "Demo Dental Clinic",
            "email": "info@demodental.com",
            "phone": "+1-555-0101",
            "address": "123 Main Street",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62701",
            "country": "US",
            "organization_type_id": 1,  # Solo Practice
            "industry_type_id": 1,  # General Dentistry
            "timezone": "America/Chicago",
            "locale": "en_US",
            "is_active": True,
        },
        {
            "id": "smile-center-002",
            "name": "Smile Center Orthodontics",
            "email": "admin@smilecenter.com",
            "phone": "+1-555-0102",
            "address": "456 Oak Avenue",
            "city": "Springfield",
            "state": "IL",
            "zip_code": "62702",
            "country": "US",
            "organization_type_id": 2,  # Group Practice
            "industry_type_id": 2,  # Orthodontics
            "timezone": "America/Chicago",
            "locale": "en_US",
            "is_active": True,
        }
    ]
    
    for org_data in organizations:
        existing = Organization.query.filter_by(id=org_data["id"]).first()
        if not existing:
            org = Organization(**org_data)
            db.session.add(org)
            
            # Create tenant for organization
            tenant = Tenant(
                organization_id=org.id,
                subdomain=org.name.lower().replace(' ', '-'),
                status_id=1,  # Active
                plan_id=2,  # Starter plan
                trial_ends_at=datetime.utcnow() + timedelta(days=30),
                settings={
                    "appointment_reminder_hours": 24,
                    "auto_confirm_appointments": True,
                    "enable_sms_notifications": True,
                    "default_appointment_duration": 30
                }
            )
            db.session.add(tenant)
    
    db.session.commit()
    print("✅ Organizations and tenants seeded successfully.")