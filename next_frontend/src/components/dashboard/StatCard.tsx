'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Widget } from '@/types/widget';

interface StatCardProps {
  widget: Widget;
}

export function StatCard({ widget }: StatCardProps) {
  // In real app, fetch data from widget.dataSource.endpoint
  const mockValue = widget.title.includes('Patients') ? '1,247' : 
                    widget.title.includes('Appointments') ? '12' : 
                    widget.title.includes('Revenue') ? '$18,420' : 'N/A';

  return (
    <Card className="h-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{widget.title}</CardTitle>
        <div className="drag-handle cursor-move">⋮⋮</div>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{mockValue}</div>
        <p className="text-xs text-muted-foreground">+20.1% from last month</p>
      </CardContent>
    </Card>
  );
}
