# backend/app/seed/user_seeds.py
from app import db
from app.models import User, UserRole
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

def seed_users():
    """Seed sample users for each organization"""
    
    # Get roles for assignment
    super_admin_role = UserRole.query.filter_by(name="Super Administrator").first()
    dentist_role = UserRole.query.filter_by(name="Dentist").first()
    hygienist_role = UserRole.query.filter_by(name="Dental Hygienist").first()
    receptionist_role = UserRole.query.filter_by(name="Receptionist").first()
    
    users = [
        # Demo Dental Clinic Staff
        {
            "email": "admin@demodental.com",
            "first_name": "Sarah",
            "last_name": "Johnson",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "demo-dental-001",
            "role_id": super_admin_role.id,
            "phone": "+1-555-1001",
            "license_number": "DENT12345",
            "specialty": "General Dentistry",
            "is_active": True,
            "email_verified": True,
        },
        {
            "email": "dr.miller@demodental.com",
            "first_name": "Michael",
            "last_name": "Miller",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "demo-dental-001",
            "role_id": dentist_role.id,
            "phone": "+1-555-1002",
            "license_number": "DENT12346",
            "specialty": "Restorative Dentistry",
            "is_active": True,
            "email_verified": True,
        },
        {
            "email": "emily@demodental.com",
            "first_name": "Emily",
            "last_name": "Chen",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "demo-dental-001",
            "role_id": hygienist_role.id,
            "phone": "+1-555-1003",
            "license_number": "HYG12345",
            "is_active": True,
            "email_verified": True,
        },
        {
            "email": "reception@demodental.com",
            "first_name": "Lisa",
            "last_name": "Garcia",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "demo-dental-001",
            "role_id": receptionist_role.id,
            "phone": "+1-555-1004",
            "is_active": True,
            "email_verified": True,
        },
        
        # Smile Center Staff
        {
            "email": "admin@smilecenter.com",
            "first_name": "Robert",
            "last_name": "Wilson",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "smile-center-002",
            "role_id": super_admin_role.id,
            "phone": "+1-555-2001",
            "license_number": "DENT22345",
            "specialty": "Orthodontics",
            "is_active": True,
            "email_verified": True,
        },
        {
            "email": "dr.lee@smilecenter.com",
            "first_name": "Jennifer",
            "last_name": "Lee",
            "password_hash": generate_password_hash("demo123"),
            "organization_id": "smile-center-002",
            "role_id": dentist_role.id,
            "phone": "+1-555-2002",
            "license_number": "DENT22346",
            "specialty": "Orthodontics",
            "is_active": True,
            "email_verified": True,
        }
    ]
    
    for user_data in users:
        existing = User.query.filter_by(email=user_data["email"]).first()
        if not existing:
            user = User(**user_data)
            db.session.add(user)
    
    db.session.commit()
    print("✅ Users seeded successfully.")