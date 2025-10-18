// src/types/reports.ts
export interface Report {
  id: number;
  title: string;
  type: ReportType;
  parameters: ReportParameters;
  format: ReportFormat;
  status: ReportStatus;
  generatedAt?: Date;
  downloadUrl?: string;
  createdBy: number;
  createdAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface ReportParameters {
  dateRange: DateRange;
  filters: ReportFilters;
  grouping?: ReportGrouping;
  metrics: string[];
}

export interface DateRange {
  start: Date;
  end: Date;
}

export interface ReportFilters {
  organizationId?: string;
  patientIds?: number[];
  providerIds?: number[];
  appointmentTypes?: AppointmentType[];
  statuses?: string[];
}

export interface ReportGrouping {
  by: 'day' | 'week' | 'month' | 'year' | 'provider' | 'service';
}

export enum ReportType {
  FINANCIAL = 'financial',
  APPOINTMENT = 'appointment',
  PATIENT = 'patient',
  INVENTORY = 'inventory',
  PERFORMANCE = 'performance',
  COMPLIANCE = 'compliance'
}

export enum ReportFormat {
  PDF = 'pdf',
  EXCEL = 'excel',
  CSV = 'csv',
  HTML = 'html'
}

export enum ReportStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}