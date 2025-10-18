// src/types/compliance.ts
export interface ComplianceRequirement {
  id: number;
  standard: ComplianceStandard;
  version: string;
  requirement: string;
  description: string;
  category: ComplianceCategory;
  controls: ComplianceControl[];
  evidenceRequired: EvidenceType[];
  frequency: ComplianceFrequency;
  responsibleRole: string;
  status: ComplianceStatus;
  lastAssessment?: Date;
  nextAssessment?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface ComplianceControl {
  id: string;
  description: string;
  implementation: string;
  testing: string;
  remediation: string;
}

export interface ComplianceAssessment {
  id: number;
  requirementId: number;
  status: AssessmentStatus;
  findings: AssessmentFinding[];
  evidence: AssessmentEvidence[];
  assessedBy: number;
  assessedAt: Date;
  approvedBy?: number;
  approvedAt?: Date;
  createdAt: Date;
  
  // Relations
  requirement?: ComplianceRequirement;
  assessedByUser?: User;
  approvedByUser?: User;
}

export interface AssessmentFinding {
  type: FindingType;
  severity: FindingSeverity;
  description: string;
  recommendation: string;
  status: FindingStatus;
  dueDate?: Date;
}

export interface AssessmentEvidence {
  type: EvidenceType;
  description: string;
  fileUrl?: string;
  collectedAt: Date;
  collectedBy: number;
}

export interface AuditTrail {
  id: number;
  action: AuditAction;
  resource: string;
  resourceId?: number;
  user: number;
  timestamp: Date;
  details: AuditDetails;
  ipAddress: string;
  
  // Relations
  userDetail?: User;
}

export enum ComplianceStandard {
  HIPAA = 'hipaa',
  GDPR = 'gdpr',
  PCI_DSS = 'pci_dss',
  SOC2 = 'soc2',
  ISO27001 = 'iso27001',
  HITRUST = 'hitrust'
}

export enum ComplianceCategory {
  PRIVACY = 'privacy',
  SECURITY = 'security',
  DATA_PROTECTION = 'data_protection',
  ACCESS_CONTROL = 'access_control',
  AUDIT = 'audit'
}

export enum ComplianceFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  QUARTERLY = 'quarterly',
  ANNUALLY = 'annually',
  CONTINUOUS = 'continuous'
}

export enum ComplianceStatus {
  COMPLIANT = 'compliant',
  NON_COMPLIANT = 'non_compliant',
  PARTIALLY_COMPLIANT = 'partially_compliant',
  NOT_APPLICABLE = 'not_applicable'
}

export enum AssessmentStatus {
  PLANNED = 'planned',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  REVIEWED = 'reviewed',
  APPROVED = 'approved'
}

export enum EvidenceType {
  DOCUMENT = 'document',
  SCREENSHOT = 'screenshot',
  LOG = 'log',
  CONFIGURATION = 'configuration',
  INTERVIEW = 'interview',
  OBSERVATION = 'observation'
}