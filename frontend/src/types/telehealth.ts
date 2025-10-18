// src/types/telehealth.ts
export interface TelehealthSession {
  id: number;
  patientId: number;
  providerId: number;
  appointmentId?: number;
  roomId: string;
  status: SessionStatus;
  type: SessionType;
  scheduledStart: Date;
  actualStart?: Date;
  actualEnd?: Date;
  duration: number;
  recordingUrl?: string;
  transcript?: string;
  notes?: string;
  technicalIssues: TechnicalIssue[];
  qualityMetrics: QualityMetrics;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  patient?: Patient;
  provider?: User;
  appointment?: Appointment;
}

export interface TechnicalIssue {
  type: IssueType;
  severity: IssueSeverity;
  description: string;
  occurredAt: Date;
  resolvedAt?: Date;
}

export interface QualityMetrics {
  videoQuality: number;
  audioQuality: number;
  latency: number;
  jitter: number;
  packetLoss: number;
}

export interface TelehealthSettings {
  videoEnabled: boolean;
  audioEnabled: boolean;
  recordingEnabled: boolean;
  transcriptionEnabled: boolean;
  waitingRoomEnabled: boolean;
  maxParticipants: number;
  defaultDuration: number;
  preSessionChecklist: string[];
}

export enum SessionStatus {
  SCHEDULED = 'scheduled',
  STARTED = 'started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
  FAILED = 'failed'
}

export enum SessionType {
  CONSULTATION = 'consultation',
  FOLLOW_UP = 'follow_up',
  EMERGENCY = 'emergency',
  SECOND_OPINION = 'second_opinion'
}

export enum IssueType {
  CONNECTION = 'connection',
  AUDIO = 'audio',
  VIDEO = 'video',
  PERMISSIONS = 'permissions',
  PLATFORM = 'platform'
}

export enum IssueSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}