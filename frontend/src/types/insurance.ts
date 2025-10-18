// src/types/insurance.ts
export interface InsurancePolicy {
  id: number;
  patientId: number;
  provider: string;
  type: InsuranceType;
  policyNumber: string;
  groupNumber?: string;
  subscriberId: number;
  relationship: Relationship;
  effectiveDate: Date;
  expirationDate: Date;
  verificationStatus: VerificationStatus;
  benefits: Benefits;
  copayments: Copayments;
  deductibles: Deductibles;
  limitations: Limitation[];
  notes?: string;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  subscriber?: Patient;
  claims?: InsuranceClaim[];
}

export interface Benefits {
  medical: Coverage;
  dental: Coverage;
  vision: Coverage;
  prescription: Coverage;
}

export interface Coverage {
  inNetwork: NetworkCoverage;
  outOfNetwork: NetworkCoverage;
  limitations: string[];
}

export interface NetworkCoverage {
  percentage: number;
  annualMaximum?: number;
  lifetimeMaximum?: number;
}

export interface Copayments {
  officeVisit: number;
  specialist: number;
  emergency: number;
  prescription: number;
}

export interface Deductibles {
  individual: number;
  family: number;
  met: number;
}

export interface Limitation {
  type: string;
  description: string;
  appliesTo: string[];
}

export enum InsuranceType {
  COMMERCIAL = 'commercial',
  MEDICARE = 'medicare',
  MEDICAID = 'medicaid',
  TRICARE = 'tricare',
  VA = 'va',
  OTHER = 'other'
}

export enum Relationship {
  SELF = 'self',
  SPOUSE = 'spouse',
  CHILD = 'child',
  OTHER = 'other'
}

export enum VerificationStatus {
  PENDING = 'pending',
  VERIFIED = 'verified',
  EXPIRED = 'expired',
  TERMINATED = 'terminated'
}