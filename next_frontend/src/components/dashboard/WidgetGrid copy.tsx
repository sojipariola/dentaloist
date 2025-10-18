// next_frontend/src/components/dashboard/WidgetGrid.tsx

'use client';

import { useEffect, useState } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout'; //
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { Widget } from '@/types/widget';
import { StatCard } from './StatCard';
import { Card, CardContent } from '@/components/ui/card';

const ResponsiveGridLayout = WidthProvider(Responsive);
async function fetchWidgets(): Promise<Widget[]> {
  const response = await fetch('/api/dashboard/widgets');
  if (!response.ok) {
    throw new Error('Failed to fetch widgets');
  }
  return response.json();
}

export function WidgetGrid() {
  const [widgets, setWidgets] = useState<Widget[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadWidgets = async () => {
      try {
        const data = await fetchWidgets();
        setWidgets(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadWidgets();
  }, []);

  if (loading) return <div className="p-4">Loading widgets...</div>;

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
        return (
          <Card key={widget.id}>
            <CardContent className="p-4">
              <h3 className="font-semibold">{widget.title}</h3>
              <p>Unknown widget type: {widget.type}</p>
            </CardContent>
          </Card>
        );
    }
  };

  return (
    <div className="p-2">
      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: layout }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
        rowHeight={100}
        width={1200}
        draggableHandle=".drag-handle"
      >
        {widgets.map(renderWidget)}
      </ResponsiveGridLayout>
    </div>
  );
}
