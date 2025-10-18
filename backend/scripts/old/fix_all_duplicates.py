#!/usr/bin/env python3
import re
import os

# Dictionary to track index renames
index_renames = {}

def find_all_duplicates():
    """Find all duplicate index names across all model files"""
    print("🔍 Finding all duplicate index names...")
    
    index_locations = {}
    
    # Search through all model files
    models_dir = "app/models"
    for root, dirs, files in os.walk(models_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Find all db.Index calls
                    matches = re.finditer(r"db\.Index\('([^']+)',[^)]+\)", content)
                    for match in matches:
                        index_name = match.group(1)
                        if index_name not in index_locations:
                            index_locations[index_name] = []
                        index_locations[index_name].append(file_path)
    
    # Return only duplicates
    duplicates = {name: files for name, files in index_locations.items() if len(files) > 1}
    return duplicates

def generate_unique_names(duplicates):
    """Generate unique names for duplicate indexes"""
    renames = {}
    for index_name, files in duplicates.items():
        for i, file_path in enumerate(files):
            # Get model name from file path
            model_name = os.path.basename(file_path).replace('.py', '')
            if i == 0:
                # Keep the first occurrence as is (or add model prefix if needed)
                new_name = f"idx_{model_name}_{index_name}" if index_name.startswith('idx_') else f"idx_{model_name}_{index_name}"
            else:
                # Add model prefix for duplicates
                new_name = f"idx_{model_name}_{index_name}" if index_name.startswith('idx_') else f"idx_{model_name}_{index_name}"
            renames[(file_path, index_name)] = new_name
    return renames

def fix_duplicate_indexes():
    """Fix all duplicate index names"""
    print("🔧 Fixing all duplicate index names...")
    
    duplicates = find_all_duplicates()
    
    if not duplicates:
        print("✅ No duplicate indexes found!")
        return True
    
    print(f"🚨 Found {len(duplicates)} duplicate index names:")
    for name, files in duplicates.items():
        print(f"   '{name}' in:")
        for file in files:
            print(f"     - {file}")
    
    # Generate new names
    renames = generate_unique_names(duplicates)
    
    # Apply renames
    for (file_path, old_name), new_name in renames.items():
        print(f"   Renaming: {old_name} → {new_name} in {file_path}")
        
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Replace the index name
        new_content = re.sub(
            f"db\\.Index\\('{old_name}',",
            f"db.Index('{new_name}',",
            content
        )
        
        with open(file_path, 'w') as f:
            f.write(new_content)
    
    print(f"✅ Fixed {len(renames)} duplicate index names")
    return True

if __name__ == "__main__":
    if fix_duplicate_indexes():
        print("🎉 All duplicates fixed!")
    else:
        print("💥 Failed to fix duplicates")
