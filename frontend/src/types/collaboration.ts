// src/types/collaboration.ts
export interface CollaborationSpace {
  id: number;
  name: string;
  description?: string;
  type: SpaceType;
  category: SpaceCategory;
  members: SpaceMember[];
  settings: SpaceSettings;
  content: SpaceContent[];
  activity: SpaceActivity[];
  isPublic: boolean;
  isArchived: boolean;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface SpaceMember {
  userId: number;
  role: MemberRole;
  joinedAt: Date;
  lastActive?: Date;
  status: MemberStatus;
  
  // Relations
  user?: User;
}

export interface SpaceContent {
  id: number;
  type: ContentType;
  title: string;
  content: any;
  author: number;
  version: number;
  parentId?: number;
  tags: string[];
  permissions: ContentPermissions;
  stats: ContentStats;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  authorUser?: User;
}

export interface SpaceActivity {
  id: number;
  type: ActivityType;
  user: number;
  targetType: string;
  targetId?: number;
  details: any;
  timestamp: Date;
  
  // Relations
  userDetail?: User;
}

export interface SpaceSettings {
  permissions: SpacePermissions;
  notifications: SpaceNotifications;
  features: SpaceFeatures;
  appearance: SpaceAppearance;
}

export interface ContentPermissions {
  view: string[];
  edit: string[];
  comment: string[];
  share: string[];
}

export interface ContentStats {
  views: number;
  downloads: number;
  comments: number;
  likes: number;
  shares: number;
}

export interface SpacePermissions {
  join: PermissionLevel;
  create: PermissionLevel;
  edit: PermissionLevel;
  comment: PermissionLevel;
  share: PermissionLevel;
}

export interface SpaceNotifications {
  email: boolean;
  push: boolean;
  desktop: boolean;
  frequency: NotificationFrequency;
}

export interface SpaceFeatures {
  chat: boolean;
  video: boolean;
  whiteboard: boolean;
  polling: boolean;
  tasks: boolean;
}

export interface SpaceAppearance {
  theme: string;
  layout: string;
  colors: string[];
}

export enum SpaceType {
  TEAM = 'team',
  PROJECT = 'project',
  DEPARTMENT = 'department',
  TOPIC = 'topic',
  COMMUNITY = 'community'
}

export enum SpaceCategory {
  DEVELOPMENT = 'development',
  DESIGN = 'design',
  MARKETING = 'marketing',
  SUPPORT = 'support',
  GENERAL = 'general'
}

export enum MemberRole {
  VIEWER = 'viewer',
  CONTRIBUTOR = 'contributor',
  EDITOR = 'editor',
  ADMIN = 'admin',
  OWNER = 'owner'
}

export enum MemberStatus {
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  PENDING = 'pending',
  BANNED = 'banned'
}

export enum ContentType {
  DOCUMENT = 'document',
  SPREADSHEET = 'spreadsheet',
  PRESENTATION = 'presentation',
  WHITEBOARD = 'whiteboard',
  TASK_LIST = 'task_list',
  POLL = 'poll'
}

export enum ActivityType {
  CREATE = 'create',
  UPDATE = 'update',
  COMMENT = 'comment',
  LIKE = 'like',
  SHARE = 'share',
  JOIN = 'join',
  LEAVE = 'leave'
}

export enum PermissionLevel {
  EVERYONE = 'everyone',
  MEMBERS = 'members',
  ADMINS = 'admins',
  SPECIFIC = 'specific'
}

export enum NotificationFrequency {
  INSTANT = 'instant',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  NEVER = 'never'
}