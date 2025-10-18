# backend/scripts/fix_all_lookup_seeders.py
import os
import sys
import glob

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fix_lookup_seeders():
    """Fix all lookup seeder files by adding code fields and proper structure"""
    
    lookup_files = glob.glob('app/seed/lookups/*_seed.py')
    
    print("🔧 Fixing all lookup seeder files...")
    
    for file_path in lookup_files:
        print(f"\n📁 Processing: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Check if file already has the new pattern
            if 'no_autoflush' in content and 'seeded_count' in content:
                print("   ✅ Already fixed - skipping")
                continue
            
            # This is a complex transformation, so we'll create new files
            # For now, let's just identify which files need manual fixes
            if 'code' not in content or 'code": None' in content:
                print("   ❌ Needs manual fix - missing code fields")
            else:
                print("   ⚠️  May need structure update")
                
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    
    print(f"\n📋 Summary: {len(lookup_files)} lookup seeder files found")
    print("💡 Manual fixes needed for files marked with ❌")

if __name__ == '__main__':
    fix_lookup_seeders()