// src/types/analytics.ts
export interface AnalyticsData {
  metrics: AnalyticsMetrics;
  trends: AnalyticsTrends;
  comparisons: AnalyticsComparisons;
  predictions: AnalyticsPredictions;
}

export interface AnalyticsMetrics {
  totalPatients: number;
  totalAppointments: number;
  totalRevenue: number;
  averageWaitTime: number;
  patientSatisfaction: number;
  occupancyRate: number;
}

export interface AnalyticsTrends {
  revenue: TrendData;
  appointments: TrendData;
  newPatients: TrendData;
  cancellationRate: TrendData;
}

export interface TrendData {
  current: number;
  previous: number;
  change: number;
  changePercentage: number;
  dataPoints: DataPoint[];
}

export interface DataPoint {
  date: Date;
  value: number;
}

export interface AnalyticsComparisons {
  byProvider: ProviderComparison[];
  byService: ServiceComparison[];
  byLocation: LocationComparison[];
}

export interface ProviderComparison {
  providerId: number;
  providerName: string;
  appointments: number;
  revenue: number;
  satisfaction: number;
}

export interface ServiceComparison {
  service: string;
  count: number;
  revenue: number;
  averageDuration: number;
}

export interface LocationComparison {
  location: string;
  appointments: number;
  revenue: number;
  utilization: number;
}

export interface AnalyticsPredictions {
  demandForecast: DemandForecast;
  revenueProjection: RevenueProjection;
  resourceAllocation: ResourceAllocation;
}

export interface DemandForecast {
  nextWeek: number;
  nextMonth: number;
  nextQuarter: number;
  confidence: number;
}

export interface RevenueProjection {
  nextWeek: number;
  nextMonth: number;
  nextQuarter: number;
  growthRate: number;
}

export interface ResourceAllocation {
  recommendedStaff: number;
  optimalSchedule: ScheduleRecommendation;
  inventoryRequirements: InventoryRecommendation;
}

export interface ScheduleRecommendation {
  peakHours: string[];
  suggestedShifts: ShiftSuggestion[];
}

export interface ShiftSuggestion {
  day: string;
  start: string;
  end: string;
  staffCount: number;
}

export interface InventoryRecommendation {
  items: InventoryItemRecommendation[];
  totalCost: number;
}

export interface InventoryItemRecommendation {
  itemId: number;
  itemName: string;
  quantity: number;
  cost: number;
}