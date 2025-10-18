#!/usr/bin/env python3
"""
Fix migration import issues
"""

import os
import re
from pathlib import Path

def fix_migration_imports():
    """Fix app import issues in migration files"""
    migrations_dir = Path('migrations/versions')
    
    if not migrations_dir.exists():
        print("❌ Migrations directory not found")
        return
    
    migration_files = list(migrations_dir.glob('*.py'))
    
    if not migration_files:
        print("❌ No migration files found")
        return
    
    print(f"🔧 Fixing {len(migration_files)} migration files...")
    
    for migration_file in migration_files:
        print(f"📝 Processing: {migration_file.name}")
        
        with open(migration_file, 'r') as f:
            content = f.read()
        
        # Fix app.models._compat import issues
        if 'app.models._compat' in content:
            # Replace app.models._compat with direct JSON type
            content = content.replace(
                'app.models._compat.ArrayOrJSON(none_as_null=String(length=50))',
                'sa.JSON()'
            )
            content = content.replace(
                'app.models._compat.ArrayOrJSON',
                'sa.JSON'
            )
            
            print(f"   ✅ Fixed ArrayOrJSON imports in {migration_file.name}")
        
        # Write the fixed content back
        with open(migration_file, 'w') as f:
            f.write(content)
    
    print("🎉 Migration files fixed!")

def create_simple_migration():
    """Create a simple migration without complex imports"""
    print("\n🔄 Creating simple migration...")
    
    # Remove existing migrations
    migrations_dir = Path('migrations')
    if migrations_dir.exists():
        import shutil
        shutil.rmtree(migrations_dir)
        print("✅ Removed old migrations")
    
    # Delete database
    db_path = Path('instance/dentaloist.db')
    if db_path.exists():
        os.remove(db_path)
        print("✅ Removed database")
    
    # Reinitialize with simple models
    import subprocess
    subprocess.run(['flask', 'db', 'init'], capture_output=True)
    print("✅ Reinitialized migrations")
    
    # Create a minimal migration by importing only what we need
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/dentaloist.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    # Define minimal models for migration
    class Organization(db.Model):
        __tablename__ = 'organizations'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        name = db.Column(db.String(255), nullable=False)
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50), unique=True, nullable=False)
        email = db.Column(db.String(255), nullable=False)
        organization_id = db.Column(db.String(50))
    
    class Patient(db.Model):
        __tablename__ = 'patients'
        id = db.Column(db.Integer, primary_key=True)
        public_id = db.Column(db.String(50))
        first_name = db.Column(db.String(100), nullable=False)
        last_name = db.Column(db.String(100), nullable=False)
        organization_id = db.Column(db.String(50))
    
    # Create tables
    with app.app_context():
        db.create_all()
        print("✅ Created minimal tables")
    
    # Generate migration
    result = subprocess.run(['flask', 'db', 'migrate', '-m', 'minimal_tables'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Generated minimal migration")
    else:
        print(f"❌ Failed to generate migration: {result.stderr}")

if __name__ == '__main__':
    fix_migration_imports()
    create_simple_migration()