// src/types/community-forums.ts
export interface Forum {
  id: number;
  name: string;
  description: string;
  category: ForumCategory;
  type: ForumType;
  settings: ForumSettings;
  stats: ForumStats;
  moderators: number[];
  isActive: boolean;
  isPrivate: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  moderatorUsers?: User[];
}

export interface ForumThread {
  id: number;
  forumId: number;
  title: string;
  content: string;
  author: number;
  type: ThreadType;
  status: ThreadStatus;
  tags: string[];
  votes: number;
  views: number;
  replies: number;
  lastReply?: ForumReply;
  pinned: boolean;
  locked: boolean;
  featured: boolean;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  forum?: Forum;
  authorUser?: User;
}

export interface ForumReply {
  id: number;
  threadId: number;
  content: string;
  author: number;
  parentId?: number;
  votes: number;
  accepted: boolean;
  edited: boolean;
  editedAt?: Date;
  deleted: boolean;
  deletedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  thread?: ForumThread;
  authorUser?: User;
  parent?: ForumReply;
}

export interface ForumSettings {
  permissions: ForumPermissions;
  moderation: ModerationSettings;
  notifications: NotificationSettings;
  appearance: AppearanceSettings;
}

export interface ForumStats {
  threads: number;
  replies: number;
  members: number;
  activeMembers: number;
  dailyPosts: number;
  solvedThreads: number;
}

export interface ForumPermissions {
  createThread: PermissionLevel;
  createReply: PermissionLevel;
  vote: PermissionLevel;
  edit: PermissionLevel;
  delete: PermissionLevel;
  moderate: PermissionLevel;
}

export interface ModerationSettings {
  preModeration: boolean;
  flagThreshold: number;
  autoLock: number;
  wordFilter: string[];
}

export interface NotificationSettings {
  email: boolean;
  push: boolean;
  digest: boolean;
  frequency: NotificationFrequency;
}

export interface AppearanceSettings {
  theme: string;
  layout: string;
  customCSS?: string;
}

export enum ForumCategory {
  GENERAL = 'general',
  SUPPORT = 'support',
  FEEDBACK = 'feedback',
  ANNOUNCEMENTS = 'announcements',
  OFF_TOPIC = 'off_topic'
}

export enum ForumType {
  DISCUSSION = 'discussion',
  QNA = 'qna',
  IDEA = 'idea',
  BUG = 'bug'
}

export enum ThreadType {
  QUESTION = 'question',
  DISCUSSION = 'discussion',
  POLL = 'poll',
  ANNOUNCEMENT = 'announcement'
}

export enum ThreadStatus {
  OPEN = 'open',
  CLOSED = 'closed',
  SOLVED = 'solved',
  DUPLICATE = 'duplicate'
}

export enum PermissionLevel {
  EVERYONE = 'everyone',
  MEMBERS = 'members',
  MODERATORS = 'moderators',
  ADMINS = 'admins'
}