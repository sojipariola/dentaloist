// src/types/security.ts
export interface SecurityPolicy {
  id: number;
  name: string;
  type: PolicyType;
  description: string;
  rules: SecurityRule[];
  isActive: boolean;
  appliesTo: PolicyScope;
  exceptions: PolicyException[];
  createdAt: Date;
  updatedAt: Date;
}

export interface SecurityRule {
  action: RuleAction;
  conditions: RuleCondition[];
  effect: RuleEffect;
  priority: number;
}

export interface RuleCondition {
  field: string;
  operator: ConditionOperator;
  value: any;
}

export interface PolicyScope {
  users: number[];
  roles: string[];
  groups: string[];
  locations: number[];
  devices: string[];
}

export interface PolicyException {
  userId: number;
  reason: string;
  expiresAt?: Date;
  approvedBy: number;
  approvedAt: Date;
}

export interface SecurityEvent {
  id: number;
  type: SecurityEventType;
  severity: EventSeverity;
  description: string;
  source: EventSource;
  target: EventTarget;
  details: EventDetails;
  actionTaken: string;
  resolved: boolean;
  resolvedAt?: Date;
  resolvedBy?: number;
  createdAt: Date;
  
  // Relations
  resolvedByUser?: User;
}

export interface EventSource {
  ip: string;
  userAgent: string;
  userId?: number;
  location?: GeoLocation;
}

export interface EventTarget {
  type: string;
  id?: number;
  name: string;
}

export interface EventDetails {
  before?: any;
  after?: any;
  metadata: Record<string, any>;
}

export interface SecurityScan {
  id: number;
  type: ScanType;
  status: ScanStatus;
  findings: SecurityFinding[];
  startedAt: Date;
  completedAt?: Date;
  duration?: number;
  scanner: string;
  createdAt: Date;
}

export interface SecurityFinding {
  type: FindingType;
  severity: FindingSeverity;
  description: string;
  location: string;
  recommendation: string;
  status: FindingStatus;
  resolvedAt?: Date;
  resolvedBy?: number;
}

export enum PolicyType {
  ACCESS_CONTROL = 'access_control',
  PASSWORD = 'password',
  SESSION = 'session',
  DATA_PROTECTION = 'data_protection',
  NETWORK = 'network'
}

export enum RuleAction {
  ALLOW = 'allow',
  DENY = 'deny',
  REQUIRE_2FA = 'require_2fa',
  LOG = 'log',
  ALERT = 'alert'
}

export enum RuleEffect {
  ALLOW = 'allow',
  DENY = 'deny',
  CHALLENGE = 'challenge'
}

export enum SecurityEventType {
  LOGIN = 'login',
  LOGOUT = 'logout',
  ACCESS_DENIED = 'access_denied',
  PASSWORD_CHANGE = 'password_change',
  PERMISSION_CHANGE = 'permission_change',
  DATA_EXPORT = 'data_export',
  CONFIG_CHANGE = 'config_change'
}

export enum EventSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum ScanType {
  VULNERABILITY = 'vulnerability',
  COMPLIANCE = 'compliance',
  PENETRATION = 'penetration',
  CODE_ANALYSIS = 'code_analysis'
}

export enum ScanStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum FindingType {
  VULNERABILITY = 'vulnerability',
  MISCONFIGURATION = 'misconfiguration',
  COMPLIANCE_VIOLATION = 'compliance_violation',
  WEAK_PASSWORD = 'weak_password'
}

export enum FindingSeverity {
  INFO = 'info',
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum FindingStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  FALSE_POSITIVE = 'false_positive'
}