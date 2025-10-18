# backend/scripts/debug_import_issue.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def debug_import_issue():
    print("🔍 COMPREHENSIVE IMPORT DEBUG")
    print("=" * 50)
    
    # Test 1: Check if clinical.py exists and can be imported
    clinical_path = 'app/models/clinical.py'
    print(f"1. Checking {clinical_path}...")
    if os.path.exists(clinical_path):
        print("   ✅ clinical.py exists")
        
        # Check file size
        size = os.path.getsize(clinical_path)
        print(f"   📏 File size: {size} bytes")
        
        # Check if it's empty
        if size == 0:
            print("   ❌ File is empty!")
            return False
    else:
        print("   ❌ clinical.py not found!")
        return False
    
    # Test 2: Try to import the clinical module
    print("\n2. Testing clinical module import...")
    try:
        import app.models.clinical as clinical_mod
        print("   ✅ clinical module imported")
        
        # List everything in the module
        items = [name for name in dir(clinical_mod) if not name.startswith('_')]
        print(f"   📦 Contents: {items}")
        
    except Exception as e:
        print(f"   ❌ Failed to import clinical module: {e}")
        return False
    
    # Test 3: Try to import Appointment class
    print("\n3. Testing Appointment class import...")
    try:
        from app.models.clinical import Appointment
        print("   ✅ Appointment class imported")
        print(f"   🏷️  Table name: {getattr(Appointment, '__tablename__', 'NOT SET')}")
        print(f"   📍 Module: {Appointment.__module__}")
        
    except Exception as e:
        print(f"   ❌ Failed to import Appointment: {e}")
        return False
    
    # Test 4: Check the actual import line in the seeder
    print("\n4. Checking seeder import statements...")
    seeder_path = 'scripts/seed_demo_data.py'
    with open(seeder_path, 'r') as f:
        seeder_content = f.read()
    
    # Find clinical imports
    import re
    clinical_imports = re.findall(r'from app\.models\.clinical.*', seeder_content)
    print("   Import statements found:")
    for imp in clinical_imports:
        print(f"   📝 {imp}")
    
    # Test 5: Simulate the exact import the seeder is doing
    print("\n5. Testing exact seeder import...")
    try:
        # This is what the seeder should be doing
        exec("from app.models.clinical import Appointment")
        print("   ✅ Seeder-style import works")
    except Exception as e:
        print(f"   ❌ Seeder-style import failed: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = debug_import_issue()
    if success:
        print("\n🎉 All import tests passed!")
        print("💡 The issue might be elsewhere in the seeder")
    else:
        print("\n❌ Import issue found!")