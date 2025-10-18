// src/types/billing.ts
export interface Invoice {
  id: number;
  patientId: number;
  appointmentId?: number;
  invoiceNumber: string;
  issueDate: Date;
  dueDate: Date;
  status: InvoiceStatus;
  items: InvoiceItem[];
  subtotal: number;
  tax: number;
  discount: number;
  total: number;
  paidAmount: number;
  balance: number;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  appointment?: Appointment;
  payments?: Payment[];
}

export interface InvoiceItem {
  description: string;
  quantity: number;
  unitPrice: number;
  amount: number;
  taxRate: number;
  category: BillingCategory;
}

export interface Payment {
  id: number;
  invoiceId: number;
  amount: number;
  paymentMethod: PaymentMethod;
  transactionId?: string;
  status: PaymentStatus;
  processedAt: Date;
  notes?: string;
  createdAt: Date;
  
  // Relations
  invoice?: Invoice;
}

export interface InsuranceClaim {
  id: number;
  patientId: number;
  appointmentId: number;
  insuranceProvider: string;
  policyNumber: string;
  submittedAmount: number;
  approvedAmount?: number;
  status: ClaimStatus;
  submissionDate: Date;
  responseDate?: Date;
  denialReason?: string;
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
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
  CHECK = 'check',
  BANK_TRANSFER = 'bank_transfer',
  INSURANCE = 'insurance'
}

export enum PaymentStatus {
  PENDING = 'pending',
  COMPLETED = 'completed',
  FAILED = 'failed',
  REFUNDED = 'refunded'
}

export enum ClaimStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  PROCESSING = 'processing',
  APPROVED = 'approved',
  PARTIAL = 'partial',
  DENIED = 'denied',
  PAID = 'paid'
}

export enum BillingCategory {
  CONSULTATION = 'consultation',
  PROCEDURE = 'procedure',
  LABORATORY = 'laboratory',
  MEDICATION = 'medication',
  EQUIPMENT = 'equipment',
  OTHER = 'other'
}