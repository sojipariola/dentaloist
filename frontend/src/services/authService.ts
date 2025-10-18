// authService.js
class AuthService {
  constructor() {
    this.baseURL = 'http://127.0.0.1:5000'; // Your backend URL
  }

  async login(email, password) {
    console.log('🔐 Attempting login...');
    
    const response = await fetch(`${this.baseURL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        email: email, 
        password: password 
      }),
    });

    console.log('📡 Login response status:', response.status);

    if (response.ok) {
      const data = await response.json();
      console.log('✅ Login successful:', data);
      
      // Store the token and user data
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      return data;
    } else {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      console.error('❌ Login failed:', response.status, errorData);
      throw new Error(errorData.error || `Login failed: ${response.status}`);
    }
  }

  getAuthHeader() {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn('⚠️ No token found in localStorage');
    }
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  async makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('token');
    
    if (!token) {
      console.error('❌ No authentication token available');
      this.redirectToLogin();
      throw new Error('Authentication required');
    }

    const fullUrl = url.startsWith('http') ? url : `${this.baseURL}${url}`;
    
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    };

    console.log('📤 Making authenticated request:', fullUrl);

    try {
      const response = await fetch(fullUrl, {
        ...options,
        headers,
      });

      console.log('📥 Response status:', response.status);

      if (response.status === 401) {
        console.warn('🔐 Token expired or invalid');
        this.logout();
        this.redirectToLogin();
        throw new Error('Authentication expired');
      }

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Request failed: ${response.status} - ${errorText}`);
      }

      return response;
    } catch (error) {
      console.error('❌ Request error:', error);
      throw error;
    }
  }

  async getAppointments(organizationId) {
    try {
      const todayResponse = await this.makeAuthenticatedRequest(
        `/api/appointments/today?organization_id=${organizationId}`
      );
      const upcomingResponse = await this.makeAuthenticatedRequest(
        `/api/appointments/upcoming?organization_id=${organizationId}`
      );

      const today = await todayResponse.json();
      const upcoming = await upcomingResponse.json();

      return {
        today,
        upcoming
      };
    } catch (error) {
      console.error('Failed to fetch appointments:', error);
      throw error;
    }
  }

  redirectToLogin() {
    if (window.location.pathname !== '/login') {
      console.log('🔄 Redirecting to login...');
      window.location.href = '/login';
    }
  }

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    console.log('👋 User logged out');
  }

  isAuthenticated() {
    const token = localStorage.getItem('token');
    return !!token;
  }

  getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
}

export default new AuthService();