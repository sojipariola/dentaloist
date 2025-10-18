// src/types/feedback.ts
export interface Feedback {
  id: number;
  type: FeedbackType;
  category: FeedbackCategory;
  title: string;
  description: string;
  rating?: number;
  status: FeedbackStatus;
  submittedBy: number;
  assignedTo?: number;
  priority: FeedbackPriority;
  tags: string[];
  attachments: Attachment[];
  comments: FeedbackComment[];
  resolution?: string;
  resolvedAt?: Date;
  resolvedBy?: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  submittedByUser?: User;
  assignedToUser?: User;
  resolvedByUser?: User;
}

export interface FeedbackComment {
  id: number;
  feedbackId: number;
  authorId: number;
  content: string;
  isInternal: boolean;
  createdAt: Date;
  
  // Relations
  author?: User;
}

export interface FeedbackStats {
  total: number;
  byStatus: Record<FeedbackStatus, number>;
  byCategory: Record<FeedbackCategory, number>;
  byPriority: Record<FeedbackPriority, number>;
  averageRating: number;
  responseTime: number;
}

export interface FeedbackSettings {
  categories: string[];
  priorities: string[];
  autoAssign: boolean;
  defaultAssignee?: number;
  responseTimeGoal: number;
  escalationRules: EscalationRule[];
}

export interface EscalationRule {
  priority: FeedbackPriority;
  responseTime: number;
  assignee: number;
}

export enum FeedbackType {
  BUG = 'bug',
  FEATURE = 'feature',
  IMPROVEMENT = 'improvement',
  QUESTION = 'question',
  COMPLIMENT = 'compliment',
  COMPLAINT = 'complaint'
}

export enum FeedbackCategory {
  UI = 'ui',
  FUNCTIONALITY = 'functionality',
  PERFORMANCE = 'performance',
  SECURITY = 'security',
  DOCUMENTATION = 'documentation',
  OTHER = 'other'
}

export enum FeedbackStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
  DUPLICATE = 'duplicate'
}

export enum FeedbackPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}