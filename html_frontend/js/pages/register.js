import { register } from '../auth.js';

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('register-form');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userData = {
            first_name: document.getElementById('first_name').value,
            last_name: document.getElementById('last_name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value,
            role: document.getElementById('role').value
        };
        
        try {
            // Show loading state
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Creating account...';
            submitBtn.disabled = true;
            
            // Attempt registration
            const user = await register(userData);
            
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
            alert('Registration failed: ' + error.message);
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
});