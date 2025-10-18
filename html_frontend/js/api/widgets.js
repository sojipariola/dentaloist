import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchWidgets() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch widgets');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching widgets:', error);
        throw error;
    }
}

export async function createWidget(widgetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(widgetData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create widget');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating widget:', error);
        throw error;
    }
}

export async function updateWidget(id, widgetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(widgetData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update widget');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating widget:', error);
        throw error;
    }
}

export async function deleteWidget(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete widget');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting widget:', error);
        throw error;
    }
}