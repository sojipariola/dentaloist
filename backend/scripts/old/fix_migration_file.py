# backend/scripts/fix_migration_file.py
import os
import glob

def fix_migration_file():
    """Fix the ArrayOrJSON references in migration files"""
    
    # Find the latest migration file
    migration_files = glob.glob('migrations/versions/*.py')
    if not migration_files:
        print("❌ No migration files found")
        return False
    
    migration_file = sorted(migration_files)[-1]  # Get the latest
    print(f"📝 Fixing migration file: {migration_file}")
    
    # Read the file
    with open(migration_file, 'r') as f:
        content = f.read()
    
    # Replace the problematic lines
    replacements = {
        "app.models._compat.ArrayOrJSON(none_as_null=String(length=50))": "sa.JSON()",
        "app.models._compat.ArrayOrJSON(none_as_null=String(length=100))": "sa.JSON()", 
        "app.models._compat.ArrayOrJSON(none_as_null=String(length=255))": "sa.JSON()",
    }
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Check if changes were made
    if content != original_content:
        # Create backup
        backup_file = migration_file + '.backup'
        with open(backup_file, 'w') as f:
            f.write(original_content)
        print(f"✅ Created backup: {backup_file}")
        
        # Write fixed content
        with open(migration_file, 'w') as f:
            f.write(content)
        print("✅ Migration file fixed successfully")
        
        # Show the changes
        print("📋 Changes made:")
        for old, new in replacements.items():
            if old in original_content:
                print(f"   {old} → {new}")
    else:
        print("✅ No changes needed - file already fixed")
    
    return True

if __name__ == '__main__':
    success = fix_migration_file()
    if success:
        print("\n🔄 Now run: python -m flask db upgrade")
    else:
        print("\n❌ Fix failed!")