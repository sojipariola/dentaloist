// src/services/appointmentService.ts
// appointmentsService.js
import authService from './authService';

class AppointmentsService {
  async getUpcomingAppointments(organizationId) {
    const response = await authService.makeAuthenticatedRequest(
      `/api/appointments/upcoming?organization_id=${organizationId}`
    );
    
    if (response && response.ok) {
      return await response.json();
    }
    throw new Error('Failed to fetch appointments');
  }

  async getTodayAppointments(organizationId) {
    const response = await authService.makeAuthenticatedRequest(
      `/api/appointments/today?organization_id=${organizationId}`
    );
    
    if (response && response.ok) {
      return await response.json();
    }
    throw new Error('Failed to fetch today appointments');
  }
}

export default new AppointmentsService();


