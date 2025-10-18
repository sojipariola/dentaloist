// src/types/e-prescribing.ts
export interface Prescription {
  id: number;
  patientId: number;
  prescriberId: number;
  medication: MedicationInfo;
  dosage: Dosage;
  duration: Duration;
  refills: RefillInfo;
  instructions: string;
  status: PrescriptionStatus;
  pharmacy?: PharmacyInfo;
  sentAt?: Date;
  filledAt?: Date;
  pickedUpAt?: Date;
  adverseEvents: AdverseEvent[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  prescriber?: User;
}

export interface MedicationInfo {
  name: string;
  ndc: string;
  generic: boolean;
  form: MedicationForm;
  strength: string;
  manufacturer?: string;
}

export interface Dosage {
  amount: number;
  unit: string;
  frequency: string;
  route: AdministrationRoute;
  timing: string[];
}

export interface Duration {
  start: Date;
  end: Date;
  asNeeded: boolean;
}

export interface RefillInfo {
  allowed: boolean;
  quantity: number;
  interval: number;
  expires: Date;
}

export interface PharmacyInfo {
  name: string;
  address: Address;
  phone: string;
  fax?: string;
  npi?: string;
}

export interface AdverseEvent {
  type: string;
  severity: EventSeverity;
  description: string;
  occurredAt: Date;
  reportedAt: Date;
  actions: string[];
}

export enum PrescriptionStatus {
  DRAFT = 'draft',
  SENT = 'sent',
  RECEIVED = 'received',
  FILLED = 'filled',
  PICKED_UP = 'picked_up',
  EXPIRED = 'expired',
  CANCELLED = 'cancelled'
}

export enum MedicationForm {
  TABLET = 'tablet',
  CAPSULE = 'capsule',
  LIQUID = 'liquid',
  INJECTION = 'injection',
  TOPICAL = 'topical',
  INHALER = 'inhaler'
}

export enum AdministrationRoute {
  ORAL = 'oral',
  TOPICAL = 'topical',
  INJECTION = 'injection',
  INHALATION = 'inhalation',
  RECTAL = 'rectal'
}

export enum EventSeverity {
  MILD = 'mild',
  MODERATE = 'moderate',
  SEVERE = 'severe',
  LIFE_THREATENING = 'life_threatening'
}