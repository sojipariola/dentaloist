import { fetchWidgets } from '../api/widgets.js';

export class WidgetManager {
    constructor(containerId) {
        this.containerId = containerId;
        this.container = null;
        this.widgets = [];
    }
    
    async init() {
        this.container = document.getElementById(this.containerId);
        if (!this.container) return;
        
        await this.loadWidgets();
        this.renderWidgets();
    }
    
    async loadWidgets() {
        try {
            this.widgets = await fetchWidgets();
        } catch (error) {
            console.error('Error loading widgets:', error);
            // Use mock data for demo
            this.widgets = [
                {
                    id: 1,
                    type: 'stats_card',
                    title: 'Total Patients',
                    data_source: { endpoint: '/api/stats/patients', type: 'number' },
                    value: 127,
                    size: 'small',
                    width: 2,
                    height: 2
                },
                {
                    id: 2,
                    type: 'stats_card',
                    title: 'Today's Appointments',
                    data_source: { endpoint: '/api/stats/appointments/today', type: 'number' },
                    value: 8,
                    size: 'small',
                    width: 2,
                    height: 2
                },
                {
                    id: 3,
                    type: 'stats_card',
                    title: 'Monthly Revenue',
                    data_source: { endpoint: '/api/stats/revenue/monthly', type: 'currency' },
                    value: 18420,
                    size: 'medium',
                    width: 4,
                    height: 3
                }
            ];
        }
    }
    
    renderWidgets() {
        if (!this.container) return;
        
        this.container.innerHTML = '';
        this.container.style.display = 'grid';
        this.container.style.gridTemplateColumns = 'repeat(auto-fit, minmax(280px, 1fr))';
        this.container.style.gap = '1rem';
        this.container.style.padding = '1rem';
        
        this.widgets.forEach(widget => {
            const widgetEl = this.createWidgetElement(widget);
            this.container.appendChild(widgetEl);
        });
    }
    
    createWidgetElement(widget) {
        const el = document.createElement('div');
        el.className = `widget ${widget.type} ${widget.size || ''}`;
        el.style.gridColumn = `span ${widget.width || 3}`;
        el.style.gridRow = `span ${widget.height || 2}`;
        el.dataset.widgetId = widget.id;
        
        switch(widget.type) {
            case 'stats_card':
                el.innerHTML = `
                    <div class="widget-header">
                        <h3 class="title">${widget.title}</h3>
                        <button class="widget-settings btn-icon">⚙️</button>
                    </div>
                    <div class="widget-body">
                        <div class="value">${this.formatValue(widget.value, widget.data_source?.type)}</div>
                    </div>
                `;
                break;
            default:
                el.innerHTML = `
                    <div class="widget-header">
                        <h3 class="title">${widget.title}</h3>
                        <button class="widget-settings btn-icon">⚙️</button>
                    </div>
                    <div class="widget-body">
                        <div>Content for ${widget.type}</div>
                    </div>
                `;
        }
        
        // Add event listeners
        const settingsBtn = el.querySelector('.widget-settings');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.showWidgetSettings(widget);
            });
        }
        
        return el;
    }
    
    formatValue(value, type) {
        switch(type) {
            case 'currency':
                return new Intl.NumberFormat('en-US', {
                    style: 'currency',
                    currency: 'USD'
                }).format(value);
            case 'number':
                return new Intl.NumberFormat('en-US').format(value);
            default:
                return value;
        }
    }
    
    showWidgetSettings(widget) {
        alert(`Settings for widget: ${widget.title}`);
        // In a real app, this would show a modal with widget configuration options
    }
    
    static async initialize(containerId) {
        const manager = new WidgetManager(containerId);
        await manager.init();
        return manager;
    }
}