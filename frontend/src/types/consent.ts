// src/types/consent.ts
export interface Consent {
  id: number;
  patientId: number;
  formId: number;
  type: ConsentType;
  version: string;
  content: string;
  data: Record<string, any>;
  status: ConsentStatus;
  signedBy: number;
  signedAt: Date;
  witnessId?: number;
  witnessName?: string;
  witnessSignature?: string;
  revokedAt?: Date;
  revokedReason?: string;
  expiresAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  form?: Form;
  signedByUser?: User;
  witness?: User;
}

export interface ConsentTemplate {
  id: number;
  name: string;
  type: ConsentType;
  category: ConsentCategory;
  content: string;
  fields: ConsentField[];
  version: string;
  isActive: boolean;
  organizationId: string;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organization?: Organization;
  createdByUser?: User;
}

export interface ConsentField {
  id: string;
  type: FieldType;
  label: string;
  required: boolean;
  description?: string;
  options?: FieldOption[];
}

export interface ConsentHistory {
  id: number;
  consentId: number;
  action: ConsentAction;
  performedBy: number;
  changes?: ConsentChanges;
  reason?: string;
  createdAt: Date;
  
  // Relations
  consent?: Consent;
  performedByUser?: User;
}

export enum ConsentType {
  TREATMENT = 'treatment',
  PRIVACY = 'privacy',
  RESEARCH = 'research',
  PHOTOGRAPHY = 'photography',
  MINOR = 'minor',
  FINANCIAL = 'financial'
}

export enum ConsentCategory {
  GENERAL = 'general',
  PROCEDURE = 'procedure',
  MEDICATION = 'medication',
  ANESTHESIA = 'anesthesia',
  EMERGENCY = 'emergency'
}

export enum ConsentStatus {
  DRAFT = 'draft',
  PENDING = 'pending',
  SIGNED = 'signed',
  EXPIRED = 'expired',
  REVOKED = 'revoked'
}

export enum ConsentAction {
  CREATE = 'create',
  UPDATE = 'update',
  SIGN = 'sign',
  REVOKE = 'revoke',
  EXPIRE = 'expire'
}