// src/types/surveys.ts
export interface Survey {
  id: number;
  title: string;
  description?: string;
  type: SurveyType;
  category: SurveyCategory;
  questions: SurveyQuestion[];
  logic: SurveyLogic;
  settings: SurveySettings;
  isActive: boolean;
  isAnonymous: boolean;
  organizationId: string;
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  organization?: Organization;
  createdByUser?: User;
  responses?: SurveyResponse[];
}

export interface SurveyQuestion {
  id: string;
  type: QuestionType;
  text: string;
  description?: string;
  required: boolean;
  options?: QuestionOption[];
  scale?: ScaleSettings;
  validation?: QuestionValidation;
  position: number;
}

export interface SurveyResponse {
  id: number;
  surveyId: number;
  patientId?: number;
  respondentId?: number;
  answers: Record<string, any>;
  score?: number;
  duration: number;
  completedAt: Date;
  createdAt: Date;
  
  // Relations
  survey?: Survey;
  patient?: Patient;
  respondent?: User;
}

export interface SurveyAnalysis {
  totalResponses: number;
  completionRate: number;
  averageScore: number;
  questionStats: QuestionStat[];
  trend: ResponseTrend;
  demographics: DemographicBreakdown;
}

export interface QuestionStat {
  questionId: string;
  type: QuestionType;
  responses: number;
  average?: number;
  distribution: Record<string, number>;
  insights: string[];
}

export interface ResponseTrend {
  daily: TrendPoint[];
  weekly: TrendPoint[];
  monthly: TrendPoint[];
}

export interface TrendPoint {
  period: string;
  count: number;
  average: number;
}

export interface DemographicBreakdown {
  byAge: Record<string, number>;
  byGender: Record<string, number>;
  byLocation: Record<string, number>;
}

export enum SurveyType {
  SATISFACTION = 'satisfaction',
  ASSESSMENT = 'assessment',
  FEEDBACK = 'feedback',
  RESEARCH = 'research',
  SCREENING = 'screening'
}

export enum SurveyCategory {
  PATIENT = 'patient',
  STAFF = 'staff',
  CLINICAL = 'clinical',
  OPERATIONAL = 'operational'
}

export enum QuestionType {
  TEXT = 'text',
  MULTIPLE_CHOICE = 'multiple_choice',
  CHECKBOX = 'checkbox',
  RATING = 'rating',
  SCALE = 'scale',
  RANKING = 'ranking',
  DATE = 'date'
}