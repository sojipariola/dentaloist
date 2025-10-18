// frontend/src/services/reports/reportsService.ts
// src/services/reports/reportsService.ts
import { apiClient } from '../api';
import { API_ENDPOINTS } from '../api/config';
import { Report } from './types';

const normalizeError = (err: any, fallbackMessage: string): Error => {
  if (err instanceof Error) return err;
  if (err && typeof err === 'object' && 'message' in err) {
    return new Error((err as any).message);
  }
  return new Error(fallbackMessage);
};

export class ReportsService {
  async fetchReports(params?: {
    startDate?: string;
    endDate?: string;
    type?: string;
  }): Promise<Report[]> {
    try {
      const queryString = params
        ? '?' + new URLSearchParams(params as Record<string, string>).toString()
        : '';
      return await apiClient.get(API_ENDPOINTS.REPORTS.LIST + queryString);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to fetch reports');
    }
  }

  async generateReport(data: { type: string; startDate: string; endDate: string }): Promise<Report> {
    try {
      return await apiClient.post(API_ENDPOINTS.REPORTS.GENERATE, data);
    } catch (err: any) {
      throw normalizeError(err, 'Failed to generate report');
    }
  }
}

export const reportsService = new ReportsService(); 