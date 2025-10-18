# init_tenants.py
from app import create_app, db
from app.models.models import Organization, SubscriptionPlan

app = create_app()

with app.app_context():
    # Create default tenant
    default_org = Organization.query.get(1)
    if not default_org:
        default_org = Organization(
            id=1,
            name="Default Tenant",
            type="clinic",
            subscription_plan=SubscriptionPlan.ENTERPRISE,
            max_staff=None,
            max_patients=None,
            is_active=True
        )
        db.session.add(default_org)
        db.session.commit()
        print("Default tenant created successfully!")