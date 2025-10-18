// src/app/dashboard/dentist/page.tsx - Dentist Dashboard
'use client';

import { useState, useEffect } from 'react';
import { Calendar, Users, Clock, Stethoscope } from 'lucide-react';
import { appointmentsApi } from '@/lib/api';
import { useAuth } from '@/lib/hooks/useAuth';

export default function DentistDashboard() {
  const { user } = useAuth();
  const [todayAppointments, setTodayAppointments] = useState([]);
  const [upcomingAppointments, setUpcomingAppointments] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      if (user?.organization_id) {
        try {
          const [todayResponse, upcomingResponse] = await Promise.all([
            appointmentsApi.getToday(user.organization_id),
            appointmentsApi.getUpcoming(user.organization_id)
          ]);
          
          setTodayAppointments(todayResponse.data);
          setUpcomingAppointments(upcomingResponse.data);
        } catch (error) {
          console.error('Failed to fetch dentist data:', error);
        }
      }
    };

    fetchData();
  }, [user]);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dentist Dashboard</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Clock className="w-5 h-5 mr-2 text-blue-600" />
            Today's Appointments
          </h2>
          <div className="space-y-3">
            {todayAppointments.slice(0, 5).map((appt: any) => (
              <div key={appt.id} className="border-b pb-3 last:border-b-0">
                <p className="font-medium">{appt.patient.first_name} {appt.patient.last_name}</p>
                <p className="text-sm text-gray-600">{appt.type} • {new Date(appt.start_time).toLocaleTimeString()}</p>
              </div>
            ))}
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <Calendar className="w-5 h-5 mr-2 text-green-600" />
            Upcoming Appointments
          </h2>
          <div className="space-y-3">
            {upcomingAppointments.slice(0, 5).map((appt: any) => (
              <div key={appt.id} className="border-b pb-3 last:border-b-0">
                <p className="font-medium">{appt.patient.first_name} {appt.patient.last_name}</p>
                <p className="text-sm text-gray-600">{appt.type} • {new Date(appt.start_time).toLocaleDateString()}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}