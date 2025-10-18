from app import db
from app.models.lookups import OrganizationType
import uuid


def seed_organization_types():
    """Seed organization types with required code field"""
    
    organization_types_data = [
        {
            'name': 'Solo Practice',
            'code': 'SOLO_PRACTICE',  # ← ADD THIS REQUIRED FIELD
            'description': 'Single dentist practice',
            'max_users': 5,
            'max_patients': 2000,
            'features_available': {
                'basic_scheduling': True,
                'patient_records': True,
                'billing': True,
                'reporting': True
            },
            'requires_verification': False,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Group Practice',
            'code': 'GROUP_PRACTICE',  # ← ADD THIS REQUIRED FIELD
            'description': 'Multiple dentists sharing facilities',
            'max_users': 20,
            'max_patients': 10000,
            'features_available': {
                'basic_scheduling': True,
                'patient_records': True,
                'billing': True,
                'reporting': True,
                'multi_location': True
            },
            'requires_verification': False,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Dental Clinic',
            'code': 'DENTAL_CLINIC',  # ← ADD THIS REQUIRED FIELD
            'description': 'Larger clinic with multiple providers',
            'max_users': 50,
            'max_patients': 25000,
            'features_available': {
                'basic_scheduling': True,
                'patient_records': True,
                'billing': True,
                'reporting': True,
                'multi_location': True,
                'advanced_analytics': True
            },
            'requires_verification': True,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Dental Hospital',
            'code': 'DENTAL_HOSPITAL',  # ← ADD THIS REQUIRED FIELD
            'description': 'Hospital-based dental department',
            'max_users': 100,
            'max_patients': 50000,
            'features_available': {
                'basic_scheduling': True,
                'patient_records': True,
                'billing': True,
                'reporting': True,
                'multi_location': True,
                'advanced_analytics': True,
                'integration_api': True
            },
            'requires_verification': True,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Dental School',
            'code': 'DENTAL_SCHOOL',  # ← ADD THIS REQUIRED FIELD
            'description': 'Educational institution with dental program',
            'max_users': 200,
            'max_patients': 100000,
            'features_available': {
                'basic_scheduling': True,
                'patient_records': True,
                'billing': True,
                'reporting': True,
                'multi_location': True,
                'advanced_analytics': True,
                'integration_api': True,
                'educational_tools': True
            },
            'requires_verification': True,
            'sort_order': 4,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for org_type_data in organization_types_data:
            # Check if organization type already exists by code
            existing_org_type = OrganizationType.query.filter_by(code=org_type_data['code']).first()
            
            if existing_org_type:
                # Update existing organization type
                print(f"🔄 Updating existing organization type: {org_type_data['name']}")
                for key, value in org_type_data.items():
                    setattr(existing_org_type, key, value)
                updated_count += 1
            else:
                # Add new organization type
                print(f"✅ Adding new organization type: {org_type_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in org_type_data:
                    org_type_data['public_id'] = str(uuid.uuid4())
                
                org_type = OrganizationType(**org_type_data)
                db.session.add(org_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Organization types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("🏢 Organization types added:")
            for org_type_data in organization_types_data:
                org_type = OrganizationType.query.filter_by(code=org_type_data['code']).first()
                if org_type:
                    users_info = f"{org_type.max_users} users, {org_type.max_patients} patients"
                    verification = "🔒 Verified" if org_type.requires_verification else "✅ Open"
                    print(f"   • {org_type.name} - {users_info} - {verification}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding organization types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_organization_types()