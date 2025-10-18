// src/types/mobile-app.ts

export interface MobileApp {
  id: number;
  name: string;
  platform: Platform;
  version: string;
  build: string;
  status: AppStatus;
  features: AppFeature[];
  settings: AppSettings;
  statistics: AppStatistics;
  releases: AppRelease[];
  feedback: AppFeedback[];
  createdAt: Date;
  updatedAt: Date;
}

export interface AppFeature {
  name: string;
  description: string;
  enabled: boolean;
  required: boolean;
  permissions: string[];
}

export interface AppSettings {
  notifications: NotificationSettings;
  privacy: PrivacySettings;
  appearance: AppearanceSettings;
  performance: PerformanceSettings;
}

export interface AppStatistics {
  downloads: number;
  activeUsers: number;
  sessions: number;
  crashRate: number;
  rating: number;
  reviews: number;
  retention: number;
}

export interface AppRelease {
  version: string;
  build: string;
  type: ReleaseType;
  status: ReleaseStatus;
  changes: Change[];
  releasedAt: Date;
  mandatory: boolean;
  rollout: number;
  downloadUrl: string;
  size: number;
}

export interface AppFeedback {
  id: number;
  type: FeedbackType;
  rating: number;
  comment: string;
  device: DeviceInfo;
  os: OSInfo;
  contact: ContactInfo;
  status: FeedbackStatus;
  createdAt: Date;
}

export interface DeviceInfo {
  model: string;
  manufacturer: string;
  screen: ScreenInfo;
  memory: MemoryInfo;
}

export interface OSInfo {
  name: string;
  version: string;
  sdk: string;
}

export interface ScreenInfo {
  width: number;
  height: number;
  density: number;
}

export interface MemoryInfo {
  total: number;
  available: number;
}

export interface PerformanceSettings {
  cache: CacheSettings;
  network: NetworkSettings;
  battery: BatterySettings;
}

export interface CacheSettings {
  enabled: boolean;
  size: number;
  expiration: number;
}

export interface NetworkSettings {
  timeout: number;
  retry: number;
  compression: boolean;
}

export interface BatterySettings {
  optimization: boolean;
  background: boolean;
}

export enum Platform {
  IOS = 'ios',
  ANDROID = 'android',
  CROSS_PLATFORM = 'cross_platform'
}

export enum AppStatus {
  DEVELOPMENT = 'development',
  TESTING = 'testing',
  PRODUCTION = 'production',
  MAINTENANCE = 'maintenance',
  DEPRECATED = 'deprecated'
}

export enum ReleaseType {
  MAJOR = 'major',
  MINOR = 'minor',
  PATCH = 'patch',
  HOTFIX = 'hotfix'
}

export enum ReleaseStatus {
  DRAFT = 'draft',
  SUBMITTED = 'submitted',
  APPROVED = 'approved',
  REJECTED = 'rejected',
  LIVE = 'live'
}

export enum FeedbackType {
  BUG = 'bug',
  FEATURE = 'feature',
  GENERAL = 'general',
  PERFORMANCE = 'performance'
}

export enum FeedbackStatus {
  NEW = 'new',
  REVIEWED = 'reviewed',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved'
}