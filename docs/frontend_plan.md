# Here's the routes grouped logically for frontend development, organized by priority and functionality:

# 🎯 PRIORITY 1: CORE AUTH & USER MANAGEMENT
Authentication & Session Management
# User Authentication
POST /api/auth/login              # User login
POST /api/auth/logout             # User logout  
POST /api/auth/refresh            # Refresh token
GET  /api/auth/me                 # Get current user
# Web Authentication (for admin/portal)
GET,POST /web/login               # Web portal login
GET,POST /web/change-password     # Change password
GET,POST /web/forgot-password     # Password recovery
GET,POST /web/reset-password/<token> # Password reset
# Security & Sessions
GET  /api/auth/sessions           # Get active sessions
DELETE /api/auth/sessions/<session_id> # Revoke session
GET  /api/auth/security/attempts  # Login attempts
GET  /api/auth/security/stats     # Security statistics
User Management
# Current User
GET  /api/users/me                # Get current user profile
PUT  /api/users/me                # Update current user
PUT  /api/users/me/password       # Change password
GET  /api/users/me/settings       # Get user settings
PUT  /api/users/me/settings       # Update user settings
# User Management
GET  /api/users/                  # List all users
POST /api/users/                  # Create new user
GET  /api/users/<user_id>         # Get user details
PUT  /api/users/<user_id>         # Update user
DELETE /api/users/<user_id>       # Delete user
GET  /api/users/<user_id>/profile # Get user profile

# 🎯 PRIORITY 2: PATIENT MANAGEMENT
Patient CRUD Operations
# Patient Management
GET  /api/patients/               # List patients
POST /api/patients/               # Create patient
GET  /api/patients/<patient_id>   # Get patient details
PUT  /api/patients/<patient_id>   # Update patient
DELETE /api/patients/<patient_id> # Delete patient
POST /api/patients/<patient_id>/reactivate # Reactivate patient
# Patient Data & Statistics
GET  /api/patients/stats          # Patient statistics
POST /api/patients/import         # Import patients
Patient Medical History
GET,POST,PUT /api/patients/<patient_id>/medical-history # Medical history

# 🎯 PRIORITY 3: APPOINTMENT MANAGEMENT
Appointment Core Operations
# Appointment CRUD
GET  /api/appointments/           # List appointments
POST /api/appointments/           # Create appointment
GET  /api/appointments/<appointment_id> # Get appointment
PUT  /api/appointments/<appointment_id> # Update appointment
DELETE /api/appointments/<appointment_id> # Delete appointment
# Appointment Actions
POST /api/appointments/<appointment_id>/cancel    # Cancel appointment
POST /api/appointments/<appointment_id>/complete  # Complete appointment
Appointment Views & Availability
# Appointment Views
GET /api/appointments/today       # Today's appointments
GET /api/appointments/upcoming    # Upcoming appointments
GET /api/appointments/availability # Check availability

# 🎯 PRIORITY 4: CLINICAL MANAGEMENT
Medical Records
# Medical Records
GET  /api/clinical/records        # List medical records
POST /api/clinical/records        # Create medical record
GET  /api/clinical/records/<record_id> # Get medical record
PUT  /api/clinical/records/<record_id> # Update medical record
DELETE /api/clinical/records/<record_id> # Delete medical record
# Record Management
POST /api/clinical/records/<record_id>/attachments # Upload attachment
DELETE /api/clinical/records/<record_id>/attachments/<attachment_id> # Delete attachment
POST /api/clinical/records/<record_id>/lock # Lock record
Clinical Dashboard & Search
GET /api/clinical/dashboard/patient/<patient_id> # Patient clinical dashboard
GET /api/clinical/search         # Search clinical data

# 🎯 PRIORITY 5: BILLING & FINANCE
Invoices & Payments
# Invoices
GET  /api/billing/invoices        # List invoices
POST /api/billing/invoices        # Create invoice
GET  /api/billing/invoices/<invoice_id> # Get invoice
PUT  /api/billing/invoices/<invoice_id> # Update invoice
DELETE /api/billing/invoices/<invoice_id> # Delete invoice
# Payments
POST /api/billing/payments        # Create payment
DELETE /api/billing/payments/<payment_id> # Delete payment
Insurance Management
# Insurance Plans
GET  /api/insurance/plans         # List insurance plans
POST /api/insurance/plans         # Create insurance plan
GET  /api/insurance/plans/<plan_id> # Get insurance plan
PUT  /api/insurance/plans/<plan_id> # Update insurance plan
DELETE /api/insurance/plans/<plan_id> # Delete insurance plan
# Insurance Operations
GET  /api/insurance/plans/<plan_id>/coverage # Get coverage
POST /api/insurance/plans/<plan_id>/verify # Verify insurance
POST /api/insurance/coverage/check # Check coverage

# 🎯 PRIORITY 6: DASHBOARD & ANALYTICS
Dashboard Data
# Dashboard Widgets
GET /api/dashboard/data/appointment-stats    # Appointment statistics
GET /api/dashboard/data/financial-overview   # Financial overview
GET /api/dashboard/data/patient-metrics      # Patient metrics
GET /api/dashboard/data/widget/<widget_type> # Widget data
# Dashboard Management
GET  /api/dashboard/layout        # Get dashboard layout
PUT  /api/dashboard/layout        # Update dashboard layout
GET  /api/dashboard/widgets       # Get widgets
POST /api/dashboard/widgets       # Create widget
PUT  /api/dashboard/widgets/<widget_id> # Update widget
DELETE /api/dashboard/widgets/<widget_id> # Delete widget
Analytics & Reports
# Analytics
GET /api/analytics/dashboard      # Dashboard analytics
GET /api/analytics/appointments   # Appointment analytics
GET /api/analytics/patients       # Patient analytics
GET /api/analytics/revenue        # Revenue analytics
# Reports
GET /api/reports/analytics        # Analytics reports
GET /api/reports/financial        # Financial reports
GET /api/reports/financial/summary # Financial summary
GET /api/reports/financial/aging  # Aging report

# 🎯 PRIORITY 7: ORGANIZATION & SETTINGS
Organization Management
# Organization CRUD
GET  /api/organizations/          # List organizations
POST /api/organizations/          # Create organization
GET  /api/organizations/<org_id>  # Get organization
PUT  /api/organizations/<org_id>  # Update organization
DELETE /api/organizations/<org_id> # Delete organization
# Organization Operations
GET  /api/organizations/current   # Get current organization
GET  /api/organizations/<org_id>/users # Get organization users
GET  /api/organizations/<org_id>/stats # Organization statistics
PUT  /api/organizations/<org_id>/subscription # Update subscription
Settings Management
# System Settings
GET  /api/settings/               # Get all settings
GET,PUT /api/settings/organization # Organization settings
GET,PUT /api/settings/organization/practice # Practice settings
GET,PUT /api/settings/user        # User settings
GET,PUT /api/settings/preferences # User preferences
GET,PUT /api/settings/notifications # Notification settings

# 🎯 PRIORITY 8: CLINICAL FEATURES
Prescriptions
GET  /api/prescriptions/          # List prescriptions
POST /api/prescriptions/          # Create prescription
GET  /api/prescriptions/<prescription_id> # Get prescription
PUT  /api/prescriptions/<prescription_id> # Update prescription
DELETE /api/prescriptions/<prescription_id> # Delete prescription
# Prescription Actions
POST /api/prescriptions/<prescription_id>/approve # Approve prescription
POST /api/prescriptions/<prescription_id>/cancel # Cancel prescription
POST /api/prescriptions/<prescription_id>/dispense # Dispense prescription
GET  /api/prescriptions/patient/<patient_id> # Patient prescriptions
Lab Orders
GET  /api/labs/orders             # List lab orders
POST /api/labs/orders             # Create lab order
GET  /api/labs/orders/<order_id>  # Get lab order
PUT  /api/labs/orders/<order_id>  # Update lab order
# Lab Order Actions
POST /api/labs/orders/<order_id>/results # Add lab results
POST /api/labs/orders/<order_id>/approve # Approve results
POST /api/labs/orders/<order_id>/reject  # Reject results
PUT  /api/labs/orders/<order_id>/status  # Update status

# 🎯 PRIORITY 9: ADVANCED FEATURES
Family Members & Relationships
GET  /api/family_members/         # List family members
POST /api/family_members/         # Create family member
GET  /api/family_members/<fm_id>  # Get family member
PUT  /api/family_members/<fm_id>  # Update family member
DELETE /api/family_members/<fm_id> # Delete family member
# Family Relationships
GET  /api/family_members/<fm_id>/relationships # Get relationships
POST /api/family_members/<fm_id>/relationships # Create relationship
DELETE /api/family_members/relationships/<relationship_id> # Delete relationship
Notifications
GET  /api/notifications/          # Get notifications
GET  /api/notifications/<notification_id> # Get notification
POST /api/notifications/<notification_id>/read # Mark as read
POST /api/notifications/<notification_id>/unread # Mark as unread
POST /api/notifications/read-all  # Mark all as read
POST /api/notifications/clear-all # Clear all notifications
Telemedicine
GET  /api/telemedicine/sessions   # List sessions
POST /api/telemedicine/sessions   # Create session
GET  /api/telemedicine/sessions/<session_id> # Get session
PUT  /api/telemedicine/sessions/<session_id> # Update session
# Session Actions
POST /api/telemedicine/sessions/<session_id>/start # Start session
POST /api/telemedicine/sessions/<session_id>/join  # Join session
POST /api/telemedicine/sessions/<session_id>/end   # End session
POST /api/telemedicine/sessions/<session_id>/cancel # Cancel session

# 🎯 PRIORITY 10: SYSTEM & ADMIN
Admin Interface (Flask-Admin)
# Admin CRUD interfaces for all major models
/admin/user/, /admin/patient/, /admin/appointment/, /admin/organization/
/admin/invoice/, /admin/payment/, /admin/treatment/, /admin/role/
Health & Monitoring
GET /health, /healthz            # Health checks
GET /api/health/                 # Detailed health
GET /api/health/liveness         # Liveness probe
GET /api/health/readiness        # Readiness probe
GET /api/health/metrics          # Metrics

# 🚀 FRONTEND DEVELOPMENT ORDER:
Phase 1: Foundation
Authentication & User Management
Basic Dashboard
Patient Management
Appointment Management

Phase 2: Core Clinical
Medical Records
Clinical Dashboard
Prescriptions & Lab Orders

Phase 3: Business Operations
Billing & Invoices
Insurance Management
Reporting & Analytics

Phase 4: Advanced Features
Family Management
Notifications
Telemedicine
Settings & Configuration

Phase 5: System Features
Admin Interface
Audit & Security
Integrations

This grouping follows a logical flow from basic authentication to advanced clinical features, making it easier to develop the frontend in manageable phases.


# Navigate to your project directory
cd /home/soji/Documents/Projects/Dentaloist

# Create Vite React project
# yarn create vite@latest vite_frontend -- --template react
# or for TypeScript:
yarn create vite@latest vite_frontend -- --template react-ts

cd vite_frontend
yarn install

# Core dependencies
yarn add axios react-router-dom
yarn add @tanstack/react-query
yarn add lucide-react  # For icons

# UI components (choose one)
yarn add tailwindcss @headlessui/react @heroicons/react
# OR
yarn add @mui/material @emotion/react @emotion/styled
# OR
yarn add antd


# UI stack (Tailwind + shadcn/ui)
yarn add tailwindcss postcss autoprefixer
yarn add @radix-ui/react-dropdown-menu @radix-ui/react-dialog @radix-ui/react-toast

# Development dependencies
yarn add -D @types/react @types/react-dom  # For TypeScript


vite_frontend/
  ├── src/
  │   ├── assets/               # Static assets (logos, images, global styles)
  │   ├── components/           # Reusable building blocks
  │   │   ├── ui/               # Buttons, Inputs, Modals, Alerts, etc.
  │   │   ├── layout/           # Navbar, Sidebar, AuthLayout, DashboardLayout
  │   │   └── forms/            # Reusable form components (LoginForm, etc.)
  │   ├── contexts/             # React Context providers (AuthContext, ThemeContext)
  │   │   └── AuthContext.tsx          # Updated with backend integration  
  │   ├── hooks/                # Custom React hooks (useAuth, useApi, usePatients)
  │   │   ├── useAuth.ts               # New
  │   │   ├── usePatients.ts           # New
  │   │   └── useAppointments.ts       # New  
  │   ├── pages/                # Route-level pages
  │   │   ├── auth/             # Login, Register, Forgot/Reset password
  │   │   ├── dashboard/        # Dashboard homepage
  │   │   ├── patients/         # Patient list, details, edit
  │   │   ├── appointments/     # Appointment list, booking, details
  │   │   └── settings/         # User settings
  │   ├── services/             # API + business logic layer
  │   │   ├── api/              # Axios instance, interceptors
  │   │   │   ├── index.ts             # Axios instance & config
  │   │   │   └── endpoints.ts         # API endpoints
  │   │   └── auth/             # Auth service (login, logout, refresh)
  │   │   ├── authService.ts           # Auth service
  │   │   ├── patientService.ts        # Patient service
  │   │   └── appointmentService.ts    # Appointment service
  │   ├── store/                # React Query / Zustand / Redux
  │   ├── types/                # Global TypeScript types/interfaces
  │   ├── utils/                # Utility/helper functions
  │   ├── App.tsx               # Root app w/ routes
  │   ├── main.tsx              # Entry point
  │   └── vite-env.d.ts
  ├── public/                   # Static files served as-is
  ├── index.html
  ├── tsconfig.json
  ├── package.json
  └── yarn.lock

# Stop the dev server first (Ctrl+C)
# Remove current problematic versions
yarn remove react react-dom react-router-dom

# Install stable, compatible versions
yarn add react@^18.2.0 react-dom@^18.2.0 react-router-dom@^6.20.1

# Install correct type definitions
yarn add --dev @types/react@^18.2.0 @types/react-dom@^18.2.0

# Remove incompatible type packages
yarn remove @types/react-router @types/react-router-dom

# Clear cache and reinstall
rm -rf node_modules/.vite
yarn install
yarn dev





# Stop the dev server first (Ctrl+C)
# Check if main files exist
ls -la src/main.*
ls -la src/App.*
ls -la index.html

# Check for TypeScript errors
yarn type-check

# Check for build errors
yarn build


# 1. Stop dev server (Ctrl+C)
# 2. Fix dependencies
yarn remove react react-dom react-router-dom
yarn add react@^18.2.0 react-dom@^18.2.0 react-router-dom@^6.20.1
yarn add --dev @types/react@^18.2.0 @types/react-dom@^18.2.0
yarn remove @types/react-router @types/react-router-dom
# 3. Clear cache
rm -rf node_modules/.vite
# 4. Reinstall
yarn install
# 5. Create simple test App.tsx (use the simple version above)
# 6. Start dev server
yarn dev



# Stop dev server first (Ctrl+C)
# Remove all React-related packages
yarn remove react react-dom react-router-dom
# Install compatible versions
yarn add react@^18.2.0 react-dom@^18.2.0 react-router-dom@^6.20.1
# Install correct type definitions
yarn add --dev @types/react@^18.2.0 @types/react-dom@^18.2.0
# Remove incompatible type packages
yarn remove @types/react-router @types/react-router-dom
# Clear cache
rm -rf node_modules/.vite
# Reinstall everything
yarn install
# Try building the project
yarn build
# If build succeeds, serve the production build
yarn preview

# Check React versions
yarn list --pattern "react"
# Check TypeScript can find modules
yarn type-check
# Check if React packages are in node_modules
ls node_modules | grep react
# Check package.json for React versions
cat package.json | grep -A 5 -B 5 "react"
# Check if index.html exists and has the root div
cat index.html | grep -A 5 -B 5 "root"



# Stop dev server (Ctrl+C)
# Remove node_modules and lock file
rm -rf node_modules
rm -f yarn.lock
# Reinstall everything
yarn install
# Start dev server
yarn dev

# package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "@tanstack/react-query": "^5.8.4",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@types/node": "^20.10.0",
    "@typescript-eslint/eslint-plugin": "^8.45.0",
    "@typescript-eslint/parser": "^8.45.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.57.0",
    "eslint-plugin-react": "^7.34.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.9",
    "globals": "^13.24.0",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.3",
    "vite": "^5.0.0"
  }
}

# tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "allowJs": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}



# workspace issues
# Check if we're in a workspace
ls -la ../
cat ../package.json
# Go to the root directory and run commands from there
cd ..
yarn workspace dentaloist-frontend dev
# Check if there's a yarn workspace configuration
cat ../package.json | grep -A 10 -B 10 "workspace"


# Stay in the vite_frontend directory
cd ~/Documents/Projects/Dentaloist/vite_frontend

# Remove the workspace reference by deleting the root yarn files
rm -rf ../.yarn
rm -f ../yarn.lock
rm -f ../.yarnrc.yml
# Reinstall in the current directory
yarn install
# Now try to start dev server
yarn dev


# Ensure we're in the frontend directory
cd ~/Documents/Projects/Dentaloist/vite_frontend
# Remove any workspace configuration
rm -f .yarnrc.yml
rm -f ../.yarnrc.yml
# Clear and reinstall
rm -rf node_modules
yarn install
# Now try
yarn dev