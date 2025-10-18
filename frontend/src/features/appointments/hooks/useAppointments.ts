// src/features/appointments/hooks/useAppointments.ts
import { useState, useEffect } from 'react';
import { Appointment } from '@/types';
import { appointmentService } from '@/services/appointmentService';

export const useAppointments = (filters = {}) => {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    loadAppointments();
  }, [filters]);

  const loadAppointments = async () => {
    try {
      setIsLoading(true);
      const data = await appointmentService.getAppointments(filters);
      setAppointments(data);
    } catch (err) {
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  };

  const createAppointment = async (appointmentData: Partial<Appointment>) => {
    try {
      const newAppointment = await appointmentService.createAppointment(appointmentData);
      setAppointments(prev => [...prev, newAppointment]);
      return newAppointment;
    } catch (err) {
      setError(err as Error);
      throw err;
    }
  };

  return {
    appointments,
    isLoading,
    error,
    createAppointment,
    refresh: loadAppointments
  };
};