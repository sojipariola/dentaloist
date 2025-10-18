'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

// Mock appointment data
const mockAppointments = [
  { id: 1, time: '9:00 AM', patient: 'John Smith', type: 'Cleaning' },
  { id: 2, time: '10:30 AM', patient: 'Jane Doe', type: 'Checkup' },
  { id: 3, time: '1:00 PM', patient: 'Bob Johnson', type: 'Filling' },
  { id: 4, time: '3:00 PM', patient: 'Alice Brown', type: 'Consultation' },
];

export function AppointmentCalendar() {
  const [selectedDate, setSelectedDate] = useState(new Date());

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold">Today, {selectedDate.toLocaleDateString()}</h3>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">←</Button>
          <Button variant="outline" size="sm">Today</Button>
          <Button variant="outline" size="sm">→</Button>
        </div>
      </div>
      
      <div className="space-y-2">
        {mockAppointments.map((appt) => (
          <Card key={appt.id}>
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-semibold">{appt.time}</h4>
                  <p className="text-sm text-muted-foreground">{appt.patient}</p>
                  <p className="text-xs text-muted-foreground">{appt.type}</p>
                </div>
                <Button size="sm">View</Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
