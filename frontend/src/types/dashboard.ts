// src/types/dashboard.ts
export interface Dashboard {
  userId: number;
  layout: DashboardLayout;
  widgets: DashboardWidget[];
  createdAt: Date;
  updatedAt: Date;
}

export interface DashboardLayout {
  type: 'grid' | 'free';
  columns: number;
  breakpoints: LayoutBreakpoints;
}

export interface LayoutBreakpoints {
  sm: number;
  md: number;
  lg: number;
  xl: number;
}

export interface DashboardWidget {
  id: string;
  type: WidgetType;
  title: string;
  description?: string;
  size: WidgetSize;
  position: WidgetPosition;
  dataSource: WidgetDataSource;
  refreshInterval: number;
  filters?: WidgetFilters;
  isVisible: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface WidgetPosition {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface WidgetDataSource {
  endpoint: string;
  method: 'GET' | 'POST';
  params: Record<string, any>;
  transform?: string;
}

export interface WidgetFilters {
  dateRange?: DateRange;
  categories?: string[];
  metrics?: string[];
}

export enum WidgetType {
  STATS_CARD = 'stats_card',
  LINE_CHART = 'line_chart',
  BAR_CHART = 'bar_chart',
  PIE_CHART = 'pie_chart',
  TABLE = 'table',
  CALENDAR = 'calendar',
  ACTIVITY_FEED = 'activity_feed'
}

export enum WidgetSize {
  SMALL = 'small',
  MEDIUM = 'medium',
  LARGE = 'large',
  XLARGE = 'xlarge'
}