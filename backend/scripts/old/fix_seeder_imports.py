# backend/scripts/fix_seeder_imports.py
import os
import re

def fix_seeder_imports():
    print("🔧 FIXING SEEDER IMPORTS")
    print("=" * 50)
    
    seeder_file = 'scripts/seed_demo_data.py'
    
    if not os.path.exists(seeder_file):
        print(f"❌ {seeder_file} not found")
        return False
    
    # Read the seeder file
    with open(seeder_file, 'r') as f:
        content = f.read()
    
    # Find and replace problematic imports
    replacements = {
        r'from app\.models\.clinical\.appointment import Appointment': 
            'from app.models.clinical import Appointment',
        r'from app\.models\.clinical\.treatment import Treatment': 
            'from app.models.clinical import Treatment',
        r'from app\.models\.clinical\.note import ClinicalNote': 
            'from app.models.clinical import ClinicalNote',
        r'from app\.models\.clinical\.allergy import Allergy': 
            'from app.models.clinical import Allergy',
        r'from app\.models\.clinical\.prescription import Prescription': 
            'from app.models.clinical import Prescription',
        r'from app\.models\.clinical\.vital_sign import VitalSign': 
            'from app.models.clinical import VitalSign',
    }
    
    new_content = content
    for old, new in replacements.items():
        new_content = re.sub(old, new, new_content)
    
    if new_content != content:
        # Backup original
        backup_file = seeder_file + '.backup'
        with open(backup_file, 'w') as f:
            f.write(content)
        print(f"✅ Created backup: {backup_file}")
        
        # Write fixed version
        with open(seeder_file, 'w') as f:
            f.write(new_content)
        print("✅ Fixed import statements in seeder")
    else:
        print("✅ No changes needed - imports already correct")
    
    return True

if __name__ == '__main__':
    success = fix_seeder_imports()
    if success:
        print("\n📝 Now try running the seeder again:")
        print("python scripts/seed_demo_data.py")