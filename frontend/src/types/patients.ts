// src/types/patients.ts
export interface Patient {
  id: number;
  organizationId: string;
  firstName: string;
  lastName: string;
  email?: string;
  phone?: string;
  dateOfBirth?: Date;
  gender?: Gender;
  address?: Address;
  emergencyContact?: EmergencyContact;
  medicalHistory?: MedicalHistory;
  allergies?: Allergy[];
  medications?: Medication[];
  insurance?: InsuranceInfo;
  notes?: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organization?: Organization;
  appointments?: Appointment[];
  familyMembers?: FamilyMember[];
}

export interface PatientCreate {
  firstName: string;
  lastName: string;
  email?: string;
  phone?: string;
  dateOfBirth?: Date;
  gender?: Gender;
  address?: Address;
}

export interface Address {
  street: string;
  city: string;
  state: string;
  postalCode: string;
  country: string;
}

export interface EmergencyContact {
  name: string;
  relationship: string;
  phone: string;
  email?: string;
}

export interface MedicalHistory {
  conditions: MedicalCondition[];
  surgeries: Surgery[];
  familyHistory: FamilyHistory[];
  dentalHistory: DentalHistory;
}

export interface MedicalCondition {
  condition: string;
  diagnosedDate?: Date;
  status: 'active' | 'resolved';
  notes?: string;
}

export interface Surgery {
  procedure: string;
  date: Date;
  surgeon?: string;
  notes?: string;
}

export interface FamilyHistory {
  condition: string;
  relation: string;
  notes?: string;
}

export interface DentalHistory {
  lastDentalVisit?: Date;
  brushingFrequency: string;
  flossingFrequency: string;
  concerns: string[];
}

export interface Allergy {
  allergen: string;
  severity: 'mild' | 'moderate' | 'severe';
  reaction: string;
  notes?: string;
}

export interface Medication {
  name: string;
  dosage: string;
  frequency: string;
  startDate: Date;
  endDate?: Date;
  prescribedBy?: string;
  notes?: string;
}

export interface InsuranceInfo {
  provider: string;
  policyNumber: string;
  groupNumber?: string;
  effectiveDate: Date;
  expirationDate: Date;
  verificationStatus: 'verified' | 'pending' | 'rejected';
}

export enum Gender {
  MALE = 'male',
  FEMALE = 'female',
  OTHER = 'other',
  PREFER_NOT_TO_SAY = 'prefer_not_to_say'
}