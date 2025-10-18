explain basic usage flow(types - services - hooks - contexts - components - layout - utils - app) of next.js components that I need to develop base-page, dashboard-page, report-page, billing-page, organizations-page, patients-page, appointments-page, reports-page using the file architecture:

create for me, a ready to use, functioning, downloadable 'src' zip folder that can be fixed directly into my project(flask backend and next.js frontend) using the models supplied for the proposed 'src' architecture:

# This is our file Architecture
frontend/
├─ public/                # Static files: images, fonts, favicon
├─ src/
│  ├─ app/                # App-specific setup (Next.js 13+ App Router)
│  │  ├─ layout.tsx       # Root layout
│  │  ├─ page.tsx         # Landing / Home page
│  │  ├─ globals.css      # Global styles
│  │  ├─ loading.tsx      # Global loading indicator
│  │  └─ head.tsx         # SEO / meta tags
│  │
│  ├─ components/         # Reusable UI components
│  │  ├─ ui/              # Generic UI components (Button, Input, Modal)
│  │  ├─ layout/          # Layout-specific components (Navbar, Sidebar, Footer)
│  │  ├─ forms/           # Form components
│  │  └─ dashboard/       # Dashboard-specific widgets
│  │
│  ├─ features/           # Domain-specific modules / feature slices
│  │  ├─ auth/            # Login, signup, auth context/hooks
│  │  ├─ organization/    # Org management, tenant switching
│  │  ├─ users/           # User CRUD, roles
│  │  ├─ patients/        # Patient management
│  │  ├─ appointments/    # Appointment booking & management
│  │  └─ billing/         # Payment, subscriptions
│  │
│  ├─ hooks/              # Custom React hooks
│  │  ├─ useAuth.ts
│  │  └─ useFetch.ts
│  │
│  ├─ context/            # Global state or context providers
│  │  ├─ AuthContext.tsx
│  │  └─ TenantContext.tsx
│  │
│  ├─ services/           # API calls / integrations
│  │  ├─ api.ts           # Axios / fetch setup
│  │  ├─ authService.ts
│  │  └─ appointmentService.ts
│  │
│  ├─ types/              # TypeScript interfaces & enums
│  │  ├─ index.d.ts
│  │  └─ appointment.ts
│  │
│  ├─ utils/              # Utility functions & helpers
│  │  ├─ formatters.ts
│  │  └─ validators.ts
│  │
│  └─ styles/             # Tailwind, global CSS, or SCSS
│     └─ tailwind.css
├─ .env.local
├─ next.config.js
├─ package.json
└─ tsconfig.json


src/ // (Next.js 15, TypeScript, app router)
├── services/
│   ├── api/
│   │   ├── index.ts              # Main API client instance
│   │   ├── config.ts             # API configuration
│   │   ├── interceptors.ts       # Request/response interceptors
│   │   └── types.ts              # API-specific types
│   ├── appointments/
│   │   ├── index.ts
│   │   ├── appointmentsService.ts
│   │   └── types.ts
│   ├── auth/
│   │   ├── index.ts              # Auth service exports
│   │   ├── authService.ts        # Main auth service
│   │   └── types.ts              # Auth-specific types
│   ├── billing/
│   │   ├── index.ts
│   │   ├── billingService.ts
│   │   └── types.ts
│   ├── organizations/
│   │   ├── index.ts
│   │   ├── organizationsService.ts
│   │   └── types.ts
│   ├── patients/
│   │   ├── index.ts
│   │   ├── patientsService.ts
│   │   └── types.ts
│   ├── reports/
│   │   ├── index.ts
│   │   ├── reportsService.ts
│   │   └── types.ts
│   ├── widget/
│   │   ├── index.ts
│   │   ├── widgetService.ts
│   │   └── types.ts
│   └── index.ts                  # Main services export




for this response, i want to act like an expert frontend developer, using the backend model and proposed model frontend file structure (can be altered slightly with explanations) I supply, develop a world-class, complete functional 'src/' structure with good graphics, wired up with the backend's api and can be plugged into an existing, configured next.js, react, typescript frontend

 
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── loading.tsx
│   ├── dashboard/
│   │   └── page.tsx
│   ├── appointments/
│   │   └── page.tsx
│   ├── patients/
│   │   └── page.tsx
│   ├── billing/
│   │   └── page.tsx
│   ├── organizations/
│   │   └── page.tsx
│   ├── reports/
│   │   └── page.tsx
│   └── api/
│       └── auth/
│           └── route.ts
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   └── Card.tsx
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── dashboard/
│   │   ├── StatsCard.tsx
│   │   ├── RecentAppointments.tsx
│   │   └── WidgetGrid.tsx
│   └── forms/
│       ├── AppointmentForm.tsx
│       ├── PatientForm.tsx
│       └── LoginForm.tsx
├── features/
│   ├── auth/
│   │   ├── components/
│   │   │   └── Login.tsx
│   │   └── hooks/
│   │       └── useAuth.ts
│   ├── appointments/
│   │   ├── components/
│   │   │   ├── AppointmentList.tsx
│   │   │   └── CalendarView.tsx
│   │   ├── hooks/
│   │   │   └── useAppointments.ts
│   │   └── types.ts
│   ├── patients/
│   │   ├── components/
│   │   │   ├── PatientList.tsx
│   │   │   └── PatientProfile.tsx
│   │   ├── hooks/
│   │   │   └── usePatients.ts
│   │   └── types.ts
│   └── billing/
│       ├── components/
│       │   └── InvoiceList.tsx
│       ├── hooks/
│       │   └── useBilling.ts
│       └── types.ts
├── hooks/
│   ├── useAuth.ts
│   ├── useFetch.ts
│   └── useSocket.ts
├── context/
│   ├── AuthContext.tsx
│   └── AppContext.tsx
├── services/
│   ├── api.ts
│   ├── authService.ts
│   ├── appointmentService.ts
│   ├── patientService.ts
│   └── billingService.ts
├── types/
│   ├── index.ts
│   ├── auth.ts
│   ├── organizations.ts
│   ├── reports.ts
│   ├── appointments.ts
│   ├── patients.ts
│   └── billing.ts
├── utils/
│   ├── formatters.ts
│   ├── validators.ts
│   └── constants.ts
└── styles/
    └── globals.css



// Example usage in a component
import { useAuth } from '@/contexts/AuthContext';
import { debugAuth } from '@/services/authService';

const MyComponent = () => {
  const { user, isLoading } = useAuth();
  
  useEffect(() => {
    // Temporary debug
    debugAuth();
  }, []);
  
  // ...
};


