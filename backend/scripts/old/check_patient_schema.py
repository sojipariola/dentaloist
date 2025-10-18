# scripts/check_patient_schema.py
import os
import sys

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import inspect

def check_patient_schema():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("=== PATIENTS TABLE SCHEMA ===")
        columns = inspector.get_columns('patients')
        for column in columns:
            nullable = "NULL" if column['nullable'] else "NOT NULL"
            default = f" DEFAULT {column['default']}" if column['default'] else ""
            print(f"  {column['name']:25} {str(column['type']):30} {nullable}{default}")
        
        print("\n=== PATIENT MODEL COLUMNS ===")
        from app.models import Patient
        patient_columns = [c.key for c in Patient.__table__.columns]
        for col in patient_columns:
            print(f"  {col}")

if __name__ == "__main__":
    check_patient_schema()