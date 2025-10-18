# backend/scripts/batch_fix_lookup_seeders.py
import os
import sys
import glob
import re

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_fixed_template():
    """Return the fixed template for lookup seeders"""
    return '''from app import db
from app.models.lookup_models import {model_class}
import uuid


def {function_name}():
    """Seed {human_name} with required code field"""
    
    data_list = {data_list}

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in data_list:
            # Check if record already exists by code
            existing = {model_class}.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing record
                print(f"🔄 Updating existing {singular_name}: {{data['name']}}")
                for key, value in data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new record
                print(f"✅ Adding new {singular_name}: {{data['name']}}")
                
                # Generate public_id if not provided
                if 'public_id' not in data:
                    data['public_id'] = str(uuid.uuid4())
                
                record = {model_class}(**data)
                db.session.add(record)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ {human_name} seeded: {{seeded_count}} added, {{updated_count}} updated")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding {human_name}: {{e}}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        {function_name}()
'''

def extract_model_class(content):
    """Extract model class from import statement"""
    match = re.search(r'from app\.models\.lookup_models import (\w+)', content)
    if match:
        return match.group(1)
    return None

def extract_function_name(content):
    """Extract function name from content"""
    match = re.search(r'def (\w+)\(\):', content)
    if match:
        return match.group(1)
    return None

def extract_data_list(content):
    """Extract the data list from content"""
    # Find the list assignment
    match = re.search(r'(\w+)\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if match:
        var_name = match.group(1)
        list_content = match.group(2)
        
        # Try to find the actual list content more accurately
        start = content.find(var_name + ' = [')
        if start != -1:
            bracket_count = 1
            pos = start + len(var_name) + 3  # Position after '['
            while pos < len(content) and bracket_count > 0:
                if content[pos] == '[':
                    bracket_count += 1
                elif content[pos] == ']':
                    bracket_count -= 1
                pos += 1
            
            if bracket_count == 0:
                list_content = content[start + len(var_name) + 3:pos-1]
                # Clean up the list content
                list_content = re.sub(r'#.*?$', '', list_content, flags=re.MULTILINE)
                list_content = list_content.strip()
                return list_content
    return None

def add_code_fields(data_list_content):
    """Add code fields to each dictionary in the data list"""
    if not data_list_content:
        return None
    
    # Split into individual dictionary entries
    entries = []
    current_entry = ""
    brace_count = 0
    
    for char in data_list_content:
        if char == '{':
            brace_count += 1
            current_entry += char
        elif char == '}':
            brace_count -= 1
            current_entry += char
            if brace_count == 0:
                entries.append(current_entry.strip())
                current_entry = ""
        else:
            if brace_count > 0 or current_entry:
                current_entry += char
    
    fixed_entries = []
    for i, entry in enumerate(entries):
        if entry:
            # Check if entry already has a code field
            if '"code"' not in entry and "'code'" not in entry:
                # Extract the name field to generate a code
                name_match = re.search(r"['\"]name['\"]\s*:\s*['\"]([^'\"]+)['\"]", entry)
                if name_match:
                    name = name_match.group(1)
                    code = name.upper().replace(' ', '_').replace('-', '_')
                    
                    # Insert code field after the opening brace
                    brace_pos = entry.find('{')
                    if brace_pos != -1:
                        fixed_entry = entry[:brace_pos+1] + f'\n            "code": "{code}",' + entry[brace_pos+1:]
                        fixed_entries.append(fixed_entry)
                    else:
                        fixed_entries.append(entry)
                else:
                    fixed_entries.append(entry)
            else:
                fixed_entries.append(entry)
    
    return '[\n        ' + ',\n        '.join(fixed_entries) + '\n    ]'

def batch_fix_seeders():
    """Fix all lookup seeder files that need code fields"""
    
    lookup_files = glob.glob('app/seed/lookups/*_seed.py')
    fixed_count = 0
    skipped_count = 0
    
    print("🔧 Batch fixing lookup seeder files...")
    
    for file_path in lookup_files:
        # Skip template file
        if '_template_seed.py' in file_path:
            continue
            
        print(f"\n📁 Processing: {file_path}")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Skip files that are already fixed
            if 'no_autoflush' in content and 'seeded_count' in content:
                print("   ✅ Already fixed - skipping")
                skipped_count += 1
                continue
            
            # Extract components
            model_class = extract_model_class(content)
            function_name = extract_function_name(content)
            data_list_content = extract_data_list(content)
            
            if not all([model_class, function_name, data_list_content]):
                print("   ❌ Could not extract required components - manual fix needed")
                continue
            
            # Generate names for template
            human_name = function_name.replace('seed_', '').replace('_', ' ').title()
            singular_name = human_name.rstrip('s')  # Remove trailing 's'
            
            # Add code fields to data list
            fixed_data_list = add_code_fields(data_list_content)
            
            if not fixed_data_list:
                print("   ❌ Could not process data list - manual fix needed")
                continue
            
            # Generate new content
            new_content = get_fixed_template().format(
                model_class=model_class,
                function_name=function_name,
                human_name=human_name,
                singular_name=singular_name,
                data_list=fixed_data_list
            )
            
            # Write fixed content
            with open(file_path, 'w') as f:
                f.write(new_content)
            
            print(f"   ✅ Fixed successfully")
            fixed_count += 1
            
        except Exception as e:
            print(f"   ❌ Error fixing file: {e}")
    
    print(f"\n🎉 Batch fix completed:")
    print(f"   ✅ Fixed: {fixed_count} files")
    print(f"   ⏭️  Skipped (already fixed): {skipped_count} files")
    print(f"   📁 Total processed: {len(lookup_files)} files")

if __name__ == '__main__':
    batch_fix_seeders()