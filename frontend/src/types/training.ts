// src/types/training.ts
export interface TrainingCourse {
  id: number;
  title: string;
  description: string;
  category: CourseCategory;
  level: CourseLevel;
  duration: number;
  points: number;
  prerequisites: number[];
  objectives: string[];
  content: CourseContent[];
  assessments: Assessment[];
  instructors: number[];
  status: CourseStatus;
  enrollment: EnrollmentInfo;
  metadata: CourseMetadata;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  instructorUsers?: User[];
}

export interface CourseContent {
  id: number;
  type: ContentType;
  title: string;
  content: any;
  duration: number;
  order: number;
  prerequisites: number[];
  resources: Resource[];
  completed: boolean;
}

export interface Assessment {
  id: number;
  type: AssessmentType;
  title: string;
  questions: Question[];
  passingScore: number;
  timeLimit?: number;
  attempts: number;
  shuffle: boolean;
  feedback: FeedbackSettings;
}

export interface EnrollmentInfo {
  total: number;
  completed: number;
  inProgress: number;
  notStarted: number;
  averageScore: number;
  completionRate: number;
}

export interface CourseMetadata {
  version: string;
  lastUpdated: Date;
  rating: number;
  reviews: number;
  difficulty: DifficultyLevel;
  tags: string[];
}

export interface TrainingProgress {
  userId: number;
  courseId: number;
  status: ProgressStatus;
  progress: number;
  currentContent: number;
  score?: number;
  startedAt: Date;
  completedAt?: Date;
  timeSpent: number;
  attempts: number;
  certificates: Certificate[];
  
  // Relations
  user?: User;
  course?: TrainingCourse;
}

export interface Certificate {
  id: number;
  courseId: number;
  userId: number;
  issuedAt: Date;
  expiresAt?: Date;
  credential: string;
  verificationUrl: string;
  
  // Relations
  course?: TrainingCourse;
  user?: User;
}

export enum CourseCategory {
  TECHNICAL = 'technical',
  SOFT_SKILLS = 'soft_skills',
  COMPLIANCE = 'compliance',
  PRODUCT = 'product',
  LEADERSHIP = 'leadership'
}

export enum CourseLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced'
}

export enum CourseStatus {
  DRAFT = 'draft',
  PUBLISHED = 'published',
  ARCHIVED = 'archived',
  COMING_SOON = 'coming_soon'
}

export enum ContentType {
  VIDEO = 'video',
  ARTICLE = 'article',
  QUIZ = 'quiz',
  EXERCISE = 'exercise',
  DOWNLOAD = 'download'
}

export enum AssessmentType {
  QUIZ = 'quiz',
  EXAM = 'exam',
  PROJECT = 'project',
  PRACTICAL = 'practical'
}

export enum ProgressStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  FAILED = 'failed'
}