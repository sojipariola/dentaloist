# scripts/check_staff_schema.py
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

def check_staff_schema():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("=== STAFF TABLE SCHEMA ===")
        columns = inspector.get_columns('staff')
        for column in columns:
            nullable = "NULL" if column['nullable'] else "NOT NULL"
            default = f" DEFAULT {column['default']}" if column['default'] else ""
            print(f"  {column['name']:25} {str(column['type']):30} {nullable}{default}")

if __name__ == "__main__":
    check_staff_schema()