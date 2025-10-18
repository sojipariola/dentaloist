# backend/app/seed/financial_seeds.py
from app import db
from app.models import Invoice, InvoiceStatus, Payment, PaymentStatus, PaymentMethod, Patient
from datetime import datetime, timedelta
import random

def seed_financial_data():
    """Seed invoices and payments"""
    
    orgs = ["demo-dental-001", "smile-center-002"]
    invoice_statuses = InvoiceStatus.query.filter_by(is_active=True).all()
    payment_statuses = PaymentStatus.query.filter_by(is_active=True).all()
    payment_methods = PaymentMethod.query.filter_by(is_active=True).all()
    
    invoices = []
    payments = []
    
    for org_id in orgs:
        patients = Patient.query.filter_by(organization_id=org_id).all()
        
        for patient in random.sample(patients, min(20, len(patients))):
            # Create 1-3 invoices per patient
            for i in range(random.randint(1, 3)):
                invoice_date = datetime.utcnow() - timedelta(days=random.randint(1, 90))
                due_date = invoice_date + timedelta(days=30)
                status = random.choice(invoice_statuses)
                
                subtotal = round(random.uniform(100, 1000), 2)
                tax = round(subtotal * 0.08, 2)
                total = subtotal + tax
                
                invoice = Invoice(
                    organization_id=org_id,
                    patient_id=patient.id,
                    invoice_number=f"INV-{org_id[:3].upper()}-{random.randint(1000, 9999)}",
                    invoice_date=invoice_date,
                    due_date=due_date,
                    status_id=status.id,
                    subtotal=subtotal,
                    tax_amount=tax,
                    total_amount=total,
                    description=f"Dental services for {patient.first_name} {patient.last_name}",
                    items=[
                        {
                            "description": "Dental Examination",
                            "quantity": 1,
                            "unit_price": 75.00,
                            "amount": 75.00
                        },
                        {
                            "description": "Teeth Cleaning",
                            "quantity": 1,
                            "unit_price": 85.00,
                            "amount": 85.00
                        },
                        {
                            "description": "X-Rays",
                            "quantity": 1,
                            "unit_price": 120.00,
                            "amount": 120.00
                        }
                    ],
                    created_by=1
                )
                invoices.append(invoice)
                
                # Create payments for some invoices
                if status.name in ["Paid", "Partial"]:
                    payment_method = random.choice(payment_methods)
                    payment_status = PaymentStatus.query.filter_by(name="Completed").first()
                    
                    payment_amount = total if status.name == "Paid" else round(total * random.uniform(0.3, 0.7), 2)
                    
                    payment = Payment(
                        organization_id=org_id,
                        patient_id=patient.id,
                        invoice_id=invoice.id,
                        payment_method_id=payment_method.id,
                        status_id=payment_status.id,
                        amount=payment_amount,
                        payment_date=invoice_date + timedelta(days=random.randint(1, 15)),
                        reference_number=f"PMT-{random.randint(10000, 99999)}",
                        notes="Payment received",
                        created_by=1
                    )
                    payments.append(payment)
    
    db.session.bulk_save_objects(invoices)
    db.session.bulk_save_objects(payments)
    db.session.commit()
    print(f"✅ {len(invoices)} invoices and {len(payments)} payments seeded successfully.")