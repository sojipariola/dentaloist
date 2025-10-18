#!/usr/bin/env python3
"""
Seed all lookup data from app/seed/lookups files
"""

import sys
import os
import importlib.util
from pathlib import Path

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Now import using the full path
from backend.app import create_app, db


def create_app():
    """Create Flask app for seeding"""
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev-secret-key'
    
    return app

def seed_all_lookups():
    """Seed all lookup data from seed files"""
    app = create_app()
    
    # Initialize with your app's db
    # from app import db
    db.init_app(app)
    
    with app.app_context():
        print("📋 SEEDING ALL LOOKUP DATA")
        print("=" * 50)
        
        lookup_dir = Path('app/seed/lookups')
        
        if not lookup_dir.exists():
            print(f"❌ Lookup directory not found: {lookup_dir}")
            return
        
        # Get all seed files
        seed_files = sorted(lookup_dir.glob('*_seed.py'))
        
        if not seed_files:
            print(f"❌ No seed files found in {lookup_dir}")
            return
        
        print(f"📁 Found {len(seed_files)} lookup seed files:")
        
        # Import and run each seed file
        for seed_file in seed_files:
            print(f"\n🔄 Seeding: {seed_file.name}")
            
            try:
                # Dynamically import the seed module
                spec = importlib.util.spec_from_file_location(seed_file.stem, seed_file)
                seed_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(seed_module)
                
                # Check if the module has a seed function
                if hasattr(seed_module, 'seed'):
                    seed_module.seed(db)
                    print(f"   ✅ Successfully seeded: {seed_file.name}")
                else:
                    print(f"   ⚠️  No seed function found in: {seed_file.name}")
                    
            except Exception as e:
                print(f"   ❌ Error seeding {seed_file.name}: {e}")
                import traceback
                traceback.print_exc()
        
        print(f"\n🎉 LOOKUP SEEDING COMPLETE!")
        print(f"📊 Seeded {len(seed_files)} lookup tables")

def verify_lookups():
    """Verify that lookups were seeded properly"""
    app = create_app()
    
    from app import db
    db.init_app(app)
    
    with app.app_context():
        print(f"\n🔍 VERIFYING LOOKUP DATA")
        print("=" * 40)
        
        from app.models import (
            UserRole, OrganizationType, Gender, AppointmentStatus, AppointmentType,
            PaymentStatus, InvoiceStatus, PaymentMethod, TreatmentStatus, TreatmentType,
            AllergySeverity, MedicationRoute
        )
        
        lookup_tables = [
            ('User Roles', UserRole),
            ('Organization Types', OrganizationType),
            ('Genders', Gender),
            ('Appointment Statuses', AppointmentStatus),
            ('Appointment Types', AppointmentType),
            ('Payment Statuses', PaymentStatus),
            ('Invoice Statuses', InvoiceStatus),
            ('Payment Methods', PaymentMethod),
            ('Treatment Statuses', TreatmentStatus),
            ('Treatment Types', TreatmentType),
            ('Allergy Severities', AllergySeverity),
            ('Medication Routes', MedicationRoute)
        ]
        
        all_good = True
        for name, model in lookup_tables:
            count = model.query.count()
            if count > 0:
                print(f"   ✅ {name}: {count} records")
            else:
                print(f"   ❌ {name}: No records found!")
                all_good = False
        
        if all_good:
            print(f"\n🎉 All lookup tables seeded successfully!")
        else:
            print(f"\n⚠️  Some lookup tables missing data!")

if __name__ == '__main__':
    seed_all_lookups()
    verify_lookups()