# backend/scripts/seed_lookups_unified.py
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.seed.lookups import seed_all

def seed_all_lookups():
    """Seed all lookup tables using the existing seed structure"""
    app = create_app()
    
    with app.app_context():
        print("📋 Seeding lookup data...")
        try:
            seed_all()
            print("✅ Lookup data seeded successfully")
        except Exception as e:
            print(f"❌ Error seeding lookup data: {e}")
            raise

if __name__ == '__main__':
    seed_all_lookups()