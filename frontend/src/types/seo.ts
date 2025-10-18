// src/types/seo.ts
export interface SEOAnalysis {
  id: number;
  url: string;
  title: string;
  metaDescription: string;
  keywords: Keyword[];
  content: ContentAnalysis;
  technical: TechnicalAnalysis;
  performance: PerformanceMetrics;
  recommendations: Recommendation[];
  score: number;
  createdAt: Date;
}

export interface Keyword {
  term: string;
  volume: number;
  difficulty: number;
  position: number;
  trend: Trend;
}

export interface ContentAnalysis {
  wordCount: number;
  readability: ReadabilityScore;
  structure: StructureAnalysis;
  relevance: RelevanceScore;
  uniqueness: number;
}

export interface TechnicalAnalysis {
  mobile: MobileScore;
  speed: SpeedScore;
  security: SecurityScore;
  accessibility: AccessibilityScore;
  crawlability: CrawlabilityScore;
}

export interface PerformanceMetrics {
  loadTime: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  totalBlockingTime: number;
}

export interface Recommendation {
  type: RecommendationType;
  priority: Priority;
  description: string;
  action: string;
  impact: number;
}

export interface SEOSettings {
  meta: MetaSettings;
  sitemap: SitemapSettings;
  robots: RobotsSettings;
  analytics: AnalyticsSettings;
  social: SocialSettings;
}

export interface MetaSettings {
  titleTemplate: string;
  descriptionTemplate: string;
  defaultImage: string;
  canonical: boolean;
}

export interface SitemapSettings {
  enabled: boolean;
  frequency: SitemapFrequency;
  priority: number;
  include: string[];
  exclude: string[];
}

export interface RobotsSettings {
  rules: RobotRule[];
  sitemap: string;
  crawlDelay: number;
}

export interface AnalyticsSettings {
  google: GoogleAnalytics;
  tracking: TrackingSettings;
  goals: Goal[];
}

export interface SocialSettings {
  openGraph: OpenGraphSettings;
  twitter: TwitterSettings;
  facebook: FacebookSettings;
}

export enum Trend {
  UP = 'up',
  DOWN = 'down',
  STABLE = 'stable'
}

export enum RecommendationType {
  CONTENT = 'content',
  TECHNICAL = 'technical',
  PERFORMANCE = 'performance',
  SECURITY = 'security'
}

export enum Priority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum SitemapFrequency {
  ALWAYS = 'always',
  HOURLY = 'hourly',
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  YEARLY = 'yearly',
  NEVER = 'never'
}