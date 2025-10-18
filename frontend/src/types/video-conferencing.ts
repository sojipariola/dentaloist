// src/types/video-conferencing.ts
export interface VideoConference {
  id: number;
  title: string;
  description?: string;
  type: ConferenceType;
  status: ConferenceStatus;
  roomId: string;
  joinUrl: string;
  startTime: Date;
  endTime?: Date;
  duration: number;
  participants: ConferenceParticipant[];
  settings: ConferenceSettings;
  recording?: RecordingInfo;
  transcript?: TranscriptInfo;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface ConferenceParticipant {
  userId: number;
  role: ParticipantRole;
  joinedAt: Date;
  leftAt?: Date;
  duration: number;
  status: ParticipantStatus;
  device: string;
  location?: string;
  
  // Relations
  user?: User;
}

export interface ConferenceSettings {
  videoEnabled: boolean;
  audioEnabled: boolean;
  screenShareEnabled: boolean;
  recordingEnabled: boolean;
  transcriptionEnabled: boolean;
  waitingRoomEnabled: boolean;
  maxParticipants: number;
  allowJoinBeforeHost: boolean;
  muteOnEntry: boolean;
  autoRecord: boolean;
}

export interface RecordingInfo {
  status: RecordingStatus;
  startTime?: Date;
  endTime?: Date;
  duration?: number;
  fileUrl?: string;
  fileSize?: number;
  format: RecordingFormat;
}

export interface TranscriptInfo {
  status: TranscriptStatus;
  text?: string;
  fileUrl?: string;
  confidence: number;
  speakerCount: number;
}

export interface ConferenceStats {
  totalConferences: number;
  totalParticipants: number;
  averageDuration: number;
  byType: Record<ConferenceType, number>;
  byStatus: Record<ConferenceStatus, number>;
  peakUsage: PeakUsage;
}

export interface PeakUsage {
  time: Date;
  participants: number;
  conferences: number;
}

export enum ConferenceType {
  MEETING = 'meeting',
  WEBINAR = 'webinar',
  TRAINING = 'training',
  SUPPORT = 'support'
}

export enum ConferenceStatus {
  SCHEDULED = 'scheduled',
  STARTED = 'started',
  IN_PROGRESS = 'in_progress',
  ENDED = 'ended',
  CANCELLED = 'cancelled'
}

export enum ParticipantStatus {
  INVITED = 'invited',
  JOINED = 'joined',
  LEFT = 'left',
  MISSED = 'missed'
}

export enum RecordingStatus {
  NOT_STARTED = 'not_started',
  RECORDING = 'recording',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}

export enum RecordingFormat {
  MP4 = 'mp4',
  WEBM = 'webm',
  AUDIO_ONLY = 'audio_only'
}

export enum TranscriptStatus {
  NOT_STARTED = 'not_started',
  PROCESSING = 'processing',
  COMPLETED = 'completed',
  FAILED = 'failed'
}