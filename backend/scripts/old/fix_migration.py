#!/usr/bin/env python3
import re

# Read the migration file
with open('migrations/versions/e19e89194fdf_initial_migration.py', 'r') as f:
    content = f.read()

# Replace PostgreSQL JSON types with SQLAlchemy JSON
content = re.sub(r'postgresql\.JSON\(astext_type=Text\(\)\)', 'sa.JSON()', content)
content = re.sub(r'postgresql\.JSONB\(astext_type=Text\(\)\)', 'sa.JSON()', content)

# Write the fixed content back
with open('migrations/versions/e19e89194fdf_initial_migration.py', 'w') as f:
    f.write(content)

print("✅ Migration file fixed!")
