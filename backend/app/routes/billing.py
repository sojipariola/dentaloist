# backend/app/routes/billing.py

from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
import json
from sqlalchemy import or_, and_, func

from ..models import db, Invoice, PaymentRecord, InsuranceClaim, Patient, Appointment, Organization
from ..utils.auth import get_current_user, permission_required
from ..utils.tenancy import tenant_required, multi_tenant_query
from ..utils.rate_limit import rate_limit
from ..utils.validation import validate_invoice_data, validate_payment_data, validate_insurance_claim_data

billing_bp = Blueprint('billing', __name__, url_prefix='/api/billing')

# ===== Invoice Routes =====

@billing_bp.route('/invoices', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_billing', 'manage_billing'])
@rate_limit(limit=60, period=60)  # 60 requests per minute
def get_invoices():
    """
    Get paginated list of invoices with advanced filtering
    """
    try:
        current_user = get_current_user()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100 per page
        status = request.args.get('status')
        patient_id = request.args.get('patient_id')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        search = request.args.get('search')
        
        # Build query with tenant filtering
        query = multi_tenant_query(Invoice)
        
        # Apply filters
        if status and status != 'all':
            query = query.filter(Invoice.status == status)
        
        if patient_id:
            query = query.filter(Invoice.patient_id == patient_id)
        
        if date_from:
            try:
                date_from_obj = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                query = query.filter(Invoice.issue_date >= date_from_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_from format. Use ISO format.'}), 400
        
        if date_to:
            try:
                date_to_obj = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                query = query.filter(Invoice.issue_date <= date_to_obj)
            except ValueError:
                return jsonify({'error': 'Invalid date_to format. Use ISO format.'}), 400
        
        if search:
            search_filter = or_(
                Invoice.invoice_number.ilike(f'%{search}%'),
                Invoice.patient.has(Patient.first_name.ilike(f'%{search}%')),
                Invoice.patient.has(Patient.last_name.ilike(f'%{search}%'))
            )
            query = query.filter(search_filter)
        
        # Order by most recent first
        invoices = query.order_by(Invoice.issue_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Calculate summary statistics
        summary = db.session.query(
            func.count(Invoice.id),
            func.sum(Invoice.total),
            func.sum(Invoice.balance)
        ).filter(Invoice.organization_id == g.tenant_id).first()
        
        return jsonify({
            'invoices': [invoice.to_dict(include_patient=True) for invoice in invoices.items],
            'pagination': {
                'total': invoices.total,
                'pages': invoices.pages,
                'current_page': page,
                'per_page': per_page
            },
            'summary': {
                'total_invoices': summary[0] or 0,
                'total_amount': float(summary[1] or 0),
                'total_balance': float(summary[2] or 0)
            }
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching invoices: {str(e)}")
        return jsonify({'error': 'Failed to fetch invoices'}), 500

@billing_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_billing', 'manage_billing'])
def get_invoice(invoice_id):
    """
    Get detailed invoice information including payments
    """
    try:
        invoice = multi_tenant_query(Invoice).filter_by(id=invoice_id).first_or_404()
        
        return jsonify({
            'invoice': invoice.to_dict(include_patient=True, include_payments=True),
            'payments': [payment.to_dict() for payment in invoice.payments]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching invoice {invoice_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch invoice'}), 500

@billing_bp.route('/invoices', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def create_invoice():
    """
    Create a new invoice
    """
    try:
        data = request.get_json()
        
        # Validate invoice data
        validation_error = validate_invoice_data(data)
        if validation_error:
            return validation_error
        
        # Verify patient belongs to current tenant
        patient = multi_tenant_query(Patient).filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        # Verify appointment belongs to current tenant (if provided)
        if data.get('appointment_id'):
            appointment = multi_tenant_query(Appointment).filter_by(id=data['appointment_id']).first()
            if not appointment:
                return jsonify({'error': 'Appointment not found or access denied'}), 404
        
        # Generate invoice number if not provided
        invoice_number = data.get('invoice_number')
        if not invoice_number:
            invoice_number = generate_invoice_number()
        
        # Calculate totals
        subtotal = sum(item['unit_price'] * item['quantity'] for item in data['items'])
        tax = data.get('tax', 0)
        discount = data.get('discount', 0)
        total = subtotal + tax - discount
        
        invoice = Invoice(
            organization_id=g.tenant_id,
            patient_id=data['patient_id'],
            appointment_id=data.get('appointment_id'),
            invoice_number=invoice_number,
            issue_date=datetime.fromisoformat(data['issue_date'].replace('Z', '+00:00')),
            due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')),
            items=data['items'],
            subtotal=Decimal(str(subtotal)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            tax=Decimal(str(tax)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            discount=Decimal(str(discount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            total=Decimal(str(total)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            balance=Decimal(str(total)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            status='pending',
            notes=data.get('notes', ''),
            terms=data.get('terms', '')
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        # Log invoice creation
        current_app.logger.info(f"Invoice {invoice_number} created for patient {data['patient_id']} by user {g.user.id}")
        
        return jsonify({
            'message': 'Invoice created successfully',
            'invoice': invoice.to_dict(include_patient=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating invoice: {str(e)}")
        return jsonify({'error': 'Failed to create invoice'}), 500

@billing_bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def update_invoice(invoice_id):
    """
    Update an existing invoice
    """
    try:
        invoice = multi_tenant_query(Invoice).filter_by(id=invoice_id).first_or_404()
        
        if invoice.status == 'paid':
            return jsonify({'error': 'Cannot modify paid invoice'}), 400
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['due_date', 'notes', 'terms', 'status']
        for field in allowed_fields:
            if field in data:
                if field == 'due_date':
                    setattr(invoice, field, datetime.fromisoformat(data[field].replace('Z', '+00:00')))
                else:
                    setattr(invoice, field, data[field])
        
        invoice.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice updated successfully',
            'invoice': invoice.to_dict(include_patient=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating invoice {invoice_id}: {str(e)}")
        return jsonify({'error': 'Failed to update invoice'}), 500

@billing_bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def delete_invoice(invoice_id):
    """
    Delete an invoice (soft delete)
    """
    try:
        invoice = multi_tenant_query(Invoice).filter_by(id=invoice_id).first_or_404()
        
        if invoice.status == 'paid':
            return jsonify({'error': 'Cannot delete paid invoice'}), 400
        
        # Soft delete
        invoice.is_deleted = True
        invoice.deleted_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting invoice {invoice_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete invoice'}), 500

# ===== Payment Routes =====

@billing_bp.route('/payments', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def create_payment():
    """
    Record a payment for an invoice
    """
    try:
        data = request.get_json()
        
        # Validate payment data
        validation_error = validate_payment_data(data)
        if validation_error:
            return validation_error
        
        invoice = multi_tenant_query(Invoice).filter_by(id=data['invoice_id']).first_or_404()
        
        if invoice.status == 'paid':
            return jsonify({'error': 'Invoice is already paid'}), 400
        
        payment_amount = Decimal(str(data['amount'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        if payment_amount <= 0:
            return jsonify({'error': 'Payment amount must be positive'}), 400
        
        if payment_amount > invoice.balance:
            return jsonify({'error': 'Payment amount exceeds invoice balance'}), 400
        
        payment = PaymentRecord(
            invoice_id=data['invoice_id'],
            amount=payment_amount,
            method=data['method'],
            processor=data.get('processor'),
            transaction_id=data.get('transaction_id'),
            notes=data.get('notes', ''),
            payment_date=datetime.fromisoformat(data.get('payment_date', datetime.utcnow().isoformat()).replace('Z', '+00:00'))
        )
        
        db.session.add(payment)
        
        # Update invoice balance and status
        invoice.paid_amount += payment_amount
        invoice.balance = invoice.total - invoice.paid_amount
        
        if invoice.balance <= 0:
            invoice.status = 'paid'
            invoice.paid_date = datetime.utcnow()
        else:
            invoice.status = 'partial'
        
        invoice.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log payment
        current_app.logger.info(f"Payment of {payment_amount} recorded for invoice {invoice.invoice_number} by user {g.user.id}")
        
        return jsonify({
            'message': 'Payment recorded successfully',
            'payment': payment.to_dict(),
            'invoice': invoice.to_dict(include_patient=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error recording payment: {str(e)}")
        return jsonify({'error': 'Failed to record payment'}), 500

@billing_bp.route('/payments/<int:payment_id>', methods=['DELETE'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def delete_payment(payment_id):
    """
    Delete a payment (soft delete) and recalculate invoice balance
    """
    try:
        payment = PaymentRecord.query.join(Invoice).filter(
            PaymentRecord.id == payment_id,
            Invoice.organization_id == g.tenant_id
        ).first_or_404()
        
        invoice = payment.invoice
        
        if invoice.status == 'void':
            return jsonify({'error': 'Cannot modify voided invoice'}), 400
        
        # Soft delete payment
        payment.is_deleted = True
        payment.deleted_at = datetime.utcnow()
        
        # Recalculate invoice balances
        invoice.paid_amount = db.session.query(
            func.coalesce(func.sum(PaymentRecord.amount), 0)
        ).filter(
            PaymentRecord.invoice_id == invoice.id,
            PaymentRecord.is_deleted == False
        ).scalar()
        
        invoice.balance = invoice.total - invoice.paid_amount
        
        if invoice.paid_amount <= 0:
            invoice.status = 'pending'
            invoice.paid_date = None
        elif invoice.balance > 0:
            invoice.status = 'partial'
        else:
            invoice.status = 'paid'
        
        invoice.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'message': 'Payment deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting payment {payment_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete payment'}), 500

# ===== Insurance Claim Routes =====

@billing_bp.route('/insurance-claims', methods=['POST'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def create_insurance_claim():
    """
    Submit an insurance claim
    """
    try:
        data = request.get_json()
        
        # Validate insurance claim data
        validation_error = validate_insurance_claim_data(data)
        if validation_error:
            return validation_error
        
        # Verify patient and appointment belong to current tenant
        patient = multi_tenant_query(Patient).filter_by(id=data['patient_id']).first()
        if not patient:
            return jsonify({'error': 'Patient not found or access denied'}), 404
        
        appointment = multi_tenant_query(Appointment).filter_by(id=data['appointment_id']).first()
        if not appointment:
            return jsonify({'error': 'Appointment not found or access denied'}), 404
        
        claim = InsuranceClaim(
            organization_id=g.tenant_id,
            patient_id=data['patient_id'],
            appointment_id=data['appointment_id'],
            insurance_provider=data['insurance_provider'],
            policy_number=data['policy_number'],
            subscriber_name=data.get('subscriber_name'),
            subscriber_dob=data.get('subscriber_dob'),
            relationship_to_subscriber=data.get('relationship_to_subscriber', 'self'),
            submitted_amount=Decimal(str(data['submitted_amount'])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
            submission_date=datetime.utcnow(),
            status='submitted',
            diagnosis_codes=data.get('diagnosis_codes', []),
            procedure_codes=data.get('procedure_codes', []),
            notes=data.get('notes', '')
        )
        
        db.session.add(claim)
        db.session.commit()
        
        # Log claim submission
        current_app.logger.info(f"Insurance claim submitted for patient {data['patient_id']} by user {g.user.id}")
        
        return jsonify({
            'message': 'Insurance claim submitted successfully',
            'claim': claim.to_dict(include_patient=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error submitting insurance claim: {str(e)}")
        return jsonify({'error': 'Failed to submit insurance claim'}), 500

@billing_bp.route('/insurance-claims/<int:claim_id>', methods=['PUT'])
@jwt_required()
@tenant_required
@permission_required(['manage_billing'])
def update_insurance_claim(claim_id):
    """
    Update insurance claim status or information
    """
    try:
        claim = multi_tenant_query(InsuranceClaim).filter_by(id=claim_id).first_or_404()
        
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['status', 'approved_amount', 'rejection_reason', 'payment_date', 'notes']
        for field in allowed_fields:
            if field in data:
                if field in ['approved_amount']:
                    setattr(claim, field, Decimal(str(data[field])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                elif field == 'payment_date' and data[field]:
                    setattr(claim, field, datetime.fromisoformat(data[field].replace('Z', '+00:00')))
                else:
                    setattr(claim, field, data[field])
        
        claim.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Insurance claim updated successfully',
            'claim': claim.to_dict(include_patient=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating insurance claim {claim_id}: {str(e)}")
        return jsonify({'error': 'Failed to update insurance claim'}), 500

# ===== Utility Routes =====

@billing_bp.route('/dashboard', methods=['GET'])
@jwt_required()
@tenant_required
@permission_required(['view_billing', 'manage_billing'])
def billing_dashboard():
    """
    Get billing dashboard statistics
    """
    try:
        # Calculate various statistics
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        # Invoice statistics
        invoice_stats = db.session.query(
            func.count(Invoice.id),
            func.sum(Invoice.total),
            func.sum(Invoice.balance)
        ).filter(
            Invoice.organization_id == g.tenant_id,
            Invoice.issue_date >= thirty_days_ago
        ).first()
        
        # Payment statistics
        payment_stats = db.session.query(
            func.count(PaymentRecord.id),
            func.sum(PaymentRecord.amount)
        ).join(Invoice).filter(
            Invoice.organization_id == g.tenant_id,
            PaymentRecord.payment_date >= thirty_days_ago,
            PaymentRecord.is_deleted == False
        ).first()
        
        # Insurance claim statistics
        claim_stats = db.session.query(
            func.count(InsuranceClaim.id),
            func.sum(InsuranceClaim.submitted_amount),
            func.sum(InsuranceClaim.approved_amount or 0)
        ).filter(
            InsuranceClaim.organization_id == g.tenant_id,
            InsuranceClaim.submission_date >= thirty_days_ago
        ).first()
        
        # Recent invoices
        recent_invoices = multi_tenant_query(Invoice).order_by(
            Invoice.issue_date.desc()
        ).limit(5).all()
        
        # Overdue invoices
        overdue_invoices = multi_tenant_query(Invoice).filter(
            Invoice.due_date < datetime.utcnow(),
            Invoice.status.in_(['pending', 'partial'])
        ).count()
        
        return jsonify({
            'stats': {
                'total_invoices': invoice_stats[0] or 0,
                'total_invoice_amount': float(invoice_stats[1] or 0),
                'outstanding_balance': float(invoice_stats[2] or 0),
                'total_payments': payment_stats[0] or 0,
                'total_payment_amount': float(payment_stats[1] or 0),
                'total_claims': claim_stats[0] or 0,
                'total_claimed_amount': float(claim_stats[1] or 0),
                'total_approved_amount': float(claim_stats[2] or 0),
                'overdue_invoices': overdue_invoices
            },
            'recent_invoices': [invoice.to_dict(include_patient=True) for invoice in recent_invoices]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching billing dashboard: {str(e)}")
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500

# ===== Helper Functions =====

def generate_invoice_number():
    """
    Generate a unique invoice number
    Format: INV-{year}{month}{day}-{sequence}
    """
    today = datetime.utcnow()
    date_part = today.strftime("%Y%m%d")
    
    # Get the count of invoices for today
    count = Invoice.query.filter(
        Invoice.organization_id == g.tenant_id,
        func.date(Invoice.created_at) == today.date()
    ).count()
    
    sequence = count + 1
    return f"INV-{date_part}-{sequence:04d}"