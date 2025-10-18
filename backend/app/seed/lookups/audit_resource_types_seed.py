# app/seed/lookups/audit_resource_types_seed.py

from app import db
from app.models import AuditResourceType
import uuid


def seed_audit_resource_types():
    """Seed audit resource types with required code field"""
    
    resource_types_data = [
        {
            'name': 'User',
            'code': 'USER',
            'description': 'System users and user accounts',
            'module': 'user',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 0,
            'is_active': True
        },
        {
            'name': 'Patient', 
            'code': 'PATIENT',
            'description': 'Patient records and demographic information',
            'module': 'patient',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 1,
            'is_active': True
        },
        {
            'name': 'Appointment',
            'code': 'APPOINTMENT',
            'description': 'Appointment scheduling and management',
            'module': 'appointment',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 2,
            'is_active': True
        },
        {
            'name': 'Organization',
            'code': 'ORGANIZATION',
            'description': 'Organization settings and configuration',
            'module': 'organization',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 3,
            'is_active': True
        },
        {
            'name': 'Financial Transaction',
            'code': 'FINANCIAL_TRANSACTION',
            'description': 'Financial transactions and payments',
            'module': 'financial',
            'requires_audit': True,
            'retention_days': 730,  # Longer retention for financial records
            'sort_order': 4,
            'is_active': True
        },
        {
            'name': 'Invoice',
            'code': 'INVOICE',
            'description': 'Billing invoices and statements',
            'module': 'financial',
            'requires_audit': True,
            'retention_days': 730,
            'sort_order': 5,
            'is_active': True
        },
        {
            'name': 'Medical Record',
            'code': 'MEDICAL_RECORD',
            'description': 'Patient medical records and treatment history',
            'module': 'clinical',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 6,
            'is_active': True
        },
        {
            'name': 'Treatment',
            'code': 'TREATMENT',
            'description': 'Dental treatments and procedures',
            'module': 'clinical',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 7,
            'is_active': True
        },
        {
            'name': 'Prescription',
            'code': 'PRESCRIPTION',
            'description': 'Medication prescriptions and orders',
            'module': 'clinical',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 8,
            'is_active': True
        },
        {
            'name': 'Inventory Item',
            'code': 'INVENTORY_ITEM',
            'description': 'Medical supplies and inventory items',
            'module': 'inventory',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 9,
            'is_active': True
        },
        {
            'name': 'Product',
            'code': 'PRODUCT',
            'description': 'Products and services offered',
            'module': 'inventory',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 10,
            'is_active': True
        },
        {
            'name': 'Setting',
            'code': 'SETTING',
            'description': 'System configuration and settings',
            'module': 'system',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 11,
            'is_active': True
        },
        {
            'name': 'Widget',
            'code': 'WIDGET',
            'description': 'Dashboard widgets and analytics components',
            'module': 'analytics',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 12,
            'is_active': True
        },
        {
            'name': 'Dashboard',
            'code': 'DASHBOARD',
            'description': 'Analytics dashboards and layouts',
            'module': 'analytics',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 13,
            'is_active': True
        },
        {
            'name': 'Report',
            'code': 'REPORT',
            'description': 'System reports and analytics',
            'module': 'analytics',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 14,
            'is_active': True
        },
        {
            'name': 'Role',
            'code': 'ROLE',
            'description': 'User roles and permissions',
            'module': 'security',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 15,
            'is_active': True
        },
        {
            'name': 'Permission',
            'code': 'PERMISSION',
            'description': 'System permissions and access rights',
            'module': 'security',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 16,
            'is_active': True
        },
        {
            'name': 'Audit Trail',
            'code': 'AUDIT_TRAIL',
            'description': 'Audit trail entries themselves',
            'module': 'security',
            'requires_audit': False,  # Don't audit the audit trail to avoid recursion
            'retention_days': 365,
            'sort_order': 17,
            'is_active': True
        },
        {
            'name': 'Integration',
            'code': 'INTEGRATION',
            'description': 'External integrations and API connections',
            'module': 'system',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 18,
            'is_active': True
        },
        {
            'name': 'Webhook',
            'code': 'WEBHOOK',
            'description': 'Webhook configurations and events',
            'module': 'system',
            'requires_audit': True,
            'retention_days': 180,
            'sort_order': 19,
            'is_active': True
        },
        {
            'name': 'Notification',
            'code': 'NOTIFICATION',
            'description': 'System notifications and alerts',
            'module': 'system',
            'requires_audit': False,  # Typically don't audit notifications
            'retention_days': 90,
            'sort_order': 20,
            'is_active': True
        },
        {
            'name': 'Tenant',
            'code': 'TENANT',
            'description': 'Multi-tenant organization instances',
            'module': 'system',
            'requires_audit': True,
            'retention_days': 365,
            'sort_order': 21,
            'is_active': True
        },
        {
            'name': 'Subscription',
            'code': 'SUBSCRIPTION',
            'description': 'Billing subscriptions and plans',
            'module': 'financial',
            'requires_audit': True,
            'retention_days': 730,
            'sort_order': 22,
            'is_active': True
        }
    ]

    seeded_count = 0
    updated_count = 0

    # Use no_autoflush to prevent premature flushing
    with db.session.no_autoflush:
        for resource_type_data in resource_types_data:
            # Check if resource type already exists by code
            existing_resource_type = AuditResourceType.query.filter_by(code=resource_type_data['code']).first()
            
            if existing_resource_type:
                # Update existing resource type
                print(f"🔄 Updating existing audit resource type: {resource_type_data['name']}")
                for key, value in resource_type_data.items():
                    setattr(existing_resource_type, key, value)
                updated_count += 1
            else:
                # Add new resource type
                print(f"✅ Adding new audit resource type: {resource_type_data['name']}")
                
                # Generate public_id if not provided
                if 'public_id' not in resource_type_data:
                    resource_type_data['public_id'] = str(uuid.uuid4())
                
                resource_type = AuditResourceType(**resource_type_data)
                db.session.add(resource_type)
                seeded_count += 1

    try:
        db.session.commit()
        print(f"✅ Audit Resource Types seeded: {seeded_count} added, {updated_count} updated")
        
        # Print summary
        if seeded_count > 0:
            print("📝 Audit Resource Types added:")
            for resource_type_data in resource_types_data:
                resource_type = AuditResourceType.query.filter_by(code=resource_type_data['code']).first()
                if resource_type:
                    audit_status = "Audited" if resource_type.requires_audit else "Not Audited"
                    print(f"   • {resource_type.name} ({resource_type.module}) - {audit_status} - {resource_type.retention_days} days retention")
                    
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding audit resource types: {e}")
        raise

    return seeded_count


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_audit_resource_types()