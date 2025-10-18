'use client';

import { useEffect, useState } from 'react';
import { Widget } from '@/types/widget';
import { StatCard } from './StatCard';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

export function WidgetGrid() {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadWidgets = async () => {
      try {
        const data = await widgetApi.getAll();
        setWidgets(data);
      } catch (err) {
        console.error(err);
        // Mock for demo
        setWidgets([
          { id: '1', type: 'stats_card', title: 'Total Patients', position: { x: 0, y: 0, w: 2, h: 2 }, dataSource: {}, refreshInterval: 300, isVisible: true, size: 'medium' },
          { id: '2', type: 'stats_card', title: 'Today’s Appointments', position: { x: 2, y: 0, w: 2, h: 2 }, dataSource: {}, refreshInterval: 300, isVisible: true, size: 'medium' },
        ]);
      } finally {
        setLoading(false);
      }
    };
    loadWidgets();
  }, []);

  if (loading) return <div>Loading widgets...</div>;

  const layout = widgets.map(w => ({
    i: w.id,
    x: w.position.x,
    y: w.position.y,
    w: w.position.w,
    h: w.position.h,
    static: false,
  }));

  const renderWidget = (widget: Widget) => {
    switch(widget.type) {
      case 'stats_card':
        return <StatCard key={widget.id} widget={widget} />;
      default:
        return <div key={widget.id}>Unknown widget type: {widget.type}</div>;
    }
  };

  return (
    <div className="p-4">
      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: layout }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
        rowHeight={100}
        width={1200}
      >
        {widgets.map(renderWidget)}
      </ResponsiveGridLayout>
    </div>
  );
}