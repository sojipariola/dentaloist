from app import db
from app.models.lookups import ProductType
import uuid


def seed_product_types():
    """Seed product types with correct field structure"""
    
    product_types_data = [
        {
            'name': 'Medical Supply',
            'code': 'MEDICAL_SUPPLY',
            'description': 'Medical supplies and equipment for clinical use',
            'is_medical': True,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Pharmaceutical',
            'code': 'PHARMACEUTICAL',
            'description': 'Pharmaceutical products and medications',
            'is_medical': True,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Dental Material',
            'code': 'DENTAL_MATERIAL',
            'description': 'Dental materials, consumables, and restorative materials',
            'is_medical': True,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Equipment',
            'code': 'EQUIPMENT',
            'description': 'Medical and dental equipment, instruments, and devices',
            'is_medical': True,
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Laboratory Supply',
            'code': 'LAB_SUPPLY',
            'description': 'Dental laboratory supplies and materials',
            'is_medical': True,
            'sort_order': 5,
            'is_active': True
        },
        {
            'name': 'Personal Protective Equipment',
            'code': 'PPE',
            'description': 'Personal protective equipment for clinical staff',
            'is_medical': True,
            'sort_order': 6,
            'is_active': True
        },
        {
            'name': 'Diagnostic Supply',
            'code': 'DIAGNOSTIC_SUPPLY',
            'description': 'Diagnostic materials and testing supplies',
            'is_medical': True,
            'sort_order': 7,
            'is_active': True
        },
        {
            'name': 'Orthodontic Supply',
            'code': 'ORTHODONTIC_SUPPLY',
            'description': 'Orthodontic materials and appliances',
            'is_medical': True,
            'sort_order': 8,
            'is_active': True
        },
        {
            'name': 'Endodontic Supply',
            'code': 'ENDODONTIC_SUPPLY',
            'description': 'Endodontic materials and root canal supplies',
            'is_medical': True,
            'sort_order': 9,
            'is_active': True
        },
        {
            'name': 'Periodontic Supply',
            'code': 'PERIODONTIC_SUPPLY',
            'description': 'Periodontic materials and gum treatment supplies',
            'is_medical': True,
            'sort_order': 10,
            'is_active': True
        },
        {
            'name': 'Prosthodontic Supply',
            'code': 'PROSTHODONTIC_SUPPLY',
            'description': 'Prosthodontic materials for crowns, bridges, and dentures',
            'is_medical': True,
            'sort_order': 11,
            'is_active': True
        },
        {
            'name': 'Oral Surgery Supply',
            'code': 'ORAL_SURGERY_SUPPLY',
            'description': 'Oral surgery materials and surgical supplies',
            'is_medical': True,
            'sort_order': 12,
            'is_active': True
        },
        {
            'name': 'Radiology Supply',
            'code': 'RADIOLOGY_SUPPLY',
            'description': 'Radiology and imaging supplies',
            'is_medical': True,
            'sort_order': 13,
            'is_active': True
        },
        {
            'name': 'Anesthesia Supply',
            'code': 'ANESTHESIA_SUPPLY',
            'description': 'Anesthesia and sedation supplies',
            'is_medical': True,
            'sort_order': 14,
            'is_active': True
        },
        {
            'name': 'Office Supply',
            'code': 'OFFICE_SUPPLY',
            'description': 'Office supplies, stationery, and administrative materials',
            'is_medical': False,
            'sort_order': 15,
            'is_active': True
        },
        {
            'name': 'Cleaning Supply',
            'code': 'CLEANING_SUPPLY',
            'description': 'Cleaning and sterilization supplies',
            'is_medical': False,
            'sort_order': 16,
            'is_active': True
        },
        {
            'name': 'Furniture',
            'code': 'FURNITURE',
            'description': 'Office and clinical furniture',
            'is_medical': False,
            'sort_order': 17,
            'is_active': True
        },
        {
            'name': 'Software',
            'code': 'SOFTWARE',
            'description': 'Software licenses and digital products',
            'is_medical': False,
            'sort_order': 18,
            'is_active': True
        },
        {
            'name': 'Educational Material',
            'code': 'EDUCATIONAL_MATERIAL',
            'description': 'Patient education materials and models',
            'is_medical': False,
            'sort_order': 19,
            'is_active': True
        },
        {
            'name': 'Consumable',
            'code': 'CONSUMABLE',
            'description': 'General consumable products and supplies',
            'is_medical': False,
            'sort_order': 20,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for data in product_types_data:
            # Check if product type already exists by code
            existing = ProductType.query.filter_by(code=data['code']).first()
            
            if existing:
                # Update existing product type
                print(f"🔄 Updating existing product type: {data['name']}")
                # Only update fields that actually exist in the model
                valid_fields = {}
                for key, value in data.items():
                    if hasattr(ProductType, key):
                        valid_fields[key] = value
                for key, value in valid_fields.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Add new product type - only include fields that exist in the model
                print(f"✅ Adding new product type: {data['name']}")
                
                # Filter out invalid fields
                valid_data = {}
                for key, value in data.items():
                    if hasattr(ProductType, key):
                        valid_data[key] = value
                
                # Generate public_id if not provided
                if 'public_id' not in valid_data:
                    valid_data['public_id'] = str(uuid.uuid4())
                
                product_type = ProductType(**valid_data)
                db.session.add(product_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Product types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📦 Product types added:")
            for data in product_types_data:
                product_type = ProductType.query.filter_by(code=data['code']).first()
                if product_type:
                    medical_status = "🏥 Medical" if getattr(product_type, 'is_medical', False) else "📄 Non-medical"
                    print(f"   • {product_type.name} - {medical_status}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding product types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_product_types()