import { getCurrentUser, logout } from '../auth.js';

export class Header {
    constructor() {
        this.element = null;
        this.currentUser = getCurrentUser();
    }
    
    async init() {
        // Load header HTML
        const response = await fetch('components/header.html');
        const html = await response.text();
        
        this.element = document.createElement('div');
        this.element.innerHTML = html;
        document.getElementById('header-container').appendChild(this.element.firstElementChild);
        
        this.bindEvents();
        this.updateUserInfo();
    }
    
    bindEvents() {
        const toggleBtn = document.getElementById('toggle-sidebar');
        const themeToggle = document.getElementById('theme-toggle');
        const logoutBtn = document.getElementById('logout');
        
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                document.body.classList.toggle('sidebar-collapsed');
            });
        }
        
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
        }
        
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                logout();
            });
        }
    }
    
    updateUserInfo() {
        if (!this.currentUser) return;
        
        const userName = document.getElementById('user-name');
        if (userName) {
            userName.textContent = `${this.currentUser.first_name} ${this.currentUser.last_name}`;
        }
    }
    
    toggleTheme() {
        const themeLink = document.getElementById('theme-link');
        const themeToggle = document.getElementById('theme-toggle');
        
        if (themeLink.getAttribute('href').includes('light')) {
            themeLink.setAttribute('href', 'css/themes/dark.css');
            themeToggle.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            themeLink.setAttribute('href', 'css/themes/light.css');
            themeToggle.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    }
    
    static async initialize() {
        const header = new Header();
        await header.init();
        return header;
    }
}