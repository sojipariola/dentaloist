import { lazy } from 'react'

export const privateRoutes = [
  {
    path: '/dashboard',
    component: lazy(() => import('@/pages/dashboard/Overview')),
  },
  {
    path: '/patients',
    component: lazy(() => import('@/pages/patients/PatientsList')),
  },
  {
    path: '/patients/:id',
    component: lazy(() => import('@/pages/patients/PatientDetails')),
  },
  {
    path: '/patients/new',
    component: lazy(() => import('@/pages/patients/PatientForm')),
  },
  {
    path: '/patients/:id/edit',
    component: lazy(() => import('@/pages/patients/PatientForm')),
  },
  {
    path: '/appointments',
    component: lazy(() => import('@/pages/appointments/AppointmentsList')),
  },
  {
    path: '/appointments/:id',
    component: lazy(() => import('@/pages/appointments/AppointmentDetails')),
  },
  {
    path: '/appointments/new',
    component: lazy(() => import('@/pages/appointments/AppointmentForm')),
  },
  {
    path: '/appointments/:id/edit',
    component: lazy(() => import('@/pages/appointments/AppointmentForm')),
  },
  // Clinical routes
  {
    path: '/clinical',
    component: lazy(() => import('@/pages/clinical/ClinicalRecords')),
  },
  {
    path: '/clinical/records',
    component: lazy(() => import('@/pages/clinical/ClinicalRecords')),
  },
  {
    path: '/clinical/treatment-plans',
    component: lazy(() => import('@/pages/clinical/TreatmentPlans')),
  },
  {
    path: '/clinical/treatment-plans/new',
    component: lazy(() => import('@/pages/clinical/TreatmentPlanForm')),
  },
  {
    path: '/clinical/notes/new',
    component: lazy(() => import('@/pages/clinical/ClinicalNoteForm')),
  },
  // Billing routes
  {
    path: '/billing',
    component: lazy(() => import('@/pages/billing/Invoices')),
  },
  {
    path: '/billing/invoices',
    component: lazy(() => import('@/pages/billing/Invoices')),
  },
  {
    path: '/billing/invoices/new',
    component: lazy(() => import('@/pages/billing/InvoiceForm')),
  },
  {
    path: '/billing/payments',
    component: lazy(() => import('@/pages/billing/Payments')),
  },
  {
    path: '/billing/payments/new',
    component: lazy(() => import('@/pages/billing/PaymentForm')),
  },
  // Inventory routes
  {
    path: '/inventory',
    component: lazy(() => import('@/pages/inventory/InventoryItems')),
  },
  {
    path: '/inventory/items',
    component: lazy(() => import('@/pages/inventory/InventoryItems')),
  },
  {
    path: '/inventory/items/new',
    component: lazy(() => import('@/pages/inventory/InventoryItemForm')),
  },
]