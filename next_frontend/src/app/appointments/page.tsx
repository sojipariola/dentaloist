// src/app/appointments/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { Plus, Calendar, Clock, User } from 'lucide-react';
import { appointmentsApi } from '@/lib/api';
import { useAuth } from '@/lib/hooks/useAuth';
import { Appointment } from '@/types';

export default function Appointments() {
  const { user } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await appointmentsApi.getAll(user?.organization_id);
        setAppointments(response.data);
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (user) {
      fetchAppointments();
    }
  }, [user]);

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Appointments</h1>
        <button className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          <Plus className="w-4 h-4" />
          <span>New Appointment</span>
        </button>
      </div>

      <div className="grid gap-4">
        {appointments.map((appointment) => (
          <div key={appointment.id} className="bg-white p-6 rounded-lg shadow border">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">{appointment.title}</h3>
                <p className="text-gray-600">{appointment.description}</p>
                
                <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                  <span className="flex items-center">
                    <Calendar className="w-4 h-4 mr-1" />
                    {new Date(appointment.start_time).toLocaleDateString()}
                  </span>
                  <span className="flex items-center">
                    <Clock className="w-4 h-4 mr-1" />
                    {new Date(appointment.start_time).toLocaleTimeString()}
                  </span>
                  <span className="flex items-center">
                    <User className="w-4 h-4 mr-1" />
                    {appointment.patient.first_name} {appointment.patient.last_name}
                  </span>
                </div>
              </div>

              <div className="text-right">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  appointment.status === 'scheduled' ? 'bg-blue-100 text-blue-800' :
                  appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' :
                  appointment.status === 'completed' ? 'bg-gray-100 text-gray-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {appointment.status}
                </span>
                <p className="text-lg font-semibold text-gray-900 mt-2">
                  ${appointment.cost}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {appointments.length === 0 && (
        <div className="text-center py-12">
          <Calendar className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">No appointments scheduled</p>
        </div>
      )}
    </div>
  );
}