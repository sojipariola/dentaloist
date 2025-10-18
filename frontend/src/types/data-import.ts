// src/types/data-import.ts
export interface DataImport {
  id: number;
  name: string;
  type: ImportType;
  format: ImportFormat;
  status: ImportStatus;
  progress: number;
  totalRecords: number;
  processedRecords: number;
  successfulRecords: number;
  failedRecords: number;
  fileUrl?: string;
  fileSize?: number;
  mappings: FieldMapping[];
  validationRules: ValidationRule[];
  importedBy: number;
  importedAt?: Date;
  error?: string;
  createdAt: Date;
  
  // Relations
  importedByUser?: User;
}

export interface FieldMapping {
  sourceField: string;
  targetField: string;
  transformation?: Transformation;
  defaultValue?: any;
  required: boolean;
}

export interface Transformation {
  type: TransformationType;
  parameters: any;
}

export interface ValidationRule {
  field: string;
  type: ValidationType;
  rule: any;
  message: string;
}

export interface ImportTemplate {
  id: number;
  name: string;
  type: ImportType;
  format: ImportFormat;
  mappings: FieldMapping[];
  validationRules: ValidationRule[];
  isActive: boolean;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface ImportResult {
  success: boolean;
  summary: ImportSummary;
  details: ImportDetail[];
  errors: ImportError[];
}

export interface ImportSummary {
  total: number;
  successful: number;
  failed: number;
  skipped: number;
  duration: number;
}

export interface ImportDetail {
  record: any;
  status: 'success' | 'failed' | 'skipped';
  errors?: string[];
}

export interface ImportError {
  row: number;
  field: string;
  error: string;
  value: any;
}

export enum ImportType {
  PATIENTS = 'patients',
  APPOINTMENTS = 'appointments',
  INVENTORY = 'inventory',
  USERS = 'users',
  BILLING = 'billing'
}

export enum ImportFormat {
  CSV = 'csv',
  EXCEL = 'excel',
  JSON = 'json',
  XML = 'xml'
}

export enum ImportStatus {
  PENDING = 'pending',
  VALIDATING = 'validating',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum TransformationType {
  UPPERCASE = 'uppercase',
  LOWERCASE = 'lowercase',
  TRIM = 'trim',
  DATE_FORMAT = 'date_format',
  NUMBER_FORMAT = 'number_format',
  LOOKUP = 'lookup',
  CONCAT = 'concat'
}

export enum ValidationType {
  REQUIRED = 'required',
  UNIQUE = 'unique',
  FORMAT = 'format',
  RANGE = 'range',
  LENGTH = 'length',
  PATTERN = 'pattern'
}