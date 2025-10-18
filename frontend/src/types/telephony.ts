// src/types/telephony.ts
export interface PhoneCall {
  id: number;
  from: string;
  to: string;
  direction: CallDirection;
  type: CallType;
  status: CallStatus;
  duration: number;
  recordingUrl?: string;
  transcript?: string;
  notes?: string;
  tags: string[];
  cost?: number;
  participantId?: number;
  participantType?: ParticipantType;
  startedAt: Date;
  endedAt?: Date;
  createdAt: Date;
  
  // Relations
  participant?: any;
}

export interface CallQueue {
  id: number;
  name: string;
  description?: string;
  members: number[];
  settings: QueueSettings;
  stats: QueueStats;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  memberUsers?: User[];
}

export interface IVRMenu {
  id: number;
  name: string;
  greeting: string;
  options: IVROption[];
  timeout: number;
  maxAttempts: number;
  fallback: FallbackAction;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface IVROption {
  digit: string;
  action: IVRAction;
  target?: string;
  description?: string;
}

export interface CallRecording {
  id: number;
  callId: number;
  url: string;
  format: RecordingFormat;
  duration: number;
  size: number;
  quality: RecordingQuality;
  transcription?: string;
  storage: StorageInfo;
  createdAt: Date;
  
  // Relations
  call?: PhoneCall;
}

export interface StorageInfo {
  provider: string;
  bucket: string;
  path: string;
  retention: number;
}

export interface QueueSettings {
  strategy: QueueStrategy;
  timeout: number;
  maxWait: number;
  maxSize: number;
  music?: string;
  announcements: Announcement[];
}

export interface QueueStats {
  waiting: number;
  answered: number;
  abandoned: number;
  averageWait: number;
  averageTalk: number;
  serviceLevel: number;
}

export interface Announcement {
  message: string;
  frequency: number;
  enabled: boolean;
}

export enum CallDirection {
  INBOUND = 'inbound',
  OUTBOUND = 'outbound'
}

export enum CallType {
  VOICE = 'voice',
  VIDEO = 'video',
  CONFERENCE = 'conference'
}

export enum CallStatus {
  RINGING = 'ringing',
  ANSWERED = 'answered',
  COMPLETED = 'completed',
  BUSY = 'busy',
  FAILED = 'failed',
  NO_ANSWER = 'no_answer'
}

export enum ParticipantType {
  PATIENT = 'patient',
  PROVIDER = 'provider',
  STAFF = 'staff',
  EXTERNAL = 'external'
}

export enum IVRAction {
  ROUTE = 'route',
  PLAY = 'play',
  RECORD = 'record',
  HANGUP = 'hangup',
  QUEUE = 'queue'
}

export enum QueueStrategy {
  ROUND_ROBIN = 'round_robin',
  LEAST_RECENT = 'least_recent',
  FEWEST_CALLS = 'fewest_calls',
  RANDOM = 'random'
}

export enum RecordingQuality {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high'
}

export enum FallbackAction {
  VOICEMAIL = 'voicemail',
  OPERATOR = 'operator',
  HANGUP = 'hangup'
}