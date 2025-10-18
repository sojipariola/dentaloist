// admin.js - Unified Dentaloist Admin JavaScript

class AdminDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
        this.initializeSidebar();
        this.initializeCharts();
        this.startAutoRefresh();
    }

    bindEvents() {
        // Refresh stats button
        const refreshBtn = document.querySelector('.btn-refresh');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshStats());
        }

        // Quick action cards hover effects
        this.enhanceActionCards();
        
        // Search functionality
        this.initializeSearch();

        // Form submissions
        this.initializeForms();
    }

    initializeSidebar() {
        this.setupAccordionPersistance();
        this.setupResponsiveSidebar();
    }


    // ADD THIS METHOD TO YOUR AdminDashboard CLASS
    async refreshStats() {
        const btn = document.querySelector('.btn-refresh');
        if (!btn) return;

        const originalText = btn.innerHTML;
        
        btn.innerHTML = '<i class="material-icons spin">refresh</i> Refreshing...';
        btn.disabled = true;
        
        try {
            const response = await fetch('/admin/api/stats');
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.message || data.error);
            }
            
            // Update stats with animation
            this.animateCounter('stat-users', data.total_users || 0);
            this.animateCounter('stat-patients', data.total_patients || 0);
            this.animateCounter('stat-appointments', data.total_appointments || 0);
            this.animateCounter('stat-organizations', data.total_organizations || 0);
            
            this.showNotification('Stats updated successfully', 'success');
            
        } catch (error) {
            console.error('Failed to refresh stats:', error);
            this.showNotification('Failed to refresh stats: ' + error.message, 'error');
        } finally {
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 1000);
        }
    }

    animateCounter(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const currentValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const stepTime = 16;
        const steps = duration / stepTime;
        const increment = (targetValue - currentValue) / steps;
        let current = currentValue;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= targetValue) || (increment < 0 && current <= targetValue)) {
                clearInterval(timer);
                current = targetValue;
            }
            element.textContent = Math.round(current).toLocaleString();
        }, stepTime);
    }

    setupAccordionPersistance() {
        const accordionHeaders = document.querySelectorAll('.accordion-header');
        
        accordionHeaders.forEach(header => {
            header.addEventListener('click', () => {
                const category = header.querySelector('.accordion-title').textContent.trim();
                const isOpen = header.classList.contains('active');
                
                const state = JSON.parse(localStorage.getItem('sidebarState') || '{}');
                state[category] = isOpen;
                localStorage.setItem('sidebarState', JSON.stringify(state));
            });
        });

        this.restoreAccordionStates();
    }

    restoreAccordionStates() {
        const state = JSON.parse(localStorage.getItem('sidebarState') || '{}');
        
        document.querySelectorAll('.accordion-header').forEach(header => {
            const category = header.querySelector('.accordion-title').textContent.trim();
            if (state[category]) {
                if (!header.classList.contains('active')) {
                    header.click();
                }
            }
        });
    }

    setupResponsiveSidebar() {
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                document.getElementById('sidebar').classList.remove('open');
            } else {
                document.getElementById('sidebar').classList.remove('open');
            }
        });

        const mainContent = document.getElementById('mainContent');
        if (mainContent) {
            mainContent.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    document.getElementById('sidebar').classList.remove('open');
                }
            });
        }
    }

    enhanceActionCards() {
        const actionItems = document.querySelectorAll('.action-item');
        
        actionItems.forEach(item => {
            item.addEventListener('mouseenter', () => {
                const arrow = item.querySelector('.action-arrow');
                if (arrow) {
                    arrow.style.transform = 'translateX(5px)';
                }
            });
            
            item.addEventListener('mouseleave', () => {
                const arrow = item.querySelector('.action-arrow');
                if (arrow) {
                    arrow.style.transform = 'translateX(0)';
                }
            });
        });
    }

    initializeSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
        }
    }

    initializeForms() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e, form);
            });
        });
    }

    async refreshStats() {
        const btn = document.querySelector('.btn-refresh');
        if (!btn) return;

        const originalText = btn.innerHTML;
        
        btn.innerHTML = '<i class="material-icons spin">refresh</i> Refreshing...';
        btn.disabled = true;
        
        try {
            const response = await fetch('/admin/api/stats');
            const data = await response.json();
            
            this.animateCounter('stat-users', data.total_users || 0);
            this.animateCounter('stat-patients', data.total_patients || 0);
            this.animateCounter('stat-appointments', data.total_appointments || 0);
            this.animateCounter('stat-organizations', data.total_organizations || 0);
            
            this.showNotification('Stats updated successfully', 'success');
            
        } catch (error) {
            console.error('Failed to refresh stats:', error);
            this.showNotification('Failed to refresh stats', 'error');
        } finally {
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 1000);
        }
    }

    animateCounter(elementId, targetValue) {
        const element = document.getElementById(elementId);
        if (!element) return;

        const currentValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const stepTime = 16;
        const steps = duration / stepTime;
        const increment = (targetValue - currentValue) / steps;
        let current = currentValue;
        
        const timer = setInterval(() => {
            current += increment;
            if ((increment > 0 && current >= targetValue) || (increment < 0 && current <= targetValue)) {
                clearInterval(timer);
                current = targetValue;
            }
            element.textContent = Math.round(current).toLocaleString();
        }, stepTime);
    }

    handleSearch(query) {
        console.log('Search query:', query);
        // Implement search functionality
    }

    handleFormSubmit(e, form) {
        // Add form validation and submission handling
        console.log('Form submitted:', form);
    }

    initializeCharts() {
        // Initialize charts if needed
    }

    startAutoRefresh() {
        // Auto-refresh stats every 5 minutes
        setInterval(() => {
            this.refreshStats();
        }, 5 * 60 * 1000);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="material-icons">${this.getNotificationIcon(type)}</i>
                <span>${message}</span>
            </div>
        `;

        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${this.getNotificationColor(type)};
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideInRight 0.3s ease-out;
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check_circle',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };
        return icons[type] || 'info';
    }

    getNotificationColor(type) {
        const colors = {
            success: '#27ae60',
            error: '#e74c3c',
            warning: '#f39c12',
            info: '#3498db'
        };
        return colors[type] || '#3498db';
    }

    // Utility method for API calls
    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            this.showNotification('API request failed', 'error');
            throw error;
        }
    }

    // Delete item confirmation
    confirmDelete(itemId, itemName, deleteUrl, redirectUrl) {
        if (confirm(`Are you sure you want to delete this ${itemName}? This action cannot be undone.`)) {
            const formData = new FormData();
            formData.append('id', itemId);
            
            fetch(deleteUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.showNotification(`${itemName} deleted successfully`, 'success');
                    setTimeout(() => {
                        window.location.href = redirectUrl;
                    }, 1000);
                } else {
                    this.showNotification('Error: ' + data.error, 'error');
                }
            })
            .catch(error => {
                this.showNotification('Error: ' + error, 'error');
            });
        }
    }
}

// Global functions for template use
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

function toggleAccordion(header) {
    const content = header.nextElementSibling;
    const isOpen = content.classList.contains('open');
    
    document.querySelectorAll('.accordion-content.open').forEach(item => {
        if (item !== content) {
            item.classList.remove('open');
            item.previousElementSibling.classList.remove('active');
        }
    });
    
    if (!isOpen) {
        content.classList.add('open');
        header.classList.add('active');
    } else {
        content.classList.remove('open');
        header.classList.remove('active');
    }
}

// Enhanced logout function
function logoutUser() {
    if (confirm('Are you sure you want to logout?')) {
        showLoading('Logging out...');
        
        // Try multiple logout methods
        const logoutPromises = [];
        
        // Method 1: Form submission
        const form = document.getElementById('logout-form');
        if (form) {
            logoutPromises.push(
                new Promise((resolve) => {
                    form.submit();
                    setTimeout(resolve, 1000);
                })
            );
        }
        
        // Method 2: Fetch API to admin logout
        logoutPromises.push(
            fetch('{{ url_for("admin.admin_logout") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                credentials: 'same-origin'
            }).catch(() => null)
        );
        
        // Method 3: Fetch API to auth logout
        logoutPromises.push(
            fetch('{{ url_for("auth.logout") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                credentials: 'same-origin'
            }).catch(() => null)
        );
        
        // Execute all methods and redirect
        Promise.race(logoutPromises)
            .then(() => {
                window.location.href = '/';
            })
            .catch(() => {
                window.location.href = '/';
            });
    }
}

function showLoading(message) {
    // Simple loading indicator
    const loading = document.createElement('div');
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        font-size: 1.2rem;
    `;
    loading.textContent = message;
    document.body.appendChild(loading);
    
    setTimeout(() => {
        if (loading.parentNode) {
            loading.parentNode.removeChild(loading);
        }
    }, 3000);
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.adminDashboard = new AdminDashboard();

    // Auto-open accordion for active page
    const activeLink = document.querySelector('.accordion-link.active');
    if (activeLink) {
        const accordionItem = activeLink.closest('.accordion-item');
        if (accordionItem) {
            const accordionHeader = accordionItem.querySelector('.accordion-header');
            if (accordionHeader && !accordionHeader.classList.contains('active')) {
                toggleAccordion(accordionHeader);
            }
        }
    }

    // Open first accordion by default if none are active
    const anyOpen = document.querySelector('.accordion-content.open');
    if (!anyOpen) {
        const firstAccordion = document.querySelector('.accordion-header');
        if (firstAccordion) {
            toggleAccordion(firstAccordion);
        }
    }

    // Close sidebar when clicking on a link (mobile)
    document.querySelectorAll('.accordion-link').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                document.getElementById('sidebar').classList.remove('open');
            }
        });
    });

    // Close sidebar when clicking outside (mobile)
    document.addEventListener('click', function(event) {
        const sidebar = document.getElementById('sidebar');
        const toggleBtn = document.querySelector('.sidebar-toggle');
        
        if (window.innerWidth <= 768 && 
            sidebar && 
            !sidebar.contains(event.target) && 
            toggleBtn &&
            !toggleBtn.contains(event.target) &&
            sidebar.classList.contains('open')) {
            sidebar.classList.remove('open');
        }
    });
});

// Add CSS animations for notifications
const notificationStyles = `
@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

@keyframes slideOutRight {
    from {
        transform: translateX(0);
        opacity: 1;
    }
    to {
        transform: translateX(100%);
        opacity: 0;
    }
}

.notification {
    font-family: inherit;
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Export for global access
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdminDashboard;
}
// 

// In your dashboard.html extra_js block