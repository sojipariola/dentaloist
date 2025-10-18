// src/types/files.ts
export interface FileRecord {
  id: number;
  name: string;
  type: FileType;
  size: number;
  mimeType: string;
  path: string;
  category: FileCategory;
  tags: string[];
  description?: string;
  uploadedBy: number;
  patientId?: number;
  appointmentId?: number;
  isEncrypted: boolean;
  encryptionKey?: string;
  accessControl: AccessControl[];
  version: number;
  previousVersionId?: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  uploadedByUser?: User;
  patient?: Patient;
  appointment?: Appointment;
}

export interface AccessControl {
  userId: number;
  permission: FilePermission;
  grantedAt: Date;
  grantedBy: number;
}

export interface FileUpload {
  file: File;
  category: FileCategory;
  patientId?: number;
  appointmentId?: number;
  tags?: string[];
  description?: string;
  encrypt?: boolean;
}

export enum FileType {
  DOCUMENT = 'document',
  IMAGE = 'image',
  VIDEO = 'video',
  AUDIO = 'audio',
  ARCHIVE = 'archive',
  OTHER = 'other'
}

export enum FileCategory {
  MEDICAL_RECORD = 'medical_record',
  CONSENT_FORM = 'consent_form',
  INSURANCE = 'insurance',
  BILLING = 'billing',
  LAB_RESULT = 'lab_result',
  XRAY = 'xray',
  PHOTO = 'photo',
  PRESCRIPTION = 'prescription',
  REPORT = 'report'
}

export enum FilePermission {
  VIEW = 'view',
  DOWNLOAD = 'download',
  EDIT = 'edit',
  DELETE = 'delete',
  SHARE = 'share'
}