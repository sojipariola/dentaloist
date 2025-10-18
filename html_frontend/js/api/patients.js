import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchPatients(searchTerm = '') {
    try {
        const url = searchTerm 
            ? `${API_BASE_URL}/api/patients?search=${encodeURIComponent(searchTerm)}`
            : `${API_BASE_URL}/api/patients`;
            
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch patients');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching patients:', error);
        throw error;
    }
}

export async function createPatient(patientData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create patient');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating patient:', error);
        throw error;
    }
}

export async function updatePatient(id, patientData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update patient');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating patient:', error);
        throw error;
    }
}

export async function deletePatient(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete patient');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting patient:', error);
        throw error;
    }
}