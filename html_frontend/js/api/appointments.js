import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchAppointments(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const url = `${API_BASE_URL}/api/appointments?${params.toString()}`;
        
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch appointments');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching appointments:', error);
        throw error;
    }
}

export async function createAppointment(appointmentData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(appointmentData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating appointment:', error);
        throw error;
    }
}

export async function updateAppointment(id, appointmentData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(appointmentData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating appointment:', error);
        throw error;
    }
}

export async function cancelAppointment(id, reason) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments/${id}/cancel`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ reason })
        });
        
        if (!response.ok) {
            throw new Error('Failed to cancel appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error canceling appointment:', error);
        throw error;
    }
}