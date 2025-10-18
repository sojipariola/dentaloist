// src/types/data-export.ts
export interface DataExport {
  id: number;
  name: string;
  type: ExportType;
  format: ExportFormat;
  scope: ExportScope;
  filters: ExportFilters;
  status: ExportStatus;
  progress: number;
  fileUrl?: string;
  fileSize?: number;
  generatedBy: number;
  generatedAt?: Date;
  expiresAt?: Date;
  error?: string;
  createdAt: Date;
  
  // Relations
  generatedByUser?: User;
}

export interface ExportFilters {
  dateRange?: DateRange;
  entities: string[];
  fields: string[];
  conditions: FilterCondition[];
}

export interface FilterCondition {
  field: string;
  operator: FilterOperator;
  value: any;
}

export interface ExportTemplate {
  id: number;
  name: string;
  type: ExportType;
  format: ExportFormat;
  scope: ExportScope;
  filters: ExportFilters;
  schedule?: ExportSchedule;
  isActive: boolean;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface ExportSchedule {
  frequency: ScheduleFrequency;
  time: string;
  dayOfWeek?: number;
  dayOfMonth?: number;
  timezone: string;
  nextRun: Date;
}

export enum ExportType {
  PATIENTS = 'patients',
  APPOINTMENTS = 'appointments',
  BILLING = 'billing',
  MEDICAL_RECORDS = 'medical_records',
  INVENTORY = 'inventory',
  ANALYTICS = 'analytics'
}

export enum ExportFormat {
  CSV = 'csv',
  EXCEL = 'excel',
  JSON = 'json',
  XML = 'xml',
  PDF = 'pdf'
}

export enum ExportScope {
  ALL = 'all',
  SELECTED = 'selected',
  FILTERED = 'filtered'
}

export enum ExportStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

export enum FilterOperator {
  EQUALS = 'equals',
  NOT_EQUALS = 'not_equals',
  CONTAINS = 'contains',
  STARTS_WITH = 'starts_with',
  ENDS_WITH = 'ends_with',
  GREATER_THAN = 'greater_than',
  LESS_THAN = 'less_than',
  BETWEEN = 'between',
  IN = 'in',
  NOT_IN = 'not_in'
}

export enum ScheduleFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly',
  YEARLY = 'yearly'
}