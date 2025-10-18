// src/types/chat.ts
export interface ChatMessage {
  id: number;
  threadId: number;
  senderId: number;
  content: string;
  type: MessageType;
  attachments: ChatAttachment[];
  reactions: Reaction[];
  edited: boolean;
  editedAt?: Date;
  deleted: boolean;
  deletedAt?: Date;
  readBy: number[];
  createdAt: Date;
  
  // Relations
  sender?: User;
  thread?: ChatThread;
}

export interface ChatThread {
  id: number;
  type: ThreadType;
  title: string;
  description?: string;
  participants: ThreadParticipant[];
  lastMessage?: ChatMessage;
  unreadCount: number;
  isArchived: boolean;
  isPinned: boolean;
  muted: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface ThreadParticipant {
  userId: number;
  joinedAt: Date;
  lastReadAt?: Date;
  role: ParticipantRole;
  status: ParticipantStatus;
  
  // Relations
  user?: User;
}

export interface ChatAttachment {
  id: number;
  name: string;
  type: AttachmentType;
  size: number;
  url: string;
  thumbnailUrl?: string;
  createdAt: Date;
}

export interface Reaction {
  emoji: string;
  userId: number;
  createdAt: Date;
  
  // Relations
  user?: User;
}

export interface ChatPresence {
  userId: number;
  status: PresenceStatus;
  lastSeen: Date;
  device: string;
  location?: string;
  
  // Relations
  user?: User;
}

export enum MessageType {
  TEXT = 'text',
  IMAGE = 'image',
  FILE = 'file',
  SYSTEM = 'system',
  TYPING = 'typing'
}

export enum ThreadType {
  DIRECT = 'direct',
  GROUP = 'group',
  CHANNEL = 'channel',
  TEAM = 'team'
}

export enum ParticipantRole {
  MEMBER = 'member',
  ADMIN = 'admin',
  OWNER = 'owner'
}

export enum ParticipantStatus {
  ACTIVE = 'active',
  MUTED = 'muted',
  BANNED = 'banned'
}

export enum PresenceStatus {
  ONLINE = 'online',
  OFFLINE = 'offline',
  AWAY = 'away',
  BUSY = 'busy',
  DO_NOT_DISTURB = 'do_not_disturb'
}

export enum AttachmentType {
  IMAGE = 'image',
  DOCUMENT = 'document',
  VIDEO = 'video',
  AUDIO = 'audio'
}