// src/contexts/WidgetContext.tsx
'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { WidgetConfig, CreateWidgetDto, UpdateWidgetDto } from '@/types/widget';
import { widgetsService } from '@/services/widgets/widgetsService';
import { useAuth } from './AuthContext';

interface WidgetContextType {
  widgets: WidgetConfig[];
  isLoading: boolean;
  error: string | null;
  addWidget: (widgetData: CreateWidgetDto) => Promise<void>;
  updateWidget: (widgetId: string, widgetData: UpdateWidgetDto) => Promise<void>;
  deleteWidget: (widgetId: string) => Promise<void>;
  refreshWidgets: () => Promise<void>;
  reorderWidgets: (widgets: WidgetConfig[]) => void;
}

const WidgetContext = createContext<WidgetContextType | undefined>(undefined);

export const useWidgets = (): WidgetContextType => {
  const context = useContext(WidgetContext);
  if (context === undefined) {
    throw new Error('useWidgets must be used within a WidgetProvider');
  }
  return context;
};

interface WidgetProviderProps {
  children: ReactNode;
}

export const WidgetProvider: React.FC<WidgetProviderProps> = ({ children }) => {
  const [widgets, setWidgets] = useState<WidgetConfig[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  const loadWidgets = async () => {
    if (!isAuthenticated) {
      setWidgets([]);
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      const response = await widgetsService.getWidgets();
      setWidgets(response.widgets);
    } catch (err: any) {
      setError(err.message);
      console.error('Failed to load widgets:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const addWidget = async (widgetData: CreateWidgetDto) => {
    try {
      const response = await widgetsService.createWidget(widgetData);
      setWidgets(prev => [...prev, response.widget]);
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const updateWidget = async (widgetId: string, widgetData: UpdateWidgetDto) => {
    try {
      const response = await widgetsService.updateWidget(widgetId, widgetData);
      setWidgets(prev => prev.map(w => 
        w.id === widgetId ? response.widget : w
      ));
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const deleteWidget = async (widgetId: string) => {
    try {
      await widgetsService.deleteWidget(widgetId);
      setWidgets(prev => prev.filter(w => w.id !== widgetId));
    } catch (err: any) {
      throw new Error(err.message);
    }
  };

  const reorderWidgets = (newWidgets: WidgetConfig[]) => {
    setWidgets(newWidgets);
    // Here you would typically save the new order to the backend
  };

  useEffect(() => {
    loadWidgets();
  }, [isAuthenticated]);

  const value: WidgetContextType = {
    widgets,
    isLoading,
    error,
    addWidget,
    updateWidget,
    deleteWidget,
    refreshWidgets: loadWidgets,
    reorderWidgets
  };

  return (
    <WidgetContext.Provider value={value}>
      {children}
    </WidgetContext.Provider>
  );
};