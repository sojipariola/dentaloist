src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                  # Graphical Homepage
│   ├── dashboard/
│   │   ├── page.tsx              # Role-based redirect
│   │   ├── dentist/
│   │   │   └── page.tsx          # Dentist Dashboard
│   │   ├── admin/
│   │   │   └── page.tsx          # Admin Dashboard
│   │   └── [role]/               # Dynamic role routing
│   ├── login/
│   │   └── page.tsx
│   └── api/                      # Next.js route handlers (optional proxy)
│
├── components/
│   ├── ui/                       # ShadCN-like UI primitives
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── table.tsx
│   │   └── ...
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── ThemeToggle.tsx
│   ├── dashboard/
│   │   ├── WidgetGrid.tsx
│   │   ├── StatCard.tsx
│   │   ├── AppointmentCalendar.tsx
│   │   └── PatientTable.tsx
│   └── homepage/
│       ├── Hero.tsx
│       ├── FeatureGrid.tsx
│       └── TestimonialCarousel.tsx
│
├── lib/
│   ├── api/
│   │   ├── client.ts             # Axios/Fetch client
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   ├── appointments.ts
│   │   ├── widgets.ts
│   │   └── index.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── usePermissions.ts
│   │   └── useWidgets.ts
│   └── utils/
│       ├── date.ts
│       ├── permissions.ts
│       └── currency.ts
│
├── types/
│   ├── user.ts
│   ├── patient.ts
│   ├── appointment.ts
│   ├── widget.ts
│   └── index.ts
│
├── styles/
│   ├── globals.css
│   └── theme.css
│
├── public/
│   ├── images/
│   └── icons/
│
└── store/                        # Zustand (lightweight state)
    ├── authStore.ts
    └── widgetStore.ts