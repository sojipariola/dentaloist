# scripts/seed_database.py

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

import click
import random
from datetime import datetime, timedelta
from faker import Faker

from app import create_app
from app.models import db
from app.models.core import (User, Organization, Tenant, FamilyMember, 
        SecurityEvent, UserSession, LoginAttempt)
from app.models.lookups import Gender, UserRole, SubscriptionPlan, OrganizationType
from app.models.role_permission import Role
from app.models.clinical import Appointment, Patient, TreatmentPlan, Prescription
from app.models.financial import Invoice, Payment
from app.models.inventory import InventoryItem, InventoryTransaction
from app.models.analytics import AnalyticsEvent, Notification
import uuid
from sqlalchemy.inspection import inspect
from werkzeug.security import generate_password_hash

fake = Faker()
app = create_app()


@click.command("seed-database")
@click.option("--drop", is_flag=True, help="Drop and recreate all tables before seeding.")
def seed_database(drop):
    """Seed the entire Dentaloist database with realistic fake data for multi-tenants."""
    with app.app_context():
        if drop:
            click.echo("⚠️ Dropping existing tables...")
            db.drop_all()
        click.echo("📦 Creating tables...")
        db.create_all()
        
        click.echo("🌱 Seeding lookup data...")
        seed_lookups()
        
        click.echo("🏢 Creating organizations, tenants, and subscription plans...")
        orgs = seed_organizations_and_tenants()
        
        click.echo("👥 Creating users for each tenant...")
        seed_users(orgs)
        
        click.echo("🦷 Seeding clinical data...")
        seed_clinical_data(orgs)
        
        click.echo("💳 Seeding financial data...")
        seed_financial_data(orgs)
        
        click.echo("🏭 Seeding inventory data...")
        seed_inventory_data(orgs)
        
        click.echo("👪 Seeding family data...")
        seed_family_data(orgs)
        
        click.echo("🛡️  Seeding security and analytics data...")
        seed_security_and_analytics_data(orgs)
        
        click.echo("🔔 Seeding notifications...")
        seed_notifications(orgs)
        
        db.session.commit()
        
        click.echo("✅ Database seeding completed successfully!")
        print_dashboard_summary()


# ------------------ SEEDING HELPERS ------------------

def safe_create(model, **fields):
    """Create model instance safely by including only valid columns."""
    model_columns = {c.key for c in inspect(model).mapper.column_attrs}
    valid_data = {k: v for k, v in fields.items() if k in model_columns}
    return model(**valid_data)

def seed_lookups():
    now = datetime.utcnow()
    org_type_data = [
        ("DENTAL", "Dental Clinic"),
        ("HOSP", "Hospital"),
        ("LAB", "Laboratory"),
        ("SPEC", "Specialty Practice")
    ]
    org_types = []
    for code, name in org_type_data:
        org_type = OrganizationType(
            code=code,
            name=name,
            description=f"{name} type organization",
            max_users=10,
            max_patients=1000,
            features_available={},
            requires_verification=False,
            sort_order=0,
            color=None,
            public_id=str(uuid.uuid4()),
            created_at=now,
            updated_at=now,
            is_active=True
        )
        db.session.add(org_type)
        org_types.append(org_type)
    db.session.commit()
    print(f"🏷️ Seeded {len(org_types)} organization types")

    # ✅ 3. Create Organizations with valid organization_type_id
    organizations = []
    for i in range(4):
        org_type = fake.random_element(elements=org_types)
        org = safe_create(
            Organization,
            name=f"{fake.company()} Dental Clinic",
            address=fake.address(),
            city=fake.city(),
            state=fake.state_abbr(),
            postal_code=fake.postcode(),
            country="USA",
            phone=fake.phone_number(),
            email=fake.company_email(),
            organization_type_id=org_type.id,  # 👈 FIXED: now not NULL
            status="active",
            is_verified=False,
            is_active=True,
            public_id=str(uuid.uuid4()),
            created_at=now,
            updated_at=now
        )
        organizations.append(org)
        db.session.add(org)
    db.session.commit()
    print(f"🏢 Created {len(organizations)} organizations linked to org types")

    # ✅ 4. Seed Genders
    genders = [
        safe_create(
            Gender,
            code=g[:1].upper(),
            name=g,
            is_active=True,
            created_at=now,
            updated_at=now,
            public_id=str(uuid.uuid4())
        )
        for g in ["Male", "Female", "Other"]
    ]
    db.session.add_all(genders)

    # ✅ 5. Seed Roles per Organization
    roles = []
    for org in organizations:
        for r in ["Admin", "Dentist", "Nurse", "Receptionist", "Accountant"]:
            role = safe_create(
                Role,
                name=r,
                is_system_role=False,
                organization_id=org.id,
                is_active=True,
                public_id=str(uuid.uuid4()),
                created_at=now,
                updated_at=now
            )
            db.session.add(role)
            roles.append(role)
    print(f"👥 Seeded {len(roles)} roles across organizations")

    # ✅ 6. Seed User Roles
    user_roles = [
        safe_create(
            UserRole,
            name=ur,
            is_active=True,
            created_at=now,
            updated_at=now,
            public_id=str(uuid.uuid4())
        )
        for ur in ["System Admin", "Clinic Manager", "Practitioner", "Support Staff"]
    ]
    db.session.add_all(user_roles)

    db.session.commit()
    print("🌱 Lookup + organization roles seeded successfully!")




def seed_organizations_and_tenants():
    """Seed 4 organizations and assign each a tenant + subscription plan."""
    orgs = []
    plans = [
        ("Dentaloist Basic", 49.99),
        ("Dentaloist Pro", 99.99),
        ("Dentaloist Enterprise", 249.99),
        ("Dentaloist Ultimate", 499.99)
    ]
    
    for i in range(4):
        plan_name, price = plans[i]
        plan = SubscriptionPlan(
            name=plan_name,
            price=price,
            duration_days=30,
            features={
                "appointments": True,
                "billing": True,
                "inventory": True,
                "analytics": i >= 1,
                "multi_tenant": i >= 2,
            }
        )
        db.session.add(plan)
        db.session.flush()
        
        org = Organization(
            name=f"{fake.company()} Dental Clinic",
            public_id=f"ORG-{fake.uuid4()[:8]}",
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.company_email(),
            subscription_plan_id=plan.id,
        )
        db.session.add(org)
        db.session.flush()
        
        tenant = Tenant(
            name=f"{org.name} Tenant",
            organization_id=org.id
        )
        db.session.add(tenant)
        db.session.flush()
        
        org.tenant_id = tenant.id
        orgs.append(org)
    
    db.session.commit()
    return orgs


def seed_users(orgs):
    """Create users for each organization/tenant with hashed passwords."""
    admin_role = UserRole.query.filter_by(name="System Admin").first()
    default_password = "Password123!" 

    for org in orgs:
        tenant_id = org.tenant_id
        for _ in range(5):
            user = User(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number(),
                organization_id=org.id,
                tenant_id=tenant_id,
                user_role_id=admin_role.id,
                password_hash=generate_password_hash(default_password),
                is_admin=random.choice([True, False])
            )
            db.session.add(user)
    db.session.commit()
    click.echo(f"🔑 All seeded users have default password: {default_password}")



def seed_clinical_data(orgs):
    """Seed patients and appointments for each tenant."""
    for org in orgs:
        patients = []
        for _ in range(10):
            p = Patient(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                date_of_birth=fake.date_of_birth(),
                gender_id=random.randint(1, 3),
                tenant_id=org.tenant_id
            )
            db.session.add(p)
            patients.append(p)
        db.session.flush()
        
        for _ in range(15):
            appt = Appointment(
                patient_id=random.choice(patients).id,
                scheduled_date=fake.date_time_between(start_date="-30d", end_date="+10d"),
                status=random.choice(["completed", "scheduled", "cancelled"]),
                tenant_id=org.tenant_id
            )
            db.session.add(appt)
    db.session.commit()


def seed_financial_data(orgs):
    for org in orgs:
        for _ in range(5):
            invoice = Invoice(
                amount=random.uniform(100, 2000),
                due_date=fake.date_between(start_date="today", end_date="+30d"),
                status=random.choice(["paid", "pending", "overdue"]),
                tenant_id=org.tenant_id
            )
            db.session.add(invoice)
        for _ in range(5):
            payment = Payment(
                amount=random.uniform(100, 2000),
                method=random.choice(["card", "cash", "bank_transfer"]),
                date=fake.date_time_this_year(),
                tenant_id=org.tenant_id
            )
            db.session.add(payment)
    db.session.commit()


def seed_inventory_data(orgs):
    for org in orgs:
        for _ in range(10):
            item = InventoryItem(
                name=fake.word(),
                quantity=random.randint(10, 200),
                unit_price=random.uniform(5, 500),
                tenant_id=org.tenant_id
            )
            db.session.add(item)
        db.session.flush()
        
        for _ in range(15):
            trans = InventoryTransaction(
                item_id=random.randint(1, 10),
                quantity=random.randint(1, 10),
                transaction_type=random.choice(["add", "use"]),
                timestamp=fake.date_time_this_year(),
                tenant_id=org.tenant_id
            )
            db.session.add(trans)
    db.session.commit()


def seed_family_data(orgs):
    for org in orgs:
        for _ in range(5):
            fm = FamilyMember(
                user_id=random.randint(1, 5),
                relationship=random.choice(["Spouse", "Child", "Parent"]),
                name=fake.name(),
                tenant_id=org.tenant_id
            )
            db.session.add(fm)
    db.session.commit()


def seed_security_and_analytics_data(orgs):
    for org in orgs:
        for _ in range(10):
            ev = SecurityEvent(
                user_id=random.randint(1, 5),
                description=fake.sentence(),
                ip_address=fake.ipv4(),
                tenant_id=org.tenant_id
            )
            db.session.add(ev)
        for _ in range(25):
            ae = AnalyticsEvent(
                user_id=random.randint(1, 5),
                action=fake.word(),
                timestamp=fake.date_time_this_year(),
                tenant_id=org.tenant_id
            )
            db.session.add(ae)
    db.session.commit()


def seed_notifications(orgs):
    for org in orgs:
        for _ in range(10):
            notif = Notification(
                user_id=random.randint(1, 5),
                message=fake.sentence(),
                read=random.choice([True, False]),
                tenant_id=org.tenant_id
            )
            db.session.add(notif)
    db.session.commit()


def print_dashboard_summary():
    """Print summary counts per domain."""
    click.echo("\n📊 DATABASE DASHBOARD SUMMARY:")
    click.echo(f"   - Organizations: {Organization.query.count()}")
    click.echo(f"   - Tenants: {Tenant.query.count()}")
    click.echo(f"   - Users: {User.query.count()}")
    click.echo(f"   - Patients: {Patient.query.count()}")
    click.echo(f"   - Appointments: {Appointment.query.count()}")
    click.echo(f"   - Invoices: {Invoice.query.count()}")
    click.echo(f"   - Payments: {Payment.query.count()}")
    click.echo(f"   - Inventory Items: {InventoryItem.query.count()}")
    click.echo(f"   - Inventory Transactions: {InventoryTransaction.query.count()}")
    click.echo(f"   - Family Members: {FamilyMember.query.count()}")
    click.echo(f"   - Security Events: {SecurityEvent.query.count()}")
    click.echo(f"   - Analytics Events: {AnalyticsEvent.query.count()}")
    click.echo(f"   - Notifications: {Notification.query.count()}")
    click.echo("✅ All domains seeded successfully!\n")


if __name__ == "__main__":
    seed_database()

'''
rm instance/dentaloist.db
python3 setup_database.py
python3 scripts/seed_database.py

'''