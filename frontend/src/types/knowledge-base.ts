// src/types/knowledge-base.ts
export interface KnowledgeBaseArticle {
  id: number;
  title: string;
  content: string;
  excerpt?: string;
  category: KBCategory;
  tags: string[];
  status: ArticleStatus;
  author: number;
  reviewer?: number;
  publishedAt?: Date;
  lastUpdatedBy?: number;
  lastUpdatedAt?: Date;
  views: number;
  helpful: number;
  notHelpful: number;
  relatedArticles: number[];
  attachments: Attachment[];
  metadata: ArticleMetadata;
  createdAt: Date;
  
  // Relations
  authorUser?: User;
  reviewerUser?: User;
  lastUpdatedByUser?: User;
}

export interface KBCategory {
  id: number;
  name: string;
  description?: string;
  parentId?: number;
  order: number;
  articleCount: number;
  isActive: boolean;
  createdAt: Date;
  
  // Relations
  parent?: KBCategory;
}

export interface ArticleMetadata {
  readingTime: number;
  wordCount: number;
  difficulty: DifficultyLevel;
  lastReviewed?: Date;
  reviewFrequency: number;
  seo: SEOData;
}

export interface SEOData {
  title: string;
  description: string;
  keywords: string[];
  slug: string;
  canonicalUrl?: string;
}

export interface KBSearchResult {
  articles: KnowledgeBaseArticle[];
  categories: KBCategory[];
  tags: string[];
  total: number;
  query: string;
  suggestions: string[];
}

export interface KBFeedback {
  id: number;
  articleId: number;
  rating: number;
  comment?: string;
  submittedBy: number;
  helpful: boolean;
  createdAt: Date;
  
  // Relations
  article?: KnowledgeBaseArticle;
  submittedByUser?: User;
}

export interface KBSettings {
  categories: string[];
  defaultCategory: number;
  feedbackEnabled: boolean;
  ratingEnabled: boolean;
  searchEnabled: boolean;
  relatedArticles: number;
  popularArticles: number;
  reviewProcess: ReviewProcess;
}

export interface ReviewProcess {
  required: boolean;
  reviewers: number[];
  approvalThreshold: number;
  expiration: number;
}

export enum ArticleStatus {
  DRAFT = 'draft',
  REVIEW = 'review',
  PUBLISHED = 'published',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}

export enum DifficultyLevel {
  BEGINNER = 'beginner',
  INTERMEDIATE = 'intermediate',
  ADVANCED = 'advanced',
  EXPERT = 'expert'
}

export enum KBCategoryType {
  GETTING_STARTED = 'getting_started',
  HOW_TO = 'how_to',
  TROUBLESHOOTING = 'troubleshooting',
  BEST_PRACTICES = 'best_practices',
  REFERENCE = 'reference'
}