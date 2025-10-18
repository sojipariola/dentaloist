#!/usr/bin/env python3

# Read the current analytics.py
with open('app/models/analytics.py', 'r') as f:
    content = f.read()

# Check if AuditTrail already exists
if 'class AuditTrail' in content:
    print("AuditTrail class already exists in analytics.py")
else:
    # Find a good place to insert AuditTrail (after other model classes)
    # Look for the first class definition to understand the structure
    import re
    
    # Add AuditTrail class before the AnalyticsEvent class or at the end of class definitions
    audit_trail_class = '''
class AuditTrail(db.Model):
    """Track user actions and changes in the system"""
    __tablename__ = 'audit_trails'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(100), nullable=False)
    resource_id = db.Column(db.Integer, nullable=True)
    old_values = db.Column(db.JSON, nullable=True)
    new_values = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('audit_trails', lazy=True))
    
    def __repr__(self):
        return f'<AuditTrail {self.action} {self.resource_type}>'
'''

    # Try to insert after other model classes, before AnalyticsEvent
    if 'class AnalyticsEvent' in content:
        # Insert before AnalyticsEvent
        pattern = r'(class AnalyticsEvent\(db\.Model\):)'
        replacement = audit_trail_class + r'\n\n\1'
        content = re.sub(pattern, replacement, content)
        print("Added AuditTrail class before AnalyticsEvent")
    else:
        # Add at the end of the file before the last line if it's an import or other
        lines = content.split('\n')
        # Find a good insertion point (after imports and before function definitions)
        insertion_point = 0
        for i, line in enumerate(lines):
            if line.startswith('class ') and 'db.Model' in line:
                insertion_point = i
                break
        
        if insertion_point > 0:
            lines.insert(insertion_point, audit_trail_class)
            content = '\n'.join(lines)
            print(f"Added AuditTrail at line {insertion_point}")
        else:
            # Just append at a reasonable position
            content = content + '\n\n' + audit_trail_class
            print("Appended AuditTrail class to the file")

    # Write the updated content back
    with open('app/models/analytics.py', 'w') as f:
        f.write(content)

print("Done!")
