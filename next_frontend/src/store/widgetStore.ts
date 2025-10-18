import { create } from 'zustand';
import { Widget } from '@/types/widget';

interface WidgetState {
  widgets: Widget[];
  loading: boolean;
  error: string | null;
  setWidgets: (widgets: Widget[]) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  addWidget: (widget: Widget) => void;
  updateWidget: (id: string, widget: Partial<Widget>) => void;
  removeWidget: (id: string) => void;
}

export const useWidgetStore = create<WidgetState>((set) => ({
  widgets: [],
  loading: false,
  error: null,
  setWidgets: (widgets) => set({ widgets }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  addWidget: (widget) => set((state) => ({ widgets: [...state.widgets, widget] })),
  updateWidget: (id, updatedWidget) =>
    set((state) => ({
      widgets: state.widgets.map((w) => (w.id === id ? { ...w, ...updatedWidget } : w)),
    })),
  removeWidget: (id) =>
    set((state) => ({
      widgets: state.widgets.filter((w) => w.id !== id),
    })),
}));
