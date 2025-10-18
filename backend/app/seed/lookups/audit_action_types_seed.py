# app/seed/lookups/audit_action_types_seed.py

from app import db
from app.models import AuditActionType
import uuid


def seed_audit_action_types():
    """Seed audit action types with required code field"""
    
    action_types_data = [
        {
            'name': 'Create',
            'code': 'CREATE',
            'description': 'Create a new resource',
            'category': 'CREATE',
            'requires_approval': False,
            'log_level': 'info',
            'is_sensitive': False,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Read', 
            'code': 'READ',
            'description': 'View or access a resource',
            'category': 'READ',
            'requires_approval': False,
            'log_level': 'info',
            'is_sensitive': False,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Update',
            'code': 'UPDATE',
            'description': 'Modify an existing resource',
            'category': 'UPDATE',
            'requires_approval': False,
            'log_level': 'info',
            'is_sensitive': False,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Delete',
            'code': 'DELETE',
            'description': 'Remove a resource',
            'category': 'DELETE',
            'requires_approval': True,
            'log_level': 'warning',
            'is_sensitive': True,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Login',
            'code': 'LOGIN',
            'description': 'User login attempt',
            'category': 'SYSTEM',
            'requires_approval': False,
            'log_level': 'info',
            'is_sensitive': False,
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Logout',
            'code': 'LOGOUT',
            'description': 'User logout',
            'category': 'SYSTEM',
            'requires_approval': False,
            'log_level': 'info',
            'is_sensitive': False,
            'sort_order': 5,
            'is_active': True
        },
        {
            'name': 'Login Failed',
            'code': 'LOGIN_FAILED',
            'description': 'Failed login attempt',
            'category': 'SECURITY',
            'requires_approval': False,
            'log_level': 'warning',
            'is_sensitive': True,
            'sort_order': 6,
            'is_active': True
        },
        {
            'name': 'Permission Change',
            'code': 'PERMISSION_CHANGE',
            'description': 'User permissions modified',
            'category': 'SECURITY',
            'requires_approval': True,
            'log_level': 'warning',
            'is_sensitive': True,
            'sort_order': 7,
            'is_active': True
        },
        {
            'name': 'Export',
            'code': 'EXPORT',
            'description': 'Data export operation',
            'category': 'SYSTEM',
            'requires_approval': True,
            'log_level': 'info',
            'is_sensitive': True,
            'sort_order': 8,
            'is_active': True
        },
        {
            'name': 'Import',
            'code': 'IMPORT',
            'description': 'Data import operation',
            'category': 'SYSTEM',
            'requires_approval': True,
            'log_level': 'info',
            'is_sensitive': True,
            'sort_order': 9,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for action_type_data in action_types_data:
            # Check if action type already exists by code
            existing_action_type = AuditActionType.query.filter_by(code=action_type_data['code']).first()
            
            if existing_action_type:
                # Update existing action type
                print(f"🔄 Updating existing audit action type: {action_type_data['name']}")
                for key, value in action_type_data.items():
                    setattr(existing_action_type, key, value)
                updated_count += 1
            else:
                # Add new action type
                print(f"✅ Adding new audit action type: {action_type_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in action_type_data:
                    action_type_data['public_id'] = str(uuid.uuid4())
                
                action_type = AuditActionType(**action_type_data)
                db.session.add(action_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Audit Action Types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("🔍 Audit Action Types added:")
            for action_type_data in action_types_data:
                action_type = AuditActionType.query.filter_by(code=action_type_data['code']).first()
                if action_type:
                    sensitivity = "Sensitive" if action_type.is_sensitive else "Normal"
                    print(f"   • {action_type.name} ({action_type.code}) - {sensitivity}")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding audit action types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_audit_action_types()