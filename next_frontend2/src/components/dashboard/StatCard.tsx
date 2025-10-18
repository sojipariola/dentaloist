'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Widget } from '@/types/widget';

interface StatCardProps {
  widget: Widget;
}

export function StatCard({ widget }: StatCardProps) {
  // In real app, fetch data from widget.dataSource.endpoint
  const mockValue = widget.title.includes('Patients') ? '1,247' : 
                    widget.title.includes('Appointments') ? '12' : '$18,420';

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="text-sm font-medium">{widget.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{mockValue}</div>
        <p className="text-xs text-muted-foreground">+20.1% from last month</p>
      </CardContent>
    </Card>
  );
}