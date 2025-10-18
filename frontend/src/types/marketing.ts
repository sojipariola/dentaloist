// src/types/marketing.ts
export interface Campaign {
  id: number;
  name: string;
  type: CampaignType;
  status: CampaignStatus;
  audience: Audience;
  content: CampaignContent;
  schedule: CampaignSchedule;
  budget: CampaignBudget;
  metrics: CampaignMetrics;
  tags: string[];
  createdBy: number;
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  createdByUser?: User;
}

export interface Audience {
  segments: string[];
  filters: AudienceFilter[];
  size: number;
  estimatedReach: number;
}

export interface CampaignContent {
  subject: string;
  body: string;
  media: Media[];
  callToAction: CallToAction;
  personalization: Personalization[];
}

export interface CampaignSchedule {
  start: Date;
  end?: Date;
  frequency: Frequency;
  timezone: string;
}

export interface CampaignBudget {
  total: number;
  spent: number;
  type: BudgetType;
  daily?: number;
}

export interface CampaignMetrics {
  sent: number;
  delivered: number;
  opened: number;
  clicked: number;
  converted: number;
  revenue: number;
  roi: number;
  costPerClick: number;
  costPerConversion: number;
}

export interface Lead {
  id: number;
  source: LeadSource;
  status: LeadStatus;
  contact: ContactInfo;
  details: LeadDetails;
  score: number;
  owner?: number;
  campaignId?: number;
  notes: string[];
  tags: string[];
  createdAt: Date;
  updatedAt: Date;
  
  // Relations
  ownerUser?: User;
  campaign?: Campaign;
}

export interface LeadDetails {
  interest: string;
  budget?: number;
  timeline?: string;
  requirements: string[];
  interactions: Interaction[];
}

export interface Interaction {
  type: InteractionType;
  date: Date;
  details: string;
  outcome: Outcome;
}

export enum CampaignType {
  EMAIL = 'email',
  SMS = 'sms',
  SOCIAL = 'social',
  SEARCH = 'search',
  DISPLAY = 'display'
}

export enum CampaignStatus {
  DRAFT = 'draft',
  SCHEDULED = 'scheduled',
  RUNNING = 'running',
  PAUSED = 'paused',
  COMPLETED = 'completed'
}

export enum BudgetType {
  TOTAL = 'total',
  DAILY = 'daily',
  LIFETIME = 'lifetime'
}

export enum LeadSource {
  WEBSITE = 'website',
  REFERRAL = 'referral',
  SOCIAL = 'social',
  EVENT = 'event',
  PAID = 'paid'
}

export enum LeadStatus {
  NEW = 'new',
  CONTACTED = 'contacted',
  QUALIFIED = 'qualified',
  PROPOSAL = 'proposal',
  NEGOTIATION = 'negotiation',
  WON = 'won',
  LOST = 'lost'
}

export enum InteractionType {
  EMAIL = 'email',
  CALL = 'call',
  MEETING = 'meeting',
  DEMO = 'demo',
  PROPOSAL = 'proposal'
}

export enum Outcome {
  POSITIVE = 'positive',
  NEUTRAL = 'neutral',
  NEGATIVE = 'negative'
}

export enum Frequency {
  ONCE = 'once',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly'
}