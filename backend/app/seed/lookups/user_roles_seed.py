from app import db
from app.models import UserRole
import uuid


def seed_user_roles():
    """Seed user roles with required code field"""
    
    user_roles_data = [
        {
            'name': 'Super Administrator',
            'code': 'SUPER_ADMIN',  # ← ADD THIS REQUIRED FIELD
            'description': 'Full system access with all permissions',
            'is_system_role': True,
            'access_level': 'admin',
            'can_manage_users': True,
            'can_access_reports': True,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Practice Administrator',
            'code': 'PRACTICE_ADMIN',  # ← ADD THIS REQUIRED FIELD
            'description': 'Administrative access for practice management',
            'is_system_role': False,
            'access_level': 'admin',
            'can_manage_users': True,
            'can_access_reports': True,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Dentist',
            'code': 'DENTIST',  # ← ADD THIS REQUIRED FIELD
            'description': 'Clinical provider with full patient care access',
            'is_system_role': False,
            'access_level': 'provider',
            'can_manage_users': False,
            'can_access_reports': True,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Dental Assistant',
            'code': 'ASSISTANT',  # ← ADD THIS REQUIRED FIELD
            'description': 'Clinical support staff with limited access',
            'is_system_role': False,
            'access_level': 'assistant',
            'can_manage_users': False,
            'can_access_reports': False,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Receptionist',
            'code': 'RECEPTIONIST',  # ← ADD THIS REQUIRED FIELD
            'description': 'Front desk staff with scheduling and basic patient access',
            'is_system_role': False,
            'access_level': 'staff',
            'can_manage_users': False,
            'can_access_reports': False,
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Billing Specialist',
            'code': 'BILLING_SPECIALIST',  # ← ADD THIS REQUIRED FIELD
            'description': 'Financial staff with billing and payment access',
            'is_system_role': False,
            'access_level': 'staff',
            'can_manage_users': False,
            'can_access_reports': True,
            'sort_order': 5,
            'is_active': True
        },
        {
            'name': 'Patient',
            'code': 'PATIENT',  # ← ADD THIS REQUIRED FIELD
            'description': 'Patient access to personal records and appointments',
            'is_system_role': False,
            'access_level': 'patient',
            'can_manage_users': False,
            'can_access_reports': False,
            'sort_order': 6,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for role_data in user_roles_data:
            # Check if user role already exists by code
            existing_role = UserRole.query.filter_by(code=role_data['code']).first()
            
            if existing_role:
                # Update existing role
                print(f"🔄 Updating existing role: {role_data['name']}")
                for key, value in role_data.items():
                    setattr(existing_role, key, value)
                updated_count += 1
            else:
                # Add new role
                print(f"✅ Adding new role: {role_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in role_data:
                    role_data['public_id'] = str(uuid.uuid4())
                
                user_role = UserRole(**role_data)
                db.session.add(user_role)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ User roles seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("👥 User roles added:")
            for role_data in user_roles_data:
                role = UserRole.query.filter_by(code=role_data['code']).first()
                if role:
                    access_emoji = {
                        'admin': '👑',
                        'provider': '🦷', 
                        'assistant': '👩‍⚕️',
                        'staff': '💼',
                        'patient': '👤'
                    }.get(role.access_level, '❓')
                    print(f"   • {role.name} ({role.code}) {access_emoji} - {role.description}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding user roles: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_user_roles()