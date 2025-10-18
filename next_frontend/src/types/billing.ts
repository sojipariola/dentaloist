// next_frontend/src/types/billing.ts

export interface Invoice {
  id: number;
  patientId: number;
  amount: number;
  status: 'paid' | 'unpaid' | 'pending';
  dueDate: string; // ISO date string
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface Payment {
  id: number;
  invoiceId: number;
  amount: number;
  paymentDate: string; // ISO date string
  method: 'credit_card' | 'cash' | 'insurance' | 'other';
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export interface BillingSummary {
  totalInvoices: number;
  totalPaid: number;
  totalUnpaid: number;
  totalPending: number;
}

// Add other billing-related types as needed