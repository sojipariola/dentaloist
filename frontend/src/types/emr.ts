// src/types/emr.ts
export interface MedicalRecord {
  id: number;
  patientId: number;
  type: RecordType;
  category: RecordCategory;
  title: string;
  content: string;
  data: Record<string, any>;
  attachments: Attachment[];
  tags: string[];
  status: RecordStatus;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  createdByUser?: User;
}

export interface ClinicalNote {
  id: number;
  patientId: number;
  appointmentId?: number;
  type: NoteType;
  template: string;
  content: Record<string, any>;
  diagnosis?: Diagnosis[];
  medications?: Medication[];
  procedures?: Procedure[];
  followUp?: FollowUp;
  signedBy: number;
  signedAt: Date;
  isLocked: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  appointment?: Appointment;
  signedByUser?: User;
}

export interface Diagnosis {
  code: string;
  description: string;
  type: DiagnosisType;
  certainty: CertaintyLevel;
  onsetDate?: Date;
  resolvedDate?: Date;
  notes?: string;
}

export interface Procedure {
  code: string;
  description: string;
  date: Date;
  performer: number;
  location: string;
  notes?: string;
  outcomes: Outcome[];
}

export interface FollowUp {
  required: boolean;
  date?: Date;
  reason?: string;
  instructions?: string;
}

export interface Outcome {
  type: OutcomeType;
  description: string;
  value?: any;
  unit?: string;
}

export enum RecordType {
  CLINICAL_NOTE = 'clinical_note',
  LAB_RESULT = 'lab_result',
  IMAGING = 'imaging',
  PRESCRIPTION = 'prescription',
  REFERRAL = 'referral',
  ALLERGY = 'allergy',
  PROBLEM = 'problem'
}

export enum RecordCategory {
  MEDICAL = 'medical',
  DENTAL = 'dental',
  SURGICAL = 'surgical',
  BEHAVIORAL = 'behavioral'
}

export enum RecordStatus {
  DRAFT = 'draft',
  FINAL = 'final',
  AMENDED = 'amended',
  CORRECTED = 'corrected'
}

export enum NoteType {
  SOAP = 'soap',
  PROGRESS = 'progress',
  CONSULTATION = 'consultation',
  DISCHARGE = 'discharge',
  OPERATIVE = 'operative'
}

export enum DiagnosisType {
  PRIMARY = 'primary',
  SECONDARY = 'secondary',
  ADMITTING = 'admitting',
  DISCHARGE = 'discharge'
}

export enum CertaintyLevel {
  SUSPECTED = 'suspected',
  PROBABLE = 'probable',
  CONFIRMED = 'confirmed'
}

export enum OutcomeType {
  MEASUREMENT = 'measurement',
  ASSESSMENT = 'assessment',
  GOAL = 'goal',
  INTERVENTION = 'intervention'
}