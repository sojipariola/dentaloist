// src/types/user-activity.ts
export interface UserActivity {
  id: number;
  userId: number;
  type: ActivityType;
  action: string;
  resourceType: string;
  resourceId?: number;
  details: ActivityDetails;
  ipAddress: string;
  userAgent: string;
  location?: GeoLocation;
  timestamp: Date;
  
  // Relations
  user?: User;
}

export interface ActivityDetails {
  before?: any;
  after?: any;
  changes?: string[];
  metadata?: Record<string, any>;
}

export interface GeoLocation {
  country: string;
  region: string;
  city: string;
  latitude: number;
  longitude: number;
}

export interface ActivitySummary {
  totalActivities: number;
  byType: Record<ActivityType, number>;
  byHour: Record<string, number>;
  byDay: Record<string, number>;
  topUsers: TopUser[];
  recentActivities: UserActivity[];
}

export interface TopUser {
  userId: number;
  userName: string;
  count: number;
  lastActivity: Date;
  user?: User;
}

export interface SessionActivity {
  sessionId: string;
  userId: number;
  startTime: Date;
  endTime?: Date;
  duration: number;
  activities: number;
  pages: string[];
  devices: string[];
  locations: string[];
  user?: User;
}

export enum ActivityType {
  LOGIN = 'login',
  LOGOUT = 'logout',
  CREATE = 'create',
  READ = 'read',
  UPDATE = 'update',
  DELETE = 'delete',
  EXPORT = 'export',
  IMPORT = 'import',
  SECURITY = 'security',
  SYSTEM = 'system'
}