# backend/app/models/financial.py # class WidgetType(

from sqlalchemy import (Text, DateTime, Float, Integer, String, Boolean, ForeignKey, 
                       Numeric, CheckConstraint, LargeBinary)
from sqlalchemy.dialects.postgresql import JSON 
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid
from datetime import timedelta
# metadata
from .base import BaseModel
from .lookups import (
    PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, 
    ExpenseCategory, Currency
)
from . import db

# backend/app/models/financial.py
# FinancialTransaction - Central ledger for all financial activities

from sqlalchemy import Text, DateTime, Float, Integer, String, Boolean, ForeignKey, Numeric, CheckConstraint, LargeBinary
from sqlalchemy.dialects.postgresql import JSON 
from sqlalchemy.orm import relationship
from datetime import datetime, date
import uuid
from datetime import timedelta

from .base import BaseModel
from .lookups import (
    PaymentStatus, InvoiceStatus, PaymentMethod, ClaimStatus, 
    ExpenseCategory, Currency, TransactionType
)
from . import db


class FinancialTransaction(BaseModel):
    __tablename__ = 'financial_transactions'
    
    # Foreign keys
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=True)
    claim_id = db.Column(db.Integer, db.ForeignKey('insurance_claims.id'), nullable=True)
    
    # Lookup foreign keys
    transaction_type_id = db.Column(db.Integer, db.ForeignKey('transaction_types.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    
    # Transaction identification
    transaction_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    reference_number = db.Column(db.String(100), index=True)
    
    # Core transaction details
    transaction_date = db.Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    effective_date = db.Column(db.Date, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    
    # Amount details
    debit_amount = db.Column(Numeric(10, 2), default=0.0)
    credit_amount = db.Column(Numeric(10, 2), default=0.0)
    net_amount = db.Column(Numeric(10, 2), nullable=False)
    
    # Account mapping (simplified chart of accounts)
    account_type = db.Column(db.String(50), nullable=False, index=True)  # revenue, expense, asset, liability, equity
    account_subtype = db.Column(db.String(50), index=True)  # accounts_receivable, cash, insurance_receivable, etc.
    
    # Status and workflow
    status = db.Column(db.String(20), default='posted', index=True)
    is_reconciled = db.Column(db.Boolean, default=False)
    reconciled_date = db.Column(DateTime)
    
    # Payment and settlement information
    settlement_date = db.Column(db.Date)
    settlement_reference = db.Column(db.String(100))
    
    # Metadata and tracking - CHANGED FROM 'metadata' TO 'transaction_metadata'
    transaction_metadata = db.Column(db.JSON)  # Renamed from 'metadata'
    source_module = db.Column(db.String(50), nullable=False)  # billing, payment, insurance, expense, adjustment
    source_reference = db.Column(db.String(100))  # Original source document reference
    
    # Reversal tracking
    is_reversal = db.Column(db.Boolean, default=False)
    reversed_transaction_id = db.Column(db.Integer, db.ForeignKey('financial_transactions.id'), nullable=True)
    reversal_reason = db.Column(db.Text)
    
    # Audit information
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    verified_date = db.Column(DateTime)
    
    # Relationships
    organization = relationship('Organization', back_populates='financial_transactions')
    patient = relationship('Patient', back_populates='financial_transactions')
    invoice = relationship('Invoice')
    payment = relationship('Payment')
    expense = relationship('Expense')
    claim = relationship('InsuranceClaim')
    transaction_type = relationship('TransactionType', back_populates='transactions')
    currency = relationship('Currency')
    poster = relationship('User', foreign_keys=[posted_by])
    verifier = relationship('User', foreign_keys=[verified_by])
    reversed_transaction = relationship('FinancialTransaction', remote_side='FinancialTransaction.id', 
                                      backref=db.backref('reversal_transaction', uselist=False))
    
    # Indexes for common queries
    __table_args__ = (
        db.Index('idx_transaction_org_date', 'organization_id', 'transaction_date'),
        db.Index('idx_transaction_org_account', 'organization_id', 'account_type', 'account_subtype'),
        db.Index('idx_transaction_org_status', 'organization_id', 'status'),
        db.Index('idx_transaction_org_patient', 'organization_id', 'patient_id', 'transaction_date'),
        db.Index('idx_transaction_effective_date', 'effective_date'),
        db.Index('idx_transaction_reconciliation', 'organization_id', 'is_reconciled', 'transaction_date'),
        db.Index('idx_transaction_source', 'source_module', 'source_reference'),
        CheckConstraint('debit_amount >= 0', name='check_debit_positive'),
        CheckConstraint('credit_amount >= 0', name='check_credit_positive'),
        CheckConstraint(
            '(debit_amount > 0 AND credit_amount = 0) OR (credit_amount > 0 AND debit_amount = 0) OR (debit_amount = 0 AND credit_amount = 0)',
            name='check_debit_credit_exclusive'
        ),
    )

    def __init__(self, **kwargs):
        # Handle the renamed metadata field
        if 'metadata' in kwargs:
            kwargs['transaction_metadata'] = kwargs.pop('metadata')
        super().__init__(**kwargs)
        if not self.transaction_number:
            self.transaction_number = self.generate_transaction_number()
        if not self.effective_date:
            self.effective_date = datetime.utcnow().date()
        # Calculate net amount
        self.calculate_net_amount()

    def calculate_net_amount(self):
        """Calculate net amount based on debit and credit"""
        self.net_amount = float(self.debit_amount) - float(self.credit_amount)

    def _to_dict_impl(self):
        return {
            'transaction_number': self.transaction_number,
            'transaction_date': self.transaction_date.isoformat() if self.transaction_date else None,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'description': self.description,
            'transaction_type': self.transaction_type.to_dict() if self.transaction_type else None,
            'currency': self.currency.to_dict() if self.currency else None,
            'debit_amount': float(self.debit_amount) if self.debit_amount else None,
            'credit_amount': float(self.credit_amount) if self.credit_amount else None,
            'net_amount': float(self.net_amount) if self.net_amount else None,
            'account_type': self.account_type,
            'account_subtype': self.account_subtype,
            'status': self.status,
            'is_reconciled': self.is_reconciled,
            'source_module': self.source_module,
            'source_reference': self.source_reference,
            'reference_number': self.reference_number,
            'patient_name': self.patient.full_name if self.patient else None,
            'invoice_number': self.invoice.invoice_number if self.invoice else None,
            'payment_reference': self.payment.reference_number if self.payment else None,
            'expense_description': self.expense.description if self.expense else None,
            'claim_number': self.claim.claim_number if self.claim else None,
            'is_reversal': self.is_reversal,
            'reversal_reason': self.reversal_reason,
            'metadata': self.transaction_metadata or {},  # Map back to 'metadata' in API response
            'posted_by_user': self.poster.full_name if self.poster else None,
            'verified_by_user': self.verifier.full_name if self.verifier else None
        }

    @classmethod
    def generate_transaction_number(cls):
        """Generate unique transaction number"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = str(uuid.uuid4().int)[:6]
        return f"TRX-{timestamp}-{random_suffix}"

    # Factory methods for different transaction types
    @classmethod
    def create_invoice_transaction(cls, invoice, posted_by_user):
        """Create transaction for invoice creation"""
        invoice_creation_type = TransactionType.query.filter_by(code='invoice_creation').first()
        if not invoice_creation_type:
            raise ValueError("Transaction type 'invoice_creation' not found")
        
        transaction = cls(
            organization_id=invoice.organization_id,
            patient_id=invoice.patient_id,
            invoice_id=invoice.id,
            transaction_type_id=invoice_creation_type.id,
            currency_id=invoice.currency_id,
            description=f"Invoice {invoice.invoice_number} - {invoice.treatment.name if invoice.treatment else 'Services'}",
            debit_amount=invoice.total_amount,
            account_type='asset',
            account_subtype='accounts_receivable',
            source_module='billing',
            source_reference=invoice.invoice_number,
            reference_number=invoice.invoice_number,
            posted_by=posted_by_user.id,
            transaction_metadata={
                'invoice_date': invoice.invoice_date.isoformat() if invoice.invoice_date else None,
                'due_date': invoice.due_date.isoformat() if invoice.due_date else None,
                'items_count': len(invoice.items) if invoice.items else 0,
                'tax_amount': float(invoice.tax_amount) if invoice.tax_amount else 0,
                'discount_amount': float(invoice.discount_amount) if invoice.discount_amount else 0,
                'patient_responsibility': float(invoice.balance_due) if invoice.balance_due else 0
            }
        )
        return transaction

    @classmethod
    def create_payment_transaction(cls, payment, posted_by_user):
        """Create transaction for payment receipt"""
        payment_receipt_type = TransactionType.query.filter_by(code='payment_receipt').first()
        cash_receipt_type = TransactionType.query.filter_by(code='cash_receipt').first()
        
        if not payment_receipt_type or not cash_receipt_type:
            raise ValueError("Required transaction types not found")
        
        # Create accounts receivable credit
        ar_transaction = cls(
            organization_id=payment.patient.organization_id,
            patient_id=payment.patient_id,
            payment_id=payment.id,
            invoice_id=payment.invoice_id,
            transaction_type_id=payment_receipt_type.id,
            currency_id=payment.currency_id,
            description=f"Payment received - {payment.payment_method.name if payment.payment_method else 'Unknown method'}",
            credit_amount=payment.amount,
            account_type='asset',
            account_subtype='accounts_receivable',
            source_module='payment',
            source_reference=payment.reference_number,
            reference_number=payment.reference_number,
            posted_by=posted_by_user.id,
            settlement_date=payment.payment_date.date() if payment.payment_date else None,
            transaction_metadata={
                'payment_method': payment.payment_method.name if payment.payment_method else None,
                'transaction_id': payment.transaction_id,
                'fee_amount': float(payment.fee_amount) if payment.fee_amount else 0,
                'net_amount': float(payment.net_amount) if payment.net_amount else 0
            }
        )
        
        # Create cash/bank debit
        cash_account_subtype = 'cash' if payment.payment_method and payment.payment_method.code == 'cash' else 'bank'
        cash_transaction = cls(
            organization_id=payment.patient.organization_id,
            patient_id=payment.patient_id,
            payment_id=payment.id,
            transaction_type_id=cash_receipt_type.id,
            currency_id=payment.currency_id,
            description=f"Cash receipt - {payment.reference_number}",
            debit_amount=payment.net_amount or payment.amount,
            account_type='asset',
            account_subtype=cash_account_subtype,
            source_module='payment',
            source_reference=payment.reference_number,
            reference_number=payment.reference_number,
            posted_by=posted_by_user.id,
            settlement_date=payment.payment_date.date() if payment.payment_date else None,
            transaction_metadata={
                'payment_method': payment.payment_method.name if payment.payment_method else None,
                'original_amount': float(payment.amount),
                'processing_fees': float(payment.fee_amount) if payment.fee_amount else 0
            }
        )
        
        return [ar_transaction, cash_transaction]

    @classmethod
    def create_insurance_claim_transaction(cls, claim, posted_by_user):
        """Create transaction for insurance claim submission"""
        insurance_claim_type = TransactionType.query.filter_by(code='insurance_claim').first()
        if not insurance_claim_type:
            raise ValueError("Transaction type 'insurance_claim' not found")
        
        transaction = cls(
            organization_id=claim.patient.organization_id,
            patient_id=claim.patient_id,
            claim_id=claim.id,
            invoice_id=claim.invoice_id,
            transaction_type_id=insurance_claim_type.id,
            currency_id=Currency.query.filter_by(code='USD').first().id,
            description=f"Insurance claim {claim.claim_number} - {claim.insurance_provider}",
            debit_amount=claim.claim_amount,
            account_type='asset',
            account_subtype='insurance_receivable',
            source_module='insurance',
            source_reference=claim.claim_number,
            reference_number=claim.claim_number,
            posted_by=posted_by_user.id,
            transaction_metadata={
                'insurance_provider': claim.insurance_provider,
                'policy_number': claim.policy_number,
                'procedures_count': len(claim.procedures) if claim.procedures else 0,
                'submission_date': claim.submission_date.isoformat() if claim.submission_date else None,
                'patient_responsibility': float(claim.patient_responsibility) if claim.patient_responsibility else 0
            }
        )
        return transaction

    @classmethod
    def create_claim_settlement_transaction(cls, claim, posted_by_user):
        """Create transaction for insurance claim settlement"""
        if not claim.approved_amount:
            return None
            
        insurance_payment_type = TransactionType.query.filter_by(code='insurance_payment').first()
        insurance_cash_type = TransactionType.query.filter_by(code='insurance_cash_receipt').first()
        
        if not insurance_payment_type or not insurance_cash_type:
            raise ValueError("Required transaction types not found")
        
        # Create insurance receivable credit
        ar_transaction = cls(
            organization_id=claim.patient.organization_id,
            patient_id=claim.patient_id,
            claim_id=claim.id,
            transaction_type_id=insurance_payment_type.id,
            currency_id=Currency.query.filter_by(code='USD').first().id,
            description=f"Insurance payment - {claim.claim_number}",
            credit_amount=claim.approved_amount,
            account_type='asset',
            account_subtype='insurance_receivable',
            source_module='insurance',
            source_reference=claim.claim_number,
            reference_number=claim.claim_number,
            posted_by=posted_by_user.id,
            settlement_date=claim.resolution_date.date() if claim.resolution_date else None,
            transaction_metadata={
                'insurance_provider': claim.insurance_provider,
                'patient_responsibility': float(claim.patient_responsibility) if claim.patient_responsibility else 0,
                'denial_reason': claim.denial_reason,
                'adjustment_codes': claim.adjustment_codes
            }
        )
        
        transactions = [ar_transaction]
        
        # Create cash/bank entry for the payment
        if claim.approved_amount > 0:
            cash_transaction = cls(
                organization_id=claim.patient.organization_id,
                patient_id=claim.patient_id,
                claim_id=claim.id,
                transaction_type_id=insurance_cash_type.id,
                currency_id=Currency.query.filter_by(code='USD').first().id,
                description=f"Insurance payment receipt - {claim.claim_number}",
                debit_amount=claim.approved_amount,
                account_type='asset',
                account_subtype='bank',
                source_module='insurance',
                source_reference=claim.claim_number,
                reference_number=claim.claim_number,
                posted_by=posted_by_user.id,
                settlement_date=claim.resolution_date.date() if claim.resolution_date else None,
                transaction_metadata={
                    'insurance_provider': claim.insurance_provider,
                    'claim_number': claim.claim_number
                }
            )
            transactions.append(cash_transaction)
        
        return transactions

    @classmethod
    def create_expense_transaction(cls, expense, posted_by_user):
        """Create transaction for expense"""
        expense_type = TransactionType.query.filter_by(code='expense').first()
        expense_payment_type = TransactionType.query.filter_by(code='expense_payment').first()
        
        if not expense_type or not expense_payment_type:
            raise ValueError("Required transaction types not found")
        
        # Create expense debit
        expense_transaction = cls(
            organization_id=expense.organization_id,
            expense_id=expense.id,
            transaction_type_id=expense_type.id,
            currency_id=Currency.query.filter_by(code='USD').first().id,
            description=f"Expense - {expense.vendor_name or 'Miscellaneous'}: {expense.description}",
            debit_amount=expense.amount,
            account_type='expense',
            account_subtype=expense.category.name.lower().replace(' ', '_') if expense.category else 'general',
            source_module='expense',
            source_reference=expense.vendor_invoice_number,
            reference_number=expense.vendor_invoice_number,
            posted_by=posted_by_user.id,
            transaction_metadata={
                'vendor_name': expense.vendor_name,
                'category': expense.category.name if expense.category else None,
                'is_tax_deductible': expense.is_tax_deductible,
                'tax_amount': float(expense.tax_amount) if expense.tax_amount else 0,
                'incurred_by': expense.incurring_user.full_name if expense.incurring_user else None
            }
        )
        
        # Create cash/bank credit
        cash_account_subtype = 'cash' if expense.payment_method and expense.payment_method.code == 'cash' else 'bank'
        cash_transaction = cls(
            organization_id=expense.organization_id,
            expense_id=expense.id,
            transaction_type_id=expense_payment_type.id,
            currency_id=Currency.query.filter_by(code='USD').first().id,
            description=f"Payment for expense - {expense.vendor_invoice_number}",
            credit_amount=expense.amount,
            account_type='asset',
            account_subtype=cash_account_subtype,
            source_module='expense',
            source_reference=expense.vendor_invoice_number,
            reference_number=expense.vendor_invoice_number,
            posted_by=posted_by_user.id,
            transaction_metadata={
                'vendor_name': expense.vendor_name,
                'payment_method': expense.payment_method.name if expense.payment_method else None
            }
        )
        
        return [expense_transaction, cash_transaction]

    @classmethod
    def create_adjustment_transaction(cls, invoice, adjustment_type, amount, reason, posted_by_user):
        """Create adjustment transaction (discount, write-off, etc.)"""
        transaction_type_map = {
            'discount': 'invoice_discount',
            'write_off': 'write_off',
            'refund': 'refund',
            'correction': 'correction'
        }
        
        adjustment_code = transaction_type_map.get(adjustment_type, 'adjustment')
        adjustment_transaction_type = TransactionType.query.filter_by(code=adjustment_code).first()
        
        if not adjustment_transaction_type:
            raise ValueError(f"Transaction type '{adjustment_code}' not found")
        
        transaction = cls(
            organization_id=invoice.organization_id,
            patient_id=invoice.patient_id,
            invoice_id=invoice.id,
            transaction_type_id=adjustment_transaction_type.id,
            currency_id=invoice.currency_id,
            description=f"{adjustment_type.title()} - {reason}",
            credit_amount=amount,
            account_type='revenue' if adjustment_type in ['discount', 'write_off'] else 'asset',
            account_subtype='accounts_receivable',
            source_module='adjustment',
            source_reference=invoice.invoice_number,
            reference_number=f"ADJ-{invoice.invoice_number}",
            posted_by=posted_by_user.id,
            transaction_metadata={
                'adjustment_type': adjustment_type,
                'reason': reason,
                'original_invoice_amount': float(invoice.total_amount) if invoice.total_amount else 0,
                'adjusted_by': posted_by_user.full_name
            }
        )
        return transaction

    # Query methods for financial reporting
    @classmethod
    def get_patient_ledger(cls, patient_id, start_date=None, end_date=None):
        """Get complete ledger for a patient"""
        query = cls.query.filter_by(patient_id=patient_id)
        
        if start_date:
            query = query.filter(cls.effective_date >= start_date)
        if end_date:
            query = query.filter(cls.effective_date <= end_date)
            
        return query.order_by(cls.effective_date, cls.created_at).all()

    @classmethod
    def get_organization_ledger(cls, organization_id, start_date, end_date, account_type=None):
        """Get organization ledger for period"""
        query = cls.query.filter(
            cls.organization_id == organization_id,
            cls.effective_date >= start_date,
            cls.effective_date <= end_date,
            cls.status == 'posted'
        )
        
        if account_type:
            query = query.filter_by(account_type=account_type)
            
        return query.order_by(cls.effective_date, cls.account_type, cls.account_subtype).all()

    @classmethod
    def get_account_balance(cls, organization_id, account_type, account_subtype=None, as_of_date=None):
        """Get balance for specific account"""
        query = cls.query.filter(
            cls.organization_id == organization_id,
            cls.account_type == account_type,
            cls.status == 'posted'
        )
        
        if account_subtype:
            query = query.filter(cls.account_subtype == account_subtype)
        if as_of_date:
            query = query.filter(cls.effective_date <= as_of_date)
            
        transactions = query.all()
        balance = sum(float(t.net_amount) for t in transactions)
        return balance

    @classmethod
    def get_trial_balance(cls, organization_id, as_of_date=None):
        """Generate trial balance"""
        if not as_of_date:
            as_of_date = datetime.utcnow().date()
            
        query = cls.query.filter(
            cls.organization_id == organization_id,
            cls.status == 'posted'
        )
        
        if as_of_date:
            query = query.filter(cls.effective_date <= as_of_date)
            
        transactions = query.all()
        
        trial_balance = {}
        for transaction in transactions:
            account_key = f"{transaction.account_type}_{transaction.account_subtype}"
            if account_key not in trial_balance:
                trial_balance[account_key] = {
                    'account_type': transaction.account_type,
                    'account_subtype': transaction.account_subtype,
                    'debit_total': 0.0,
                    'credit_total': 0.0,
                    'balance': 0.0
                }
            
            balance_entry = trial_balance[account_key]
            balance_entry['debit_total'] += float(transaction.debit_amount)
            balance_entry['credit_total'] += float(transaction.credit_amount)
            balance_entry['balance'] += float(transaction.net_amount)
        
        return trial_balance

    @classmethod
    def get_revenue_report(cls, organization_id, start_date, end_date):
        """Generate revenue report for period"""
        revenue_transactions = cls.query.filter(
            cls.organization_id == organization_id,
            cls.account_type == 'revenue',
            cls.effective_date >= start_date,
            cls.effective_date <= end_date,
            cls.status == 'posted'
        ).all()
        
        report = {
            'total_revenue': 0.0,
            'by_source': {},
            'by_patient': {},
            'by_procedure': {}
        }
        
        for transaction in revenue_transactions:
            amount = float(transaction.debit_amount)  # Revenue increases with debits
            report['total_revenue'] += amount
            
            # Group by source
            source = transaction.source_module
            if source not in report['by_source']:
                report['by_source'][source] = 0.0
            report['by_source'][source] += amount
            
            # Group by patient
            if transaction.patient:
                patient_name = transaction.patient.full_name
                if patient_name not in report['by_patient']:
                    report['by_patient'][patient_name] = 0.0
                report['by_patient'][patient_name] += amount
            
            # Extract procedure information from transaction_metadata
            if transaction.transaction_metadata and 'procedures' in transaction.transaction_metadata:
                for procedure in transaction.transaction_metadata['procedures']:
                    proc_code = procedure.get('code', 'Unknown')
                    if proc_code not in report['by_procedure']:
                        report['by_procedure'][proc_code] = 0.0
                    report['by_procedure'][proc_code] += procedure.get('amount', 0)
        
        return report

    # Business logic methods
    def mark_as_reconciled(self, reconciled_by_user, reference=None):
        """Mark transaction as reconciled"""
        self.is_reconciled = True
        self.reconciled_date = datetime.utcnow()
        if reference:
            self.settlement_reference = reference

    def reverse_transaction(self, reversed_by_user, reason):
        """Reverse this transaction"""
        if self.is_reversal:
            return None  # Cannot reverse a reversal
        
        reversal_type = TransactionType.query.filter_by(code='reversal').first()
        if not reversal_type:
            raise ValueError("Transaction type 'reversal' not found")
        
        reversal = FinancialTransaction(
            organization_id=self.organization_id,
            patient_id=self.patient_id,
            invoice_id=self.invoice_id,
            payment_id=self.payment_id,
            expense_id=self.expense_id,
            claim_id=self.claim_id,
            transaction_type_id=reversal_type.id,
            currency_id=self.currency_id,
            description=f"Reversal: {self.description}",
            debit_amount=self.credit_amount,  # Swap debit/credit
            credit_amount=self.debit_amount,
            net_amount=-self.net_amount,
            account_type=self.account_type,
            account_subtype=self.account_subtype,
            source_module=self.source_module,
            source_reference=f"REV-{self.source_reference}",
            reference_number=f"REV-{self.reference_number}",
            posted_by=reversed_by_user.id,
            is_reversal=True,
            reversed_transaction_id=self.id,
            reversal_reason=reason,
            transaction_metadata={
                'original_transaction': self.transaction_number,
                'original_date': self.transaction_date.isoformat() if self.transaction_date else None,
                'reversal_reason': reason
            }
        )
        
        return reversal

    def verify_transaction(self, verified_by_user):
        """Verify transaction (for sensitive transactions)"""
        self.verified_by = verified_by_user.id
        self.verified_date = datetime.utcnow()
        self.status = 'verified'

    @property
    def is_debit(self):
        """Check if transaction is a debit"""
        return self.debit_amount > 0

    @property
    def is_credit(self):
        """Check if transaction is a credit"""
        return self.credit_amount > 0

    @property
    def absolute_amount(self):
        """Get absolute amount regardless of debit/credit"""
        return float(self.debit_amount) if self.debit_amount > 0 else float(self.credit_amount)

    def get_related_transactions(self):
        """Get related transactions (payments for invoices, etc.)"""
        related = []
        
        if self.invoice_id:
            # Find payments for this invoice
            payment_transactions = FinancialTransaction.query.filter_by(
                invoice_id=self.invoice_id,
                source_module='payment'
            ).all()
            related.extend(payment_transactions)
            
        if self.payment_id:
            # Find the invoice transaction for this payment
            invoice_transaction = FinancialTransaction.query.filter_by(
                payment_id=self.payment_id,
                source_module='billing'
            ).first()
            if invoice_transaction:
                related.append(invoice_transaction)
                
        return related

    @property
    def requires_verification(self):
        """Check if this transaction requires verification based on its type"""
        return (self.transaction_type and 
                self.transaction_type.requires_verification and 
                self.absolute_amount > 1000)  # Example threshold

    def can_be_reversed(self):
        """Check if this transaction can be reversed"""
        return (not self.is_reversal and 
                self.status == 'posted' and 
                datetime.utcnow().date() <= self.effective_date + timedelta(days=90))  # 90-day reversal window
                

class Invoice(BaseModel):
    __tablename__ = 'invoices'
    
    # Foreign keys
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    
    # Lookup foreign keys
    status_id = db.Column(db.Integer, db.ForeignKey('invoice_statuses.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    
    # Invoice identification
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    invoice_date = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = db.Column(DateTime, nullable=False)
    
    # Status and tracking
    sent_date = db.Column(DateTime)
    viewed_date = db.Column(DateTime)
    payment_terms = db.Column(db.String(100), default="Net 30")
    
    # Line items
    items = db.Column(db.JSON, nullable=False)
    
    # Financial totals
    subtotal = db.Column(Numeric(10, 2), nullable=False, default=0.0)
    tax_amount = db.Column(Numeric(10, 2), default=0.0)
    discount_amount = db.Column(Numeric(10, 2), default=0.0)
    total_amount = db.Column(Numeric(10, 2), nullable=False, default=0.0)
    amount_paid = db.Column(Numeric(10, 2), default=0.0)
    balance_due = db.Column(Numeric(10, 2), nullable=False, default=0.0)
    
    # Tax information
    tax_rate = db.Column(Numeric(5, 2), default=0.0)
    is_taxable = db.Column(db.Boolean, default=True)
    
    # Discount information
    discount_percentage = db.Column(Numeric(5, 2), default=0.0)
    discount_reason = db.Column(db.Text)
    
    # Payment information
    payment_instructions = db.Column(db.Text)
    
    # Notes and terms
    notes = db.Column(db.Text)
    terms_and_conditions = db.Column(db.Text)
    
    # Insurance information
    primary_insurance_id = db.Column(db.Integer, db.ForeignKey('insurance_plans.id'), nullable=True)
    secondary_insurance_id = db.Column(db.Integer, db.ForeignKey('insurance_plans.id'), nullable=True)
    insurance_estimated = db.Column(Numeric(10, 2), default=0.0)
    
    # Relationships
    organization = relationship('Organization', back_populates='invoices')
    patient = relationship('Patient', back_populates='invoices')
    treatment = relationship('Treatment', back_populates='invoices')
    appointment = relationship('Appointment', back_populates='invoices')
    primary_insurance = relationship('InsurancePlan', foreign_keys=[primary_insurance_id])
    secondary_insurance = relationship('InsurancePlan', foreign_keys=[secondary_insurance_id])
    payments = relationship('Payment', back_populates='invoice')
    claims = relationship('InsuranceClaim', back_populates='invoice')
    status = relationship('InvoiceStatus')
    currency = relationship('Currency')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_invoice_org_status', 'organization_id', 'status_id'),
        db.Index('idx_invoice_patient_date', 'patient_id', 'invoice_date'),
        db.Index('idx_invoice_due_date', 'due_date'),
        db.Index('idx_invoice_number', 'invoice_number'),
        db.Index('idx_invoice_balance', 'balance_due'),
        CheckConstraint('total_amount >= 0', name='check_invoice_total_positive'),
        CheckConstraint('balance_due >= 0', name='check_balance_due_positive'),
    )

    @property
    def is_overdue(self):
        """Check if invoice is overdue"""
        overdue_status = InvoiceStatus.query.filter_by(code='overdue').first()
        return (self.status_id == overdue_status.id if overdue_status else False) or (
            self.due_date and 
            datetime.utcnow() > self.due_date and 
            self.balance_due > 0
        )

    @property
    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue and self.due_date:
            return (datetime.utcnow() - self.due_date).days
        return 0

    @property
    def payment_progress(self):
        """Calculate payment progress percentage"""
        if self.total_amount > 0:
            return (float(self.amount_paid) / float(self.total_amount)) * 100
        return 0

    def _to_dict_impl(self):
        return {
            'invoice_number': self.invoice_number,
            'invoice_date': self.invoice_date.isoformat() if self.invoice_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status.to_dict() if self.status else None,
            'currency': self.currency.to_dict() if self.currency else None,
            'subtotal': float(self.subtotal) if self.subtotal else None,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'discount_amount': float(self.discount_amount) if self.discount_amount else None,
            'total_amount': float(self.total_amount) if self.total_amount else None,
            'amount_paid': float(self.amount_paid) if self.amount_paid else None,
            'balance_due': float(self.balance_due) if self.balance_due else None,
            'is_overdue': self.is_overdue,
            'days_overdue': self.days_overdue,
            'payment_progress': round(self.payment_progress, 2),
            'items': self.items or [],
            'patient_name': self.patient.full_name if self.patient else None,
            'treatment_description': self.treatment.name if self.treatment else None
        }

    def calculate_totals(self):
        """Calculate invoice totals from line items"""
        self.subtotal = sum(item.get('total', 0) for item in (self.items or []))
        
        # Apply discount
        if self.discount_percentage > 0:
            self.discount_amount = (self.subtotal * self.discount_percentage) / 100
        else:
            self.discount_amount = 0.0
        
        # Calculate taxable amount and tax
        taxable_amount = self.subtotal - self.discount_amount
        if self.is_taxable:
            self.tax_amount = (taxable_amount * self.tax_rate) / 100
        else:
            self.tax_amount = 0.0
        
        self.total_amount = taxable_amount + self.tax_amount
        self.balance_due = max(0, self.total_amount - self.amount_paid)

    def add_line_item(self, description, quantity, unit_price, procedure_code=None, tax_rate=0.0):
        """Add line item to invoice"""
        if not self.items:
            self.items = []
        
        total = quantity * unit_price
        line_item = {
            'description': description,
            'quantity': quantity,
            'unit_price': float(unit_price),
            'total': float(total),
            'procedure_code': procedure_code,
            'tax_rate': tax_rate
        }
        
        self.items.append(line_item)
        self.calculate_totals()
        return line_item

    def apply_payment(self, amount, payment_method_id, reference_number=None, notes=None):
        """Apply payment to invoice"""
        if amount <= 0 or amount > self.balance_due:
            return False
        
        self.amount_paid += amount
        self.balance_due = max(0, self.total_amount - self.amount_paid)
        
        # Update status
        completed_status = PaymentStatus.query.filter_by(code='completed').first()
        paid_status = InvoiceStatus.query.filter_by(code='paid').first()
        partial_status = InvoiceStatus.query.filter_by(code='partial').first()
        
        if self.balance_due == 0 and paid_status:
            self.status_id = paid_status.id
        elif self.amount_paid > 0 and partial_status:
            self.status_id = partial_status.id
        
        # Create payment record
        payment = Payment(
            invoice_id=self.id,
            patient_id=self.patient_id,
            amount=amount,
            payment_method_id=payment_method_id,
            reference_number=reference_number,
            notes=notes,
            status_id=completed_status.id if completed_status else None
        )
        
        self.payments.append(payment)
        return payment

    def mark_as_sent(self):
        """Mark invoice as sent to patient"""
        sent_status = InvoiceStatus.query.filter_by(code='sent').first()
        if sent_status:
            self.status_id = sent_status.id
            self.sent_date = datetime.utcnow()

    def mark_as_viewed(self):
        """Mark invoice as viewed by patient"""
        viewed_status = InvoiceStatus.query.filter_by(code='viewed').first()
        if viewed_status:
            self.status_id = viewed_status.id
            self.viewed_date = datetime.utcnow()

    def add_insurance_estimate(self, insurance_plan_id, estimated_amount, is_primary=True):
        """Add insurance coverage estimate"""
        if is_primary:
            self.primary_insurance_id = insurance_plan_id
        else:
            self.secondary_insurance_id = insurance_plan_id
        
        self.insurance_estimated = estimated_amount
        # Adjust patient responsibility
        self.calculate_totals()

    @classmethod
    def get_overdue_invoices(cls, organization_id, days_threshold=30):
        """Get overdue invoices for organization"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_threshold)
        
        sent_status = InvoiceStatus.query.filter_by(code='sent').first()
        viewed_status = InvoiceStatus.query.filter_by(code='viewed').first()
        partial_status = InvoiceStatus.query.filter_by(code='partial').first()
        overdue_status = InvoiceStatus.query.filter_by(code='overdue').first()
        
        status_ids = []
        if sent_status:
            status_ids.append(sent_status.id)
        if viewed_status:
            status_ids.append(viewed_status.id)
        if partial_status:
            status_ids.append(partial_status.id)
        if overdue_status:
            status_ids.append(overdue_status.id)
        
        return cls.query.filter(
            cls.organization_id == organization_id,
            cls.status_id.in_(status_ids),
            cls.balance_due > 0,
            cls.due_date < datetime.utcnow()
        ).all()

    @classmethod
    def generate_invoice_number(cls, organization_id):
        """Generate unique invoice number"""
        year = datetime.utcnow().year
        prefix = f"INV-{year}-"
        
        # Get last invoice number for this year
        last_invoice = cls.query.filter(
            cls.organization_id == organization_id,
            cls.invoice_number.like(f"{prefix}%")
        ).order_by(cls.invoice_number.desc()).first()
        
        if last_invoice:
            last_number = int(last_invoice.invoice_number.replace(prefix, ""))
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f"{prefix}{new_number:05d}"

class Payment(BaseModel):
    __tablename__ = 'payments'
    
    # Foreign keys
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    
    # Lookup foreign keys
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('payment_statuses.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'), nullable=False)
    
    # Payment details
    amount = db.Column(Numeric(10, 2), nullable=False)
    exchange_rate = db.Column(Numeric(8, 4), default=1.0)
    
    # Status and tracking
    payment_date = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_date = db.Column(DateTime)
    
    # Reference information
    reference_number = db.Column(db.String(100), unique=True, index=True)
    transaction_id = db.Column(db.String(100))
    check_number = db.Column(db.String(50))
    
    # Financial details
    fee_amount = db.Column(Numeric(10, 2), default=0.0)
    net_amount = db.Column(Numeric(10, 2))
    
    # Notes and metadata
    notes = db.Column(db.Text)
    payment_metadata = db.Column(db.JSON)
    
    # Relationships
    invoice = relationship('Invoice', back_populates='payments')
    patient = relationship('Patient', back_populates='payments')
    payment_record = relationship('PaymentRecord', back_populates='payment', uselist=False)
    payment_method = relationship('PaymentMethod')
    status = relationship('PaymentStatus')
    currency = relationship('Currency')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_payment_patient_date', 'patient_id', 'payment_date'),
        db.Index('idx_payment_invoice', 'invoice_id'),
        db.Index('idx_payment_status', 'status_id'),
        db.Index('idx_payment_method', 'payment_method_id'),
        db.Index('idx_payment_reference', 'reference_number'),
        CheckConstraint('amount > 0', name='check_payment_amount_positive'),
    )

    def _to_dict_impl(self):
        return {
            'amount': float(self.amount) if self.amount else None,
            'payment_method': self.payment_method.to_dict() if self.payment_method else None,
            'currency': self.currency.to_dict() if self.currency else None,
            'status': self.status.to_dict() if self.status else None,
            'payment_date': self.payment_date.isoformat() if self.payment_date else None,
            'payment_metadata': self.payment_metadata or {},  
            'reference_number': self.reference_number,
            'transaction_id': self.transaction_id,
            'fee_amount': float(self.fee_amount) if self.fee_amount else None,
            'net_amount': float(self.net_amount) if self.net_amount else None,
            'invoice_number': self.invoice.invoice_number if self.invoice else None,
            'patient_name': self.patient.full_name if self.patient else None
        }

    def process_payment(self, transaction_id=None, fee_amount=0.0):
        """Process the payment"""
        completed_status = PaymentStatus.query.filter_by(code='completed').first()
        if completed_status:
            self.status_id = completed_status.id
        self.processed_date = datetime.utcnow()
        self.transaction_id = transaction_id
        self.fee_amount = fee_amount
        self.net_amount = self.amount - fee_amount

    def mark_as_failed(self, error_message=None):
        """Mark payment as failed"""
        failed_status = PaymentStatus.query.filter_by(code='failed').first()
        if failed_status:
            self.status_id = failed_status.id
        if error_message:
            self.notes = f"Payment failed: {error_message}"

    def refund(self, refund_amount, reason=None):
        """Process refund for payment"""
        if refund_amount > self.amount:
            return False
        
        # Create refund record
        refund = Payment(
            patient_id=self.patient_id,
            invoice_id=self.invoice_id,
            amount=-refund_amount,  # Negative amount for refund
            payment_method_id=self.payment_method_id,
            status_id=PaymentStatus.query.filter_by(code='refunded').first().id,
            notes=f"Refund for payment {self.reference_number}: {reason}"
        )
        
        # Update original payment status if fully refunded
        refunded_status = PaymentStatus.query.filter_by(code='refunded').first()
        partially_refunded_status = PaymentStatus.query.filter_by(code='partially_refunded').first()
        
        if refund_amount == self.amount and refunded_status:
            self.status_id = refunded_status.id
        elif partially_refunded_status:
            self.status_id = partially_refunded_status.id
        
        return refund

    def generate_receipt(self):
        """Generate payment receipt data"""
        return {
            'receipt_number': self.reference_number,
            'payment_date': self.payment_date.isoformat(),
            'patient_name': self.patient.full_name if self.patient else 'N/A',
            'amount': float(self.amount),
            'payment_method': self.payment_method.name if self.payment_method else 'N/A',
            'invoice_number': self.invoice.invoice_number if self.invoice else 'N/A',
            'treatment_description': self.invoice.treatment.name if self.invoice and self.invoice.treatment else 'N/A'
        }

class PaymentRecord(BaseModel):
    __tablename__ = 'payment_records'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    
    # Payment details
    amount = db.Column(Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(10), default='USD')
    payment_method = db.Column(db.String(50))
    
    # Status and tracking
    status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(100), unique=True, index=True)
    
    # Gateway information
    gateway_response = db.Column(db.JSON)
    gateway_fees = db.Column(Numeric(10, 2), default=0.0)
    
    # Relationships
    organization = relationship('Organization', back_populates='payment_records')
    payment = relationship('Payment', back_populates='payment_record')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_payment_record_org', 'organization_id', 'created_at'),
        db.Index('idx_payment_record_status', 'status'),
        db.Index('idx_payment_record_transaction', 'transaction_id'),
    )

    def _to_dict_impl(self):
        return {
            'amount': float(self.amount) if self.amount else None,
            'currency': self.currency,
            'payment_method': self.payment_method,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'gateway_fees': float(self.gateway_fees) if self.gateway_fees else None,
            'payment_reference': self.payment.reference_number if self.payment else None
        }

class InsurancePlan(BaseModel):
    __tablename__ = 'insurance_plans'
    
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=True)
    family_member_id = db.Column(db.Integer, db.ForeignKey('family_members.id'), nullable=True)
    
    # Insurance provider information
    insurance_provider = db.Column(db.String(200), nullable=False, index=True)
    plan_name = db.Column(db.String(200), nullable=False)
    policy_number = db.Column(db.String(100), nullable=False, index=True)
    group_number = db.Column(db.String(100))
    
    # Subscriber information
    subscriber_name = db.Column(db.String(200))
    subscriber_dob = db.Column(db.Date)
    subscriber_relationship = db.Column(db.String(50))
    
    # Coverage details
    coverage_type = db.Column(db.String(100), nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date)
    is_primary = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Verification status
    verification_status = db.Column(db.String(50), default='pending')
    last_verified = db.Column(DateTime)
    verification_notes = db.Column(db.Text)
    
    # Benefits and coverage
    benefits = db.Column(db.JSON, default=dict)
    copay_info = db.Column(db.JSON, default=dict)
    deductible_info = db.Column(db.JSON, default=dict)
    annual_maximum = db.Column(Numeric(10, 2))
    annual_used = db.Column(Numeric(10, 2), default=0.0)
    
    # Contact information
    provider_phone = db.Column(db.String(20))
    provider_address = db.Column(db.Text)
    claims_address = db.Column(db.Text)
    
    # Notes
    notes = db.Column(db.Text)
    
    # Relationships
    insurance_creator = db.relationship('User', foreign_keys=[created_by], back_populates='user_created_insurance_plans')
    family_member = db.relationship('FamilyMember', foreign_keys=[family_member_id], back_populates='insurance_plans')
    organization = relationship('Organization', back_populates='insurance_plans')
    patient = relationship('Patient', back_populates='insurance_plans')
    claims = relationship('InsuranceClaim', back_populates='insurance_plan')
    invoices = db.relationship(
        'Invoice', 
        foreign_keys='Invoice.primary_insurance_id',
        back_populates='primary_insurance',
        overlaps="primary_insurance"
    )
    secondary_invoices = db.relationship(
        'Invoice', 
        foreign_keys='Invoice.secondary_insurance_id',
        back_populates='secondary_insurance',
        overlaps="secondary_insurance"
    )    
    
    # Indexes
    __table_args__ = (
        db.Index('idx_insurance_plan_org_provider', 'organization_id', 'insurance_provider'),
        db.Index('idx_insurance_plan_patient', 'patient_id'),
        db.Index('idx_insurance_plan_policy', 'policy_number'),
        db.Index('idx_insurance_plan_status', 'verification_status'),
    )

    def _to_dict_impl(self):
        return {
            'insurance_provider': self.insurance_provider,
            'plan_name': self.plan_name,
            'policy_number': self.policy_number,
            'group_number': self.group_number,
            'subscriber_name': self.subscriber_name,
            'coverage_type': self.coverage_type,
            'effective_date': self.effective_date.isoformat() if self.effective_date else None,
            'expiration_date': self.expiration_date.isoformat() if self.expiration_date else None,
            'is_primary': self.is_primary,
            'is_active': self.is_active,
            'verification_status': self.verification_status,
            'annual_maximum': float(self.annual_maximum) if self.annual_maximum else None,
            'annual_used': float(self.annual_used) if self.annual_used else None,
            'annual_remaining': float(self.annual_remaining) if self.annual_remaining else None,
            'benefits': self.benefits or {},
            'copay_info': self.copay_info or {},
            'deductible_info': self.deductible_info or {}
        }

    @property
    def is_expired(self):
        """Check if insurance plan is expired"""
        return self.expiration_date and self.expiration_date < date.today()

    @property
    def annual_remaining(self):
        """Calculate remaining annual benefit"""
        if self.annual_maximum:
            return max(0, float(self.annual_maximum) - float(self.annual_used))
        return None

    def verify_coverage(self, procedure_code, date_of_service=None):
        """Verify coverage for a specific procedure"""
        if not self.is_active or self.is_expired:
            return {'covered': False, 'reason': 'Plan not active or expired'}
        
        if date_of_service and self.effective_date and date_of_service < self.effective_date:
            return {'covered': False, 'reason': 'Service date before effective date'}
        
        if date_of_service and self.expiration_date and date_of_service > self.expiration_date:
            return {'covered': False, 'reason': 'Service date after expiration date'}
        
        # Check procedure coverage based on benefits
        procedure_type = self._get_procedure_type(procedure_code)
        coverage = self.benefits.get(procedure_type, {})
        
        if not coverage.get('covered', False):
            return {'covered': False, 'reason': f'Procedure type {procedure_type} not covered'}
        
        # Check annual maximum
        if self.annual_remaining == 0:
            return {'covered': False, 'reason': 'Annual maximum exceeded'}
        
        return {
            'covered': True,
            'copay': coverage.get('copay', 0),
            'coverage_percentage': coverage.get('coverage_percentage', 100),
            'deductible_applies': coverage.get('deductible_applies', False),
            'annual_remaining': self.annual_remaining
        }

    def _get_procedure_type(self, procedure_code):
        """Map procedure code to coverage type"""
        preventive_codes = ['D0']
        basic_codes = ['D2']
        major_codes = ['D3']
        
        if any(procedure_code.startswith(prefix) for prefix in preventive_codes):
            return 'preventive'
        elif any(procedure_code.startswith(prefix) for prefix in basic_codes):
            return 'basic'
        elif any(procedure_code.startswith(prefix) for prefix in major_codes):
            return 'major'
        else:
            return 'other'

    def update_annual_usage(self, amount):
        """Update annual usage amount"""
        if self.annual_maximum:
            self.annual_used = min(self.annual_maximum, self.annual_used + amount)

class InsuranceClaim(BaseModel):
    __tablename__ = 'insurance_claims'
    
    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    insurance_plan_id = db.Column(db.Integer, db.ForeignKey('insurance_plans.id'), nullable=False)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=True)
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatments.id'), nullable=True)
    
    # Lookup foreign key
    status_id = db.Column(db.Integer, db.ForeignKey('claim_statuses.id'), nullable=False)
    
    # Claim identification
    claim_number = db.Column(db.String(100), unique=True, index=True)
    insurance_provider = db.Column(db.String(100), nullable=False)
    policy_number = db.Column(db.String(100), nullable=False)
    
    # Claim details
    claim_amount = db.Column(Numeric(10, 2), nullable=False)
    approved_amount = db.Column(Numeric(10, 2))
    patient_responsibility = db.Column(Numeric(10, 2))
    
    # Status and tracking
    submission_date = db.Column(DateTime)
    processing_date = db.Column(DateTime)
    resolution_date = db.Column(DateTime)
    
    # Procedure information
    procedures = db.Column(db.JSON, nullable=False)
    diagnosis_codes = db.Column(db.JSON)
    
    # Provider information
    rendering_provider_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    facility_info = db.Column(db.JSON)
    
    # Response information
    denial_reason = db.Column(db.Text)
    adjustment_codes = db.Column(db.JSON)
    payer_notes = db.Column(db.Text)
    
    # Dates of service
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Relationships
    patient = relationship('Patient', back_populates='insurance_claims')
    insurance_plan = relationship('InsurancePlan', back_populates='claims')
    invoice = relationship('Invoice', back_populates='claims')
    treatment = relationship('Treatment')
    rendering_provider = relationship('User')
    status = relationship('ClaimStatus')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_insurance_claim_patient', 'patient_id', 'submission_date'),
        db.Index('idx_insurance_claim_status', 'status_id'),
        db.Index('idx_insurance_claim_number', 'claim_number'),
        db.Index('idx_insurance_claim_provider', 'insurance_provider'),
    )

    def _to_dict_impl(self):
        return {
            'claim_number': self.claim_number,
            'insurance_provider': self.insurance_provider,
            'policy_number': self.policy_number,
            'claim_amount': float(self.claim_amount) if self.claim_amount else None,
            'approved_amount': float(self.approved_amount) if self.approved_amount else None,
            'patient_responsibility': float(self.patient_responsibility) if self.patient_responsibility else None,
            'status': self.status.to_dict() if self.status else None,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'resolution_date': self.resolution_date.isoformat() if self.resolution_date else None,
            'procedures': self.procedures or [],
            'diagnosis_codes': self.diagnosis_codes or [],
            'denial_reason': self.denial_reason,
            'patient_name': self.patient.full_name if self.patient else None
        }

    def submit_claim(self):
        """Submit claim to insurance"""
        submitted_status = ClaimStatus.query.filter_by(code='submitted').first()
        if submitted_status:
            self.status_id = submitted_status.id
            self.submission_date = datetime.utcnow()
            self.claim_number = self.generate_claim_number()

    def process_response(self, approved_amount, denial_reason=None, adjustment_codes=None):
        """Process insurance response"""
        self.approved_amount = approved_amount
        self.patient_responsibility = float(self.claim_amount) - (float(approved_amount) if approved_amount else 0)
        
        approved_status = ClaimStatus.query.filter_by(code='approved').first()
        denied_status = ClaimStatus.query.filter_by(code='denied').first()
        partially_approved_status = ClaimStatus.query.filter_by(code='partially_approved').first()
        
        if approved_amount == 0 and denial_reason and denied_status:
            self.status_id = denied_status.id
            self.denial_reason = denial_reason
        elif approved_amount < self.claim_amount and partially_approved_status:
            self.status_id = partially_approved_status.id
        elif approved_status:
            self.status_id = approved_status.id
        
        self.adjustment_codes = adjustment_codes
        self.resolution_date = datetime.utcnow()
        
        # Update insurance plan annual usage
        if self.approved_amount and self.insurance_plan:
            self.insurance_plan.update_annual_usage(self.approved_amount)

    def generate_claim_number(self):
        """Generate unique claim number"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"CLM-{timestamp}-{self.patient_id}"

    def calculate_patient_responsibility(self):
        """Calculate patient responsibility after insurance"""
        if self.approved_amount is not None:
            return max(0, float(self.claim_amount) - float(self.approved_amount))
        return float(self.claim_amount)

class Expense(BaseModel):
    __tablename__ = 'expenses'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    
    # Lookup foreign keys
    category_id = db.Column(db.Integer, db.ForeignKey('expense_categories.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=True)
    
    # Expense details
    amount = db.Column(Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False, default=date.today)
    
    # Vendor information
    vendor_name = db.Column(db.String(200))
    vendor_invoice_number = db.Column(db.String(100))
    
    # Payment information
    payment_date = db.Column(db.Date)
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(50))
    
    # Tax information
    is_tax_deductible = db.Column(db.Boolean, default=True)
    tax_amount = db.Column(Numeric(10, 2), default=0.0)
    
    # Approval workflow
    status = db.Column(db.String(20), default='pending')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_date = db.Column(DateTime)
    
    # Relationships
    organization = relationship('Organization', back_populates='expenses')
    incurred_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approver = relationship('User', foreign_keys=[approved_by])
    incurring_user = relationship('User', foreign_keys=[incurred_by])
    category = relationship('ExpenseCategory')
    payment_method = relationship('PaymentMethod')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_expense_org_category', 'organization_id', 'category_id'),
        db.Index('idx_expense_date', 'expense_date'),
        db.Index('idx_expense_status', 'status'),
        db.Index('idx_expense_vendor', 'vendor_name'),
    )

    def _to_dict_impl(self):
        return {
            'amount': float(self.amount) if self.amount else None,
            'category': self.category.to_dict() if self.category else None,
            'description': self.description,
            'expense_date': self.expense_date.isoformat() if self.expense_date else None,
            'vendor_name': self.vendor_name,
            'vendor_invoice_number': self.vendor_invoice_number,
            'payment_method': self.payment_method.to_dict() if self.payment_method else None,
            'is_recurring': self.is_recurring,
            'recurrence_pattern': self.recurrence_pattern,
            'is_tax_deductible': self.is_tax_deductible,
            'tax_amount': float(self.tax_amount) if self.tax_amount else None,
            'status': self.status,
            'incurred_by_user': f"{self.incurring_user.first_name} {self.incurring_user.last_name}" if self.incurring_user else None
        }

    def approve(self, approved_by_user):
        """Approve expense"""
        self.status = 'approved'
        self.approved_by = approved_by_user.id
        self.approved_date = datetime.utcnow()

    def mark_as_paid(self, payment_method_id, payment_date=None):
        """Mark expense as paid"""
        self.status = 'paid'
        self.payment_method_id = payment_method_id
        self.payment_date = payment_date or date.today()

    @classmethod
    def get_monthly_summary(cls, organization_id, year, month):
        """Get monthly expense summary by category"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        expenses = cls.query.filter(
            cls.organization_id == organization_id,
            cls.expense_date >= start_date,
            cls.expense_date < end_date,
            cls.status == 'paid'
        ).all()
        
        summary = {}
        for expense in expenses:
            category_name = expense.category.name if expense.category else 'Unknown'
            if category_name not in summary:
                summary[category_name] = 0.0
            summary[category_name] += float(expense.amount)
        
        return summary

class FinancialReport(BaseModel):
    __tablename__ = 'financial_reports'
    
    organization_id = db.Column(db.String(50), db.ForeignKey('organizations.public_id'), nullable=False)
    
    # Report details
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50), nullable=False)
    
    # Report parameters and data
    parameters = db.Column(db.JSON)
    data = db.Column(db.JSON)
    summary = db.Column(db.JSON)
    
    # Generation info
    generated_at = db.Column(DateTime, default=datetime.utcnow)
    period_start = db.Column(DateTime)
    period_end = db.Column(DateTime)
    file_url = db.Column(db.String(255))
    
    # Access control
    is_template = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    shared_with = db.Column(db.JSON)
    
    # Audit
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    organization = db.relationship('Organization', back_populates='financial_reports')
    creator = relationship('User', foreign_keys=[created_by])
    
    # Indexes
    __table_args__ = (
        db.Index('idx_financial_report_org_type', 'organization_id', 'report_type'),
        db.Index('idx_report_period', 'period_start', 'period_end'),
        db.Index('idx_financial_idx_report_created', 'created_at'),
    )

    def _to_dict_impl(self):
        return {
            'title': self.title,
            'description': self.description,
            'report_type': self.report_type,
            'parameters': self.parameters or {},
            'summary': self.summary or {},
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'file_url': self.file_url,
            'is_template': self.is_template,
            'is_public': self.is_public,
            'created_by_user': f"{self.creator.first_name} {self.creator.last_name}" if self.creator else None
        }

    @classmethod
    def generate_financial_report(cls, organization_id, start_date, end_date, report_type='revenue'):
        """Generate financial report for period"""
        # This would contain complex query logic for financial reporting
        # Placeholder implementation
        report_data = {
            'total_revenue': 0.0,
            'total_expenses': 0.0,
            'net_income': 0.0,
            'invoice_counts': {'draft': 0, 'sent': 0, 'paid': 0, 'overdue': 0},
            'category_breakdown': {}
        }
        
        return report_data

    def share_with_users(self, user_ids):
        """Share report with specific users"""
        if not self.shared_with:
            self.shared_with = []
        
        for user_id in user_ids:
            if user_id not in self.shared_with:
                self.shared_with.append(user_id)

    def can_access(self, user):
        """Check if user can access this report"""
        if self.is_public:
            return True
        if user.id == self.created_by:
            return True
        if self.shared_with and user.id in self.shared_with:
            return True
        return False