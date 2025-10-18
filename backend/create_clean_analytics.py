import re

# Read the current file
with open('app/models/analytics.py', 'r') as f:
    content = f.read()

# Remove all __table_args__ that contain indexes
content = re.sub(r"__table_args__ = \([^)]*db\.Index[^)]*\)", "__table_args__ = ()", content)
content = re.sub(r"__table_args__ = \(.*?\)", "__table_args__ = ()", content, flags=re.DOTALL)

# Write back
with open('app/models/analytics.py', 'w') as f:
    f.write(content)

print("Removed all indexes from analytics models")
