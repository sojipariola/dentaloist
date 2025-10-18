# DentalSys - HTML/CSS/JS Frontend

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
