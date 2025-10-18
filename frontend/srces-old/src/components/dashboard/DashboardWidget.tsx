// frontend/src/components/dashboard/DashboardWidget.tsx
'use client';

import { useEffect, useState } from 'react';
import { fetchWidgets, createWidget, updateWidget, deleteWidget } from '@/services/widgets/widgetsService';

interface Widget {
  id: string;
  title: string;
  content: string;
}

const DashboardWidget: React.FC = () => {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadWidgets = async () => {
      try {
        const data = await fetchWidgets();
        setWidgets(data);
      } catch (err) {
        setError('Failed to load widgets');
      } finally {
        setLoading(false);
      }
    };

    loadWidgets();
  }, []);

  const handleCreate = async (widgetData: Omit<Widget, 'id'>) => {
    try {
      const newWidget = await createWidget(widgetData);
      setWidgets(prev => [...prev, newWidget]);
    } catch (err) {
      setError('Failed to create widget');
    }
  };

  const handleUpdate = async (id: string, widgetData: Partial<Widget>) => {
    try {
      const updatedWidget = await updateWidget(id, widgetData);
      setWidgets(prev => prev.map(w => (w.id === id ? updatedWidget : w)));
    } catch (err) {
      setError('Failed to update widget');
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteWidget(id);
      setWidgets(prev => prev.filter(w => w.id !== id));
    } catch (err) {
      setError('Failed to delete widget');
    }
  };

  if (loading) return <div>Loading widgets...</div>;
  if (error) return <div className="text-red-500">{error}</div>;

  return (
    <div className="dashboard-widgets space-y-4">
      {widgets.map(widget => (
        <div key={widget.id} className="widget p-4 border rounded shadow">
          <h3 className="text-lg font-bold">{widget.title}</h3>
          <p>{widget.content}</p>
          <div className="mt-2 space-x-2">
            <button
              onClick={() => handleUpdate(widget.id, { title: widget.title + ' (Updated)' })}
              className="px-2 py-1 bg-blue-500 text-white rounded"
            >
              Update
            </button>
            <button
              onClick={() => handleDelete(widget.id)}
              className="px-2 py-1 bg-red-500 text-white rounded"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
      <button
        onClick={() => handleCreate({ title: 'New Widget', content: 'Widget content' })}
        className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
      >
        Add Widget
      </button>
    </div>
  );
};

export default DashboardWidget;