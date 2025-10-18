// AppointmentsComponent.jsx
import React, { useState, useEffect } from 'react';
import appointmentsService from '../services/appointmentsService';
import authService from '../services/authService';

const AppointmentsComponent = () => {
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);
  const organizationId = 'org_123'; // This should come from your app context

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      setLoading(true);
      const [upcoming, today] = await Promise.all([
        appointmentsService.getUpcomingAppointments(organizationId),
        appointmentsService.getTodayAppointments(organizationId)
      ]);
      
      // Process your data here
      setAppointments([...upcoming, ...today]);
    } catch (error) {
      console.error('Failed to load appointments:', error);
      // Handle error (redirect to login, show message, etc.)
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Appointments</h2>
      {/* Render your appointments */}
    </div>
  );
};

export default AppointmentsComponent;