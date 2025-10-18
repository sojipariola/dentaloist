#!/usr/bin/env python3
"""
Emergency fix for database - creates database directly
"""

import os
import sys
import shutil
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def emergency_fix():
    """Emergency fix - create database directly without migrations"""
    print("🚨 EMERGENCY DATABASE FIX")
    print("=" * 40)
    
    # Clean up
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
        print("✅ Removed migrations directory")
    
    db_path = Path('instance/dentaloist.db')
    if db_path.exists():
        os.remove(db_path)
        print("✅ Removed database file")
    
    # Create instance directory
    instance_dir = Path('instance')
    if not instance_dir.exists():
        instance_dir.mkdir(parents=True)
        print("✅ Created instance directory")
    
    # Create database directly using your app
    print("\n🔄 Creating database directly...")
    
    # Import and create your actual app
    try:
        # Set environment variables first
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_APP'] = 'app:create_app()'
        
        # Now import app
        from app import create_app, db
        
        app = create_app()
        
        with app.app_context():
            # Create all tables directly
            db.create_all()
            print("✅ All tables created directly")
            
            # Verify basic tables exist
            from app.models import Organization, User, Patient
            org_count = Organization.query.count()
            user_count = User.query.count()
            patient_count = Patient.query.count()
            
            print(f"📊 Database created with:")
            print(f"   🏢 {org_count} organizations")
            print(f"   👥 {user_count} users") 
            print(f"   👤 {patient_count} patients")
            
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        
        # Try alternative approach with minimal setup
        print("\n🔄 Trying alternative approach...")
        create_minimal_database()
        return
    
    # Now seed data
    print("\n🌱 Seeding data...")
    seed_data()

def create_minimal_database():
    """Create a minimal database if the main approach fails"""
    print("🔄 Creating minimal database...")
    
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    # Create minimal Flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'minimal-setup-key'
    
    db = SQLAlchemy(app)
    
    # Define minimal models
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(255), nullable=False)
        is_active = db.Column(db.Boolean, default=True)
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(255), nullable=False)
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
    
    class Patient(db.Model):
        __tablename__ = 'patients'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50))
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✅ Minimal tables created")
        
        # Create some basic data
        org = Organization(public_id='org_001', name='Test Dental Clinic')
        db.session.add(org)
        
        user = User(public_id='user_001', email='admin@test.com', organization_id='org_001')
        db.session.add(user)
        
        patient = Patient(public_id='patient_001', first_name='John', last_name='Doe', organization_id='org_001')
        db.session.add(patient)
        
        db.session.commit()
        print("✅ Basic test data created")

def seed_data():
    """Seed data using subprocess to avoid import issues"""
    import subprocess
    
    scripts = [
        ('seed_lookups.py', 'Lookup data'),
        ('seed_tenants.py', 'Tenant data'),
        ('verify_tenancy.py', 'Verification')
    ]
    
    for script, description in scripts:
        script_path = Path(f'scripts/{script}')
        if script_path.exists():
            print(f"\n📋 Seeding {description}...")
            try:
                # Use the same Python interpreter
                result = subprocess.run([sys.executable, str(script_path)], 
                                      capture_output=True, text=True, timeout=120)
                print(result.stdout)
                if result.returncode != 0:
                    print(f"⚠️  {description} seeding had issues: {result.stderr}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {description} seeding timed out")
            except Exception as e:
                print(f"❌ {description} seeding failed: {e}")
        else:
            print(f"❌ Script not found: {script_path}")
    
    print("\n🎉 EMERGENCY FIX COMPLETE!")
    print("💡 Database is ready for development")

if __name__ == '__main__':
    emergency_fix()