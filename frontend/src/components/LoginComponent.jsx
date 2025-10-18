// LoginComponent.jsx
import React, { useState } from 'react';
import authService from '../services/authService';

const LoginComponent = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      console.log('🔄 Starting login process...');
      const result = await authService.login(email, password);
      console.log('✅ Login successful, user:', result.user);
      
      // After successful login, fetch appointments
      try {
        console.log('📅 Fetching appointments...');
        const appointments = await authService.getAppointments('org_123');
        console.log('✅ Appointments fetched:', appointments);
        
        // Redirect to dashboard or update state
        window.location.href = '/dashboard';
      } catch (appointmentError) {
        console.error('❌ Failed to fetch appointments:', appointmentError);
        // Still redirect since login was successful
        window.location.href = '/dashboard';
      }
      
    } catch (err) {
      console.error('❌ Login failed:', err);
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h2>Login to Dentaloist</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            placeholder="sojipariola@gmail.com"
          />
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            placeholder="Soji1111"
          />
        </div>
        
        <button 
          type="submit" 
          disabled={loading}
          style={{ 
            width: '100%', 
            padding: '10px', 
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
        
        {error && (
          <div style={{ 
            color: 'red', 
            marginTop: '10px', 
            padding: '10px', 
            backgroundColor: '#ffe6e6',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}
      </form>
    </div>
  );
};

export default LoginComponent;