# check_models_content.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Disable eventlet
os.environ['EVENTLET_NO_GREENDNS'] = 'yes'

def check_models_content():
    print("🔍 Checking model files content...")
    
    # Import your models module to see what's available
    try:
        from app.models import base, core, clinical, financial, analytics, inventory
        
        print("✅ Successfully imported model modules")
        
        # Check what classes are defined in each module
        print("\n📋 Classes in base.py:")
        for attr in dir(base):
            if not attr.startswith('_'):
                print(f"  - {attr}")
        
        print("\n📋 Classes in core.py:")
        for attr in dir(core):
            if not attr.startswith('_'):
                print(f"  - {attr}")
        
        print("\n📋 Classes in clinical.py:")
        for attr in dir(clinical):
            if not attr.startswith('_'):
                print(f"  - {attr}")
                
    except Exception as e:
        print(f"❌ Error importing modules: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_models_content()
