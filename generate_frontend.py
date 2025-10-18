import os
from pathlib import Path

# Project structure with file contents
PROJECT = {
    "html_frontend": {
        "index.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DentalSys</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/themes/light.css" id="theme-link">
</head>
<body>
    <script>
        const user = localStorage.getItem('user');
        if (user) {
            const parsed = JSON.parse(user);
            const rolePageMap = {
                'dentist': 'dashboard/dentist/appointments.html',
                'org_admin': 'dashboard/admin/patients.html',
                'lab_technician': 'dashboard/lab/lab_orders.html',
                'family_member': 'dashboard/family/patient_view.html',
                'billing_staff': 'dashboard/billing_staff/invoices.html'
            };
            window.location.href = rolePageMap[parsed.role] || 'login.html';
        } else {
            window.location.href = 'login.html';
        }
    </script>
</body>
</html>""",
        
        "login.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - DentalSys</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/themes/light.css" id="theme-link">
</head>
<body class="login-page">
    <div class="login-container">
        <h1 class="logo">🦷 DentalSys</h1>
        <h2>Welcome Back</h2>
        <form id="login-form">
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p class="footer">Don't have an account? <a href="register.html">Register</a></p>
    </div>
    <script type="module" src="js/pages/login.js"></script>
</body>
</html>""",

        "register.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Register - DentalSys</title>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/themes/light.css" id="theme-link">
</head>
<body class="login-page">
    <div class="login-container">
        <h1 class="logo">🦷 DentalSys</h1>
        <h2>Create Account</h2>
        <form id="register-form">
            <input type="text" id="first_name" placeholder="First Name" required>
            <input type="text" id="last_name" placeholder="Last Name" required>
            <input type="email" id="email" placeholder="Email" required>
            <input type="password" id="password" placeholder="Password" required>
            <select id="role" required>
                <option value="">Select Role</option>
                <option value="dentist">Dentist</option>
                <option value="org_admin">Clinic Admin</option>
                <option value="lab_technician">Lab Technician</option>
                <option value="family_member">Family Member</option>
                <option value="billing_staff">Billing Staff</option>
            </select>
            <button type="submit">Register</button>
        </form>
        <p class="footer">Already have an account? <a href="login.html">Login</a></p>
    </div>
    <script type="module" src="js/pages/register.js"></script>
</body>
</html>""",

        "dashboard": {
            "dentist": {
                "appointments.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Appointments - DentalSys</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/themes/light.css" id="theme-link">
</head>
<body>
    <div id="header-container"></div>
    <div class="main-content">
        <div id="sidebar-container"></div>
        <div class="page-content">
            <h1>🦷 Today's Appointments</h1>
            <div class="toolbar">
                <button id="add-appointment">+ New Appointment</button>
                <select id="status-filter">
                    <option value="all">All Status</option>
                    <option value="scheduled">Scheduled</option>
                    <option value="confirmed">Confirmed</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                </select>
            </div>
            <div id="appointments-list" class="grid"></div>
        </div>
    </div>
    <template id="appointment-card-template">
        <div class="appointment-card">
            <div class="card-header">
                <h3 class="title"></h3>
                <span class="status-badge"></span>
            </div>
            <div class="card-body">
                <p><strong>Patient:</strong> <span class="patient-name"></span></p>
                <p><strong>Time:</strong> <span class="time"></span></p>
                <p><strong>Type:</strong> <span class="type"></span></p>
                <p><strong>Room:</strong> <span class="room"></span></p>
            </div>
            <div class="card-footer">
                <button class="btn-view">View Details</button>
                <button class="btn-start">Start</button>
            </div>
        </div>
    </template>
    <script type="module" src="../../js/pages/appointments.js"></script>
</body>
</html>"""
            },
            "admin": {
                "patients.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Patients - DentalSys</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/themes/light.css" id="theme-link">
</head>
<body>
    <div id="header-container"></div>
    <div class="main-content">
        <div id="sidebar-container"></div>
        <div class="page-content">
            <h1>👥 Patients</h1>
            <div class="toolbar">
                <input type="text" id="search" placeholder="Search patients...">
                <button id="add-patient">+ Add Patient</button>
            </div>
            <div id="patients-table"></div>
        </div>
    </div>
    <template id="patient-row-template">
        <tr>
            <td class="patient-name"></td>
            <td class="patient-email"></td>
            <td class="patient-phone"></td>
            <td class="patient-dob"></td>
            <td>
                <button class="btn-edit">Edit</button>
                <button class="btn-view">View</button>
            </td>
        </tr>
    </template>
    <script type="module" src="../../js/pages/patients.js"></script>
</body>
</html>"""
            },
            "lab": {
                "lab_orders.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Lab Orders - DentalSys</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/themes/light.css" id="theme-link">
</head>
<body>
    <div id="header-container"></div>
    <div class="main-content">
        <div id="sidebar-container"></div>
        <div class="page-content">
            <h1>🧪 Lab Orders</h1>
            <div class="toolbar">
                <button id="create-order">+ New Order</button>
                <select id="status-filter">
                    <option value="all">All Status</option>
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                </select>
            </div>
            <div id="orders-list"></div>
        </div>
    </div>
    <script type="module" src="../../js/pages/lab_orders.js"></script>
</body>
</html>"""
            },
            "billing_staff": {
                "invoices.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Invoices - DentalSys</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/themes/light.css" id="theme-link">
</head>
<body>
    <div id="header-container"></div>
    <div class="main-content">
        <div id="sidebar-container"></div>
        <div class="page-content">
            <h1>💳 Invoices</h1>
            <div class="toolbar">
                <input type="text" id="search" placeholder="Search invoices...">
                <button id="create-invoice">+ New Invoice</button>
            </div>
            <div id="invoices-table"></div>
        </div>
    </div>
    <script type="module" src="../../js/pages/invoices.js"></script>
</body>
</html>"""
            },
            "family": {
                "patient_view.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Patient View - DentalSys</title>
    <link rel="stylesheet" href="../../css/main.css">
    <link rel="stylesheet" href="../../css/themes/light.css" id="theme-link">
</head>
<body>
    <div id="header-container"></div>
    <div class="main-content">
        <div id="sidebar-container"></div>
        <div class="page-content">
            <h1>👨‍👩‍👧‍👦 Family Patient View</h1>
            <div id="patient-profile"></div>
            <h2>Recent Appointments</h2>
            <div id="appointments-list"></div>
            <h2>Medical Records</h2>
            <div id="medical-records"></div>
        </div>
    </div>
    <script type="module" src="../../js/pages/family_view.js"></script>
</body>
</html>"""
            }
        },

        "components": {
            "header.html": """<header class="app-header">
    <div class="header-left">
        <button id="toggle-sidebar" class="btn-icon">☰</button>
        <h1>DentalSys</h1>
    </div>
    <div class="header-right">
        <button id="theme-toggle" class="btn-icon">🌙</button>
        <div class="user-menu">
            <img src="assets/images/avatar.png" alt="User" class="avatar">
            <span id="user-name">User</span>
            <button id="logout">Logout</button>
        </div>
    </div>
</header>""",

            "sidebar.html": """<aside class="app-sidebar">
    <nav>
        <ul>
            <li><a href="#" data-page="dashboard">Dashboard</a></li>
            <li><a href="#" data-page="patients">Patients</a></li>
            <li><a href="#" data-page="appointments">Appointments</a></li>
            <li><a href="#" data-page="invoices">Billing</a></li>
            <li><a href="#" data-page="lab">Lab Orders</a></li>
            <li><a href="#" data-page="settings">Settings</a></li>
        </ul>
    </nav>
</aside>""",

            "widget": {
                "stats_card.html": """<div class="widget stats-card">
    <div class="widget-header">
        <h3 class="title"></h3>
        <button class="widget-settings">⚙️</button>
    </div>
    <div class="widget-body">
        <div class="value"></div>
        <div class="trend"></div>
    </div>
</div>"""
            }
        },

        "css": {
            "main.css": """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #0d6efd;
    --primary-dark: #0a58ca;
    --secondary: #6c757d;
    --success: #198754;
    --danger: #dc3545;
    --warning: #ffc107;
    --info: #0dcaf0;
    --light: #f8f9fa;
    --dark: #212529;
    --bg: #ffffff;
    --text: #212529;
    --border: #dee2e6;
    --shadow: 0 2px 8px rgba(0,0,0,0.1);
    --radius: 8px;
    --transition: all 0.3s ease;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.6;
}

/* Layout */
.app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background: var(--primary);
    color: white;
    box-shadow: var(--shadow);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 100;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.app-sidebar {
    position: fixed;
    top: 60px;
    left: 0;
    width: 250px;
    height: calc(100vh - 60px);
    background: var(--light);
    border-right: 1px solid var(--border);
    padding: 1rem;
    transition: var(--transition);
    z-index: 90;
}

.app-sidebar.collapsed {
    transform: translateX(-100%);
}

.main-content {
    display: flex;
    margin-top: 60px;
}

.page-content {
    flex: 1;
    padding: 2rem;
    margin-left: 250px;
    transition: var(--transition);
}

.main-content.sidebar-collapsed .page-content {
    margin-left: 0;
}

/* Components */
.btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: var(--radius);
    background: var(--primary);
    color: white;
    cursor: pointer;
    font-weight: 500;
    transition: var(--transition);
}

.btn:hover {
    background: var(--primary-dark);
}

.btn-icon {
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: white;
}

.btn-danger {
    background: var(--danger);
}

.btn-success {
    background: var(--success);
}

.card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

.table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

.table th,
.table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.table th {
    background: var(--light);
    font-weight: 600;
}

/* Forms */
input, select, textarea {
    width: 100%;
    padding: 0.75rem;
    margin: 0.5rem 0;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 1rem;
}

input:focus, select:focus, textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
}

/* Login Page */
.login-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
}

.login-container {
    background: white;
    padding: 2rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

.logo {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: var(--primary);
}

/* Grid */
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1rem;
}

/* Widgets */
.widget {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem;
    box-shadow: var(--shadow);
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.widget-value {
    font-size: 2rem;
    font-weight: bold;
    color: var(--primary);
}

/* Responsive */
@media (max-width: 768px) {
    .app-sidebar {
        transform: translateX(-100%);
    }
    
    .app-sidebar.active {
        transform: translateX(0);
    }
    
    .page-content {
        margin-left: 0;
    }
    
    .main-content.sidebar-active .page-content {
        margin-left: 250px;
    }
    
    .login-container {
        max-width: 90%;
    }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}
""",

            "themes": {
                "light.css": """:root {
    --primary: #0d6efd;
    --primary-dark: #0a58ca;
    --secondary: #6c757d;
    --success: #198754;
    --danger: #dc3545;
    --warning: #ffc107;
    --info: #0dcaf0;
    --light: #f8f9fa;
    --dark: #212529;
    --bg: #ffffff;
    --text: #212529;
    --border: #dee2e6;
    --shadow: 0 2px 8px rgba(0,0,0,0.1);
}""",

                "dark.css": """:root {
    --primary: #4dabf7;
    --primary-dark: #339af0;
    --secondary: #868e96;
    --success: #51cf66;
    --danger: #ff6b6b;
    --warning: #ffd43b;
    --info: #22b8cf;
    --light: #343a40;
    --dark: #f8f9fa;
    --bg: #121212;
    --text: #e9ecef;
    --border: #343a40;
    --shadow: 0 2px 8px rgba(0,0,0,0.3);
}"""
            },

            "components": {
                "button.css": """.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.btn-primary {
    background-color: var(--primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-dark);
}

.btn-secondary {
    background-color: var(--secondary);
    color: white;
}

.btn-success {
    background-color: var(--success);
    color: white;
}

.btn-danger {
    background-color: var(--danger);
    color: white;
}

.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
}

.btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
}

.btn-block {
    display: block;
    width: 100%;
}

.btn-icon {
    padding: 0.5rem;
    width: auto;
}

.btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}""",

                "card.css": """.card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.card-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-body {
    padding: 1.5rem;
}

.card-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
    background: var(--light);
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0;
}

.card-subtitle {
    color: var(--secondary);
    font-size: 0.875rem;
    margin: 0.25rem 0 0;
}""",

                "table.css": """.table-container {
    overflow-x: auto;
    margin: 1rem 0;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background: var(--bg);
}

.table th,
.table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}

.table th {
    background: var(--light);
    font-weight: 600;
    color: var(--dark);
    position: sticky;
    top: 0;
}

.table tr:hover {
    background: rgba(0,0,0,0.02);
}

.table-striped tbody tr:nth-of-type(odd) {
    background: rgba(0,0,0,0.02);
}

.table-hover tbody tr:hover {
    background: rgba(0,0,0,0.05);
}

.table-responsive {
    display: block;
    width: 100%;
    overflow-x: auto;
}""",

                "modal.css": """.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
}

.modal-backdrop.show {
    opacity: 1;
    visibility: visible;
}

.modal {
    background: var(--bg);
    border-radius: 8px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    transform: translateY(-20px);
    transition: transform 0.3s ease;
}

.modal-backdrop.show .modal {
    transform: translateY(0);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 1.5rem 1rem;
    border-bottom: 1px solid var(--border);
}

.modal-title {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
}

.modal-body {
    padding: 1rem 1.5rem;
}

.modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
}

.close-modal {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--secondary);
}

.close-modal:hover {
    color: var(--danger);
}"""
            },

            "pages": {
                "login.css": """.login-page {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
}

.login-container {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    width: 100%;
    max-width: 420px;
    text-align: center;
}

.logo {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: #0d6efd;
    font-weight: bold;
}

.login-container h2 {
    margin-bottom: 1.5rem;
    color: #333;
}

.login-container input {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

.login-container input:focus {
    border-color: #0d6efd;
    outline: none;
    box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.25);
}

.login-container button {
    width: 100%;
    padding: 12px;
    background: #0d6efd;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    margin: 16px 0 8px;
    transition: background-color 0.3s ease;
}

.login-container button:hover {
    background: #0a58ca;
}

.login-container .footer {
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #666;
}

.login-container .footer a {
    color: #0d6efd;
    text-decoration: none;
    font-weight: 500;
}

.login-container .footer a:hover {
    text-decoration: underline;
}"""
            }
        },

        "js": {
            "config.js": """export const API_BASE_URL = 'http://localhost:5000';
export const DEFAULT_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};""",

            "auth.js": """import { API_BASE_URL, DEFAULT_HEADERS } from './config.js';

export async function login(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify({ email, password })
        });
        
        if (!response.ok) {
            throw new Error('Login failed');
        }
        
        const data = await response.json();
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('token', data.token);
        return data.user;
    } catch (error) {
        console.error('Login error:', error);
        throw error;
    }
}

export async function register(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/register`, {
            method: 'POST',
            headers: DEFAULT_HEADERS,
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        
        const data = await response.json();
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('token', data.token);
        return data.user;
    } catch (error) {
        console.error('Registration error:', error);
        throw error;
    }
}

export function logout() {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    window.location.href = 'login.html';
}

export function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

export function getToken() {
    return localStorage.getItem('token');
}

export function isAuthenticated() {
    return !!getToken();
}""",

            "api": {
                "index.js": """export * from './patients.js';
export * from './appointments.js';
export * from './users.js';
export * from './invoices.js';
export * from './widgets.js';""",

                "patients.js": """import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchPatients(searchTerm = '') {
    try {
        const url = searchTerm 
            ? `${API_BASE_URL}/api/patients?search=${encodeURIComponent(searchTerm)}`
            : `${API_BASE_URL}/api/patients`;
            
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch patients');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching patients:', error);
        throw error;
    }
}

export async function createPatient(patientData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create patient');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating patient:', error);
        throw error;
    }
}

export async function updatePatient(id, patientData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(patientData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update patient');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating patient:', error);
        throw error;
    }
}

export async function deletePatient(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/patients/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete patient');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting patient:', error);
        throw error;
    }
}""",

                "appointments.js": """import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchAppointments(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const url = `${API_BASE_URL}/api/appointments?${params.toString()}`;
        
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch appointments');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching appointments:', error);
        throw error;
    }
}

export async function createAppointment(appointmentData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(appointmentData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating appointment:', error);
        throw error;
    }
}

export async function updateAppointment(id, appointmentData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(appointmentData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating appointment:', error);
        throw error;
    }
}

export async function cancelAppointment(id, reason) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/appointments/${id}/cancel`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify({ reason })
        });
        
        if (!response.ok) {
            throw new Error('Failed to cancel appointment');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error canceling appointment:', error);
        throw error;
    }
}""",

                "widgets.js": """import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchWidgets() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch widgets');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching widgets:', error);
        throw error;
    }
}

export async function createWidget(widgetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(widgetData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create widget');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating widget:', error);
        throw error;
    }
}

export async function updateWidget(id, widgetData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(widgetData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update widget');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating widget:', error);
        throw error;
    }
}

export async function deleteWidget(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/widgets/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete widget');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting widget:', error);
        throw error;
    }
}""",

                "users.js": """import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error;
    }
}

export async function createUser(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create user');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating user:', error);
        throw error;
    }
}

export async function updateUser(id, userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update user');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating user:', error);
        throw error;
    }
}

export async function deleteUser(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete user');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting user:', error);
        throw error;
    }
}""",

                "invoices.js": """import { API_BASE_URL, DEFAULT_HEADERS } from '../config.js';
import { getToken } from '../auth.js';

const getAuthHeaders = () => ({
    ...DEFAULT_HEADERS,
    'Authorization': `Bearer ${getToken()}`
});

export async function fetchInvoices(filters = {}) {
    try {
        const params = new URLSearchParams(filters);
        const url = `${API_BASE_URL}/api/invoices?${params.toString()}`;
        
        const response = await fetch(url, {
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch invoices');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching invoices:', error);
        throw error;
    }
}

export async function createInvoice(invoiceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(invoiceData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to create invoice');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error creating invoice:', error);
        throw error;
    }
}

export async function updateInvoice(id, invoiceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices/${id}`, {
            method: 'PUT',
            headers: getAuthHeaders(),
            body: JSON.stringify(invoiceData)
        });
        
        if (!response.ok) {
            throw new Error('Failed to update invoice');
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error updating invoice:', error);
        throw error;
    }
}

export async function deleteInvoice(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/invoices/${id}`, {
            method: 'DELETE',
            headers: getAuthHeaders()
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete invoice');
        }
        
        return { success: true };
    } catch (error) {
        console.error('Error deleting invoice:', error);
        throw error;
    }
}"""
            },

            "utils": {
                "permissions.js": """export function hasPermission(user, permission) {
    if (!user || !user.permissions) return false;
    return user.permissions.includes(permission);
}

export function hasAnyPermission(user, permissions) {
    if (!user || !user.permissions) return false;
    return permissions.some(p => user.permissions.includes(p));
}

export function hasAllPermissions(user, permissions) {
    if (!user || !user.permissions) return false;
    return permissions.every(p => user.permissions.includes(p));
}

export const PERMISSIONS = {
    CREATE_PATIENT: 'create_patient',
    VIEW_PATIENT: 'view_patient',
    EDIT_PATIENT: 'edit_patient',
    DELETE_PATIENT: 'delete_patient',
    CREATE_APPOINTMENT: 'create_appointment',
    VIEW_APPOINTMENT: 'view_appointment',
    EDIT_APPOINTMENT: 'edit_appointment',
    DELETE_APPOINTMENT: 'delete_appointment',
    DIAGNOSE: 'diagnose',
    DESIGN_RESTORATION: 'design_restoration',
    UPLOAD_IMAGES: 'upload_images',
    VIEW_TREATMENT: 'view_treatment',
    MANAGE_USERS: 'manage_users',
    MANAGE_ROLES: 'manage_roles',
    VIEW_ORGANIZATION: 'view_organization',
    EDIT_ORGANIZATION: 'edit_organization',
    MANAGE_BILLING: 'manage_billing',
    VIEW_BILLING: 'view_billing',
    VIEW_ANALYTICS: 'view_analytics',
    EXPORT_DATA: 'export_data',
    ACCESS_AI_ADVICE: 'access_ai_advice'
};""",

                "dom.js": """export function createElement(tag, props = {}, children = []) {
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
}""",

                "date.js": """export function formatDate(dateString, format = 'MM/DD/YYYY HH:mm') {
    if (!dateString) return '';
    const date = new Date(dateString);
    
    const pad = (num) => String(num).padStart(2, '0');
    
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const year = date.getFullYear();
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    
    let formatted = format
        .replace('MM', month)
        .replace('DD', day)
        .replace('YYYY', year)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
    
    return formatted;
}

export function formatTime(dateString, format = '12h') {
    if (!dateString) return '';
    const date = new Date(dateString);
    
    let hours = date.getHours();
    let minutes = String(date.getMinutes()).padStart(2, '0');
    let ampm = '';
    
    if (format === '12h') {
        ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
    }
    
    return `${hours}:${minutes}${ampm ? ' ' + ampm : ''}`;
}

export function isToday(dateString) {
    const today = new Date();
    const date = new Date(dateString);
    return date.toDateString() === today.toDateString();
}

export function isPast(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    return date < now;
}

export function isFuture(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    return date > now;
}

export function addDays(dateString, days) {
    const date = new Date(dateString);
    date.setDate(date.getDate() + days);
    return date.toISOString();
}

export function getDayName(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'long' });
}"""
            },

            "components": {
                "Header.js": """import { getCurrentUser, logout } from '../auth.js';

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
}""",

                "Sidebar.js": """import { getCurrentUser, hasPermission } from '../auth.js';
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
}""",

                "WidgetManager.js": """import { fetchWidgets } from '../api/widgets.js';

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
                    title: 'Today\'s Appointments',
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
}"""
            },

            "pages": {
                "login.js": """import { login } from '../auth.js';

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
});""",

                "register.js": """import { register } from '../auth.js';

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
});""",

                "patients.js": """import { Header } from '../components/Header.js';
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
});"""
            }
        },

        "assets": {
            "images": {
                "logo.svg": """<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="45" fill="#0d6efd" />
  <text x="50" y="55" text-anchor="middle" fill="white" font-size="24" font-family="Arial">🦷</text>
</svg>"""
            }
        },

        "README.md": """# DentalSys - HTML/CSS/JS Frontend

A world-class, modular frontend for your dental/medical clinic management system.

## Features

- ✅ Role-based access control
- ✅ Responsive design with light/dark theme
- ✅ Reusable components (Header, Sidebar, Widgets)
- ✅ API integration with your Flask backend
- ✅ Modern UI with clean, professional design
- ✅ Scalable architecture for large applications

## Getting Started

1. Clone or download this repository
2. Start your Flask backend on `http://localhost:5000`
3. Open `index.html` in your browser (use Live Server or `python -m http.server 8000`)
4. Login with any email/password (mock authentication)
5. Explore the dashboard and patient management features

## File Structure
html_frontend/
├── index.html # Main entry point
├── login.html # Login page
├── dashboard/ # Role-based dashboards
├── components/ # Reusable UI components
├── css/ # Stylesheets
├── js/ # JavaScript modules
├── assets/ # Images and other assets
└── README.md

## Customization

- Modify `css/themes/light.css` and `css/themes/dark.css` to change colors
- Add new pages in the appropriate role folder under `dashboard/`
- Extend API modules in `js/api/` to connect with your Flask endpoints
- Add new components in `components/` and their JS counterparts in `js/components/`

## License

This template is provided as-is for educational and development purposes.
"""
    }
}


def create_project_structure(base_path, structure):
    """Recursively create project structure from dictionary"""
    base_path = Path(base_path)
    
    for name, content in structure.items():
        path = base_path / name
        
        if isinstance(content, dict):
            # Create directory
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {path}")
            # Recursively create subdirectories and files
            create_project_structure(path, content)
        else:
            # Create file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📄 Created file: {path}")

# Create the project
print("🚀 Generating DentalSys HTML/CSS/JS Frontend...")
create_project_structure(".", PROJECT)
print("\n🎉 Project generated successfully!")
print("\n📂 Project structure created in: ./html_frontend")
print("\n▶️ To run:")
print("1. cd html_frontend")
print("2. python -m http.server 8000")
print("3. Open http://localhost:8000 in your browser")
print("\n🔌 Make sure your Flask backend is running on http://localhost:5000")