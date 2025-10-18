import { API_BASE_URL, DEFAULT_HEADERS } from './config.js';

export async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            throw new Error('Login failed');
        }
        
        const data = await response.json();
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('token', data.token);
        return data.user;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

export async function register(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        
        const data = await response.json();
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('token', data.token);
        return data.user;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

export function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

export function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

export function getToken() {
    return localStorage.getItem('token');
}

export function isAuthenticated() {
    return !!getToken();
}