// src/types/audit-log.ts
export interface AuditLog {
  id: number;
  action: AuditAction;
  resourceType: ResourceType;
  resourceId?: number;
  userId: number;
  userIp: string;
  userAgent: string;
  details: AuditDetails;
  timestamp: Date;
  
  // Relations
  user?: User;
}

export interface AuditDetails {
  before?: any;
  after?: any;
  changes?: string[];
  metadata?: Record<string, any>;
}

export interface AuditFilter {
  action?: AuditAction[];
  resourceType?: ResourceType[];
  userId?: number;
  startDate?: Date;
  endDate?: Date;
  ipAddress?: string;
}

export interface AuditSummary {
  totalLogs: number;
  byAction: Record<AuditAction, number>;
  byResource: Record<ResourceType, number>;
  byUser: Record<number, number>;
  byHour: Record<string, number>;
}

export enum AuditAction {
  CREATE = 'create',
  READ = 'read',
  UPDATE = 'update',
  DELETE = 'delete',
  LOGIN = 'login',
  LOGOUT = 'logout',
  EXPORT = 'export',
  IMPORT = 'import',
  ACCESS = 'access',
  PERMISSION_CHANGE = 'permission_change'
}

export enum ResourceType {
  USER = 'user',
  PATIENT = 'patient',
  APPOINTMENT = 'appointment',
  ORGANIZATION = 'organization',
  BILLING = 'billing',
  MEDICAL_RECORD = 'medical_record',
  FILE = 'file',
  SETTING = 'setting'
}