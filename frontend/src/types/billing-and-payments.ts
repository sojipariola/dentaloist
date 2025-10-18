// src/types/billing-and-payments.ts
export interface Invoice {
  id: number;
  number: string;
  patientId: number;
  status: InvoiceStatus;
  issueDate: Date;
  dueDate: Date;
  items: InvoiceItem[];
  subtotal: number;
  tax: number;
  discount: number;
  total: number;
  paidAmount: number;
  balance: number;
  notes?: string;
  terms: string;
  payments: Payment[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
}

export interface Payment {
  id: number;
  invoiceId: number;
  amount: number;
  method: PaymentMethod;
  status: PaymentStatus;
  processor: PaymentProcessor;
  transactionId?: string;
  receiptUrl?: string;
  processedAt: Date;
  refundedAmount: number;
  refunds: Refund[];
  createdAt: Date;
  
  // Relations
  invoice?: Invoice;
}

export interface Refund {
  id: number;
  paymentId: number;
  amount: number;
  reason: string;
  status: RefundStatus;
  processedAt: Date;
  createdAt: Date;
  
  // Relations
  payment?: Payment;
}

export interface Subscription {
  id: number;
  patientId: number;
  plan: SubscriptionPlan;
  status: SubscriptionStatus;
  currentPeriod: DateRange;
  nextPayment: Date;
  amount: number;
  interval: SubscriptionInterval;
  trialEnd?: Date;
  cancelAt?: Date;
  paymentMethod: PaymentMethod;
  invoices: Invoice[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
}

export interface BillingSettings {
  currency: string;
  tax: TaxSettings;
  invoice: InvoiceSettings;
  payment: PaymentSettings;
  subscription: SubscriptionSettings;
}

export interface TaxSettings {
  enabled: boolean;
  rate: number;
  inclusive: boolean;
  rules: TaxRule[];
}

export interface InvoiceSettings {
  prefix: string;
  nextNumber: number;
  terms: string;
  notes: string;
  dueDays: number;
}

export interface PaymentSettings {
  methods: PaymentMethod[];
  processors: PaymentProcessor[];
  autoCharge: boolean;
  lateFee: number;
}

export interface SubscriptionSettings {
  plans: SubscriptionPlan[];
  trialDays: number;
  gracePeriod: number;
  proration: boolean;
}

export enum InvoiceStatus {
  DRAFT = 'draft',
  SENT = 'sent',
  PARTIAL = 'partial',
  PAID = 'paid',
  OVERDUE = 'overdue',
  VOID = 'void'
}

export enum PaymentMethod {
  CASH = 'cash',
  CREDIT_CARD = 'credit_card',
  DEBIT_CARD = 'debit_card',
  BANK_TRANSFER = 'bank_transfer',
  CHECK = 'check',
  DIGITAL_WALLET = 'digital_wallet'
}

export enum PaymentStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  REFUNDED = 'refunded'
}

export enum PaymentProcessor {
  STRIPE = 'stripe',
  PAYPAL = 'paypal',
  SQUARE = 'square',
  AUTHORIZE_NET = 'authorize_net'
}

export enum RefundStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum SubscriptionStatus {
  ACTIVE = 'active',
  PAST_DUE = 'past_due',
  CANCELLED = 'cancelled',
  EXPIRED = 'expired',
  TRIALING = 'trialing'
}

export enum SubscriptionInterval {
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly',
  ANNUALLY = 'annually'
}