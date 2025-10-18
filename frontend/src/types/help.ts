// src/types/help.ts
export interface HelpArticle {
  id: number;
  title: string;
  content: string;
  category: HelpCategory;
  tags: string[];
  status: ArticleStatus;
  views: number;
  helpful: number;
  notHelpful: number;
  author: number;
  lastUpdatedBy?: number;
  lastUpdatedAt?: Date;
  relatedArticles: number[];
  attachments: Attachment[];
  createdAt: Date;
  
  // Relations
  authorUser?: User;
  lastUpdatedByUser?: User;
}

export interface HelpCategory {
  id: number;
  name: string;
  description?: string;
  parentId?: number;
  order: number;
  articles: number;
  isActive: boolean;
  createdAt: Date;
  
  // Relations
  parent?: HelpCategory;
}

export interface HelpSearchResult {
  articles: HelpArticle[];
  categories: HelpCategory[];
  tags: string[];
  total: number;
  query: string;
  suggestions: string[];
}

export interface HelpFeedback {
  id: number;
  articleId: number;
  rating: number;
  comment?: string;
  submittedBy: number;
  helpful: boolean;
  createdAt: Date;
  
  // Relations
  article?: HelpArticle;
  submittedByUser?: User;
}

export interface HelpSettings {
  categories: string[];
  defaultCategory: number;
  feedbackEnabled: boolean;
  ratingEnabled: boolean;
  searchEnabled: boolean;
  relatedArticles: number;
  popularArticles: number;
}

export enum ArticleStatus {
  DRAFT = 'draft',
  PUBLISHED = 'published',
  ARCHIVED = 'archived',
  DELETED = 'deleted'
}

export enum HelpCategoryType {
  GETTING_STARTED = 'getting_started',
  USER_GUIDE = 'user_guide',
  TROUBLESHOOTING = 'troubleshooting',
  FAQ = 'faq',
  RELEASE_NOTES = 'release_notes'
}