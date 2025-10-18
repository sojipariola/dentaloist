export function createElement(tag, props = {}, children = []) {
    const element = document.createElement(tag);
    
    // Set attributes
    Object.keys(props).forEach(key => {
        if (key.startsWith('data-')) {
            element.setAttribute(key, props[key]);
        } else if (key === 'className') {
            element.className = props[key];
        } else if (key === 'textContent') {
            element.textContent = props[key];
        } else {
            element[key] = props[key];
        }
    });
    
    // Append children
    children.forEach(child => {
        if (typeof child === 'string') {
            element.appendChild(document.createTextNode(child));
        } else if (child) {
            element.appendChild(child);
        }
    });
    
    return element;
}

export function renderTemplate(templateId, data) {
    const template = document.getElementById(templateId);
    if (!template) return null;
    
    const clone = document.importNode(template.content, true);
    const element = clone.firstElementChild;
    
    // Simple data binding - replace {{key}} with data[key]
    Object.keys(data).forEach(key => {
        const value = data[key];
        const selector = `[data-bind="${key}"]`;
        const elements = element.querySelectorAll(selector);
        
        elements.forEach(el => {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.value = value;
            } else {
                el.textContent = value;
            }
        });
    });
    
    return clone;
}

export function formatDate(dateString, format = 'MM/DD/YYYY') {
    if (!dateString) return '';
    const date = new Date(dateString);
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const year = date.getFullYear();
    
    return format
        .replace('MM', month)
        .replace('DD', day)
        .replace('YYYY', year);
}

export function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

export function debounce(func, wait) {
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

export function showNotification(message, type = 'info') {
    const notification = createElement('div', {
        className: `notification notification-${type}`,
        textContent: message
    });
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}