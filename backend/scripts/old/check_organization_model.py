# check_organization_model.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models import Organization

def check_organization_model():
    app = create_app()
    
    with app.app_context():
        print("Organization model columns:")
        for column in Organization.__table__.columns:
            nullable = "NULL" if column.nullable else "NOT NULL"
            default = f" DEFAULT {column.default.arg}" if column.default else ""
            print(f"  - {column.name}: {column.type} ({nullable}){default}")

if __name__ == '__main__':
    check_organization_model()
