// src/types/tasks.ts
export interface Task {
  id: number;
  title: string;
  description?: string;
  type: TaskType;
  priority: TaskPriority;
  status: TaskStatus;
  assigneeId?: number;
  reporterId: number;
  dueDate?: Date;
  estimatedHours?: number;
  actualHours?: number;
  tags: string[];
  dependencies: number[];
  attachments: Attachment[];
  comments: Comment[];
  progress: number;
  isRecurring: boolean;
  recurrencePattern?: RecurrencePattern;
  completedAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  assignee?: User;
  reporter?: User;
}

export interface Comment {
  id: number;
  taskId: number;
  authorId: number;
  content: string;
  attachments: Attachment[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  author?: User;
}

export interface TaskFilter {
  status?: TaskStatus[];
  priority?: TaskPriority[];
  assigneeId?: number;
  reporterId?: number;
  tags?: string[];
  dueDate?: DateRange;
}

export interface TaskStats {
  total: number;
  completed: number;
  overdue: number;
  byStatus: Record<TaskStatus, number>;
  byPriority: Record<TaskPriority, number>;
  byAssignee: Record<number, number>;
}

export enum TaskType {
  GENERAL = 'general',
  FOLLOW_UP = 'follow_up',
  MAINTENANCE = 'maintenance',
  TRAINING = 'training',
  MEETING = 'meeting',
  DOCUMENTATION = 'documentation'
}

export enum TaskPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export enum TaskStatus {
  BACKLOG = 'backlog',
  TODO = 'todo',
  IN_PROGRESS = 'in_progress',
  REVIEW = 'review',
  DONE = 'done',
  CANCELLED = 'cancelled'
}