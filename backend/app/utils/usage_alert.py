# app/utils/usage_alert.py
from flask_mail import Message
from app import mail, db
from app.models.tenant import TenantUsage
from datetime import datetime, timedelta

ADMIN_EMAIL = "admin@dentaloist.com"
USAGE_THRESHOLD = 60  # percent
ADMIN_DASHBOARD_URL = "https://admin.dentaloist.com/tenants"

def check_and_alert_usage():
    tenants = TenantUsage.query.join(TenantUsage.subscription_plan).all()
    
    for tenant in tenants:
        usage = tenant.usage_percentage()
        exceeded = {k: v for k, v in usage.items() if v >= USAGE_THRESHOLD}

        if exceeded:
            if not tenant.last_notified or tenant.last_notified < datetime.utcnow() - timedelta(days=1):
                send_usage_alert_email(tenant, exceeded)
                tenant.last_notified = datetime.utcnow()
                db.session.commit()

def send_usage_alert_email(tenant, exceeded_features):
    plan = tenant.subscription_plan
    next_plan = plan.next_plan()
    
    upgrade_link = f"{ADMIN_DASHBOARD_URL}/{tenant.tenant_id}/upgrade"
    plan_info = f"""
    Tenant ID: {tenant.tenant_id}
    Current Plan: {plan.name}
    Monthly Price: ${plan.price_monthly:.2f}
    Yearly Price: ${plan.price_yearly:.2f}
    """

    exceeded_list = "\n".join([f"- {k}: {v:.1f}%" for k, v in exceeded_features.items()])

    if next_plan:
        next_plan_info = f"""
        Recommended Upgrade: {next_plan.name}
        New Monthly Price: ${next_plan.price_monthly:.2f}
        """
    else:
        next_plan_info = "⚠️ This tenant is already on the highest plan."

    subject = f"[Dentaloist SaaS] Tenant {tenant.tenant_id} Usage Alert (>{USAGE_THRESHOLD}%)"
    body = f"""
🚨 Tenant Usage Alert 🚨

{plan_info}

The following features exceeded {USAGE_THRESHOLD}% of their limits:
{exceeded_list}

{next_plan_info}

👉 Manage or upgrade this tenant’s plan here:
{upgrade_link}

Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""

    msg = Message(
        subject=subject,
        recipients=[ADMIN_EMAIL],
        body=body,
    )
    mail.send(msg)
