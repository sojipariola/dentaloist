import { Header } from '../components/Header.js';
import { Sidebar } from '../components/Sidebar.js';
import { fetchPatients, createPatient } from '../api/patients.js';
import { createElement } from '../utils/dom.js';
import { hasPermission, PERMISSIONS } from '../utils/permissions.js';
import { getCurrentUser } from '../auth.js';

class PatientsPage {
    constructor() {
        this.currentUser = getCurrentUser();
        this.patients = [];
        this.filteredPatients = [];
        this.searchTerm = '';
    }
    
    async init() {
        // Initialize header and sidebar
        await Header.initialize();
        await Sidebar.initialize();
        
        // Load patients
        await this.loadPatients();
        
        // Bind events
        this.bindEvents();
        
        // Render patients
        this.renderPatients();
    }
    
    async loadPatients() {
        try {
            this.patients = await fetchPatients();
            this.filteredPatients = [...this.patients];
        } catch (error) {
            console.error('Error loading patients:', error);
            // Mock data for demo
            this.patients = [
                { id: 1, first_name: 'John', last_name: 'Doe', email: 'john@example.com', phone: '555-1234', date_of_birth: '1985-03-15' },
                { id: 2, first_name: 'Jane', last_name: 'Smith', email: 'jane@example.com', phone: '555-5678', date_of_birth: '1990-07-22' },
                { id: 3, first_name: 'Bob', last_name: 'Johnson', email: 'bob@example.com', phone: '555-9012', date_of_birth: '1978-11-03' }
            ];
            this.filteredPatients = [...this.patients];
        }
    }
    
    bindEvents() {
        const searchInput = document.getElementById('search');
        const addPatientBtn = document.getElementById('add-patient');
        
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.searchTerm = e.target.value.toLowerCase();
                this.filterPatients();
                this.renderPatients();
            }, 300));
        }
        
        if (addPatientBtn && hasPermission(this.currentUser, PERMISSIONS.CREATE_PATIENT)) {
            addPatientBtn.addEventListener('click', () => this.showAddPatientModal());
        }
    }
    
    filterPatients() {
        if (!this.searchTerm) {
            this.filteredPatients = [...this.patients];
            return;
        }
        
        this.filteredPatients = this.patients.filter(patient => 
            patient.first_name.toLowerCase().includes(this.searchTerm) ||
            patient.last_name.toLowerCase().includes(this.searchTerm) ||
            patient.email.toLowerCase().includes(this.searchTerm) ||
            (patient.phone && patient.phone.includes(this.searchTerm))
        );
    }
    
    renderPatients() {
        const container = document.getElementById('patients-table');
        if (!container) return;
        
        // Create table
        const table = createElement('table', { className: 'table table-striped table-hover' });
        
        // Create header
        const thead = createElement('thead');
        const headerRow = createElement('tr');
        ['Name', 'Email', 'Phone', 'Date of Birth', 'Actions'].forEach(text => {
            const th = createElement('th', { textContent: text });
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Create body
        const tbody = createElement('tbody');
        
        if (this.filteredPatients.length === 0) {
            const row = createElement('tr');
            const td = createElement('td', { 
                textContent: this.searchTerm ? 'No patients found matching your search.' : 'No patients found.',
                colSpan: 5,
                style: 'text-align: center; padding: 2rem;'
            });
            row.appendChild(td);
            tbody.appendChild(row);
        } else {
            this.filteredPatients.forEach(patient => {
                const row = createElement('tr');
                
                // Name
                const nameCell = createElement('td', { 
                    textContent: `${patient.first_name} ${patient.last_name}`
                });
                row.appendChild(nameCell);
                
                // Email
                const emailCell = createElement('td', { 
                    textContent: patient.email || '-'
                });
                row.appendChild(emailCell);
                
                // Phone
                const phoneCell = createElement('td', { 
                    textContent: patient.phone || '-'
                });
                row.appendChild(phoneCell);
                
                // Date of Birth
                const dobCell = createElement('td', { 
                    textContent: patient.date_of_birth ? new Date(patient.date_of_birth).toLocaleDateString() : '-'
                });
                row.appendChild(dobCell);
                
                // Actions
                const actionsCell = createElement('td');
                const actionDiv = createElement('div', { style: 'display: flex; gap: 0.5rem;' });
                
                if (hasPermission(this.currentUser, PERMISSIONS.VIEW_PATIENT)) {
                    const viewBtn = createElement('button', { 
                        className: 'btn btn-sm',
                        textContent: 'View'
                    });
                    viewBtn.addEventListener('click', () => this.viewPatient(patient.id));
                    actionDiv.appendChild(viewBtn);
                }
                
                if (hasPermission(this.currentUser, PERMISSIONS.EDIT_PATIENT)) {
                    const editBtn = createElement('button', { 
                        className: 'btn btn-sm btn-primary',
                        textContent: 'Edit'
                    });
                    editBtn.addEventListener('click', () => this.editPatient(patient.id));
                    actionDiv.appendChild(editBtn);
                }
                
                row.appendChild(actionsCell);
                actionsCell.appendChild(actionDiv);
                tbody.appendChild(row);
            });
        }
        
        table.appendChild(tbody);
        container.innerHTML = '';
        container.appendChild(table);
    }
    
    showAddPatientModal() {
        // Create modal backdrop
        const backdrop = createElement('div', { className: 'modal-backdrop' });
        
        // Create modal
        const modal = createElement('div', { className: 'modal' });
        
        // Create modal header
        const modalHeader = createElement('div', { className: 'modal-header' });
        const modalTitle = createElement('h2', { className: 'modal-title', textContent: 'Add New Patient' });
        const closeBtn = createElement('button', { 
            className: 'close-modal',
            textContent: '×'
        });
        closeBtn.addEventListener('click', () => backdrop.remove());
        modalHeader.appendChild(modalTitle);
        modalHeader.appendChild(closeBtn);
        modal.appendChild(modalHeader);
        
        // Create modal body
        const modalBody = createElement('div', { className: 'modal-body' });
        modalBody.innerHTML = `
            <form id="add-patient-form">
                <div style="margin-bottom: 1rem;">
                    <label for="first_name" style="display: block; margin-bottom: 0.5rem;">First Name</label>
                    <input type="text" id="first_name" name="first_name" required>
                </div>
                <div style="margin-bottom: 1rem;">
                    <label for="last_name" style="display: block; margin-bottom: 0.5rem;">Last Name</label>
                    <input type="text" id="last_name" name="last_name" required>
                </div>
                <div style="margin-bottom: 1rem;">
                    <label for="email" style="display: block; margin-bottom: 0.5rem;">Email</label>
                    <input type="email" id="email" name="email">
                </div>
                <div style="margin-bottom: 1rem;">
                    <label for="phone" style="display: block; margin-bottom: 0.5rem;">Phone</label>
                    <input type="tel" id="phone" name="phone">
                </div>
                <div style="margin-bottom: 1rem;">
                    <label for="date_of_birth" style="display: block; margin-bottom: 0.5rem;">Date of Birth</label>
                    <input type="date" id="date_of_birth" name="date_of_birth">
                </div>
            </form>
        `;
        modal.appendChild(modalBody);
        
        // Create modal footer
        const modalFooter = createElement('div', { className: 'modal-footer' });
        const cancelBtn = createElement('button', { 
            className: 'btn btn-secondary',
            textContent: 'Cancel'
        });
        cancelBtn.addEventListener('click', () => backdrop.remove());
        const saveBtn = createElement('button', { 
            className: 'btn btn-primary',
            textContent: 'Save Patient'
        });
        saveBtn.addEventListener('click', async () => {
            const form = document.getElementById('add-patient-form');
            if (form.checkValidity()) {
                const formData = new FormData(form);
                const patientData = Object.fromEntries(formData.entries());
                
                try {
                    await createPatient(patientData);
                    backdrop.remove();
                    await this.loadPatients();
                    this.renderPatients();
                } catch (error) {
                    alert('Error creating patient: ' + error.message);
                }
            } else {
                form.reportValidity();
            }
        });
        modalFooter.appendChild(cancelBtn);
        modalFooter.appendChild(saveBtn);
        modal.appendChild(modalFooter);
        
        // Add modal to backdrop
        backdrop.appendChild(modal);
        
        // Show modal
        document.body.appendChild(backdrop);
        setTimeout(() => backdrop.classList.add('show'), 10);
        
        // Close on escape key
        const handleEsc = (e) => {
            if (e.key === 'Escape') {
                backdrop.remove();
                document.removeEventListener('keydown', handleEsc);
            }
        };
        document.addEventListener('keydown', handleEsc);
        
        // Close on click outside
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                backdrop.remove();
                document.removeEventListener('keydown', handleEsc);
            }
        });
    }
    
    viewPatient(patientId) {
        alert(`View patient with ID: ${patientId}`);
        // In a real app, this would navigate to a patient detail page
    }
    
    editPatient(patientId) {
        alert(`Edit patient with ID: ${patientId}`);
        // In a real app, this would show an edit modal or navigate to edit page
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    const page = new PatientsPage();
    await page.init();
});