# backend/scripts/manual_fix_instructions.py
import glob

def show_manual_fix_instructions():
    """Show instructions for manually fixing problematic seeders"""
    
    problematic_files = []
    
    for file_path in glob.glob('app/seed/lookups/*_seed.py'):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if file needs manual fix
        if 'no_autoflush' not in content or 'code' not in content:
            problematic_files.append(file_path)
    
    if problematic_files:
        print("📋 MANUAL FIX INSTRUCTIONS")
        print("=" * 50)
        print("\nFor each file below, you need to:")
        print("1. Add 'code' field to every dictionary in the data list")
        print("2. Wrap database operations in 'with db.session.no_autoflush:'")
        print("3. Check by code instead of name")
        print("4. Add error handling with try-catch")
        print("5. Generate public_id if missing")
        
        print("\n📁 Files needing manual fixes:")
        for file_path in problematic_files:
            print(f"   • {file_path}")
        
        print(f"\n💡 Total files needing manual attention: {len(problematic_files)}")
    else:
        print("✅ All files are already fixed!")

if __name__ == '__main__':
    show_manual_fix_instructions()