// src/hooks/useWidgetData.ts
import { useState, useEffect, useCallback } from 'react';
import { WidgetData, WidgetConfig } from '@/types/widget';
import { widgetsService } from '@/services/widgets/widgetsService';

export const useWidgetData = (widget: WidgetConfig) => {
  const [widgetData, setWidgetData] = useState<WidgetData>({
    widgetId: widget.id,
    data: null,
    lastUpdated: '',
    isLoading: true,
    error: undefined
  });

  const fetchData = useCallback(async () => {
    if (!widget.isVisible) return;

    setWidgetData(prev => ({ ...prev, isLoading: true, error: undefined }));

    try {
      const data = await widgetsService.getWidgetData(widget.id, widget.filters);
      setWidgetData(data);
    } catch (error) {
      setWidgetData(prev => ({
        ...prev,
        isLoading: false,
        error: error instanceof Error ? error.message : 'Failed to fetch data'
      }));
    }
  }, [widget.id, widget.isVisible, widget.filters]);

  // Initial fetch
  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // Set up refresh interval
  useEffect(() => {
    if (!widget.refreshInterval || !widget.isVisible) return;

    const interval = setInterval(fetchData, widget.refreshInterval * 1000);
    return () => clearInterval(interval);
  }, [widget.refreshInterval, widget.isVisible, fetchData]);

  return {
    data: widgetData,
    refresh: fetchData,
    isLoading: widgetData.isLoading,
    error: widgetData.error
  };
};