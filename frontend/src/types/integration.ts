// src/types/integration.ts
export interface Integration {
  id: number;
  name: string;
  type: IntegrationType;
  category: IntegrationCategory;
  status: IntegrationStatus;
  config: IntegrationConfig;
  credentials: IntegrationCredentials;
  capabilities: IntegrationCapability[];
  health: IntegrationHealth;
  lastSync?: Date;
  syncStatus: SyncStatus;
  error?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface IntegrationConfig {
  enabled: boolean;
  autoSync: boolean;
  syncInterval: number;
  timeout: number;
  retryAttempts: number;
  retryDelay: number;
}

export interface IntegrationCredentials {
  apiKey?: string;
  secret?: string;
  token?: string;
  username?: string;
  password?: string;
  endpoint?: string;
  customFields?: Record<string, string>;
}

export interface IntegrationCapability {
  name: string;
  enabled: boolean;
  config: Record<string, any>;
}

export interface IntegrationHealth {
  status: HealthStatus;
  lastCheck: Date;
  responseTime: number;
  errorRate: number;
  uptime: number;
}

export interface SyncResult {
  success: boolean;
  recordsProcessed: number;
  recordsCreated: number;
  recordsUpdated: number;
  recordsFailed: number;
  errors: string[];
  duration: number;
  nextSync: Date;
}

export enum IntegrationType {
  EHR = 'ehr',
  LAB = 'lab',
  IMAGING = 'imaging',
  PHARMACY = 'pharmacy',
  BILLING = 'billing',
  SCHEDULING = 'scheduling',
  COMMUNICATION = 'communication',
  ANALYTICS = 'analytics'
}

export enum IntegrationCategory {
  CLINICAL = 'clinical',
  FINANCIAL = 'financial',
  OPERATIONAL = 'operational',
  COMMUNICATION = 'communication',
  DATA = 'data'
}

export enum IntegrationStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  CONFIGURING = 'configuring',
  ERROR = 'error',
  MAINTENANCE = 'maintenance'
}

export enum SyncStatus {
  IDLE = 'idle',
  SYNCING = 'syncing',
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning'
}

export enum HealthStatus {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
  UNKNOWN = 'unknown'
}