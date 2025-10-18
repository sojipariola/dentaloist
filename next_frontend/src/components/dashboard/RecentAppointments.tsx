// src/components/dashboard/RecentAppointments.tsx

'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Clock, User, MapPin } from 'lucide-react';
import { appointmentsApi } from '@/lib/api';
import { Appointment } from '@/types';

interface RecentAppointmentsProps {
  organizationId?: string;
}

const statusColors = {
  scheduled: 'bg-blue-100 text-blue-800',
  confirmed: 'bg-green-100 text-green-800',
  'in-progress': 'bg-amber-100 text-amber-800',
  completed: 'bg-gray-100 text-gray-800',
  cancelled: 'bg-red-100 text-red-800',
};

export function RecentAppointments({ organizationId }: RecentAppointmentsProps) {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchAppointments = async () => {
      try {
        const response = await appointmentsApi.getToday(organizationId);
        setAppointments(response.data.slice(0, 5)); // Get only first 5 appointments
      } catch (error) {
        console.error('Failed to fetch appointments:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (organizationId) {
      fetchAppointments();
    }
  }, [organizationId]);

  if (isLoading) {
    return (
      <motion.div
        className="bg-white rounded-xl p-6 shadow-sm"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Today's Appointments</h3>
          <div className="animate-pulse bg-gray-200 h-6 w-20 rounded"></div>
        </div>
        <div className="space-y-4">
          {[1, 2, 3].map((item) => (
            <div key={item} className="animate-pulse bg-gray-100 h-20 rounded-lg"></div>
          ))}
        </div>
      </motion.div>
    );
  }

  return (
    <motion.div
      className="bg-white rounded-xl p-6 shadow-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900">Today's Appointments</h3>
        <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
          View All
        </button>
      </div>

      <div className="space-y-4">
        {appointments.map((appointment, index) => (
          <motion.div
            key={appointment.id}
            className="flex items-center justify-between p-4 border rounded-lg hover:shadow-md transition-shadow"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                <Calendar className="w-6 h-6 text-blue-600" />
              </div>
              <div>
                <h4 className="font-medium text-gray-900">{appointment.title}</h4>
                <div className="flex items-center space-x-4 text-sm text-gray-600">
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
            </div>

            <div className="flex items-center space-x-4">
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[appointment.status as keyof typeof statusColors]}`}>
                {appointment.status}
              </span>
              <div className="text-right">
                <p className="font-medium text-gray-900">{appointment.type}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {appointments.length === 0 && (
        <div className="text-center py-8">
          <Calendar className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">No appointments scheduled for today</p>
        </div>
      )}
    </motion.div>
  );
}