// src/services/widgets/widgetsService.ts
import { apiClient } from '../api';
import { 
  WidgetConfig, 
  WidgetData, 
  CreateWidgetDto, 
  UpdateWidgetDto,
  WidgetType 
} from '@/types/widget';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (typeof err === 'string') return new Error(err);
  if (err?.message) return new Error(err.message);
  return new Error(fallbackMessage);
};

export const widgetsService = {
  // Get all widgets for current user
  async getWidgets(): Promise<{ widgets: WidgetConfig[] }> {
    try {
      return await apiClient.get('/api/widgets');
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch widgets');
    }
  },

  // Get specific widget
  async getWidget(widgetId: string): Promise<{ widget: WidgetConfig }> {
    try {
      return await apiClient.get(`/api/widgets/${widgetId}`);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch widget');
    }
  },

  // Create new widget
  async createWidget(widgetData: CreateWidgetDto): Promise<{ widget: WidgetConfig }> {
    try {
      return await apiClient.post('/api/widgets', widgetData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to create widget');
    }
  },

  // Update widget
  async updateWidget(widgetId: string, widgetData: UpdateWidgetDto): Promise<{ widget: WidgetConfig }> {
    try {
      return await apiClient.put(`/api/widgets/${widgetId}`, widgetData);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to update widget');
    }
  },

  // Delete widget
  async deleteWidget(widgetId: string): Promise<{ message: string }> {
    try {
      return await apiClient.delete(`/api/widgets/${widgetId}`);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to delete widget');
    }
  },

  // Get widget data
  async getWidgetData(widgetId: string, params?: Record<string, any>): Promise<WidgetData> {
    try {
      const response = await apiClient.get(`/api/widgets/${widgetId}/data`, params);
      return {
        widgetId,
        data: response.data,
        lastUpdated: new Date().toISOString(),
        isLoading: false
      };
    } catch (err: any) {
      return {
        widgetId,
        data: null,
        lastUpdated: new Date().toISOString(),
        isLoading: false,
        error: normalizeError(err, 'Failed to fetch widget data').message
      };
    }
  },

  // Refresh widget data
  async refreshWidgetData(widgetId: string): Promise<WidgetData> {
    return this.getWidgetData(widgetId);
  },

  // Get default widgets for new users
  getDefaultWidgets(): CreateWidgetDto[] {
    return [
      {
        type: WidgetType.STATS_CARD,
        title: 'Total Patients',
        size: WidgetSize.SMALL,
        dataSource: {
          type: 'api',
          endpoint: '/api/dashboard/stats',
          method: 'GET'
        }
      },
      {
        type: WidgetType.STATS_CARD,
        title: 'Today\'s Appointments',
        size: WidgetSize.SMALL,
        dataSource: {
          type: 'api',
          endpoint: '/api/dashboard/stats',
          method: 'GET'
        }
      },
      {
        type: WidgetType.STATS_CARD,
        title: 'Monthly Revenue',
        size: WidgetSize.SMALL,
        dataSource: {
          type: 'api',
          endpoint: '/api/dashboard/stats',
          method: 'GET'
        }
      },
      {
        type: WidgetType.BAR_CHART,
        title: 'Appointments by Status',
        size: WidgetSize.MEDIUM,
        dataSource: {
          type: 'api',
          endpoint: '/api/appointments/stats',
          method: 'GET',
          params: { groupBy: 'status' }
        }
      },
      {
        type: WidgetType.LINE_CHART,
        title: 'Revenue Trend',
        size: WidgetSize.MEDIUM,
        dataSource: {
          type: 'api',
          endpoint: '/api/billing/stats',
          method: 'GET',
          params: { period: 'monthly' }
        }
      },
      {
        type: WidgetType.TABLE,
        title: 'Recent Appointments',
        size: WidgetSize.LARGE,
        dataSource: {
          type: 'api',
          endpoint: '/api/appointments',
          method: 'GET',
          params: { limit: 5, sort: 'start_time:desc' }
        }
      }
    ];
  }
};