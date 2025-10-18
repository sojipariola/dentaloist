import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error;
    }
}

export async function createUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create user');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating user:', error);
        throw error;
    }
}

export async function updateUser(id, userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update user');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating user:', error);
        throw error;
    }
}

export async function deleteUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete user');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting user:', error);
        throw error;
    }
}