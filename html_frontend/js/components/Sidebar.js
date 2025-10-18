import { getCurrentUser, hasPermission } from '../auth.js';
import { PERMISSIONS } from '../utils/permissions.js';

export class Sidebar {
    constructor() {
        this.element = null;
        this.currentUser = getCurrentUser();
    }
    
    async init() {
        // Load sidebar HTML
        const response = await fetch('components/sidebar.html');
        const html = await response.text();
        
        this.element = document.createElement('div');
        this.element.innerHTML = html;
        document.getElementById('sidebar-container').appendChild(this.element.firstElementChild);
        
        this.bindEvents();
        this.updateNavigation();
    }
    
    bindEvents() {
        const navLinks = document.querySelectorAll('.app-sidebar a');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = link.getAttribute('data-page');
                this.navigateToPage(page);
            });
        });
    }
    
    updateNavigation() {
        const navLinks = document.querySelectorAll('.app-sidebar a');
        
        navLinks.forEach(link => {
            const page = link.getAttribute('data-page');
            if (!this.shouldShowPage(page)) {
                link.parentElement.style.display = 'none';
            }
        });
    }
    
    shouldShowPage(page) {
        if (!this.currentUser) return false;
        
        const permissionMap = {
            'patients': PERMISSIONS.VIEW_PATIENT,
            'appointments': PERMISSIONS.VIEW_APPOINTMENT,
            'invoices': PERMISSIONS.VIEW_BILLING,
            'lab': PERMISSIONS.VIEW_TREATMENT,
            'settings': PERMISSIONS.VIEW_ORGANIZATION
        };
        
        if (page === 'dashboard') return true;
        if (page in permissionMap) {
            return hasPermission(this.currentUser, permissionMap[page]);
        }
        
        return true;
    }
    
    navigateToPage(page) {
        const pageMap = {
            'dashboard': this.getDashboardPage(),
            'patients': 'dashboard/admin/patients.html',
            'appointments': 'dashboard/dentist/appointments.html',
            'invoices': 'dashboard/billing_staff/invoices.html',
            'lab': 'dashboard/lab/lab_orders.html',
            'settings': 'dashboard/admin/organization.html'
        };
        
        if (page in pageMap && pageMap[page]) {
            window.location.href = pageMap[page];
        }
    }
    
    getDashboardPage() {
        if (!this.currentUser) return 'login.html';
        
        const rolePageMap = {
            'dentist': 'dashboard/dentist/appointments.html',
            'org_admin': 'dashboard/admin/patients.html',
            'lab_technician': 'dashboard/lab/lab_orders.html',
            'family_member': 'dashboard/family/patient_view.html',
            'billing_staff': 'dashboard/billing_staff/invoices.html'
        };
        
        return rolePageMap[this.currentUser.role] || 'dashboard/admin/patients.html';
    }
    
    static async initialize() {
        const sidebar = new Sidebar();
        await sidebar.init();
        return sidebar;
    }
}