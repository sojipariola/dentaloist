import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchInvoices(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const url = `${API_BASE_URL}/api/invoices?${params.toString()}`;
        
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch invoices');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching invoices:', error);
        throw error;
    }
}

export async function createInvoice(invoiceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(invoiceData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create invoice');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating invoice:', error);
        throw error;
    }
}

export async function updateInvoice(id, invoiceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(invoiceData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update invoice');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating invoice:', error);
        throw error;
    }
}

export async function deleteInvoice(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete invoice');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting invoice:', error);
        throw error;
    }
}