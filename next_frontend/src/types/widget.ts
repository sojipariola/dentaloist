export interface WidgetPosition {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface Widget {
  id: string;
  user_id: number;
  type: string;
  title: string;
  description?: string;
  size: string;
  position: WidgetPosition;
  width: number;
  height: number;
  dataSource: any;
  refreshInterval: number;
  filters?: any;
  isVisible: boolean;
  createdAt: string;
  updatedAt: string;
}
