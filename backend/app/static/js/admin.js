// ===== ADMIN CORE FUNCTIONALITY =====
class DentaloistAdmin {
    constructor() {
        this.init();
    }

    init() {
        this.initSidebar();
        this.initAccordions();
        this.initDataTables();
        this.initForms();
        this.initNotifications();
        this.initResponsive();
    }

    // ===== SIDEBAR FUNCTIONALITY =====
    initSidebar() {
        this.sidebar = document.querySelector('.sidebar');
        this.mainContent = document.getElementById('mainContent');
        this.sidebarToggle = document.querySelector('.sidebar-toggle');
        
        // Check saved state
        const sidebarState = localStorage.getItem('sidebarState');
        if (sidebarState === 'open') {
            this.openSidebar();
        }

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768 && 
                this.sidebar.classList.contains('open') &&
                !this.sidebar.contains(e.target) &&
                !this.sidebarToggle.contains(e.target)) {
                this.closeSidebar();
            }
        });
    }

    toggleSidebar() {
        if (this.sidebar.classList.contains('open')) {
            this.closeSidebar();
        } else {
            this.openSidebar();
        }
    }

    openSidebar() {
        this.sidebar.classList.add('open');
        this.mainContent.classList.add('sidebar-open');
        localStorage.setItem('sidebarState', 'open');
    }

    closeSidebar() {
        this.sidebar.classList.remove('open');
        this.mainContent.classList.remove('sidebar-open');
        localStorage.setItem('sidebarState', 'closed');
    }

    // ===== ACCORDION FUNCTIONALITY =====
    initAccordions() {
        const accordionHeaders = document.querySelectorAll('.accordion-header');
        
        accordionHeaders.forEach(header => {
            header.addEventListener('click', () => {
                this.toggleAccordion(header);
            });
        });
    }

    toggleAccordion(header) {
        const content = header.nextElementSibling;
        const isOpen = content.classList.contains('open');
        
        // Close all accordions in the same group
        const allContents = document.querySelectorAll('.accordion-content');
        const allHeaders = document.querySelectorAll('.accordion-header');
        
        allContents.forEach(c => c.classList.remove('open'));
        allHeaders.forEach(h => h.classList.remove('active'));
        
        // Open clicked accordion if it wasn't open
        if (!isOpen) {
            content.classList.add('open');
            header.classList.add('active');
        }
    }

    // ===== DATA TABLE FUNCTIONALITY =====
    initDataTables() {
        const tables = document.querySelectorAll('.data-table');
        
        tables.forEach(table => {
            this.enhanceTable(table);
        });
    }

    enhanceTable(table) {
        const headers = table.querySelectorAll('th[data-sort]');
        
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                this.sortTable(table, header);
            });
        });
    }

    sortTable(table, header) {
        const columnIndex = Array.from(header.parentElement.children).indexOf(header);
        const isAscending = header.classList.contains('sort-asc');
        const rows = Array.from(table.querySelectorAll('tbody tr'));
        
        // Remove existing sort classes
        table.querySelectorAll('th').forEach(th => {
            th.classList.remove('sort-asc', 'sort-desc');
        });
        
        // Sort rows
        rows.sort((a, b) => {
            const aValue = a.children[columnIndex].textContent.trim();
            const bValue = b.children[columnIndex].textContent.trim();
            
            let comparison = 0;
            if (aValue > bValue) comparison = 1;
            else if (aValue < bValue) comparison = -1;
            
            return isAscending ? comparison : -comparison;
        });
        
        // Update sort indicator
        header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
        
        // Re-append sorted rows
        const tbody = table.querySelector('tbody');
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
    }

    // ===== FORM FUNCTIONALITY =====
    initForms() {
        // Auto-save functionality for forms
        const autoSaveForms = document.querySelectorAll('form[data-autosave]');
        
        autoSaveForms.forEach(form => {
            let saveTimeout;
            
            form.addEventListener('input', () => {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(() => {
                    this.autoSaveForm(form);
                }, 1000);
            });
        });

        // Confirmation for destructive actions
        const destructiveButtons = document.querySelectorAll('[data-confirm]');
        
        destructiveButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const message = button.getAttribute('data-confirm') || 'Are you sure?';
                if (!confirm(message)) {
                    e.preventDefault();
                }
            });
        });
    }

    autoSaveForm(form) {
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('Changes saved automatically', 'success');
            }
        })
        .catch(error => {
            console.error('Auto-save failed:', error);
        });
    }

    // ===== NOTIFICATION SYSTEM =====
    initNotifications() {
        // Auto-dismiss alerts after 5 seconds
        const autoDismissAlerts = document.querySelectorAll('.alert[data-auto-dismiss]');
        
        autoDismissAlerts.forEach(alert => {
            setTimeout(() => {
                this.dismissAlert(alert);
            }, 5000);
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type}`;
        notification.innerHTML = `
            <div class="d-flex justify-between align-center">
                <span>${message}</span>
                <button class="btn btn-sm" onclick="this.parentElement.parentElement.remove()">
                    <i class="material-icons">close</i>
                </button>
            </div>
        `;
        
        // Add to page
        const container = document.querySelector('.notification-container') || this.createNotificationContainer();
        container.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    createNotificationContainer() {
        const container = document.createElement('div');
        container.className = 'notification-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
        `;
        document.body.appendChild(container);
        return container;
    }

    dismissAlert(alert) {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.3s ease';
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 300);
    }

    // ===== RESPONSIVE FUNCTIONALITY =====
    initResponsive() {
        // Handle window resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                this.handleResize();
            }, 250);
        });

        // Initial check
        this.handleResize();
    }

    handleResize() {
        if (window.innerWidth <= 768) {
            this.closeSidebar();
        } else {
            // Restore sidebar state on larger screens
            const sidebarState = localStorage.getItem('sidebarState');
            if (sidebarState === 'open') {
                this.openSidebar();
            }
        }
    }

    // ===== UTILITY METHODS =====
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

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // ===== API METHODS =====
    async apiCall(endpoint, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
        };

        try {
            const response = await fetch(endpoint, { ...defaultOptions, ...options });
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API call failed:', error);
            this.showNotification(error.message, 'error');
            throw error;
        }
    }

    // ===== SEARCH FUNCTIONALITY =====
    initSearch() {
        const searchInputs = document.querySelectorAll('[data-search]');
        
        searchInputs.forEach(input => {
            input.addEventListener('input', this.debounce((e) => {
                this.performSearch(e.target.value, e.target.dataset.searchTarget);
            }, 300));
        });
    }

    performSearch(query, target) {
        const targetElement = document.querySelector(target);
        if (!targetElement) return;

        const items = targetElement.querySelectorAll('[data-searchable]');
        
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            const matches = text.includes(query.toLowerCase());
            item.style.display = matches ? '' : 'none';
        });
    }
}

// ===== GLOBAL FUNCTIONS =====
function toggleSidebar() {
    if (window.admin) {
        window.admin.toggleSidebar();
    }
}

function toggleAccordion(element) {
    if (window.admin) {
        window.admin.toggleAccordion(element);
    }
}

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    window.admin = new DentaloistAdmin();
});

// ===== ERROR HANDLING =====
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// ===== KEYBOARD SHORTCUTS =====
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('[data-search]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/sidebar
    if (e.key === 'Escape') {
        if (window.innerWidth <= 768) {
            toggleSidebar();
        }
    }
});