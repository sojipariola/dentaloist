// Dentaloist Admin Custom JavaScript
class DentaloistAdmin {
    constructor() {
        this.init();
    }

    init() {
        this.initCharts();
        this.initStats();
        this.initQuickActions();
        this.initRealTimeUpdates();
        this.initPrintFunctionality();
        this.initSearchFunctionality();
    }

    // Initialize charts
    initCharts() {
        // Check if Chart.js is available
        if (typeof Chart === 'undefined') {
            console.log('Chart.js not loaded, skipping chart initialization');
            return;
        }

        // Sample chart data - you can replace this with real data
        const ctx = document.getElementById('adminChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                    datasets: [{
                        label: 'New Patients',
                        data: [12, 19, 3, 5, 2, 3],
                        borderColor: '#3498db',
                        backgroundColor: 'rgba(52, 152, 219, 0.1)',
                        tension: 0.4,
                        fill: true
                    }, {
                        label: 'Appointments',
                        data: [8, 15, 12, 17, 14, 16],
                        borderColor: '#2ecc71',
                        backgroundColor: 'rgba(46, 204, 113, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Monthly Statistics'
                        }
                    }
                }
            });
        }
    }

    // Initialize stats with real-time updates
    initStats() {
        // Add click handlers to stat cards
        document.querySelectorAll('.stat-card').forEach(card => {
            card.addEventListener('click', function() {
                const cardType = this.classList[1].replace('bg-', '');
                this.pulseAnimation();
                this.loadDetailedView(cardType);
            });
        });

        // Update stats every 30 seconds
        setInterval(() => {
            this.updateLiveStats();
        }, 30000);
    }

    // Pulse animation for stat cards
    pulseAnimation(element) {
        element.style.transform = 'scale(1.05)';
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, 300);
    }

    // Update live stats from server
    async updateLiveStats() {
        try {
            const response = await fetch('/admin/api/stats');
            const data = await response.json();
            
            this.updateStatCard('users', data.total_users);
            this.updateStatCard('patients', data.total_patients);
            this.updateStatCard('appointments', data.total_appointments);
            this.updateStatCard('organizations', data.total_organizations);
            
        } catch (error) {
            console.log('Failed to update stats:', error);
        }
    }

    // Update individual stat card
    updateStatCard(type, newValue) {
        const card = document.querySelector(`.stat-card[data-type="${type}"]`);
        if (card) {
            const numberElement = card.querySelector('.stat-number');
            const oldValue = parseInt(numberElement.textContent);
            
            if (oldValue !== newValue) {
                this.animateNumberChange(numberElement, oldValue, newValue);
            }
        }
    }

    // Animate number change
    animateNumberChange(element, start, end) {
        const duration = 1000;
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentValue = Math.floor(start + (end - start) * easeOutQuart);
            
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Initialize quick actions
    initQuickActions() {
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.executeQuickAction(btn.dataset.action);
            });
        });
    }

    // Execute quick action
    executeQuickAction(action) {
        const actions = {
            'export-data': this.exportData.bind(this),
            'clear-cache': this.clearCache.bind(this),
            'backup-db': this.backupDatabase.bind(this),
            'system-check': this.systemCheck.bind(this)
        };

        if (actions[action]) {
            actions[action]();
        }
    }

    // Export data functionality
    async exportData() {
        this.showLoading('Exporting data...');
        try {
            const response = await fetch('/admin/api/export-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                this.showNotification('Data exported successfully!', 'success');
            } else {
                throw new Error('Export failed');
            }
        } catch (error) {
            this.showNotification('Export failed: ' + error.message, 'error');
        }
        this.hideLoading();
    }

    // Clear cache
    async clearCache() {
        this.showLoading('Clearing cache...');
        try {
            const response = await fetch('/admin/api/clear-cache', {
                method: 'POST'
            });
            
            if (response.ok) {
                this.showNotification('Cache cleared successfully!', 'success');
            } else {
                throw new Error('Cache clear failed');
            }
        } catch (error) {
            this.showNotification('Cache clear failed: ' + error.message, 'error');
        }
        this.hideLoading();
    }

    // Backup database
    async backupDatabase() {
        this.showLoading('Creating backup...');
        try {
            const response = await fetch('/admin/api/backup-db', {
                method: 'POST'
            });
            
            if (response.ok) {
                this.showNotification('Backup created successfully!', 'success');
            } else {
                throw new Error('Backup failed');
            }
        } catch (error) {
            this.showNotification('Backup failed: ' + error.message, 'error');
        }
        this.hideLoading();
    }

    // System check
    async systemCheck() {
        this.showLoading('Running system check...');
        try {
            const response = await fetch('/admin/api/system-check');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.showNotification('System check passed! All systems operational.', 'success');
            } else {
                this.showNotification('System issues detected. Check logs for details.', 'warning');
            }
        } catch (error) {
            this.showNotification('System check failed: ' + error.message, 'error');
        }
        this.hideLoading();
    }

    // Initialize real-time updates
    initRealTimeUpdates() {
        // Listen for real-time events (you can integrate with Socket.io later)
        this.setupEventSource();
    }

    // Setup server-sent events for real-time updates
    setupEventSource() {
        if (typeof EventSource !== 'undefined') {
            const eventSource = new EventSource('/admin/api/events');
            
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleRealTimeEvent(data);
            };
            
            eventSource.onerror = (error) => {
                console.log('EventSource error:', error);
            };
        }
    }

    // Handle real-time events
    handleRealTimeEvent(data) {
        switch (data.type) {
            case 'new_user':
                this.showNotification(`New user registered: ${data.data.email}`, 'info');
                this.updateLiveStats();
                break;
            case 'new_appointment':
                this.showNotification(`New appointment created`, 'info');
                this.updateLiveStats();
                break;
            case 'system_alert':
                this.showNotification(data.message, 'warning');
                break;
        }
    }

    // Initialize print functionality
    initPrintFunctionality() {
        const printBtn = document.getElementById('print-dashboard');
        if (printBtn) {
            printBtn.addEventListener('click', () => {
                window.print();
            });
        }
    }

    // Initialize search functionality
    initSearchFunctionality() {
        const searchInput = document.getElementById('admin-search');
        if (searchInput) {
            searchInput.addEventListener('input', this.debounce((e) => {
                this.performSearch(e.target.value);
            }, 300));
        }
    }

    // Perform search
    async performSearch(query) {
        if (query.length < 2) return;
        
        try {
            const response = await fetch(`/admin/api/search?q=${encodeURIComponent(query)}`);
            const results = await response.json();
            this.displaySearchResults(results);
        } catch (error) {
            console.log('Search failed:', error);
        }
    }

    // Display search results
    displaySearchResults(results) {
        // Implement search results display
        console.log('Search results:', results);
    }

    // Utility: Debounce function
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

    // Show loading indicator
    showLoading(message = 'Loading...') {
        // Implement loading indicator
        console.log('Loading:', message);
    }

    // Hide loading indicator
    hideLoading() {
        // Implement hide loading
    }

    // Show notification
    showNotification(message, type = 'info') {
        // You can integrate with a notification library like Toastify
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="close" data-dismiss="alert">
                <span>&times;</span>
            </button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
}

// Initialize admin when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.dentaloistAdmin = new DentaloistAdmin();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DentaloistAdmin;
}