# backend/scripts/fix_all_lookups.py
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.models.lookups import (
    Gender, OrganizationType, TenantStatus, IndustryType,
    AppointmentType, AppointmentStatus, TreatmentType, TreatmentStatus, TreatmentPriority,
    ProductType, PaymentMethod, PaymentStatus, InvoiceStatus
)

def check_all_lookup_requirements():
    """Check all lookup tables for required code fields"""
    app = create_app()
    
    with app.app_context():
        lookup_models = [
            (Gender, 'Gender'),
            (OrganizationType, 'OrganizationType'),
            (TenantStatus, 'TenantStatus'),
            (IndustryType, 'IndustryType'),
            (AppointmentType, 'AppointmentType'),
            (AppointmentStatus, 'AppointmentStatus'),
            (TreatmentType, 'TreatmentType'),
            (TreatmentStatus, 'TreatmentStatus'),
            (TreatmentPriority, 'TreatmentPriority'),
            (ProductType, 'ProductType'),
            (PaymentMethod, 'PaymentMethod'),
            (PaymentStatus, 'PaymentStatus'),
            (InvoiceStatus, 'InvoiceStatus')
        ]
        
        print("🔍 Checking ALL lookup table requirements...\n")
        
        for model, name in lookup_models:
            try:
                columns = model.__table__.columns
                required_fields = []
                
                for column in columns:
                    if not column.nullable and column.name != 'id':
                        required_fields.append(column.name)
                
                status = "✅" if 'code' in required_fields else "❌ MISSING CODE"
                print(f"{status} {name}: Required fields: {required_fields}")
                
            except Exception as e:
                print(f"❌ {name}: Error checking - {e}")

if __name__ == '__main__':
    check_all_lookup_requirements()