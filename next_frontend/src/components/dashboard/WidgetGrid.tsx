// src/components/dashboard/WidgetGrid.tsx
'use client';

import { motion } from 'framer-motion';

interface Widget {
  id: string;
  type: string;
  title: string;
  position: { x: number; y: number; w: number; h: number };
  dataSource: any;
  refreshInterval: number;
}

const mockWidgets: Widget[] = [
  {
    id: '1',
    type: 'stats_card',
    title: 'Total Patients',
    position: { x: 0, y: 0, w: 2, h: 2 },
    dataSource: {},
    refreshInterval: 300,
  },
  {
    id: '2',
    type: 'stats_card',
    title: 'Today\'s Appointments', // Fixed: escaped apostrophe
    position: { x: 2, y: 0, w: 2, h: 2 },
    dataSource: {},
    refreshInterval: 300,
  },
  {
    id: '3',
    type: 'stats_card',
    title: 'Monthly Revenue',
    position: { x: 4, y: 0, w: 2, h: 2 },
    dataSource: {},
    refreshInterval: 300,
  },
  {
    id: '4',
    type: 'chart',
    title: 'Patient Visits',
    position: { x: 0, y: 2, w: 4, h: 3 },
    dataSource: {},
    refreshInterval: 300,
  },
];

export function WidgetGrid() {
  return (
    <div className="grid grid-cols-6 gap-4 p-4">
      {mockWidgets.map((widget, index) => (
        <motion.div
          key={widget.id}
          className="bg-white rounded-xl p-4 shadow-sm border col-span-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          style={{
            gridColumn: `span ${widget.position.w} / span ${widget.position.w}`,
            gridRow: `span ${widget.position.h} / span ${widget.position.h}`,
          }}
        >
          <h3 className="font-semibold text-gray-900 mb-2">{widget.title}</h3>
          <div className="text-2xl font-bold text-blue-600">
            {widget.type === 'stats_card' && '1,247'}
          </div>
          {widget.type === 'chart' && (
            <div className="h-32 bg-gray-100 rounded-lg flex items-center justify-center">
              <span className="text-gray-500">Chart Preview</span>
            </div>
          )}
        </motion.div>
      ))}
    </div>
  );
}