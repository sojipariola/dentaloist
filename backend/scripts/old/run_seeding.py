# backend/scripts/run_seeding.py
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_demo_data import seed_demo_data

if __name__ == '__main__':
    print("🌱 Starting comprehensive demo data seeding...")
    seed_demo_data()
    print("🎉 Demo data seeding completed!")