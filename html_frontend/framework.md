html_frontend/
├── index.html                 # Main entry point
├── about.html                 # Optional additional pages
├── contact.html
│
├── css/
│   ├── style.css              # Global styles
│   ├── components/            # Reusable component styles
│   │   ├── header.css
│   │   ├── button.css
│   │   └── card.css
│   └── pages/                 # Page-specific styles
│       ├── home.css
│       └── about.css
│
├── js/
│   ├── main.js                # Main JS logic
│   ├── api.js                 # API calls (fetch functions)
│   ├── utils.js               # Helper functions
│   └── pages/                 # Page-specific JS
│       ├── home.js
│       └── about.js
│
├── assets/
│   ├── images/
│   │   ├── logo.png
│   │   └── hero-bg.jpg
│   └── icons/
│       └── favicon.ico
│
├── lib/                       # Optional: 3rd-party libs (if not using CDN)
│   └── some-lib.min.js
│
└── README.md


html_frontend/
├── index.html                    # Main dashboard (login → redirects to role-based dash)
├── login.html
├── register.html
│
├── dashboard/
│   ├── dentist/
│   │   ├── appointments.html
│   │   ├── patients.html
│   │   ├── prescriptions.html
│   │   └── telehealth.html
│   ├── admin/
│   │   ├── users.html
│   │   ├── roles.html
│   │   ├── organization.html
│   │   └── billing.html
│   ├── lab/
│   │   └── lab_orders.html
│   ├── billing_staff/
│   │   ├── invoices.html
│   │   └── payments.html
│   └── family/
│       └── patient_view.html
│
├── components/                   # Reusable UI components (via <template> or JS)
│   ├── header.html
│   ├── sidebar.html
│   ├── card.html
│   ├── modal.html
│   ├── table.html
│   └── widget/
│       ├── stats_card.html
│       ├── line_chart.html
│       └── bar_chart.html
│
├── css/
│   ├── main.css                  # Global styles, resets, layout
│   ├── themes/
│   │   ├── light.css
│   │   └── dark.css
│   ├── components/
│   │   ├── button.css
│   │   ├── input.css
│   │   ├── card.css
│   │   ├── table.css
│   │   └── modal.css
│   └── pages/
│       ├── login.css
│       ├── dashboard.css
│       └── patients.css
│
├── js/
│   ├── config.js                 # API_BASE_URL, user settings
│   ├── auth.js                   # Login, token, logout logic
│   ├── api/
│   │   ├── users.js
│   │   ├── patients.js
│   │   ├── appointments.js
│   │   ├── invoices.js
│   │   ├── widgets.js
│   │   └── index.js              # exports all API modules
│   ├── utils/
│   │   ├── dom.js                # DOM helpers (createElement, etc.)
│   │   ├── date.js               # Format dates
│   │   └── permissions.js        # Check user permissions
│   ├── components/
│   │   ├── Header.js
│   │   ├── Sidebar.js
│   │   ├── WidgetManager.js      # Load & render widgets dynamically
│   │   └── DataTable.js          # Render tables from API data
│   └── pages/
│       ├── login.js
│       ├── dashboard.js
│       ├── patients.js
│       └── appointments.js
│
├── assets/
│   ├── images/
│   │   ├── logo.svg
│   │   └── icons/
│   └── fonts/
│
├── lib/
│   └── chart.js                  # Optional: for charts (if not using SVG/Canvas directly)
│
└── README.md