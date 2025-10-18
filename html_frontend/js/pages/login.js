import { login } from '../auth.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        try {
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Logging in...';
            submitBtn.disabled = true;
            
            // Attempt login
            const user = await login(email, password);
            
            // Redirect based on role
            const rolePageMap = {
                'dentist': 'dashboard/dentist/appointments.html',
                'org_admin': 'dashboard/admin/patients.html',
                'lab_technician': 'dashboard/lab/lab_orders.html',
                'family_member': 'dashboard/family/patient_view.html',
                'billing_staff': 'dashboard/billing_staff/invoices.html'
            };
            
            window.location.href = rolePageMap[user.role] || 'dashboard/admin/patients.html';
            
        } catch (error) {
            alert('Login failed: ' + error.message);
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});