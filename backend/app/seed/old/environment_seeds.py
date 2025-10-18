# backend/app/seed/environment_seeds.py
import os
from app import db

def seed_environment_specific():
    """Seed data specific to different environments"""
    environment = os.getenv('FLASK_ENV', 'development')
    
    if environment == 'development':
        seed_development_data()
    elif environment == 'testing':
        seed_testing_data()
    elif environment == 'production':
        seed_production_data()

def seed_development_data():
    """Seed development-specific data"""
    print("🔧 Seeding development data...")
    # Add development-specific seeds here
    seed_test_users()
    seed_sample_analytics()

def seed_testing_data():
    """Seed testing-specific data"""
    print("🧪 Seeding testing data...")
    # Minimal data for tests
    seed_minimal_test_data()

def seed_production_data():
    """Seed production-specific data"""
    print("🚀 Seeding production data...")
    # Only essential lookup data
    seed_essential_lookups_only()