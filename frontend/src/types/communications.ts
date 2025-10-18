// src/types/communications.ts
export interface Message {
  id: number;
  threadId: number;
  senderId: number;
  content: string;
  type: MessageType;
  attachments: Attachment[];
  isRead: boolean;
  readAt?: Date;
  createdAt: Date;
  
  // Relations
  sender?: User;
  thread?: MessageThread;
}

export interface MessageThread {
  id: number;
  type: ThreadType;
  title: string;
  participants: ThreadParticipant[];
  lastMessage?: Message;
  unreadCount: number;
  isArchived: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface ThreadParticipant {
  userId: number;
  joinedAt: Date;
  lastReadAt?: Date;
  role: ParticipantRole;
}

export interface Attachment {
  id: number;
  name: string;
  type: AttachmentType;
  size: number;
  url: string;
  thumbnailUrl?: string;
  createdAt: Date;
}

export interface NotificationSettings {
  email: boolean;
  sms: boolean;
  push: boolean;
  desktop: boolean;
  doNotDisturb: DoNotDisturb;
  customAlerts: CustomAlert[];
}

export interface DoNotDisturb {
  enabled: boolean;
  start: string;
  end: string;
  days: number[];
}

export interface CustomAlert {
  type: string;
  channels: string[];
  triggers: string[];
}

export enum MessageType {
  TEXT = 'text',
  IMAGE = 'image',
  FILE = 'file',
  SYSTEM = 'system',
  APPOINTMENT = 'appointment'
}

export enum ThreadType {
  DIRECT = 'direct',
  GROUP = 'group',
  TEAM = 'team',
  PATIENT = 'patient',
  SUPPORT = 'support'
}

export enum ParticipantRole {
  MEMBER = 'member',
  ADMIN = 'admin',
  OWNER = 'owner'
}

export enum AttachmentType {
  IMAGE = 'image',
  DOCUMENT = 'document',
  VIDEO = 'video',
  AUDIO = 'audio'
}