// src/types/widget.ts
export interface WidgetConfig {
  id: string;
  type: WidgetType;
  title: string;
  description?: string;
  size: WidgetSize;
  position?: WidgetPosition;
  dataSource: WidgetDataSource;
  refreshInterval?: number; // in seconds
  filters?: Record<string, any>;
  isVisible: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface WidgetPosition {
  x: number;
  y: number;
  w: number;
  h: number;
}

export enum WidgetType {
  STATS_CARD = 'stats_card',
  LINE_CHART = 'line_chart',
  BAR_CHART = 'bar_chart',
  PIE_CHART = 'pie_chart',
  TABLE = 'table',
  CALENDAR = 'calendar',
  ACTIVITY_FEED = 'activity_feed',
  QUICK_ACTIONS = 'quick_actions'
}

export enum WidgetSize {
  SMALL = 'small',
  MEDIUM = 'medium',
  LARGE = 'large',
  XLARGE = 'xlarge'
}

export interface WidgetDataSource {
  type: 'api' | 'static' | 'function';
  endpoint?: string;
  method?: 'GET' | 'POST';
  params?: Record<string, any>;
  staticData?: any;
  dataFunction?: string;
}

export interface WidgetData {
  widgetId: string;
  data: any;
  lastUpdated: string;
  isLoading: boolean;
  error?: string;
}

export interface CreateWidgetDto {
  type: WidgetType;
  title: string;
  description?: string;
  size: WidgetSize;
  dataSource: WidgetDataSource;
  refreshInterval?: number;
  filters?: Record<string, any>;
}

export interface UpdateWidgetDto extends Partial<CreateWidgetDto> {
  isVisible?: boolean;
}