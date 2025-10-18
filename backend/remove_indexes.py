import re

# Read the analytics.py file
with open('app/models/analytics.py', 'r') as f:
    content = f.read()

# Remove all db.Index calls from __table_args__
content = re.sub(r"db\.Index\([^)]+\),?\s*", "", content)

# Also remove empty tuples
content = re.sub(r"__table_args__ = \(\s*\)", "__table_args__ = ()", content)

# Write the fixed content back
with open('app/models/analytics.py', 'w') as f:
    f.write(content)

print("Removed all indexes from analytics models for testing")
