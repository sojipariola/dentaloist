#!/usr/bin/env python3
"""
COMPLETE DATABASE RESET with migration fixes
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def full_reset_fixed():
    """Complete reset with migration fixes"""
    print("🔄 COMPLETE DATABASE RESET WITH MIGRATION FIXES")
    print("=" * 60)
    
    # Confirm reset
    response = input("❓ Are you sure you want to reset everything? (yes/NO): ")
    if response.lower() != 'yes':
        print("❌ Reset cancelled.")
        return
    
    # Step 1: Clean up
    print("\n🗑️  Step 1: Cleaning up...")
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        shutil.rmtree(migrations_dir)
        print("✅ Deleted migrations directory")
    
    db_path = Path('instance/dentaloist.db')
    if db_path.exists():
        os.remove(db_path)
        print("✅ Deleted database file")
    
    # Ensure instance directory exists
    instance_dir = Path('instance')
    if not instance_dir.exists():
        instance_dir.mkdir(parents=True)
        print("✅ Created instance directory")
    
    # Step 2: Initialize with simple approach
    print("\n🔄 Step 2: Initializing simple migrations...")
    
    # Create a minimal Flask app for migrations
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'migration-fix-key'
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    # Define only essential models for migration
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(255), nullable=False)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(255), nullable=False)
        password_hash = db.Column(db.String(255))
        first_name = db.Column(db.String(100))
        last_name = db.Column(db.String(100))
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    class Patient(db.Model):
        __tablename__ = 'patients'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50))
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        organization_id = db.Column(db.String(50))
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Initialize migrations with our simple app
    with app.app_context():
        # Initialize migrations
        try:
            migrate.init_app(app, db, directory='migrations')
            print("✅ Migrations initialized")
        except Exception as e:
            print(f"❌ Failed to initialize migrations: {e}")
            return
        
        # Create tables directly (bypass migration for now)
        db.create_all()
        print("✅ Created essential tables")
    
    # Step 3: Now use the actual app to generate proper migration
    print("\n📝 Step 3: Generating proper migration...")
    
    # Set FLASK_APP to use your actual app
    os.environ['FLASK_APP'] = 'app:create_app()'
    
    try:
        # Generate migration with actual models
        result = subprocess.run([
            'flask', 'db', 'migrate', '-m', 'initial_tables'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Migration generated successfully")
            print(result.stdout)
        else:
            print(f"⚠️  Migration generation had warnings: {result.stderr}")
            
            # Try alternative approach
            print("🔄 Trying alternative migration approach...")
            result = subprocess.run([
                'flask', 'db', 'revision', '--autogenerate', '-m', 'initial_tables'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("✅ Migration generated (alternative method)")
            else:
                print(f"❌ Failed to generate migration: {result.stderr}")
                # Continue anyway - we have the basic tables
    except subprocess.TimeoutExpired:
        print("⚠️  Migration generation timed out, but basic tables are created")
    except Exception as e:
        print(f"⚠️  Migration generation error: {e}, but basic tables are created")
    
    # Step 4: Apply migrations
    print("\n🚀 Step 4: Applying migrations...")
    try:
        result = subprocess.run(['flask', 'db', 'upgrade'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Migrations applied successfully")
        else:
            print(f"⚠️  Migration application had issues: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⚠️  Migration application timed out")
    except Exception as e:
        print(f"⚠️  Migration application error: {e}")
    
    # Step 5: Seed data
    print("\n📋 Step 5: Seeding data...")
    
    # Seed lookups
    try:
        result = subprocess.run([sys.executable, 'scripts/seed_lookups.py'], capture_output=True, text=True, timeout=60)
        print("Lookup seeding output:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Lookup seeding issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Lookup seeding failed: {e}")
    
    # Seed tenants
    try:
        result = subprocess.run([sys.executable, 'scripts/seed_tenants.py'], capture_output=True, text=True, timeout=60)
        print("Tenant seeding output:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Tenant seeding issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Tenant seeding failed: {e}")
    
    # Verify
    try:
        result = subprocess.run([sys.executable, 'scripts/verify_tenancy.py'], capture_output=True, text=True, timeout=30)
        print("Verification output:")
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️  Verification issues: {result.stderr}")
    except Exception as e:
        print(f"❌ Verification failed: {e}")
    
    print("\n🎉 RESET PROCESS COMPLETED!")
    print("💡 Basic database structure is ready for development")

if __name__ == '__main__':
    full_reset_fixed()